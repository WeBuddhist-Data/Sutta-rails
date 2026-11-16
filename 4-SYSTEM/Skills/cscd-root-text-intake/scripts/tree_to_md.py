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


def main(src, dst):
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    if not data.get("tree"):
        sys.exit("STOP: this JSON was not made with cscd_xml_to_json.py --tree")
    out = ["---", f"title: {data.get('title_pali') or ''}", "---", ""]
    buf, num = [], [None]

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
            out.append(f"{'#' * g['level']} {cscd_shape.strip_heading_number(text)} ^1-h-0\n")
            continue
        m = VERSE_OPEN.match(text)
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
