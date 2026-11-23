"""For each book of a commentary, list how each XML heading rank (chapter, title, subhead …)
lands in the vault's depth. A rank that lands at more than one depth within a book points
to a tangled tree (or to deliberate nesting — read the listed lines).

usage: python rank_depth.py <commentary.md> <xml1> [xml2 ...]
"""
import re, sys, difflib, collections
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
md, xmls = sys.argv[1], sys.argv[2:]
RANKS = ("book", "chapter", "title", "subhead", "subsubhead")
strip = lambda t: re.sub(r"^\s*[\d\-–]+\.\s*", "", re.sub(r"^\s*\(\d+\)\s*(?=\d+\.)", "", t)).replace("‘‘", '"').replace("’’", '"').strip()
xh = []
for x in xmls:
    for el in ET.parse(x).getroot().find(".//body").iter():
        if el.tag in ("head", "p") and el.get("rend") in RANKS:
            xh.append((el.get("rend"), strip("".join(el.itertext()))))
vh = [(len(m.group(1)), strip(re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2))), m.group(3), i + 1)
      for i, l in enumerate(open(md, encoding="utf-8").read().replace("\r\n", "\n").split("\n"))
      for m in [re.match(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$", l)] if m]
sm = difflib.SequenceMatcher(None, [t for r, t in xh], [t for d, t, i, ln in vh], autojunk=False)
by = collections.defaultdict(lambda: collections.defaultdict(list))
for t, i1, i2, j1, j2 in sm.get_opcodes():
    if t == "equal":
        for d in range(i2 - i1):
            rank = xh[i1 + d][0]
            depth, title, hid, ln = vh[j1 + d]
            book = hid.split("-")[0]
            by[book][rank].append((depth, ln, title, hid))
for book in sorted(by, key=lambda b: (len(b), b)):
    for rank, rows in by[book].items():
        depths = collections.Counter(r[0] for r in rows)
        if len(depths) > 1:
            common = depths.most_common(1)[0][0]
            odd = [r for r in rows if r[0] != common]
            print(f"book {book} <{rank}>: depths {dict(depths)} (usual {'#' * common})")
            for depth, ln, title, hid in odd[:12]:
                print(f"    line {ln}: {'#' * depth} {title} ^{hid}")
