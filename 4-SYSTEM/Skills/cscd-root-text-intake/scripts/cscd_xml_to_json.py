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

Supported shapes: <div type="book"> containing chapter-level <div>s of ONE type
(e.g. "sutta"), each opening with a <head>; or a volume with no <div>s at all,
where each <p rend="chapter"> opens the next chapter. Any other nesting
(vagga/saṃyutta/paṇṇāsa divs inside the book) stops the script (non-zero exit,
"STOP: …" message, nothing written) —
the converter downstream only knows book > chapter > subhead, so a deeper
volume needs this script extended first, not silently flattened.

Usage: python3 -I cscd_xml_to_json.py <in.xml> <out.json>
"""
import collections
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

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


def main(src, dst):
    src = Path(src)
    root = ET.parse(src).getroot()
    body = root.find(".//body")
    chapter_type = check_shape(body)
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
            if chapter_type is None and css == "chapter":
                chap += 1        # div-less volume: a chapter paragraph opens a chapter
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
            segs.append({
                "id": f"{stem}_ch{chap}_k{len(segs) + 1}",
                "chapter": chap,
                "paragraph": child.get("n") or "",
                "content": content,
                "css_class": css,
            })

    walk(body)
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
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{src.name}: {len(segs)} segments, {chap} '{chapter_type}' chapters, "
          f"book '{title}' -> {dst}")
    print(f"  bold spans: {BOLD_STATS['spans']}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
