"""Sutta review, one nikāya at a time (the Vinaya re-check of 2026-11-23, adapted).

For every file of the nikāya (root text and commentaries) it checks:
  1. completeness: the XML files named in source_filename, read in order, against the
     vault file, line by line (Vinaya comm_coverage.py normalisation: notes as [ ],
     ‘‘ ’’ → ", spaces collapsed, no space before punctuation, a hangnum joined to the
     next line; vault transclusions, footnote definitions, **bold**, [^ref] and block IDs
     dropped; heading markers dropped and printed heading numbers stripped on both sides);
  2. the XML in 0-INBOX/raw-data is byte-identical to tipitaka-xml romn/;
  3. block IDs: every block has one, all unique, heading IDs end in -0 and their path
     length agrees with the # count; root paragraphs: ID agrees with the printed number;
  4. transclusions: every ![[file#^id]] points at an existing block of that file.

usage (from the vault root):  python -I -X utf8 0-INBOX/sutta-review/review_nikaya.py dn
"""
import re, sys, difflib, glob, os
import xml.etree.ElementTree as ET
from pathlib import Path

ROMN = Path(r"D:\Work\OpenPecha\tipitaka-xml\romn")
RAW = Path("0-INBOX/raw-data")
OUT = Path("0-INBOX/sutta-review")
NAME = {"dn": "dighanikaya", "mn": "majjhimanikaya", "sn": "samyuttanikaya",
        "an": "anguttaranikaya", "kn": "khuddakanikaya"}
RESTORE = "--restore" in sys.argv   # put dropped printed heading numbers back (approved 2026-11-25)
argv = [a for a in sys.argv[1:] if a != "--restore"]
nk = argv[0]
only = argv[1:]  # optional: restrict to these file names
files = sorted(glob.glob(f"1-SOURCES/Text/pi-{NAME[nk]}.md")) + \
        sorted(glob.glob(f"1-SOURCES/Commentaries/pi-{NAME[nk]}*.md"))
if only: files = [f for f in files if any(o in f for o in only)]

HEAD_REND = {"chapter", "title", "subhead", "subsubhead", "nikaya", "book"}
NUM = re.compile(r"^(?:\(?\d+[\d\-–.,()]*\.?\)?\s*)+(?=\D)")  # "1. X", "1.X", "(1) 1. X"
LABEL = re.compile(r"\s*\((aṭṭhakathā|ṭīkā|abhinavaṭīkā)\)\s*$")


def inner(el):
    s = el.text or ""
    for ch in el:
        if ch.tag == "note":
            s += "[" + inner(ch) + "]"
        elif ch.tag != "pb":
            s += inner(ch)
        s += ch.tail or ""
    return s


def norm(s):
    s = s.replace("‘‘", '"').replace("’’", '"')
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\[\s+", "[", s); s = re.sub(r"\s+\]", "]", s)
    return re.sub(r"\s+([.,;:!?…])", r"\1", s)


full = {}  # XML heading lines before their printed number is stripped for alignment


def xml_lines(stems):
    full.clear(); vfull.clear()
    out = []
    for st in stems:
        body = ET.parse(ROMN / st).getroot().find(".//body")
        pend = ""
        for el in body.iter():
            if el.tag not in ("head", "p", "trailer"):
                continue
            t = norm(inner(el))
            if not t:
                continue
            if el.get("rend") == "hangnum":
                pend = t + " "; continue
            head = el.tag == "head" or el.get("rend") in HEAD_REND
            if head:
                full[len(out)] = t   # the heading as printed, number included
                t = NUM.sub("", t)
            out.append((st, pend + t, "H" if head else "P")); pend = ""
    return out


def read(path):
    raw = Path(path).read_text(encoding="utf-8")
    crlf = raw.count("\r\n"); lf = raw.count("\n")
    raw = raw.replace("\r\n", "\n")
    m = re.match(r"\A---\n(.*?)\n---\n", raw, re.S)
    return m.group(1), raw[m.end():], raw[:m.end()].count("\n"), (crlf, lf)


vfull = {}


def vault_lines(body, off):
    out, eds = [], 0
    # the block ID of each line: its own, or that of the line ending its block
    raw = body.split("\n"); bid = [None] * len(raw); cur = None
    for k in range(len(raw) - 1, -1, -1):
        if not raw[k].strip(): cur = None; continue
        m = re.search(r"\s\^([\w-]+)\s*$", raw[k])
        if m: cur = m.group(1)
        bid[k] = cur
    for n, l in enumerate(raw, off + 1):
        if not l.strip() or l.startswith("![[") or re.match(r"^\[\^[\w-]+\]:", l):
            continue
        b = bid[n - off - 1]
        l = re.sub(r"\s*\^[\w-]+\s*$", "", l)
        l = re.sub(r"\[\^[\w-]+\]", "", l)
        eds += len(re.findall(r"\[Ed:[^\]]*\]", l))
        l = re.sub(r"\s*\[Ed:[^\]]*\]", "", l)
        m = re.match(r"^#+\s+(.*)$", l)
        kind = "P"
        if m:
            kind = "H"
            l = LABEL.sub("", re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(1)))
            vfull[n] = norm(l.replace("**", ""))   # the heading as the vault has it
            l = NUM.sub("", l)
        l = l.replace("**", "")
        out.append((n, norm(l), kind, b))
    return out, eds


PARANUM = re.compile(r"^(\d+(?:-\d+)?)\.\s?")


def root_numbers(xl, vl):
    """A root prints its paragraph number in the block ID, not the text: take the
    number off an XML line when the vault line lacks it, and check it against the ID.
    Only lines that are then identical are paired; the rest stay differences."""
    sm = difflib.SequenceMatcher(None, [PARANUM.sub("", t) for _, t, _ in xl],
                                 [t for _, t, _, _ in vl], autojunk=False)
    bad, n = [], 0
    xl = list(xl)
    for t, i1, i2, j1, j2 in sm.get_opcodes():
        if t != "equal": continue
        for d in range(i2 - i1):
            st, txt, k = xl[i1 + d]
            m = PARANUM.match(txt)
            if m and not vl[j1 + d][1].startswith(m.group(0)):
                n += 1
                # ^<book>-<n>, ^<book>-<a>-<b> for a printed range a-b, and in KN a zone or
                # section before the number (^5-1-5, ^1-6-3) and x<k> on a repeat (annex §4)
                if not re.fullmatch(rf"\d+(?:-\w+)?-{re.escape(m.group(1))}(?:x\d+)?", vl[j1 + d][3] or ""):
                    bad.append(f"line {vl[j1+d][0]}: XML number {m.group(1)} but ^{vl[j1+d][3]}")
                xl[i1 + d] = (st, txt[m.end():], k)
    return xl, n, bad


targets = {}


def block_ids(path):
    if path not in targets:
        _, body, _, _ = read(path)
        targets[path] = set(re.findall(r"\s\^([\w-]+)\s*$", body, re.M))
    return targets[path]


summary = []
for f in files:
    fm, body, off, (crlf, lf) = read(f)
    stems = [s.strip() for s in re.search(r"^source_filename:\s*\[(.*)\]", fm, re.M).group(1).split(",")]
    is_root = "/Text/" in f
    rep = [f"# Review: `{f}`\n", f"XML: {', '.join(stems)}\n"]
    P = rep.append

    # 2. raw-data copies
    raw_bad = []
    for st in stems:
        hits = list(RAW.rglob(st))
        if not hits: raw_bad.append(f"{st}: not in raw-data")
        elif hits[0].read_bytes() != (ROMN / st).read_bytes(): raw_bad.append(f"{st}: differs from romn")

    # 1. completeness
    xl = xml_lines(stems)
    vl, eds = vault_lines(body, off)
    nnum, numbad = 0, []
    if is_root:
        xl, nnum, numbad = root_numbers(xl, vl)
    sm = difflib.SequenceMatcher(None, [t for _, t, _ in xl], [t for _, t, _, _ in vl], autojunk=False)
    hunks = [o for o in sm.get_opcodes() if o[0] != "equal"]
    # headings that match only once the printed number is stripped: the number was dropped
    dropped = []
    for t, i1, i2, j1, j2 in sm.get_opcodes():
        if t != "equal": continue
        for d in range(i2 - i1):
            xi, (vn, _, vk, _) = i1 + d, vl[j1 + d]
            if vk != "H": continue
            xs = full.get(xi, xl[xi][1])   # an XML paragraph the vault made a heading: as printed
            if xs != vfull[vn]:
                dropped.append((vn, xs, vfull[vn]))
    # a line that is a heading on one side and text on the other (a reprinted title kept as
    # text; a paragraph the vault made a heading) is compared as printed, number included
    kind_changed, rest = [], []
    for t, i1, i2, j1, j2 in hunks:
        if t == "replace" and i2 - i1 == j2 - j1:
            left = []
            for d in range(i2 - i1):
                xi, vj = i1 + d, j1 + d
                vn, vtxt, vk, _ = vl[vj]
                xs, vs = full.get(xi, xl[xi][1]), vfull.get(vn, vtxt)
                if xl[xi][2] != vk and xs == vs:
                    kind_changed.append((vn, xl[xi][2], vk, xs))
                elif vk == "H" and xl[xi][2] == "P" and NUM.sub("", xs) == NUM.sub("", vs) and NUM.match(xs):
                    dropped.append((vn, xs, vs))
                else:
                    left.append(d)
            if not left:
                continue
        rest.append((t, i1, i2, j1, j2))
    hunks = rest
    if RESTORE and dropped:
        # put each printed number back, exactly as the XML prints it; nothing else on the line changes
        assert crlf == 0, f"{f}: expected LF line endings"
        text = Path(f).read_text(encoding="utf-8")
        lines = text.split("\n"); skipped = []
        for vn, xs, v in dropped:
            prefix = xs[:len(xs) - len(NUM.sub("", xs))]
            m = re.match(r"^(#+\s+)(\*\*)?(.*?)(\*\*)?(\s+\^[\w-]+\s*)$", lines[vn - 1])
            if not prefix or not m or bool(m.group(2)) != bool(m.group(4)):
                skipped.append((vn, xs, lines[vn - 1])); continue
            content = prefix + NUM.sub("", m.group(3))
            if norm(LABEL.sub("", content).replace("**", "")) != xs:
                skipped.append((vn, xs, lines[vn - 1])); continue
            lines[vn - 1] = m.group(1) + (m.group(2) or "") + content + (m.group(4) or "") + m.group(5)
        bk = OUT / "backups" / Path(f).name
        bk.parent.mkdir(exist_ok=True)
        if not bk.exists(): bk.write_bytes(Path(f).read_bytes())
        Path(f).write_bytes("\n".join(lines).encode("utf-8"))
        print(f"  restored {len(dropped) - len(skipped)} heading numbers in {f}; skipped {len(skipped)}")
        for s in skipped: print("    skipped", s)
    miss = sum(i2 - i1 for t, i1, i2, j1, j2 in hunks)
    extra = sum(j2 - j1 for t, i1, i2, j1, j2 in hunks)
    P("## 1. Completeness (line by line)\n")
    P(f"- XML {len(xl):,} lines; vault {len(vl):,} lines; `[Ed:]` notes removed before comparing: {eds}")
    if is_root:
        P(f"- printed paragraph numbers carried by the block ID instead of the text: {nnum}; number ≠ ID: {len(numbad)}")
        P("\n".join("  - " + b for b in numbad[:100]))
    P(f"- XML lines not matched: {miss}; vault lines not matched: {extra}; hunks: {len(hunks)}")
    P(f"- headings whose printed number is not in the vault heading: {len(dropped)}")
    P(f"- lines that are a heading on one side and text on the other, identical as printed: {len(kind_changed)}\n")
    if kind_changed:
        P("### Heading ↔ text, same words and number\n")
        P("\n".join(f"- line {n}: XML {'heading' if a == 'H' else 'text'}, vault {'heading' if b == 'H' else 'text'}: `{x}`" for n, a, b, x in kind_changed))
        P("")
    if dropped:
        P("### Headings without their printed number\n")
        P("\n".join(f"- line {n}: XML `{x}` → vault `{v}`" for n, x, v in dropped))
        P("")
    for t, i1, i2, j1, j2 in hunks:
        P(f"### {t}, vault line {vl[j1][0] if j1 < len(vl) else vl[-1][0]}")
        if t == "replace" and i2 - i1 == j2 - j1:
            for d in range(i2 - i1):
                aw, bw = xl[i1 + d][1].split(" "), vl[j1 + d][1].split(" ")
                for tt, a1, a2, b1, b2 in difflib.SequenceMatcher(None, aw, bw, autojunk=False).get_opcodes():
                    if tt != "equal":
                        P(f"- line {vl[j1+d][0]} [{xl[i1+d][2]}]: {tt}: XML `{' '.join(aw[max(0,a1-2):a2+2])}` → vault `{' '.join(bw[max(0,b1-2):b2+2])}`")
        else:
            for i in range(i1, i2): P(f"- XML [{xl[i][0]} {xl[i][2]}]: `{xl[i][1][:200]}`")
            for j in range(j1, j2): P(f"- vault line {vl[j][0]} [{vl[j][2]}]: `{vl[j][1][:200]}`")
        P("")

    # 3. block IDs
    probs, ids, nhead = [], {}, 0
    lineno = off
    for blk in re.split(r"(\n\s*\n)", body):
        start = lineno + 1 + (len(blk) - len(blk.lstrip("\n")))
        lineno += blk.count("\n")
        b = blk.strip("\n")
        if not b.strip() or b.startswith("![[") or re.match(r"^\[\^[\w-]+\]:", b):
            continue
        # a commentary paragraph may carry its transclusion lines just above it in the same block
        lines = [l for l in b.split("\n") if not l.startswith("![[")]
        b = "\n".join(lines)
        m = re.search(r"\s\^([\w-]+)\s*$", b)
        if not m:
            probs.append(f"line {start}: block without ID: `{b[:80]}`"); continue
        bid = m.group(1)
        if bid in ids: probs.append(f"line {start}: duplicate ^{bid} (first line {ids[bid]})")
        ids[bid] = start
        h = re.match(r"^(#+)\s", b)
        if h:
            nhead += 1
            lvl, segs = len(h.group(1)) - 1, bid.split("-")
            if bid != "0":
                if segs[-1] != "0": probs.append(f"line {start}: heading ^{bid} does not end in -0")
                if len(segs) - 1 != lvl: probs.append(f"line {start}: heading ^{bid} path {len(segs)-1} ≠ level {lvl}")
        elif is_root:
            mn = re.match(r"^(\d+)(?:-\d+)?\.\s", b)
            # a U block keeps a number that is not a paragraph number as text (tree_to_md.py:
            # the Vimānavatthu's sub-story titles "1. Vatthuttamadāyikāvimānavatthu ^6-U1")
            if mn and not re.search(r"-U\d+$", bid) and bid.split("-")[-1] != mn.group(1):
                probs.append(f"line {start}: ^{bid} but paragraph number {mn.group(1)}")
    P("## 2. Block IDs\n")
    P(f"- {len(ids):,} IDs ({nhead} headings), problems: {len(probs)}")
    P("\n".join("  - " + p for p in probs[:200]))
    P("")

    # 4. transclusions
    tl = re.findall(r"!\[\[([^#\]]+)#\^([\w-]+)\]\]", body)
    bad = [(t, i) for t, i in tl if not os.path.exists(t) or i not in block_ids(t)]
    P("## 3. Transclusions\n")
    P(f"- {len(tl):,} transclusions, unresolved: {len(bad)}")
    P("\n".join(f"  - {t}#^{i}" for t, i in bad[:100]))
    P("")
    P("## 4. XML copies in raw-data\n")
    P("- all byte-identical to romn/" if not raw_bad else "\n".join("- " + r for r in raw_bad))
    eol = "CRLF" if crlf == lf else "LF" if crlf == 0 else "MIXED"
    P(f"\n## 5. Line endings\n\n- {eol} (CRLF {crlf:,} of {lf:,} line breaks)")

    name = Path(f).stem
    (OUT / f"{name}-detail.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
    print(f"{name:34} XML files {len(stems):2}  XML lines {len(xl):7,}  vault {len(vl):7,}  "
          f"XML-unmatched {miss:4}  vault-unmatched {extra:4}  heading-numbers-dropped {len(dropped):5,}  IDs {len(ids):6,} id-problems {len(probs):3}  "
          + (f"numbers-in-ID {nnum:,} number≠ID {len(numbad)}  " if is_root else "")
          + f"transclusions {len(tl):6,} unresolved {len(bad):3}  raw-data-bad {len(raw_bad)}  Ed {eds}  {eol}", flush=True)
