#!/usr/bin/env python3
"""
verify_commentary.py — step 7 of cscd-commentary-intake: check a commentary
file against the CSCD XML volume(s) it came from.

1. IDs: one ID per block on its last line; content ^<book>-1 … ^<book>-N
   contiguous and unique; headings end -0; transclusions carry no ID.
2. Words: the file's word stream (frontmatter, transclusion lines, IDs, '#'
   markers and the h1's "(<layer>)" label removed) equals the XML's (notes as
   [..], doubled quotes as ", page markers dropped, numbers on headings
   stripped).
3. Citations: every XML paragraph with a printed number (@n) is, in order, a
   block that opens with that number and is preceded by exactly the root links
   it cites (ranges expanded, truncated tails "65-6" = 65–66), except the
   citations listed in <file>.unresolved.json ("unresolved", and the section
   numbers under an --unlinked heading, "unlinked_section_numbers"), which
   must have no links. The log is matched occurrence by occurrence, in order,
   so a logged "1." exempts one unlinked "1." — not every "1." in the file.
   Every link points at an existing block of the root file.
4. Bold: every <hi rend="bold"> is a **…** span, in order, with exactly the
   same text; every ** pairs up (cscd-root-text-intake/scripts/bold_check.py). Words are compared with
   the ** removed.
Exit status 1 on any problem.
With --book K, only the K-th <div type="book"> of the (single) XML is checked: a CSCD
commentary volume can hold several nipātas, each its own vault file (AN).
Usage: python3 -I verify_commentary.py <file.md> <root.md> <xml> [<xml> …] [--unresolved <log.json>] [--book K]
       (default log: <file>.unresolved.json next to the file)
"""
import difflib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "cscd-root-text-intake" / "scripts"))
import bold_check  # noqa: E402

args = sys.argv[1:]
unres_arg = None
if "--unresolved" in args:
    k = args.index("--unresolved"); unres_arg = args[k + 1]; del args[k:k + 2]
PER_SECTION = "--per-section" in args          # root IDs ^<book>-<section>-<N>
args = [a for a in args if a != "--per-section"]
PRESECTION = None                               # --presection K: as build_commentary.py
if "--presection" in args:
    k = args.index("--presection"); PRESECTION = args[k + 1]; del args[k:k + 2]
ZONES = None                                    # a zoned root's labels in order (zone_link.py)
if "--zones" in args:
    k = args.index("--zones"); ZONES = args[k + 1].split(","); del args[k:k + 2]
book_k = None
if "--book" in args:
    k = args.index("--book"); book_k = int(args[k + 1]); del args[k:k + 2]
md_path, root_path, xmls = args[0], args[1], args[2:]
problems = []
HEADING_RENDS = {"chapter", "title", "subhead", "subsubhead"}
NUM_FIX = re.compile(r"^(\d+(?:-\d+)*)\.(?=\S)")
LEAD = re.compile(r"^\s*(?:\(\d+\)\s*)?\d+(?:-\d+)*\.\s*")   # "1. ", "1-10. ", "(6) 1. "
CIT = re.compile(r"^(\d+)(?:-(\d+))?\.(?:\s|$)")
ID_RE = re.compile(r"\s\^([\w-]+)\s*$")
TRANS = re.compile(r"^!\[\[([^#\]]+)#\^([\w-]+)\]\]$")

# ---------------- XML side
def render(el, out, top=True):
    if el.tag == "pb":
        pass
    elif el.tag == "note":
        out.append(" [" + "".join(el.itertext()).strip() + "]")
    elif el.tag == "hi" and el.get("rend") == "dot":
        out.append(".")
    else:
        if el.text:
            out.append(el.text)
        for c in el:
            render(c, out, False)
    if not top and el.tail:
        out.append(el.tail)


xml_words, xml_cits, xml_bodies = [], [], []
xml_secs = []          # per citation: the printed number of the section heading it sits under
cur_sec = None
seen_sec = False
for x in xmls:
    body = ET.parse(x).getroot().find(".//body")
    if book_k is not None:
        # the K-th book, plus lines outside the books: before the first book they
        # belong to the first, after the last to the last (as cscd_xml_to_json.py)
        books = [d for d in body if d.tag == "div" and d.get("type") == "book"]
        kids = list(body); pos = [k for k, c in enumerate(kids) if c in books]
        sel = ET.Element("body")
        for k, c in enumerate(kids):
            if c is books[book_k - 1] or (c not in books and ((k < pos[0] and book_k == 1) or (k > pos[-1] and book_k == len(books)))):
                sel.append(c)
        body = sel
    xml_bodies.append(body)
    # a div-less file (KN aṭṭhakathās, tree mode): a heading paragraph tree_levels leaves out
    # is a later part's reprinted heading, kept as text with its printed number (cscd_shape)
    import cscd_shape  # noqa: E402
    lv = cscd_shape.tree_levels(body) if body.find(".//div[@type='book']") is None else None
    for el in body.iter():
        if el.tag not in ("p", "head", "trailer"):
            continue
        buf = []
        render(el, buf)
        s = "".join(buf).replace("‘‘", '"').replace("’’", '"')
        s = re.sub(r"\s+", " ", s)
        s = re.sub(r"\s+\]", "]", re.sub(r"\[\s+", "[", s)).strip()
        s = re.sub(r"^(\d+(?:-\d+)*)\s+\.", r"\1.", s)   # "8 ." = the number's two tags (as the converter)
        s = NUM_FIX.sub(r"\1. ", s)
        rend = el.get("rend") or ""
        reprinted = (lv is not None and el.tag == "p" and rend in HEADING_RENDS and id(el) not in lv
                     and not cscd_shape.part_label(cscd_shape.text_of(el)))
        if (el.tag == "head" or rend in HEADING_RENDS) and not reprinted:
            s = LEAD.sub("", s)
        xml_words += s.split()
        # a printed citation; an @n alone (the AN homage, n="0") prints nothing
        if rend == "chapter":                      # a section heading: "6. Ratanasuttavaṇṇanā"
            msec = re.match(r"^\s*(\d+)\.", "".join(el.itertext()))
            cur_sec = msec.group(1) if msec else None
            seen_sec = seen_sec or bool(msec)
        if el.tag == "p" and el.get("n") and any(h.get("rend") == "paranum" for h in el.iter("hi")):
            xml_cits.append(el.get("n"))
            # before the first numbered section: --presection (front matter quoting the root's
            # opening verses, a decision per work), as the converter
            xml_secs.append(cur_sec or (PRESECTION if not seen_sec else None))

# ---------------- md side
root_ids = set(re.findall(r"\s\^([\w-]+)\s*$", Path(root_path).read_text(encoding="utf-8"), re.M))
text = Path(md_path).read_text(encoding="utf-8")
fm, body = text.split("\n---\n", 1)
book = int(re.search(r"^root_text:.*-(\d+)\.md\s*$", fm, re.M).group(1))
lines = body.split("\n")

md_words = []
for ln in lines:
    if TRANS.match(ln.strip()):
        continue
    ln = ID_RE.sub("", ln)
    if ln.startswith("# "):
        ln = re.sub(r"\s*\([^)]*\)\s*$", "", ln)   # editorial layer label
    ln = re.sub(r"^#+\s+", "", ln)
    # a bold tag can split a doubled quote the converter then leaves as printed
    # (Jātaka-aṭṭhakathā "suggati’**’nti"): normalised here as on the XML side
    md_words += bold_check.strip_bold(ln).replace("‘‘", '"').replace("’’", '"').split()
md_bold, unpaired = bold_check.md_spans(lines, exact=True)
for u in unpaired[:5]:
    problems.append(f"unpaired ** on line: {u!r}")
problems += bold_check.compare(bold_check.xml_spans(xml_bodies, exact=True), md_bold, "xml")

# blocks
blocks, cur = [], []
for ln in lines:
    if not ln.strip():
        if cur: blocks.append(cur); cur = []
        continue
    if ln.startswith("#"):
        if cur: blocks.append(cur); cur = []
        blocks.append([ln]); continue
    cur.append(ln)
if cur: blocks.append(cur)

content_n, heads, pending, md_cits = [], [], [], []
for b in blocks:
    if all(TRANS.match(x.strip()) for x in b):
        for x in b:
            m = TRANS.match(x.strip())
            if m.group(1) != root_path:
                problems.append(f"link to another file: {x.strip()}")
            if m.group(2) not in root_ids:
                problems.append(f"link to missing root block: {x.strip()}")
            pending.append(m.group(2))
        continue
    for x in b[:-1]:
        if ID_RE.search(x):
            problems.append(f"ID on a non-last line: {x[:60]}")
    m = ID_RE.search(b[-1])
    if not m:
        problems.append(f"block without ID: {b[0][:60]}")
        pending = []; continue
    bid = m.group(1)
    if b[0].startswith("#"):
        heads.append(bid)
        if bid != "0" and not bid.endswith("-0"):
            problems.append(f"heading ID not -0: {bid}")
        if pending:
            problems.append(f"links directly before a heading: {pending[:3]}")
        pending = []; continue
    if bid.startswith("T-"):
        pending = []; continue
    mm = re.fullmatch(rf"{book}-(\d+)", bid)
    if not mm:
        problems.append(f"unexpected content ID {bid}")
    else:
        content_n.append(int(mm.group(1)))
    c = CIT.match(b[0])
    alone = re.fullmatch(r"(\d+)(?:\s+\^[\w-]+)?", b[0].strip()) if len(b) == 1 else None
    if c:
        md_cits.append((b[0].split(".")[0], list(pending), b[0][:60]))
    elif alone:
        # the number alone, its dot opening the next paragraph (Apadāna-aṭṭhakathā "314"): a
        # cited block; the XML side counts it from its @n as for any other citation
        md_cits.append((alone.group(1), list(pending), b[0][:60]))
    elif pending:
        problems.append(f"links before an uncited paragraph: {b[0][:60]}")
    pending = []

if content_n != list(range(1, len(content_n) + 1)):
    problems.append("content IDs are not ^%d-1 … contiguous" % book)
if len(set(heads)) != len(heads):
    problems.append("duplicate heading IDs")

# words
if xml_words != md_words:
    sm = difflib.SequenceMatcher(a=xml_words, b=md_words, autojunk=False)
    diffs = [o for o in sm.get_opcodes() if o[0] != "equal"]
    problems.append(f"words differ from the XML in {len(diffs)} place(s)")
    for tag, a0, a1, b0, b1 in diffs[:8]:
        problems.append(f"   {tag}: xml {' '.join(xml_words[a0:a1])[:70]!r} | md {' '.join(md_words[b0:b1])[:70]!r}")

# citations
unres_path = Path(unres_arg) if unres_arg else Path(md_path[:-3] + ".unresolved.json")
from collections import Counter
log = json.loads(unres_path.read_text(encoding="utf-8")) if unres_path.exists() else {}
remaining = Counter(u[0].rstrip(".") for u in log.get("unresolved", []) + log.get("unlinked_section_numbers", []))


COVER = {}   # printed root number -> the root block that holds it (^b-N, or a range ^b-A-B)
for rid in sorted(root_ids):
    mm = re.fullmatch(rf"{book}-(\d+)(?:-(\d+))?", rid)
    if mm:
        for k in range(int(mm.group(1)), int(mm.group(2) or mm.group(1)) + 1):
            COVER.setdefault(k, rid)


def covering(nums):
    out = []
    for k in nums:
        rid = COVER.get(k)
        if rid and rid not in out:
            out.append(rid)
    return out


def expand(n):
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", n)
    if not m:
        return None
    a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
    if b < a and len(m.group(2)) < len(m.group(1)):
        b = int(m.group(1)[: -len(m.group(2))] + m.group(2))
    if b < a:
        return None
    return list(range(a, b + 1))


if ZONES is not None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import zone_link  # noqa: E402
    ZL = zone_link.ZoneLinker(Path(root_path).read_text(encoding="utf-8"), book, ZONES)
xml_linkable = [n for n in xml_cits]
ok = bad = skipped = 0
md_by_order = [c for c in md_cits]
# every XML citation must appear, in order, as a cited block
xi = 0
for printed, links, head in md_by_order:
    if not links and remaining[printed] > 0 and (xi >= len(xml_linkable) or xml_linkable[xi] != printed):
        # logged, unlinked, and not the XML's next citation: the text's own
        # numbering, which the XML does not mark as a paragraph number (no @n)
        remaining[printed] -= 1; skipped += 1
        continue
    while xi < len(xml_linkable) and xml_linkable[xi] != printed:
        if remaining[xml_linkable[xi]] > 0:   # logged, and not a cited block in the md
            remaining[xml_linkable[xi]] -= 1; skipped += 1; xi += 1; continue
        problems.append(f"XML citation {xml_linkable[xi]} has no matching cited block (next md block cites {printed})")
        xi += 1
    if xi >= len(xml_linkable):
        problems.append(f"md block cites {printed} beyond the XML's citations"); break
    sec_here = xml_secs[xi]
    xi += 1
    exp = expand(printed)
    if not links and remaining[printed] > 0:
        remaining[printed] -= 1
        skipped += 1
        continue
    if exp is None:
        if links:
            problems.append(f"unreadable citation {printed} has links {links[:3]}")
        skipped += 1
        continue
    if ZONES is not None:
        exp = ZL.link(exp)[0]
    else:
        exp = [f"{book}-{sec_here}-{k}" for k in exp if f"{book}-{sec_here}-{k}" in root_ids] if PER_SECTION else covering(exp)
    if links == exp:
        ok += 1
    else:
        bad += 1
        problems.append(f"citation {printed}: links {links[:4]}… expected {exp[:4]}…")
for rest in xml_linkable[xi:]:
    if remaining[rest] > 0:
        remaining[rest] -= 1
        skipped += 1
    else:
        problems.append(f"XML citation {rest} has no matching cited block")

print(f"== {Path(md_path).name}: content ^{book}-1…^{book}-{len(content_n)}, headings {len(heads)}, "
      f"words md {len(md_words)} / xml {len(xml_words)}, bold spans {len(md_bold)}, citations xml {len(xml_cits)}: "
      f"linked right {ok}, wrong {bad}, unresolved (unlinked, logged) {skipped}")
print("   PASS" if not problems else "   PROBLEMS (%d):\n   - " % len(problems) + "\n   - ".join(problems[:20]))
sys.exit(1 if problems else 0)
