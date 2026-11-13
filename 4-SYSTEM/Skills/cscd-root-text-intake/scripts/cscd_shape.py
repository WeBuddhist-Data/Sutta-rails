"""cscd_shape.py — shared structure rules for CSCD volumes whose suttas are not
<div>s (cscd-root-text-intake and cscd-commentary-intake).

In the Dīghanikāya every sutta is a <div type="sutta">. In the Majjhimanikāya
the book holds <div type="vagga">s, and a sutta is only a numbered
<p rend="subhead"> inside its vagga ("1. Mūlapariyāyasuttaṃ",
"2. Sabbāsavasuttavaṇṇanā"). Unnumbered subheads in the same class are
sub-headings inside a sutta, and a ṭīkā can number sub-headings of its own
("1. Desanāhāravaṇṇanā" … under "Soḷasahāravaṇṇanā"). So a subhead is a sutta
heading only if
  - it sits in a vagga <div>,
  - it opens with "N. " and N is the next sutta number in that vagga (1, 2, …),
  - its title contains "sutta".
A numbered "…sutta…" subhead out of sequence stops the run (sutta_heads raises
ShapeError): the structure is then for a human to decide, never guessed.

Also shared:
  part_label(text)  "(Paṭhamo bhāgo)", "(Dutiyo bhāgo)" — the printed part of a
                    volume CSCD prints in two parts. Plain text, not a heading.
"""
import re

SUTTA_NUM = re.compile(r"^(\d+)\.\s")
PART_LABEL = re.compile(r"^\(\S+ bhāgo\)$")


class ShapeError(Exception):
    pass


def text_of(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def text_with_notes(el):
    """Element text with each <note> as " [..]", as the converters write it."""
    out = []

    def walk(e, top):
        if e.tag == "note":
            out.append(" [" + "".join(e.itertext()).strip() + "]")
        elif e.tag != "pb":
            out.append(e.text or "")
            for c in e:
                walk(c, False)
        if not top and e.tail:
            out.append(e.tail)
    walk(el, True)
    s = re.sub(r"\s+", " ", "".join(out)).strip()
    return re.sub(r"\s+\]", "]", re.sub(r"\[\s+", "[", s))


def part_label(text):
    return bool(PART_LABEL.match(text.replace("**", "").strip()))


def sutta_heads(book_div, vagga_type="vagga"):
    """Return the set of id()s of the <p rend="subhead"> elements that are sutta
    headings, for a book whose chapter-level divs are `vagga_type`.
    Raises ShapeError if a vagga with a <head> holds no sutta heading, or a
    numbered '…sutta…' subhead is out of sequence."""
    found = set()
    for v in book_div.iter("div"):
        if v.get("type") != vagga_type:
            continue
        expect = 1
        for p in v.iter("p"):
            if p.get("rend") != "subhead":
                continue
            t = text_of(p)
            m = SUTTA_NUM.match(t)
            if not m or "sutta" not in t.lower():
                continue
            if int(m.group(1)) != expect:
                raise ShapeError(f"vagga {v.get('id')}: sutta heading '{t[:60]}' — expected number {expect}")
            found.add(id(p))
            expect += 1
        head = v.find("head")
        if expect == 1 and head is not None and head.get("rend") == "chapter":
            # A real vagga (<head rend="chapter">) must hold suttas; a front-matter
            # div (no head, or a subsubhead head: Ganthārambhakathā) need not.
            raise ShapeError(f"vagga {v.get('id')} ('{text_of(head)[:40]}') has no numbered sutta heading")
    return found
