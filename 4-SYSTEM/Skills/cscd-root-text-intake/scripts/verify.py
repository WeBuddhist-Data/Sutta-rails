#!/usr/bin/env python3
"""verify.py — step 8 of cscd-root-text-intake: verify a converted root-text
file against the CSCD XML it came from. Prints PASS or a list of problems;
exit status 1 on any problem.

Checks
  1. IDs: content IDs unique and equal, in order, to the XML's printed paragraph
     numbers (a printed range "225-240" is the ID ^{b}-225-240); a gap the XML
     itself prints (CSCD SN Mahāvagga, abbreviated suttas) is listed, not an error;
     U-blocks listed; headings end -0; every non-blank block has exactly one ID
     on its last line; no line carries two IDs; content IDs <= 3 segments.
  2. Structure: '###' titles == every <head rend="chapter"> (number stripped);
     '####'-and-deeper heading count == <p rend="subhead"> count. In a volume
     whose suttas are numbered subheads in vagga divs (Majjhimanikāya,
     cscd_shape.py), '####' titles == those sutta headings (number stripped)
     and every other subhead is a '#####'.
  3. Text: word stream of the md (IDs, '#' markers and ** removed) == word
     stream of the XML (notes as [..], paranum removed, page breaks dropped),
     allowing only the documented heading-number strip (chapter and sutta
     headings).
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
import cscd_shape  # noqa: E402

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
        if re.match(r"^\d+(?:-\d+)?\.\s", b[0]):
            problems.append(f"N. prefix not stripped: {b[0][:60]}")

nums = []
for cid in content_ids:
    m = re.fullmatch(rf"{book}-(\d+(?:-\d+)?)", cid)
    if not m:
        problems.append(f"unexpected content id shape: {cid}")
        continue
    nums.append(m.group(1))


def span(printed):
    a, _, b = printed.partition("-")
    return int(a), int(b or a)
if len(set(heading_ids)) != len(heading_ids):
    problems.append("duplicate heading ids")
if len(set(nums)) != len(nums):
    problems.append("duplicate content ids")

# ---------- xml side ----------
root = ET.parse(xml_path).getroot()
xbody = root.find(".//body")
paranums = [p.get("n") for p in xbody.iter("p") if re.fullmatch(r"\d+(?:-\d+)?", p.get("n") or "")]
if nums != paranums:
    problems.append(f"content ids != XML paranums (md {len(nums)}, xml {len(paranums)})")
gaps = []   # printed-number jumps; allowed only because nums == the XML's own numbers
prev = 0
for x in nums:
    a, b = span(x)
    if a <= prev:
        problems.append(f"content ids out of order at {x}")
    elif a != prev + 1:
        gaps.append(f"{prev}->{x}")
    prev = b
if nums and span(nums[0])[0] != 1:
    problems.append("content ids do not start at 1")

book_div = next((d for d in xbody.iter("div") if d.get("type") == "book"), None)
vagga_shape = book_div is not None and any(d.get("type") == "vagga" for d in book_div.iter("div"))
sutta_ids = cscd_shape.sutta_heads(book_div) if vagga_shape else set()
chapter_heads = [h for h in xbody.iter("head") if h.get("rend") == "chapter"]
# A heading directly in the book <div> after a chapter <div> has closed opens a
# section of its own (SN "Sagāthāvaggo paṭhamo." + uddāna): it is a '###' too.
section_heads = []
if book_div is not None:
    after = False
    for c in book_div:
        if c.tag == "div":
            h = c.find("head")
            if h is not None and h.get("rend") == "chapter":
                section_heads.append(h)
            after = True
        elif after and c.tag == "p" and c.get("rend") in ("subhead", "title") and not cscd_shape.part_label(cscd_shape.text_of(c)):
            section_heads.append(c)
            after = False
promoted = {id(h) for h in section_heads if h.tag == "p"}
xml_sutta_titles = [re.sub(r"^\d+\.\s*", "", "".join(h.itertext()).strip()) for h in (section_heads or chapter_heads)]
md_sutta_titles = [ID_RE.sub("", l)[4:].strip() for l in lines if l.startswith("### ")]
if xml_sutta_titles != md_sutta_titles:
    problems.append("chapter (###) headings differ from XML")
# every subhead and title paragraph is a '####' or deeper heading (SN: vagga =
# title, sutta = subhead), except one promoted to a '###' section above
xml_sub = sum(1 for p in xbody.iter("p") if p.get("rend") in ("subhead", "title") and id(p) not in promoted
              and not cscd_shape.part_label(cscd_shape.text_of(p)))
md_sub = sum(1 for l in lines if re.match(r"^#{4,} ", l))
if xml_sub != md_sub:
    problems.append(f"subhead count md {md_sub} vs xml {xml_sub}")
if vagga_shape:
    xml_suttas = [re.sub(r"^\d+\.\s*", "", cscd_shape.text_with_notes(p)) for p in xbody.iter("p") if id(p) in sutta_ids]
    md_suttas = [ID_RE.sub("", l)[5:].strip() for l in lines if l.startswith("#### ")]
    if xml_suttas != md_suttas:
        problems.append(f"sutta (####) headings differ from XML (md {len(md_suttas)}, xml {len(xml_suttas)})")
    if any(l.startswith("###### ") for l in lines):
        problems.append("heading deeper than ##### in a vagga volume")


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

    els = [el for el in xbody.iter() if el.tag in ("p", "head", "trailer")]
    for k_el, el in enumerate(els):
        if True:
            start = len(out)
            nxt = els[k_el + 1] if k_el + 1 < len(els) else None
            if el.get("rend") == "hangnum" and nxt is not None and (
                    nxt.tag == "head" or nxt.get("rend") in ("subhead", "title", "subsubhead")):
                # number-only paragraph before a heading: the md keeps the number as its text
                out.append("".join(el.itertext()).strip().rstrip(".") + "\n")
                continue
            rend(el)
            if (el.tag == "head" and el.get("rend") == "chapter") or id(el) in sutta_ids \
                    or (el.tag == "p" and el.get("rend") in ("subhead", "title")):
                seg = "".join(out[start:])
                del out[start:]
                out.append(re.sub(r"^\s*\d+(?:-\d+)*\.\s*", "", seg))
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
print(f"   content ids {len(nums)} (^{book}-{nums[0]} .. ^{book}-{nums[-1]}; ranges {sum('-' in x for x in nums)}"
      f"{', gaps as printed in the XML ' + str(len(gaps)) + ': ' + ' '.join(gaps[:6]) if gaps else ''}), U-blocks {u_ids}, headings {len(heading_ids)}, chapters {len(md_sutta_titles)}, "
      f"{'suttas ' + str(len(sutta_ids)) + ', ' if vagga_shape else ''}subheads {md_sub}")
print(f"   words md {len(mw)} / xml {len(xw)}, bold spans {len(md_bold)}")
print("   PASS" if not problems else "   PROBLEMS:\n   - " + "\n   - ".join(problems))
sys.exit(1 if problems else 0)
