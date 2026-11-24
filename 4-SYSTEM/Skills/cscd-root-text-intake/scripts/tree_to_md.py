#!/usr/bin/env python3
"""
tree_to_md.py — step 4 of cscd-root-text-intake, for a volume converted with
`cscd_xml_to_json.py --tree` (Aṅguttaranikāya and other nested shapes).

Same output as json-to-source-text's tipitaka_org_book.py, except that every
heading takes its level ('#' count) from the segment's "level" field instead of
from a fixed chapter > title > subhead scheme:

    Namo tassa …                      homage (plain line; ^T-1 later)
    # <nikāya> ^0                     the nikaya segment
    ## <book> ^1-0                    the book segment (book number set by prepare_ids.py)
    ###… <heading> ^…-0               each heading at its own level, printed number stripped

Blocks, as in tipitaka_org_book.py: a paragraph opening with "N. " (or a printed
range "N-M. ", or a number-only line) starts a block; the lines after it, up to
the next numbered paragraph or heading, are its continuation; unnumbered text
right after a heading is prepended to the next numbered paragraph (prepare_ids.py
splits it off as its own block). IDs written here are provisional: apply.py and
heading_ids.py assign the real ones.

Usage: python3 -I tree_to_md.py <in.json> <out.md>
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cscd_shape  # noqa: E402

VERSE_OPEN = re.compile(r"^\s*(\d+(?:-\d+)?)(?:\.\s|\s*$)")
NUM_ALONE = re.compile(r"^\s*(\d+(?:-\d+)?)\s*\.$")


def main(src, dst):
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    if not data.get("tree"):
        sys.exit("STOP: this JSON was not made with cscd_xml_to_json.py --tree")
    out = ["---", f"title: {data.get('title_pali') or ''}", "---", ""]
    buf, num, pending, opening = [], [None], [None], [False]

    def flush():
        if buf:
            out.append("\n".join(buf) + (f" ^1-{num[0]}" if num[0] else "") + "\n")
            buf.clear()

    seen_book = False
    for g in data["segments"]:
        css, text = g["css_class"], g["content"].strip()
        if not text:
            continue
        if not seen_book:
            if css == "centered":
                out.append(text + "\n")
                continue
            if css == "nikaya":
                out.append(f"# {text} ^0\n")
                continue
            if css == "book":
                out.append(f"## {text} ^1-0\n")
                seen_book = True
                continue
        if css == "heading":
            flush()
            num[0] = None
            opening[0] = False
            out.append(f"{'#' * g['level']} {cscd_shape.strip_heading_number(text)} ^1-h-0\n")
            continue
        if text.startswith("Namo tassa"):
            # a second volume's printed opening inside one book (CSCD Therāpadāna part 2:
            # homage, nikāya, book title, "(Dutiyo bhāgo)"): each line its own block up to the
            # next heading, not the continuation of the last verse before it
            flush()
            num[0] = None
            opening[0] = True
        if opening[0]:
            out.append(text + "\n")
            continue
        if pending[0]:
            # a number printed alone in its own paragraph ("474 ." in a bodytext <p>,
            # CSCD Suttanipāta) opens the next paragraph, as a joined hangnum does
            text = f"{pending[0]}. {text}"
            pending[0] = None
        elif NUM_ALONE.match(text) and g.get("paragraph"):
            pending[0] = NUM_ALONE.match(text).group(1)
            continue
        m = VERSE_OPEN.match(text)
        if m and g.get("paragraph", None) == "" and css == "centered":
            # Text that only looks numbered: a centred title whose "N. " is not a paranum
            # (CSCD Vimānavatthu, the sub-stories "1. Vatthuttamadāyikāvimānavatthu" …
            # inside the Guttilavimāna). Its own block, marked ^1-nonum so apply.py gives
            # it a ^<book>-U<k> ID and keeps its "N. " as text. (A hangnum joined to its
            # verse may also lack @n — the Suttuddāna's 2–21 — and is a real number.)
            flush()
            num[0] = None
            out.append(f"{text} ^1-nonum\n")
            continue
        if m:
            if num[0] is not None:
                flush()
            num[0] = m.group(1)
        buf.append(text)
    flush()
    Path(dst).write_text("\n".join(out), encoding="utf-8")
    print(f"{Path(dst).name}: {sum(1 for g in data['segments'] if g['css_class'] == 'heading')} headings")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
