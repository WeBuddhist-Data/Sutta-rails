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


# ---------------------------------------------------------------------------
# Tree mode (CSCD Aṅguttaranikāya and other nested shapes)
# ---------------------------------------------------------------------------
# Heading level = markdown '#' count, read from the XML's own nesting:
#   <head rend="book">                     -> 2   (##)
#   the <head> of a <div> at depth d        -> 2 + d   (a div directly in the book: ###)
#   a heading paragraph (title > chapter > subhead > subsubhead, by rank) sits one
#   level under the innermost open heading of a higher rank in the same <div>,
#   or under the <div>'s own head: paṇṇāsaka (title) > vagga (chapter) > sutta
#   (subhead) in a ṭīkā that has no <div>s inside its book.
# A part label "(Dutiyo bhāgo)" is text, not a heading.

P_HEAD_RANK = {"title": 1, "chapter": 2, "subhead": 3, "subsubhead": 4}
LEAD_NUM = re.compile(r"^\s*(?:\(\d+\)\s*)?\d+(?:-\d+)*\.\s*")   # "1. ", "1-10. ", "(6) 1. "


def strip_heading_number(text):
    """For matching a heading by name only: the written heading keeps its number."""
    return LEAD_NUM.sub("", text).strip()


def printed_heading(text):
    """A heading as printed, its number kept ("1. Rūpādivaggo", "(1) 1. Puggalavaggo",
    "1.Sattisuttavaṇṇanā"): the form the converters write and the checks compare. A
    heading's number cannot be read back from its block ID (^1-1-0 is a structural
    path), so it stays in the text, as in the Vinaya files. A space between the number
    and its dot is markup (two tags), not text."""
    s = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"^(\d+(?:-\d+)*)\s+\.", r"\1.", s)


def tree_levels(book_div):
    """{id(element): level} for every heading element in the book <div>, in tree mode.
    A file with no book <div> at all (CSCD KN aṭṭhakathās) passes its <body>: its
    <p rend="book"> is then the book's heading (##), and the rest nests under it."""
    levels = {}
    divless_book = book_div.tag == "body"
    rank = P_HEAD_RANK
    if divless_book:
        # With no <div>s, the file's own order says which of title/chapter is outer: the KN
        # aṭṭhakathās use both ways round (Itivuttaka-aṭṭhakathā: chapter = nipāta, title = vagga
        # inside it; Apadāna-aṭṭhakathā: title outer). The first real one (part labels such as
        # "(Paṭhamo bhāgo)" are not headings) is the outer level.
        first = next((c.get("rend") for c in book_div.iter("p")
                      if c.get("rend") in ("title", "chapter") and not part_label(text_of(c))), None)
        if first == "chapter":
            rank = {"chapter": 1, "title": 2, "subhead": 3, "subsubhead": 4}

    seen_heads = set()                      # heading texts so far (number stripped)
    reprint = [False]                       # inside a later part's reprinted opening

    def walk(container, level):
        # level = the '#' count of this container's own heading (book: 2).
        has_head = container.find("head") is not None or (divless_book and container is book_div)
        open_ranks = []                     # ranks of heading paragraphs open in this container
        own_head_seen = False
        book_lines = 0
        for c in container:
            if c.tag == "div":
                walk(c, level + 1)
                continue
            if c.tag == "p" and c.get("rend") == "book":
                book_lines += 1
                reprint[0] = book_lines > 1          # a later part reprints the book title
                continue
            txt = LEAD_NUM.sub("", text_of(c)).strip()
            if reprint[0] and c.tag == "p" and c.get("rend") in P_HEAD_RANK:
                if part_label(text_of(c)):
                    continue
                if txt in seen_heads:
                    # the part's opening repeats the heading still open (CSCD Suttanipāta-
                    # aṭṭhakathā, Dutiyo bhāgo: "2. Cūḷavaggo" again): text, not a new heading
                    continue
            if c.tag == "p" and c.get("rend") not in ("centre", "nikaya", "book") and not part_label(text_of(c)):
                reprint[0] = False
            if c.tag in ("p", "head") and (c.get("rend") in P_HEAD_RANK or c.tag == "head"):
                seen_heads.add(txt)
            if c.tag == "head" and not own_head_seen:
                levels[id(c)] = level        # the container's own heading
                own_head_seen = True
                open_ranks = []
                continue
            # a heading paragraph, or a further <head> in the same container (CSCD
            # s0404a: <head rend="chapter"> vaggas straight inside the book) ranks
            # by its rend: title > chapter > subhead > subsubhead
            r = rank.get(c.get("rend")) if c.tag in ("p", "head") else None
            if r is None or part_label(text_of(c)):
                continue
            open_ranks = [x for x in open_ranks if x < r]
            # under the container's head; a <div> without a head lends its own slot
            levels[id(c)] = (level + 1 if has_head else level) + len(open_ranks)
            open_ranks.append(r)
    walk(book_div, 2)
    return levels
