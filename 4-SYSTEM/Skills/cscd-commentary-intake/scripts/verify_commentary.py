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
Usage: python3 -I verify_commentary.py <file.md> <root.md> <xml> [<xml> …] [--unresolved <log.json>]
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
md_path, root_path, xmls = args[0], args[1], args[2:]
problems = []
HEADING_RENDS = {"chapter", "title", "subhead", "subsubhead"}
NUM_FIX = re.compile(r"^(\d+(?:-\d+)*)\.(?=\S)")
LEAD = re.compile(r"^\s*\d+(?:-\d+)*\.\s*")
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
for x in xmls:
    body = ET.parse(x).getroot().find(".//body")
    xml_bodies.append(body)
    for el in body.iter():
        if el.tag not in ("p", "head", "trailer"):
            continue
        buf = []
        render(el, buf)
        s = "".join(buf).replace("‘‘", '"').replace("’’", '"')
        s = re.sub(r"\s+", " ", s)
        s = re.sub(r"\s+\]", "]", re.sub(r"\[\s+", "[", s)).strip()
        s = NUM_FIX.sub(r"\1. ", s)
        rend = el.get("rend") or ""
        if el.tag == "head" or rend in HEADING_RENDS:
            s = LEAD.sub("", s)
        xml_words += s.split()
        if el.tag == "p" and el.get("n"):
            xml_cits.append(el.get("n"))

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
    md_words += bold_check.strip_bold(ln).split()
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
    if c:
        md_cits.append((b[0].split(".")[0], list(pending), b[0][:60]))
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


xml_linkable = [n for n in xml_cits]
ok = bad = skipped = 0
md_by_order = [c for c in md_cits]
# every XML citation must appear, in order, as a cited block
xi = 0
for printed, links, head in md_by_order:
    while xi < len(xml_linkable) and xml_linkable[xi] != printed:
        if remaining[xml_linkable[xi]] > 0:   # logged, and not a cited block in the md
            remaining[xml_linkable[xi]] -= 1; skipped += 1; xi += 1; continue
        problems.append(f"XML citation {xml_linkable[xi]} has no matching cited block (next md block cites {printed})")
        xi += 1
    if xi >= len(xml_linkable):
        problems.append(f"md block cites {printed} beyond the XML's citations"); break
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
    exp = covering(exp)
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
