"""Compare a Sutta-rails commentary .md with its CST tipitaka-xml volume(s) and its root.

usage: python compare_comm.py <commentary.md> <root.md> <out_report.md> <xml1> [xml2 ...]

The commentary layout (cscd-commentary-intake): every XML <p>/<head> is one vault line
(gāthā lines grouped into one block); printed paragraph numbers stay in the text
("1. Tattha …"); content IDs are a running counter per book (^1-1 … ^1-N), with ^T-1 /
^<book>-T<k> for homage and volume openings and Roman paths for front-matter headings;
transclusion lines ![[root#^b-n]] before a numbered paragraph link the root paragraphs it
cites. Variant readings <note> are [ … ], bold is **…**, CST's ‘‘ ’’ are ".

Checks: 1 content line by line (characters, after whitespace collapsing); 2 block-ID
hygiene and running counters; 3 headings vs XML (text) and hierarchy hints;
4 every link group vs the printed number of the paragraph after it, and its targets.
"""
import re, sys, difflib
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
md_path, root_path, out_path, xml_paths = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]

HEAD_RENDS = {"nikaya": 0, "book": 1, "chapter": 1, "title": 1, "subhead": 1, "subsubhead": 2}

def inner(el):
    s = el.text or ""
    for ch in el:
        if ch.tag == "note":
            s += "[" + inner(ch) + "]"
        elif ch.tag == "hi" and ch.get("rend") == "bold":
            s += "**" + inner(ch) + "**"
        elif ch.tag != "pb":
            s += inner(ch)
        s += ch.tail or ""
    return s

def strip_num(t):
    t = re.sub(r"^\s*\(\d+\)\s*(?=\d+\.)", "", t)
    return re.sub(r"^\s*[\d\-–]+\.\s*", "", t)

xml_lines, xml_heads = [], []          # ("H"|"P", text, rend, raw) ; (level, rend, text, raw)
def walk(el, depth):
    for ch in el:
        if ch.tag == "div":
            walk(ch, depth + 1)
        elif ch.tag == "head" or (ch.tag == "p" and ch.get("rend") in HEAD_RENDS):
            raw = inner(ch).strip()
            lvl = 0 if ch.get("rend") == "nikaya" else (depth if ch.tag == "head" else depth + HEAD_RENDS[ch.get("rend")])
            xml_heads.append((lvl, ch.get("rend"), strip_num(raw), raw))
            xml_lines.append(("H", strip_num(raw), ch.get("rend"), raw))
        elif ch.tag in ("p", "trailer"):
            t = inner(ch).strip()
            if t:
                xml_lines.append(("P", t, ch.get("rend"), t))
        else:
            walk(ch, depth)
for xp in xml_paths:
    walk(ET.parse(xp).getroot().find(".//body"), 0)

# ---------------------------------------------------------------- vault
raw_md = open(md_path, encoding="utf-8").read().replace("\r\n", "\n")
fm = re.match(r"\A---\n.*?\n---\n", raw_md, flags=re.S)
off = raw_md[:fm.end()].count("\n") if fm else 0
body = raw_md[fm.end():] if fm else raw_md
LINK = re.compile(r"^!\[\[([^#\]]+)#\^([\w-]+)\]\]\s*$")
blocks, lineno = [], off + 1               # (kind, start, lines, id, links)
for raw in re.split(r"(\n\s*\n)", body):
    if not raw.strip():
        lineno += raw.count("\n"); continue
    start = lineno + len(raw) - len(raw.lstrip("\n"))
    b = raw.strip("\n")
    lines = b.split("\n")
    if all(LINK.match(l.strip()) for l in lines):
        blocks.append(("L", start, lines, None, [LINK.match(l.strip()).groups() for l in lines]))
    elif re.match(r"^#+\s", b) and "\n" not in b:
        m = re.match(r"^(#+)\s+(.*?)\s*(\^[\w-]+)?\s*$", b)
        blocks.append(("H", start, [re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2))], m.group(3), len(m.group(1)) - 1))
    else:
        mid = re.search(r"\s*\^([\w-]+)\s*$", b)
        text = b[:mid.start()] if mid else b
        blocks.append(("P", start, text.split("\n"), mid.group(1) if mid else None, None))
    lineno += raw.count("\n")

vault_lines = []                          # (kind, text, line, id)
for k, st, lines, bid, extra in blocks:
    if k == "L":
        continue
    for i, l in enumerate(lines):
        vault_lines.append((k, l, st + i, bid))

def norm(s, xml):
    if xml:
        s = s.replace("‘‘", '"').replace("’’", '"')
    return re.sub(r"\s+", " ", s).strip()

out = []; P = out.append
name = md_path.replace("\\", "/").split("/")[-1]
P(f"# Commentary check: `{name}`\n")
P("Sources: " + ", ".join(p.replace("\\", "/").split("/")[-1] for p in xml_paths) + "\n")

# 1 content
xa = [norm(l[1], True) for l in xml_lines]
va = [norm(l[1], False) for l in vault_lines]
sm = difflib.SequenceMatcher(None, xa, va, autojunk=False)
hunks = [op for op in sm.get_opcodes() if op[0] != "equal"]
P(f"## 1. Content\n\n- XML lines {len(xa)}, vault lines {len(va)}, identical {sum(i2 - i1 for t, i1, i2, j1, j2 in sm.get_opcodes() if t == 'equal')}, hunks {len(hunks)}\n")
for t, i1, i2, j1, j2 in hunks[:80]:
    vl = vault_lines[j1][2] if j1 < len(vault_lines) else vault_lines[-1][2]
    P(f"### {t} — vault line {vl}")
    if t == "replace" and i2 - i1 == j2 - j1:
        for d in range(i2 - i1):
            aw, bw = xa[i1 + d].split(" "), va[j1 + d].split(" ")
            for tt, a1, a2, b1, b2 in difflib.SequenceMatcher(None, aw, bw, autojunk=False).get_opcodes():
                if tt != "equal":
                    P(f"- line {vault_lines[j1 + d][2]}: {tt}: XML `{' '.join(aw[max(0, a1 - 2):a2 + 2])}` → vault `{' '.join(bw[max(0, b1 - 2):b2 + 2])}`")
    else:
        for i in range(i1, i2):
            P(f"- XML [{xml_lines[i][0]}/{xml_lines[i][2]}] `{xa[i][:200]}`")
        for j in range(j1, j2):
            P(f"- vault line {vault_lines[j][2]} [{vault_lines[j][0]}] `{va[j][:200]}`")
    P("")

# 2 IDs
probs = []
seen = {}
counters = {}
for k, st, lines, bid, extra in blocks:
    if k == "L":
        continue
    if not bid:
        probs.append(f"line {st}: block without ID: {lines[0][:60]!r}"); continue
    if bid in seen:
        probs.append(f"line {st}: duplicate ^{bid} (first at line {seen[bid]})")
    seen[bid] = st
    if k == "P":
        m = re.match(r"^(\d+)-(\d+)$", bid)
        if m:
            counters.setdefault(m.group(1), []).append((int(m.group(2)), st))
        elif not re.match(r"^(T-\d+|\d+-T\d+|\d+-U\d+)$", bid):
            probs.append(f"line {st}: unusual content ID ^{bid}")
    for l in lines:
        if "  " in l or l != l.strip():
            probs.append(f"line {st}: stray whitespace: {l.strip()[:60]!r}")
for book, nums in counters.items():
    ns = [n for n, s in nums]
    if ns != list(range(1, len(ns) + 1)):
        first = next(i for i, n in enumerate(ns) if n != i + 1)
        probs.append(f"book {book}: content IDs not 1…{len(ns)} — first break at line {nums[first][1]} (^{book}-{ns[first]}, expected {first + 1})")
P("## 2. Block IDs\n")
P("- running counters: " + ", ".join(f"book {b}: {len(n)}" for b, n in counters.items()))
P("\n".join("- " + p for p in probs[:80]) if probs else "- no problems")
P("")

# 3 headings
vh = [(lvl, lines[0], bid, st) for k, st, lines, bid, lvl in blocks if k == "H"]
xh = [norm(h[2], True) for h in xml_heads]
vt = [norm(h[1], False) for h in vh]
hm = difflib.SequenceMatcher(None, xh, vt, autojunk=False)
txt_mis, raw_of, lvl_mis = [], {}, []
for t, i1, i2, j1, j2 in hm.get_opcodes():
    if t == "equal":
        for d in range(i2 - i1):
            raw_of[vh[j1 + d][3]] = xml_heads[i1 + d][3]
            if xml_heads[i1 + d][0] != vh[j1 + d][0]:
                lvl_mis.append((vh[j1 + d], xml_heads[i1 + d]))
    else:
        txt_mis.append((t, [h[3] for h in xml_heads[i1:i2]], [(h[1], h[2], h[3]) for h in vh[j1:j2]]))
hints, by_parent = [], {}
for lvl, t, hid, ln in vh:
    if not hid or hid == "^0":
        continue
    segs = hid[1:].split("-")
    if segs[-1] != "0" or len(segs) - 1 != lvl:
        hints.append(f"line {ln}: `{t}` {hid}: ID path does not match heading depth {lvl}")
    m = re.match(r"^\s*(?:\(\d+\)\s*)?(\d+)[\.\-–]", raw_of.get(ln, ""))
    by_parent.setdefault("-".join(segs[:-2]), []).append((int(m.group(1)) if m else None, ln, hid, raw_of.get(ln, "")))
for parent, kids in by_parent.items():
    prev = None
    for n, ln, hid, raw in kids:
        if n is not None and prev is not None and n <= prev[0]:
            hints.append(f"line {ln}: `{raw}` {hid} restarts numbering after sibling `{prev[1]}`")
        if n is not None:
            prev = (n, raw)
seq = [b for b in blocks if b[0] in ("H", "P")]
for i, (k, st, lines, bid, lvl) in enumerate(seq):
    if k == "H" and bid != "^0":
        nxt = seq[i + 1] if i + 1 < len(seq) else None
        if nxt is None or (nxt[0] == "H" and nxt[4] <= lvl):
            hints.append(f"line {st}: `{lines[0]}` {bid} is empty")
P(f"## 3. Headings\n\n- XML {len(xh)}, vault {len(vt)}, text mismatches {len(txt_mis)}")
for t, a, b in txt_mis[:60]:
    P(f"  - {t}: XML {a} → vault {b}")
P(f"- level mismatches (XML: nikaya 0, div head = div depth, p heading = depth + 1): {len(lvl_mis)}")
for v, x in lvl_mis[:200]:
    P(f"  - line {v[3]}: `{v[1]}` {v[2]}: vault level {v[0]}, XML level {x[0]} ({x[1]})")
P(f"- hierarchy hints: {len(hints)}")
for h in hints[:200]:
    P("  - " + h)
P("")

# 4 links
root_ids = set(re.findall(r"\^([\w-]+)\s*$", open(root_path, encoding="utf-8").read(), re.M))
spans = {}                                  # book -> [(lo, hi, id)] for content IDs ^b-n and range IDs ^b-n-m
for rid in root_ids:
    m = re.match(r"^(\d+)-(\d+)(?:-(\d+))?$", rid)
    if m and not rid.endswith("-0"):
        spans.setdefault(m.group(1), []).append((int(m.group(2)), int(m.group(3) or m.group(2)), rid))
def within(book, a, b):
    """root content IDs of `book` whose span overlaps the printed range a..b, in order"""
    return [r for lo, hi, r in sorted(spans.get(book, [])) if lo <= b and hi >= a]
link_probs, groups, nlinks, missing = [], 0, 0, 0
for i, (k, st, lines, bid, links) in enumerate(blocks):
    if k != "L":
        continue
    groups += 1; nlinks += len(links)
    got = [t for f, t in links]
    for t in got:
        if t not in root_ids:
            missing += 1; link_probs.append(f"line {st}: target ^{t} not in the root")
    nxt = blocks[i + 1] if i + 1 < len(blocks) else None
    pm = re.match(r"^(\d+)(?:-(\d+))?\.", nxt[2][0]) if nxt and nxt[0] == "P" else None
    if not pm:
        link_probs.append(f"line {st}: links {got} not followed by a numbered paragraph"); continue
    a, b = pm.group(1), pm.group(2)
    if b and len(b) < len(a):
        b = a[:len(a) - len(b)] + b
    book = got[0].split("-")[0]
    want = [f"{book}-{n}" for n in range(int(a), int(b or a) + 1)] if not b or int(b) >= int(a) else None
    if got != want and got != [f"{book}-{a}-{b}"] and got != within(book, int(a), int(b or a)):
        link_probs.append(f"line {nxt[1]}: printed `{pm.group(0)}` but links {got}")
P(f"## 4. Root links\n\n- groups {groups}, links {nlinks}, targets missing {missing}, groups not matching the printed number {len(link_probs) - missing}")
for p in link_probs[:80]:
    P("  - " + p)

open(out_path, "w", encoding="utf-8").write("\n".join(out))
print(f"lines X{len(xa)}/V{len(va)} hunks={len(hunks)} idProbs={len(probs)} heads X{len(xh)}/V{len(vt)} "
      f"headTxtMis={len(txt_mis)} headLvlMis={len(lvl_mis)} hints={len(hints)} linkGroups={groups} links={nlinks} "
      f"linkMissing={missing} linkMismatch={len(link_probs) - missing}")
