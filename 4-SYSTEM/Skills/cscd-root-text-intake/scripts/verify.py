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
  With --tree (a volume converted with cscd_xml_to_json.py --tree), check 2 is:
     every heading of the XML, at its tree level (cscd_shape.tree_levels) and with
     the same text (number stripped), equals the md headings, in order.
Usage: python3 -I verify.py <book> <file.md> <file.xml> [--tree]
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bold_check  # noqa: E402
import cscd_shape  # noqa: E402

TREE = "--tree" in sys.argv
# --per-section: the book numbers each section (top-level division) from 1 (CSCD
# Khuddakapāṭha); content IDs are ^<book>-<section>-<N>, section = its position.
PER_SECTION = "--per-section" in sys.argv
# --zoned: the book has more than one numbering run, each a zone (apply.py --zones
# "1=1@…,2=2@…"); content IDs are ^<book>-<run>-<N>, run = the k-th time the XML's
# printed numbers start again at 1 (CSCD Suttanipāta: the verses 1-1155, then the
# Suttuddāna 1-21).
# --zone-labels L1,L2,…: run k's zone label is Lk instead of k (human decision; CSCD
# Paṭisambhidāmagga: M,1,2,3 = the Mātikā, then the three vaggas). Implies --zoned.
_args = sys.argv[1:]
ZONE_LABELS = None
if "--zone-labels" in _args:
    _k = _args.index("--zone-labels"); ZONE_LABELS = _args[_k + 1].split(","); del _args[_k:_k + 2]
ZONED = "--zoned" in _args or ZONE_LABELS is not None
book, md_path, xml_path = [a for a in _args if a not in ("--tree", "--per-section", "--zoned")][:3]
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

_raw = open(xml_path, "rb").read()
_xml_text = _raw.decode("utf-16") if _raw[:2] in (b"\xff\xfe", b"\xfe\xff") else _raw.decode("utf-8")
_xml_plain = {re.sub(r"<[^>]+>", "", m).strip() for m in re.findall(r"<p rend=\"[^\"]+\"[^>]*>(.*?)</p>", _xml_text, re.S)
              if "paranum" not in m}


def xml_unnumbered(line):
    """The XML has a <p> with exactly this text and no paranum."""
    return line in _xml_plain


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
        if re.match(r"^\d+(?:-\d+)?\.\s", b[0]) and not (
                bid in u_ids and xml_unnumbered(ID_RE.sub("", b[0]).strip())):
            # (a U block may open "N. " where the XML prints it as text with no paranum:
            # the Vimānavatthu's numbered sub-stories inside the Guttilavimāna)
            problems.append(f"N. prefix not stripped: {b[0][:60]}")

nums = []
PLAIN_ZONE = bool(ZONE_LABELS) and "" in ZONE_LABELS   # one run keeps plain ^<book>-N (Nettippakaraṇa)
for cid in content_ids:
    # `x<k>` marks the k-th repeat of a number the XML prints more than once (Rule 2): it
    # counts as that printed number (CSCD Theragāthā prints 1204 twice)
    if ZONED:
        # zoned: "<label>|<N>"; with a plain zone, ^<book>-N is label "" (no printed ranges then)
        m = re.fullmatch(rf"{book}-(?:([A-Za-z0-9]+)-)?(\d+(?:-\d+)?)(?:x\d+)?" if PLAIN_ZONE else
                         rf"{book}-([A-Za-z0-9]+)-(\d+(?:-\d+)?)(?:x\d+)?", cid)
        if not m:
            problems.append(f"unexpected content id shape: {cid}")
            continue
        nums.append(f"{m.group(1) or ''}|{m.group(2)}")
        continue
    m = re.fullmatch(
                     rf"{book}-(\d+-\d+(?:-\d+)?)(?:x\d+)?" if PER_SECTION else rf"{book}-(\d+(?:-\d+)?)(?:x\d+)?", cid)
    if not m:
        problems.append(f"unexpected content id shape: {cid}")
        continue
    nums.append(m.group(1))


def span(printed):
    a, _, b = printed.partition("-")
    return int(a), int(b or a)
if len(set(heading_ids)) != len(heading_ids):
    problems.append("duplicate heading ids")
if len(set(content_ids)) != len(content_ids):
    problems.append("duplicate content ids")

# ---------- xml side ----------
root = ET.parse(xml_path).getroot()
xbody = root.find(".//body")
# a paragraph with a printed number (<hi rend="paranum">); an @n alone is not printed
# (CSCD AN: the homage has n="0")
def printed(p):
    return re.fullmatch(r"\d+(?:-\d+)?", p.get("n") or "") and any(h.get("rend") == "paranum" for h in p.iter("hi"))
paranums = [p.get("n") for p in xbody.iter("p") if printed(p)]
if PER_SECTION:
    _book = next(d for d in xbody.iter("div") if d.get("type") == "book")
    _secs = [d for d in _book if d.tag == "div"]
    paranums = [f"{k}-{p.get('n')}" for k, d in enumerate(_secs, 1) for p in d.iter("p") if printed(p)]
elif ZONED:
    # the number as printed (<hi rend="paranum">), not @n: the Suttanipāta's Suttuddāna
    # prints "1." on n="1156" and 2–21 with no @n at all
    _printed = []   # (number, a heading came between it and the previous number)
    _head_since = False
    for p in xbody.iter():
        if p.tag == "head" or (p.tag == "p" and p.get("rend") in ("subhead", "subsubhead", "title", "chapter", "book")):
            _head_since = True
            continue
        if p.tag != "p":
            continue
        _h = next((h for h in p.iter("hi") if h.get("rend") == "paranum"), None)
        if _h is not None and re.fullmatch(r"\d+(?:-\d+)?", "".join(_h.itertext()).strip()):
            _printed.append(("".join(_h.itertext()).strip(), _head_since))
            _head_since = False
    # runs: a new one at each restart at 1, an inner run may end by resuming the outer (zones.py)
    import zones  # noqa: E402
    _runs = zones.assign(_printed)
    if ZONE_LABELS and max(_runs, default=0) != len(ZONE_LABELS):
        problems.append(f"{max(_runs, default=0)} numbering runs in the XML but {len(ZONE_LABELS)} zone labels")
    paranums = [f"{(ZONE_LABELS[z - 1] if ZONE_LABELS and z <= len(ZONE_LABELS) else z)}|{n}"
                for z, (n, _hs) in zip(_runs, _printed)]
if nums != paranums:
    problems.append(f"content ids != XML paranums (md {len(nums)}, xml {len(paranums)})")
gaps = []   # printed-number jumps; allowed only because nums == the XML's own numbers
prev, prev_sec, last_of = 0, None, {}
for x in nums:
    if PER_SECTION or ZONED:
        sec, x = x.split("|" if ZONED else "-", 1)
        if sec != prev_sec:
            last_of[prev_sec] = prev
            prev, prev_sec = last_of.get(sec, 0), sec   # a resumed zone continues where it stopped
    a, b = span(x)
    if a == prev == b:
        repeats = locals().get("repeats", []) + [x]   # a number the XML prints twice (x-suffixed ID)
    elif a <= prev:
        problems.append(f"content ids out of order at {x}")
    elif a != prev + 1:
        gaps.append(f"{prev}->{x}")
    prev = b
if nums and span(nums[0].split("|" if ZONED else "-", 1)[1] if PER_SECTION or ZONED else nums[0])[0] != 1:
    problems.append("content ids do not start at 1")

book_div = next((d for d in xbody.iter("div") if d.get("type") == "book"), None)
vagga_shape = not TREE and book_div is not None and any(d.get("type") == "vagga" for d in book_div.iter("div"))
tree_lv = cscd_shape.tree_levels(book_div) if TREE else {}
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
xml_sutta_titles = [cscd_shape.printed_heading("".join(h.itertext())) for h in (section_heads or chapter_heads)]
md_sutta_titles = [ID_RE.sub("", l)[4:].strip() for l in lines if l.startswith("### ")]
if TREE:
    xml_tree = [(tree_lv[id(e)], cscd_shape.printed_heading(cscd_shape.text_with_notes(e)))
                for e in book_div.iter() if id(e) in tree_lv]
    md_tree = [(len(m.group(1)), m.group(2).strip()) for m in
               (re.match(r"^(#{2,}) (.*?)(?:\s+\^[\w-]+)?\s*$", l) for l in lines) if m]
    if xml_tree != md_tree:
        import difflib
        ops = [o for o in difflib.SequenceMatcher(None, xml_tree, md_tree, autojunk=False).get_opcodes() if o[0] != "equal"]
        problems.append(f"headings (level, title) differ from the XML tree in {len(ops)} place(s) (md {len(md_tree)}, xml {len(xml_tree)})")
        for op, a0, a1, b0, b1 in ops[:5]:
            problems.append(f"   {op}: xml {xml_tree[a0:a1][:2]} | md {md_tree[b0:b1][:2]}")
elif xml_sutta_titles != md_sutta_titles:
    problems.append("chapter (###) headings differ from XML")
# every subhead and title paragraph is a '####' or deeper heading (SN: vagga =
# title, sutta = subhead), except one promoted to a '###' section above
xml_sub = sum(1 for p in xbody.iter("p") if p.get("rend") in ("subhead", "title") and id(p) not in promoted
              and not cscd_shape.part_label(cscd_shape.text_of(p)))
md_sub = sum(1 for l in lines if re.match(r"^#{4,} ", l))
if xml_sub != md_sub and not TREE:
    problems.append(f"subhead count md {md_sub} vs xml {xml_sub}")
if vagga_shape:
    xml_suttas = [cscd_shape.printed_heading(cscd_shape.text_with_notes(p)) for p in xbody.iter("p") if id(p) in sutta_ids]
    md_suttas = [ID_RE.sub("", l)[5:].strip() for l in lines if l.startswith("#### ")]
    if xml_suttas != md_suttas:
        problems.append(f"sutta (####) headings differ from XML (md {len(md_suttas)}, xml {len(xml_suttas)})")
    if any(l.startswith("###### ") for l in lines):
        problems.append("heading deeper than ##### in a vagga volume")


def xml_words():
    out = []
    in_head = [False]

    def rend(el, top=True):
        if el.tag == "pb":
            pass
        elif el.tag == "note":
            out.append(" [" + "".join(el.itertext()).strip() + "]")
        elif el.tag == "hi" and el.get("rend") == "dot" and in_head[0]:
            out.append(el.text or "")   # "152<hi rend="dot">.</hi> …" in a heading: the number's dot, stripped below
        elif el.tag == "hi" and el.get("rend") in ("paranum", "dot") and not in_head[0]:
            pass
        else:
            if el.text: out.append(el.text)
            for c in el: rend(c, False)
        tail = el.tail
        if tail and el.tag == "hi" and el.get("rend") == "paranum" and tail.startswith(".") and not in_head[0]:
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
            is_head = (el.tag == "head" and el.get("rend") == "chapter") or id(el) in sutta_ids \
                or (el.tag == "p" and el.get("rend") in ("subhead", "title")) or id(el) in tree_lv
            in_head[0] = is_head
            rend(el)
            in_head[0] = False
            if is_head:
                seg = "".join(out[start:])
                del out[start:]
                out.append(cscd_shape.printed_heading(seg))   # a heading keeps its printed number
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
_show = lambda x: x.lstrip("|").replace("|", "-")   # zoned "label|N" -> "label-N" / "N"
print(f"   content ids {len(nums)} (^{book}-{_show(nums[0])} .. ^{book}-{_show(nums[-1])}; ranges {sum('-' in (x.split('|' if ZONED else '-', 1)[1] if PER_SECTION or ZONED else x) for x in nums)}"
      f"{', gaps as printed in the XML ' + str(len(gaps)) + ': ' + ' '.join(gaps[:6]) if gaps else ''}), U-blocks {u_ids}, headings {len(heading_ids)}, chapters {len(md_sutta_titles)}, "
      f"{'suttas ' + str(len(sutta_ids)) + ', ' if vagga_shape else ''}subheads {md_sub}")
print(f"   words md {len(mw)} / xml {len(xw)}, bold spans {len(md_bold)}")
print("   PASS" if not problems else "   PROBLEMS:\n   - " + "\n   - ".join(problems))
sys.exit(1 if problems else 0)
