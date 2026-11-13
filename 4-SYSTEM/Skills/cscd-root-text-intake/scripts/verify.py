#!/usr/bin/env python3
"""verify.py — step 8 of cscd-root-text-intake: verify a converted root-text
file against the CSCD XML it came from. Prints PASS or a list of problems;
exit status 1 on any problem.

Checks
  1. IDs: content IDs ^{b}-1..^{b}-N contiguous, unique, match the XML paranums;
     U-blocks listed; headings end -0; every non-blank block has exactly one ID
     on its last line; no line carries two IDs; content IDs <= 3 segments.
  2. Structure: '###' titles == every <head rend="chapter"> (number stripped);
     '####' count == <p rend="subhead"> count.
  3. Text: word stream of the md (IDs, '#' markers and ** removed) == word
     stream of the XML (notes as [..], paranum removed, page breaks dropped),
     allowing only the documented heading-number strip.
  4. Bold: every <hi rend="bold"> is a **…** span at the same place, in order,
     with exactly the same text; every ** pairs up (bold_check.py).
Usage: python3 -I verify.py <book> <file.md> <file.xml>
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bold_check  # noqa: E402

book, md_path, xml_path = sys.argv[1:4]
problems = []

# ---------- md side ----------
text = open(md_path, encoding="utf-8").read()
body = text.split("\n---\n", 1)[1]
lines = body.split("\n")
ID_RE = re.compile(r"\s\^([\w-]+)\s*$")

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

content_ids, heading_ids, u_ids = [], [], []
for b in blocks:
    for ln in b[:-1]:
        if ID_RE.search(ln):
            problems.append(f"ID on non-last line: {ln[:80]}")
    last = b[-1]
    if last.count(" ^") > 1:
        problems.append(f"two IDs on a line: {last[:80]}")
    m = ID_RE.search(last)
    if not m:
        problems.append(f"block without ID: {b[0][:80]}")
        continue
    bid = m.group(1)
    if b[0].startswith("#"):
        heading_ids.append(bid)
        if bid != "0" and not bid.endswith("-0"):
            problems.append(f"heading id not -0: {bid}")
    elif bid.startswith("T-"):
        pass
    else:
        if bid.endswith("-0"):
            problems.append(f"content id ends -0: {bid}")
        if len(bid.split("-")) > 3:
            problems.append(f"content id > 3 segments: {bid}")
        if re.fullmatch(rf"{book}-U\d+", bid):
            u_ids.append(bid)
        else:
            content_ids.append(bid)
        if re.match(r"^\d+\.\s", b[0]):
            problems.append(f"N. prefix not stripped: {b[0][:60]}")

nums = []
for cid in content_ids:
    m = re.fullmatch(rf"{book}-(\d+)", cid)
    if not m:
        problems.append(f"unexpected content id shape: {cid}")
        continue
    nums.append(int(m.group(1)))
if len(set(heading_ids)) != len(heading_ids):
    problems.append("duplicate heading ids")
if len(set(nums)) != len(nums):
    problems.append("duplicate content ids")

# ---------- xml side ----------
root = ET.parse(xml_path).getroot()
xbody = root.find(".//body")
paranums = [int(p.get("n")) for p in xbody.iter("p") if (p.get("n") or "").isdigit()]
if nums != paranums:
    problems.append(f"content ids != XML paranums (md {len(nums)}, xml {len(paranums)})")
if nums != list(range(1, max(nums) + 1)):
    problems.append("content ids not contiguous 1..N")

chapter_heads = [h for h in xbody.iter("head") if h.get("rend") == "chapter"]
xml_sutta_titles = [re.sub(r"^\d+\.\s*", "", "".join(h.itertext()).strip()) for h in chapter_heads]
md_sutta_titles = [ID_RE.sub("", l)[4:].strip() for l in lines if l.startswith("### ")]
if xml_sutta_titles != md_sutta_titles:
    problems.append("chapter (###) headings differ from XML")
xml_sub = sum(1 for p in xbody.iter("p") if p.get("rend") == "subhead")
md_sub = sum(1 for l in lines if l.startswith("#### "))
if xml_sub != md_sub:
    problems.append(f"subhead count md {md_sub} vs xml {xml_sub}")


def xml_words():
    out = []

    def rend(el, top=True):
        if el.tag == "pb":
            pass
        elif el.tag == "note":
            out.append(" [" + "".join(el.itertext()).strip() + "]")
        elif el.tag == "hi" and el.get("rend") in ("paranum", "dot"):
            pass
        else:
            if el.text: out.append(el.text)
            for c in el: rend(c, False)
        tail = el.tail
        if tail and el.tag == "hi" and el.get("rend") == "paranum" and tail.startswith("."):
            tail = tail[1:]   # untagged dot after the number belongs to the number
        if not top and tail: out.append(tail)

    for el in xbody.iter():
        if el.tag in ("p", "head", "trailer"):
            start = len(out)
            rend(el)
            if el.tag == "head" and el.get("rend") == "chapter":
                seg = "".join(out[start:])
                del out[start:]
                out.append(re.sub(r"^\s*\d+\.\s*", "", seg))
            out.append("\n")
    joined = "".join(out).replace("‘‘", '"').replace("’’", '"')  # same as step 1
    return re.sub(r"\[\s+", "[", re.sub(r"\s+\]", "]", joined)).split()


def md_words():
    out = []
    for ln in lines:
        ln = ID_RE.sub("", ln)
        ln = re.sub(r"^#+\s+", "", ln)
        out.append(bold_check.strip_bold(ln))
    return " ".join(out).split()


xw, mw = xml_words(), md_words()
if xw != mw:
    import difflib
    sm = difflib.SequenceMatcher(a=xw, b=mw, autojunk=False)
    diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]
    problems.append(f"text differs from XML in {len(diffs)} place(s)")
    for tag, a0, a1, b0, b1 in diffs[:10]:
        problems.append(f"   {tag}: xml {' '.join(xw[a0:a1])[:80]!r} | md {' '.join(mw[b0:b1])[:80]!r}")

md_bold, unpaired = bold_check.md_spans(lines, exact=True)
for u in unpaired[:5]:
    problems.append(f"unpaired ** on line: {u!r}")
problems += bold_check.compare(bold_check.xml_spans([xbody], exact=True), md_bold, "xml")

print(f"== {md_path}")
print(f"   content ids {len(nums)} (^{book}-{min(nums)} .. ^{book}-{max(nums)}), U-blocks {u_ids}, headings {len(heading_ids)}, chapters {len(md_sutta_titles)}, subheads {md_sub}")
print(f"   words md {len(mw)} / xml {len(xw)}, bold spans {len(md_bold)}")
print("   PASS" if not problems else "   PROBLEMS:\n   - " + "\n   - ".join(problems))
sys.exit(1 if problems else 0)
