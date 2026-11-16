#!/usr/bin/env python3
"""
cscd_xml_to_json.py — step 3 of cscd-root-text-intake.

Turn one VRI CSCD (Chaṭṭha Saṅgāyana) romanised TEI XML volume into the
tipitaka.org-style segment JSON that json-to-source-text's
converters/tipitaka_org_book.py reads.

Schema written:
    id, title_pali, collection, pitaka, layer, layer_type, source_filename,
    source_url, total_segments, segments[] {id, chapter, paragraph, content, css_class}

Mapping:
    <p rend="X">            -> css_class X   ("centre" -> "centered")
    <head rend="book">      -> css_class "book"
    <head rend="chapter">   -> css_class "chapter"   (one per chapter-level <div>)
    <trailer rend="centre"> -> css_class "centered"
    <hi rend="paranum">N</hi><hi rend="dot">.</hi>  -> leading "N."  (the dot may
                               also be plain text right after the paranum)
    <note>x</note>          -> " [x]"    (variant readings kept inline)
    ‘‘ / ’’                 -> "         (as in the tipitaka.org exports)
    <pb .../>               -> dropped   (page markers)
    <hi rend="bold">x</hi>  -> **x**     exactly where the XML's tags are, as on
                               tipitaka.app (spaces and punctuation inside the tag
                               stay inside: **‘jātaka’**nti, **passatā. ** Sabba).
                               Nothing is moved, merged or dropped, so deleting
                               every ** gives back the text unchanged. In the
                               commentaries it marks the word being explained.
    other <hi>              -> plain text
chapter = 1-based index of the enclosing chapter-level <div> (0 before the first).

Supported shapes:
  - <div type="book"> containing chapter-level <div>s of ONE type (e.g. "sutta"),
    each opening with a <head> (Dīghanikāya);
  - <div type="book"> containing <div type="vagga">s whose suttas are numbered
    <p rend="subhead">s (Majjhimanikāya). Those sutta headings get css_class
    "sutta" (one level above the other subheads); the rule is cscd_shape.py's,
    and a vagga whose suttas cannot be found that way stops the script;
  - a volume with no <div>s at all, where each <p rend="chapter"> opens the next
    chapter.
Any other nesting (saṃyutta > vagga, nested divs of one type …) stops the script
(non-zero exit, "STOP: …" message, nothing written): a deeper volume needs this
script extended first, never silently flattened.

Line-level rules (each one printed in the run summary, for the report):
  - <p rend="hangnum">N.</p> holds only a paragraph number; its text is the next
    paragraph (a gāthā). The two are joined into one segment "N. <text>", as
    tipitaka.app shows them, so the paragraph keeps its number. A hangnum not
    followed by a text paragraph of the same chapter stops the script, except:
    a hangnum directly before a heading (CSCD SN Mahāvagga "312-323", a vagga of
    abbreviated suttas that prints only their numbers and a heading) has no text
    of its own; it stays where it is, as a block holding just the number.
  - "(Paṭhamo bhāgo)", "(Dutiyo bhāgo)": the part of a volume printed in two parts.
    Kept as plain text (css "centered"), never a heading. The nikāya and book
    lines a later part reprints in the same file are kept as plain text too.
  - Plain text before the first chapter with no heading of its own (e.g. the
    "(Paṭhamo bhāgo)" line) is put in the first chapter, so it is not a section
    of its own.

Options (Aṅguttaranikāya and other nested shapes):
  --book K   take only the K-th <div type="book"> of the file. A CSCD commentary
             volume can hold several nipātas as separate books (s0402a.att =
             Duka-, Tika-, Catukkanipāta), and tipitaka.app shows each as its own
             book; one vault file per book. A file with several books and no
             --book stops the run.
  --tree     tree mode: every heading segment gets css_class "heading" and a
             "level" ('#' count) read from the XML's nesting (cscd_shape.tree_levels):
             a <div>'s head is one level under its parent's; a heading paragraph
             (title > chapter > subhead > subsubhead) sits under the innermost
             open heading of a higher rank. Used where divisions nest in more
             than one way (nipāta > paṇṇāsaka > vagga > sutta; vaggas outside a
             paṇṇāsaka; peyyāla sections), or a book has no inner <div>s but
             heading paragraphs of several ranks (AN ṭīkā). The md converters are
             tree_to_md.py (root) and commentary_converter.py's tree branch.

Usage: python3 -I cscd_xml_to_json.py <in.xml> <out.json> [--book K] [--tree]
"""
import collections
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cscd_shape  # noqa: E402

HEADING_CSS = ("chapter", "subhead", "subsubhead", "title", "sutta", "heading")

LAYER = {"mul": ("mula", "mul"), "att": ("atthakatha", "att"),
         "tik": ("tika", "tik"), "nrf": ("other", "nrf")}
PITAKA = {"s": "sutta", "v": "vinaya", "e": "anna"}
RAW_BASE = "https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn/"


def render(el, out, top=True):
    if el.tag == "pb":
        pass
    elif el.tag == "note":
        out.append(" [" + "".join(el.itertext()).strip() + "]")
    elif el.tag == "hi" and el.get("rend") == "paranum":
        # Number only. The dot is either a <hi rend="dot"> (below) or, in a few
        # CSCD paragraphs (e.g. DN Mahāvagga 389), plain text in the tail.
        out.append("".join(el.itertext()).strip())
    elif el.tag == "hi" and el.get("rend") == "dot":
        out.append(".")
    elif el.tag == "hi" and el.get("rend") == "bold":
        out.append(B_OPEN)
        if el.text:
            out.append(el.text)
        for child in el:
            render(child, out, top=False)
        out.append(B_CLOSE)
    else:
        if el.text:
            out.append(el.text)
        for child in el:
            render(child, out, top=False)
    if not top and el.tail:
        out.append(el.tail)


B_OPEN, B_CLOSE = "\ue000", "\ue001"   # bold tag positions; clean() writes them as **


BOLD_STATS = collections.Counter()


def clean(s):
    # CSCD writes double quotes as doubled single quotes; the tipitaka.org
    # exports, and this vault's root texts, use a straight '"'.
    # Single quotes ‘ ’ stay as printed.
    s = s.replace("‘‘", '"').replace("’’", '"')
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\[\s+", "[", s)
    s = re.sub(r"\s+\]", "]", s)
    s = s.strip()
    BOLD_STATS["spans"] += s.count(B_OPEN)
    s = s.replace(B_OPEN, "**").replace(B_CLOSE, "**")
    # The converter recognises a numbered paragraph only as "N. text". CSCD
    # sometimes prints no space after the dot (DN Mahāvagga 335–342, 354, 370:
    # '370."Apariyositasaṅkappo'); the prefix is stripped later, so this adds
    # nothing to the text.
    # The number and its dot are two tags; a space CSCD leaves between them
    # (KN s0502a: <hi rend="paranum">8</hi> <hi rend="dot">.</hi>) is markup, not text.
    s = re.sub(r"^(\d+(?:-\d+)*)\s+\.", r"\1.", s)
    return re.sub(r"^(\d+(?:-\d+)*)\.(?=\S)", r"\1. ", s)


def check_shape(body):
    """Stop (non-zero exit) unless the volume is book > one chapter-level div
    type. Returns that div type, or None for a volume with no <div>s at all
    whose chapters are marked by <p rend="chapter"> (some CSCD ṭīkā volumes)."""
    if not any(True for _ in body.iter("div")):
        if not any(p.get("rend") == "chapter" for p in body.iter("p")):
            sys.exit("STOP: no <div>s and no <p rend='chapter'> — unsupported shape.")
        return None
    books = [d for d in body.iter("div") if d.get("type") == "book"]
    if len(books) != 1:
        sys.exit(f"STOP: expected exactly one <div type='book'>, found {len(books)}")
    inner = collections.Counter()
    for d in books[0].iter("div"):
        if d is books[0]:
            continue
        inner[d.get("type")] += 1
    if len(inner) != 1:
        sys.exit(f"STOP: unsupported div nesting {dict(inner)} — extend this script "
                 "before converting this volume (see SKILL.md, Rules).")
    chapter_type = next(iter(inner))
    for d in books[0].iter("div"):
        if d.get("type") == chapter_type and any(
                c.get("type") == chapter_type for c in d.iter("div") if c is not d):
            sys.exit(f"STOP: nested <div type='{chapter_type}'> — unsupported.")
    return chapter_type


def main(src, dst, book=None, tree=False):
    src = Path(src)
    root = ET.parse(src).getroot()
    body = root.find(".//body")
    levels = {}
    if book is not None or tree:
        books = [d for d in body.iter("div") if d.get("type") == "book"]
        if tree and book is None and not books and not any(True for _ in body.iter("div")):
            # a volume with no <div>s at all (CSCD KN aṭṭhakathās): the body is the book
            books = None
        if books is None:
            levels = cscd_shape.tree_levels(body)
        elif book is None and len(books) != 1:
            sys.exit(f"STOP: {len(books)} books in this file — give --book K (1..{len(books)})")
        if book is not None and not 1 <= book <= len(books):
            sys.exit(f"STOP: --book {book}: the file has {len(books)} book(s)")
    if (book is not None or tree) and books is not None:
        book_div = books[(book or 1) - 1]
        # Lines outside the book <div>s: before the first book they belong to the
        # first (homage, nikāya); after the last, to the last (s0402t's closing
        # "Dutiyo bhāgo niṭṭhito.", which tipitaka.app puts in tika-an-4). A line
        # between two books stops the run.
        kids = list(body)
        pos = [k for k, c in enumerate(kids) if c in books]
        between = [c for k, c in enumerate(kids) if c not in books and pos[0] < k < pos[-1]]
        if between:
            sys.exit("STOP: text between two book <div>s — which book does it belong to?")
        new_body = ET.Element("body")
        for k, c in enumerate(kids):
            if c is book_div or (c not in books and ((k < pos[0] and book_div is books[0])
                                                    or (k > pos[-1] and book_div is books[-1]))):
                new_body.append(c)
        body = new_body
        if tree:
            levels = cscd_shape.tree_levels(book_div)
    chapter_type = None if tree else check_shape(body)
    suttas = set()
    if chapter_type == "vagga":
        book_div = next(d for d in body.iter("div") if d.get("type") == "book")
        try:
            suttas = cscd_shape.sutta_heads(book_div)
        except cscd_shape.ShapeError as e:
            sys.exit(f"STOP: {e} — the sutta level cannot be read; decide it with a human.")
    notes = {"hangnum joined": [], "hangnum kept as a number-only block": [], "part labels as text": [], "reprinted title lines as text": [],
             "moved into the first chapter": []}
    stem = src.name.split(".")[0]
    kind = src.name.split(".")[1]
    layer, layer_type = LAYER.get(kind, (kind, kind))
    segs = []
    chap = 0
    title = None

    after_chapter = False   # True once a chapter <div> has closed

    def walk(el):
        nonlocal chap, title, after_chapter
        for child in el:
            if child.tag == "div":
                if child.get("type") == chapter_type:
                    chap += 1
                    after_chapter = False
                    walk(child)
                    after_chapter = True
                else:
                    walk(child)
                continue
            if child.tag not in ("p", "head", "trailer"):
                continue
            rend = child.get("rend") or ""
            if child.tag == "head":
                css = "book" if rend == "book" else "chapter"
            elif child.tag == "trailer":
                css = "centered"
            else:
                css = "centered" if rend == "centre" else rend
            if id(child) in suttas:
                css = "sutta"
            if tree:
                if id(child) in levels and not (child.tag == "head" and rend == "book"):
                    css = "heading"
                elif css == "chapter":       # a p rend="chapter" that is not a heading here
                    css = "bodytext"
            if chapter_type is None and css == "chapter" and not tree:
                chap += 1        # div-less volume: a chapter paragraph opens a chapter
            if css in ("subhead", "subsubhead", "title") and cscd_shape.part_label(cscd_shape.text_of(child)):
                notes["part labels as text"].append(cscd_shape.text_of(child))
                css = "centered"
            if css in ("nikaya", "book") and child.tag == "p" and title is not None:
                notes["reprinted title lines as text"].append(cscd_shape.text_of(child))
                css = "centered"
            if after_chapter and css in ("subhead", "subsubhead", "title"):
                # A heading after the last chapter <div> has closed (e.g. a
                # commentary's Nigamanakathā) opens a section of its own;
                # closing lines with no heading stay with the chapter before.
                chap += 1
                after_chapter = False
            buf = []
            render(child, buf)
            content = clean("".join(buf))
            if not content:
                continue
            if css == "book" and title is None:
                title = content
            seg = {
                "id": f"{stem}_ch{chap}_k{len(segs) + 1}",
                "chapter": chap,
                "paragraph": child.get("n") or "",
                "content": content,
                "css_class": css,
            }
            if css == "heading":
                seg["level"] = levels[id(child)]
            segs.append(seg)

    walk(body)

    # hangnum: a number-only paragraph opens the paragraph after it.
    joined = []
    k = 0
    while k < len(segs):
        g = segs[k]
        if g["css_class"] == "hangnum":
            nxt = segs[k + 1] if k + 1 < len(segs) else None
            if re.fullmatch(r"\d+(?:-\d+)?", g["content"]) and nxt is not None \
                    and nxt["chapter"] == g["chapter"] and nxt["css_class"] in HEADING_CSS:
                notes["hangnum kept as a number-only block"].append(g["content"])
                joined.append(dict(g, css_class="bodytext"))
                k += 1
                continue
            if not re.fullmatch(r"\d+(?:-\d+)?\.", g["content"]) or nxt is None \
                    or nxt["chapter"] != g["chapter"] or nxt["css_class"] in HEADING_CSS:
                sys.exit(f"STOP: hangnum {g['content']!r} is not followed by a text paragraph of its chapter")
            notes["hangnum joined"].append(g["content"])
            joined.append(dict(nxt, content=g["content"] + " " + nxt["content"],
                               paragraph=g["paragraph"] or nxt["paragraph"]))
            k += 2
            continue
        joined.append(g)
        k += 1
    segs[:] = joined

    # Plain text before the first chapter, with no heading of its own, belongs
    # to the first chapter (else the downstream converters open a section for it).
    # Only for <div> volumes: in a div-less later part (DN s0105t) these lines are
    # a second volume's opening, which merge_parts.py keeps with the chapter before.
    book_at = next((k for k, g in enumerate(segs) if g["css_class"] == "book"), None)
    if book_at is not None and chapter_type is not None and not tree:
        pre = [g for g in segs[book_at + 1:] if g["chapter"] == 0]
        later = [g["chapter"] for g in segs if g["chapter"] > 0]
        if pre and later and not any(g["css_class"] in HEADING_CSS for g in pre):
            for g in pre:
                g["chapter"] = min(later)
                notes["moved into the first chapter"].append(g["content"][:60])

    for k, g in enumerate(segs):
        g["id"] = f"{stem}_ch{g['chapter']}_k{k + 1}"

    data = {
        "id": stem,
        "title_pali": title,
        "collection": PITAKA.get(stem[0], ""),
        "pitaka": PITAKA.get(stem[0], ""),
        "layer": layer,
        "layer_type": layer_type,
        "source_filename": src.name,
        "source_url": RAW_BASE + src.name,
        "total_segments": len(segs),
        "segments": segs,
    }
    if book is not None:
        data["book_in_file"] = book
    if tree:
        data["tree"] = True
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    shape = f"tree mode, {sum(1 for g in segs if g['css_class'] == 'heading')} headings" if tree \
        else f"{chap} '{chapter_type}' chapters"
    print(f"{src.name}{f' book {book}' if book else ''}: {len(segs)} segments, {shape}, book '{title}' -> {dst}")
    print(f"  bold spans: {BOLD_STATS['spans']}")
    if suttas:
        print(f"  sutta headings (numbered subheads in vagga divs): {len(suttas)}")
    for what, items in notes.items():
        if items:
            print(f"  {what} ({len(items)}): {', '.join(items[:12])}{' …' if len(items) > 12 else ''}")


if __name__ == "__main__":
    args = sys.argv[1:]
    tree_mode = "--tree" in args
    args = [a for a in args if a != "--tree"]
    book_k = None
    if "--book" in args:
        i = args.index("--book")
        book_k = int(args[i + 1])
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    main(args[0], args[1], book=book_k, tree=tree_mode)
