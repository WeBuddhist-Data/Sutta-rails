"""Sutta review, second pass: four checks the first pass (review_nikaya.py) left to build time.

  A. Page breaks and exact spacing (the Vinaya found 3,111 spaces the conversion put where a
     <pb/> sat before punctuation, "word ."). Lines are aligned by their letters only, then
     compared with exact spacing and punctuation. Every difference is listed, and marked
     when it sits at a <pb/>.
  B. Bold: every <hi rend="bold"> is a **…** span with exactly the same text, in order
     (cscd-root-text-intake/scripts/bold_check.py, as the verifiers use it).
  C. Structure: each heading's parent is the heading one level up whose ID path is its own
     minus one segment; no level is skipped; no heading is empty (no text and no
     sub-heading under it); numbered siblings run on (restarts listed, they can be the
     source's own).
  D. Links (commentaries): each paragraph that opens with a printed citation is preceded by
     links to the root blocks that hold exactly those numbers, and each link holds one of
     them.

usage (vault root): python -I -X utf8 0-INBOX/sutta-review/review_more.py <dn|mn|sn|an|kn> [file-name filter …]
"""
import difflib, glob, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, "4-SYSTEM/Skills/cscd-root-text-intake/scripts")
import bold_check  # noqa: E402

ROMN = Path(r"D:\Work\OpenPecha\tipitaka-xml\romn")
OUT = Path("0-INBOX/sutta-review")
NAME = {"dn": "dighanikaya", "mn": "majjhimanikaya", "sn": "samyuttanikaya",
        "an": "anguttaranikaya", "kn": "khuddakanikaya"}
nk, only = sys.argv[1], sys.argv[2:]
files = sorted(glob.glob(f"1-SOURCES/Text/pi-{NAME[nk]}.md")) + sorted(glob.glob(f"1-SOURCES/Commentaries/pi-{NAME[nk]}*.md"))
if only: files = [f for f in files if any(o in f for o in only)]
PB = "\x00"
LEADNUM = re.compile(r"^(?:\(?\d+[\d\-–.,()]*\.?\)?\s*)+(?=\D)")   # printed number(s) opening a line
LABEL = re.compile(r"\s*\((aṭṭhakathā|ṭīkā|abhinavaṭīkā)\)\s*$")
CIT = re.compile(r"^(\d+)(?:-(\d+))?\.(?:\s|$)")


# ---------------------------------------------------------------- A. exact text
def render(el, out, top=True):
    if el.tag == "pb":
        out.append(PB)
    elif el.tag == "note":
        out.append(" [" + "".join(el.itertext()).strip() + "]")
    elif el.tag == "hi" and el.get("rend") == "dot":
        out.append(".")
    else:
        if el.text: out.append(el.text)
        for c in el: render(c, out, False)
    if not top and el.tail: out.append(el.tail)


def exact(s):
    """The converter's own normalisation: quotes, runs of whitespace, spaces inside [ ]."""
    s = s.replace("‘‘", '"').replace("’’", '"')
    # page markers with the whitespace around them: one space if there is any, else none
    # ("me <pb/> sutaṃ" is "me sutaṃ"; "dhammaṃ<pb/>." is "dhammaṃ.")
    s = re.sub(r"\s*\x00[\s\x00]*", lambda m: (" " if m.group(0).replace(PB, "") else "") + PB, s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\[\s+", "[", s); s = re.sub(r"\s+\]", "]", s)
    s = s.replace(" " + PB + " ", " " + PB)
    # a page marker at either end of the line: the space next to it is not inside the line
    s = re.sub(r"^[\s\x00]+", lambda m: PB if PB in m.group(0) else "", s)
    return re.sub(r"[\s\x00]+$", lambda m: PB if PB in m.group(0) else "", s)


def key(s):
    return re.sub(r"[\W\d_]+", "", s.replace(PB, ""))


def xml_lines(stems):
    out, pend = [], ""
    for st in stems:
        body = ET.parse(ROMN / st).getroot().find(".//body")
        for el in body.iter():
            if el.tag not in ("head", "p", "trailer"): continue
            buf = []; render(el, buf)
            t = exact("".join(buf))
            if not t.replace(PB, "").strip(): continue
            if el.get("rend") == "hangnum":
                pend = t + " "; continue
            out.append(pend + t); pend = ""
    return out


def vault_lines(body):
    out = []
    for n, l in enumerate(body.split("\n"), 1):
        if not l.strip() or l.startswith("![[") or re.match(r"^\[\^[\w-]+\]:", l): continue
        l = re.sub(r"\s*\^[\w-]+\s*$", "", l)
        l = re.sub(r"\[\^[\w-]+\]", "", l)
        l = re.sub(r"\s*\[Ed:[^\]]*\]", "", l)
        m = re.match(r"^#+\s+(.*)$", l)
        if m: l = LABEL.sub("", m.group(1))
        out.append((n, exact(bold_check.strip_bold(l))))
    return out


def strip_num(s):
    # a printed paragraph or heading number: a root keeps it in the ID, a commentary adds a
    # space after "N." in a paragraph; both are known, so the number is left out of the compare
    s = re.sub(r"^(\d+(?:-\d+)*)\s+\.", r"\1.", s)
    return LEADNUM.sub("", s, count=1).lstrip()


def spacing(xl, vl):
    """Exact differences between lines aligned by their letters."""
    sm = difflib.SequenceMatcher(None, [key(t) for t in xl], [key(t) for _, t in vl], autojunk=False)
    diffs, unaligned = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            unaligned.append((op, xl[i1:i2], vl[j1:j2])); continue
        for d in range(i2 - i1):
            xs, (n, vs) = xl[i1 + d], vl[j1 + d]
            if xs.replace(PB, "") == vs: continue
            a, b = strip_num(xs), strip_num(vs)
            if a.replace(PB, "") == b: continue
            # character diff, with the page-break positions mapped onto the XML text
            pos, plain = [], []
            for c in a:
                if c == PB: pos.append(len(plain))
                else: plain.append(c)
            plain = "".join(plain)
            for o, a0, a1, b0, b1 in difflib.SequenceMatcher(None, plain, b, autojunk=False).get_opcodes():
                if o == "equal": continue
                at_pb = any(a0 - 1 <= p <= a1 + 1 for p in pos)
                kind = ("space added" if o == "insert" and b[b0:b1].strip() == "" else
                        "space removed" if o == "delete" and plain[a0:a1].strip() == "" else "text")
                diffs.append((n, kind, at_pb, plain[max(0, a0 - 25):a1 + 25], b[max(0, b0 - 25):b1 + 25]))
    return diffs, unaligned


# ---------------------------------------------------------------- C. structure
def structure(body):
    heads = []
    lines = body.split("\n")
    for n, l in enumerate(lines, 1):
        m = re.match(r"^(#+)\s+(.*?)\s+\^([\w-]+)\s*$", l)
        if m: heads.append((n, len(m.group(1)), re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2)), m.group(3)))
    probs, restarts = [], []
    stack = {}   # level -> heading
    last_num = {}  # parent id -> last printed number among its children
    for k, (n, lv, t, hid) in enumerate(heads):
        for L in [L for L in stack if L >= lv]: del stack[L]
        if lv > 2:
            par = stack.get(lv - 1)
            if par is None:
                probs.append(f"line {n}: level {lv} `{t}` ^{hid} has no level-{lv-1} parent (a level is skipped)")
            elif par[3].split("-")[:-1] != hid.split("-")[:-2]:
                probs.append(f"line {n}: `{t}` ^{hid} sits under ^{par[3]} but its ID path says otherwise")
            pid = par[3] if par else None
            mnum = re.match(r"^\(?(\d+)[.)]", t)
            if mnum and pid:
                v = int(mnum.group(1)); prev = last_num.get(pid)
                if prev is not None and v != prev + 1:
                    restarts.append(f"line {n}: `{t}` after sibling number {prev} (under ^{pid})")
                last_num[pid] = v
        stack[lv] = (n, lv, t, hid)
        # empty: no text and no deeper heading before the next heading of the same or higher level
        nxt = heads[k + 1] if k + 1 < len(heads) else None
        if lv >= 2 and (nxt is None or nxt[1] <= lv):
            stop = nxt[0] - 1 if nxt else len(lines)
            if not any(x.strip() and not x.startswith("![[") for x in lines[n:stop]):
                probs.append(f"line {n}: `{t}` ^{hid} is empty")
    return len(heads), probs, restarts


# ---------------------------------------------------------------- D. links
def cited(m):
    a = int(m.group(1)); b = m.group(2)
    if b is None: return set([a])
    bb = int(b)
    if bb < a and len(b) < len(m.group(1)):   # truncated tail "133-4." = 133-134
        bb = int(m.group(1)[:-len(b)] + b)
    return set(range(a, bb + 1)) if bb >= a else set([a])


def holds(rid):
    """Numbers a root block can hold, from its ID alone: the last number, and a range
    'a-b' when the last two segments are numbers (a printed range, or a zone + number)."""
    parts = [re.sub(r"x\d+$", "", p) for p in rid.split("-")[1:]]
    nums = [int(p) for p in parts if p.isdigit()]
    if not nums: return set()
    out = {nums[-1]}
    if len(parts) >= 2 and parts[-1].isdigit() and parts[-2].isdigit() and int(parts[-2]) < int(parts[-1]):
        out |= set(range(int(parts[-2]), int(parts[-1]) + 1))
    return out


def links(body, root_hold):
    lines = body.split("\n")
    probs, unlinked, n_cit, pend, absent = [], [], 0, [], []
    for n, l in enumerate(lines, 1):
        s = l.strip()
        if not s: continue
        m = re.match(r"^!\[\[([^#\]]+)#\^([\w-]+)\]\]$", s)
        if m: pend.append(m.group(2)); continue
        if s.startswith("#"):
            if pend: probs.append(f"line {n}: links directly before a heading: {pend[:3]}")
            pend = []; continue
        txt = s.replace("**", "")
        c = CIT.match(txt)
        if c:
            n_cit += 1
            want = cited(c)
            if not pend:
                unlinked.append(f"line {n}: `{txt[:70]}`")
            else:
                got = set().union(*(holds(r) for r in pend))
                stray = [r for r in pend if not (holds(r) & want)]
                # numbers the root itself does not print (a gap in its own numbering) cannot be linked
                gone = {x for x in want - got if x not in root_hold.get(pend[0].split("-")[0], set())}
                if not stray and gone and want - got == gone:
                    absent.append(f"line {n}: cites {c.group(0).strip()}; the root has no paragraph "
                                  f"{sorted(gone)[:6]}{'…' if len(gone) > 6 else ''} → links {pend[:5]}{'…' if len(pend) > 5 else ''}")
                elif not want <= got or stray:
                    probs.append(f"line {n}: cites {c.group(0).strip()} → links {pend}")
        elif pend:
            probs.append(f"line {n}: links before a paragraph with no printed number: {pend[:3]} `{txt[:50]}`")
        pend = []
    return n_cit, probs, unlinked, absent


# ---------------------------------------------------------------- run
for f in files:
    text = Path(f).read_text(encoding="utf-8")
    fm, body = text.split("\n---\n", 1)
    stems = [s.strip() for s in re.search(r"^source_filename:\s*\[(.*)\]", fm, re.M).group(1).split(",")]
    lined = "\n" * (fm.count("\n") + 2) + body   # padded so that every line number is the file's
    is_root = "/Text/" in f
    name = Path(f).stem
    rep = [f"# Second-pass review: `{f}`\n"]; P = rep.append

    xl, vl = xml_lines(stems), vault_lines(lined)
    diffs, unaligned = spacing(xl, vl)
    pb_total = sum(t.count(PB) for t in xl)
    P(f"## A. Page breaks and exact spacing\n\n- XML page markers: {pb_total:,}; XML lines {len(xl):,}, vault lines {len(vl):,}")
    kinds = {}
    for d in diffs: kinds[(d[1], d[2])] = kinds.get((d[1], d[2]), 0) + 1
    P(f"- differences: {len(diffs)} " + (str({f'{k[0]}{" at a page break" if k[1] else ""}': v for k, v in kinds.items()}) if diffs else ""))
    P(f"- lines not aligned by their letters: {sum(len(a) + len(b) for _, a, b in unaligned)}\n")
    for n, kind, at_pb, a, b in diffs[:300]:
        P(f"- line {n}: {kind}{' (at a page break)' if at_pb else ''}: XML `{a}` → vault `{b}`")
    for op, a, b in unaligned[:50]:
        P(f"- {op}: XML {[x.replace(PB, '')[:100] for x in a][:3]} | vault {[(n, t[:100]) for n, t in b][:3]}")

    bodies = [ET.parse(ROMN / st).getroot().find(".//body") for st in stems]
    md = [re.sub(r"^(#{7,}\s+)\*\*(.*)\*\*(\s+\^[\w-]+)$", r"\1\2\3", l) for l in body.split("\n")]
    md_sp, unpaired = bold_check.md_spans(md, exact=True)
    xml_sp = bold_check.xml_spans(bodies, exact=True)
    bprob = bold_check.compare(xml_sp, md_sp, "xml") + [f"unpaired ** on line: {u!r}" for u in unpaired[:5]]
    P(f"\n## B. Bold\n\n- XML spans {len(xml_sp):,}, vault spans {len(md_sp):,}: " + ("identical, in order" if not bprob else "DIFFER"))
    P("\n".join("  - " + p for p in bprob))

    nh, sprob, restarts = structure(lined)
    P(f"\n## C. Structure\n\n- headings {nh:,}; problems {len(sprob)}; numbered-sibling restarts or gaps {len(restarts)} (often the source's own)")
    P("\n".join("  - " + p for p in sprob[:200]))
    if restarts:
        P("\n### Sibling number restarts / gaps\n"); P("\n".join("- " + r for r in restarts[:400]))

    root_hold = {}
    if not is_root:
        rt = re.search(r"^root_text:\s*(\S+)", fm, re.M).group(1)
        for rid in re.findall(r"\s\^([\w-]+)\s*$", Path(rt).read_text(encoding="utf-8"), re.M):
            root_hold.setdefault(rid.split("-")[0], set()).update(holds(rid))
    ncit, lprob, unl, absent = (0, [], [], []) if is_root else links(lined, root_hold)
    if not is_root:
        P(f"\n## D. Links\n\n- paragraphs with a printed citation: {ncit:,}; link problems {len(lprob)}; "
          f"with no links {len(unl)}; citing a number the root does not print {len(absent)}")
        P("\n".join("  - " + p for p in lprob[:200]))
        if absent:
            P("\n### Cited numbers the root does not print (every number it does print is linked)\n")
            P("\n".join("- " + a for a in absent[:200]))
        if unl: P("\n### Printed citations with no links\n"); P("\n".join("- " + u for u in unl[:200]))
    (OUT / f"{name}-more.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
    sp_pb = sum(v for k, v in kinds.items() if k[1])
    print(f"{name:32} pb {pb_total:6,}  spacing-diffs {len(diffs):4} (at pb {sp_pb})  unaligned {sum(len(a)+len(b) for _,a,b in unaligned):3}  "
          f"bold {len(xml_sp):6,}/{len(md_sp):6,} {'OK' if not bprob else 'DIFF'}  struct-problems {len(sprob):3} restarts {len(restarts):4}  "
          + ("" if is_root else f"citations {ncit:6,} link-problems {len(lprob):3} root-gaps {len(absent):2} unlinked {len(unl):3}"), flush=True)
