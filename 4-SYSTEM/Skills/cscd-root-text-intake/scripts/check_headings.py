#!/usr/bin/env python3
"""check_headings.py — an independent heading check for cscd-root-text-intake and
cscd-commentary-intake (it does not use the converters' level rules).

Every heading element of the XML (<head> other than the book's, and <p> with rend
subhead / subsubhead / title / chapter), in order and with the same text (printed
number or range kept as printed, notes as [..]), must be a markdown heading (### or
deeper) of the file, and the file must have no heading the XML lacks. Part labels
("(Dutiyo bhāgo)") are text, not headings.

Usage: python3 -I check_headings.py <file.md> <xml> [<xml> …] [--book K]
"""
import difflib, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cscd_shape as cs  # noqa: E402

args = sys.argv[1:]
ALL = "--all" in args                   # print every difference in full
args = [a for a in args if a != "--all"]
book_k = None
if "--book" in args:
    i = args.index("--book"); book_k = int(args[i + 1]); del args[i:i + 2]
md, xmls = args[0], args[1:]
xh = []
for x in xmls:
    body = ET.parse(x).getroot().find(".//body")
    if book_k is not None:
        body = [d for d in body.iter("div") if d.get("type") == "book"][book_k - 1]
    books, reprint = 0, False
    for e in body.iter():
        if e.tag == "p" and e.get("rend") == "book":
            books += 1
            reprint = books > 1              # a later part reprints the book title …
            continue
        if (e.tag == "head" and e.get("rend") != "book") or (
                e.tag == "p" and e.get("rend") in ("subhead", "subsubhead", "title", "chapter")):
            t = cs.text_with_notes(e).replace("‘‘", '"').replace("’’", '"')
            if cs.part_label(t):
                continue
            h = cs.printed_heading(t)
            if reprint and h in xh:
                continue                     # … and the heading still open: text, not a heading
            reprint = False
            xh.append(h)
        elif e.tag == "p" and e.get("rend") not in ("centre", "nikaya"):
            reprint = False
lines = Path(md).read_text(encoding="utf-8").split("\n---\n", 1)[1].split("\n")
mh = [cs.printed_heading(re.sub(r"\s+\^[\w-]+$", "", l[l.index(" ") + 1:])).replace("**", "")
      for l in lines if re.match(r"^#{3,} ", l)]
ops = [o for o in difflib.SequenceMatcher(None, xh, mh, autojunk=False).get_opcodes() if o[0] != "equal"]
print(f"{Path(md).name}: xml headings {len(xh)}, md headings {len(mh)}, "
      + ("ALL MATCH" if not ops else f"{len(ops)} difference(s)"))
for op, a, b, c, d in (ops if ALL else ops[:5]):
    print("   ", op, xh[a:b] if ALL else xh[a:b][:3], "|", mh[c:d] if ALL else mh[c:d][:3])
sys.exit(1 if ops else 0)
