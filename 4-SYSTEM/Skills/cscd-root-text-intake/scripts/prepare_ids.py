#!/usr/bin/env python3
"""
prepare_ids.py — step 4 of cscd-root-text-intake (between the converter and apply.py).

Two mechanical fixes on the converter's markdown, both required before
apply.py can see every numbered paragraph:

1. Set the book number on the '##' line (`## <title> ^<book>-0`). apply.py
   reads the book from that ID.
2. Split "buried" numbers: tipitaka_org_book.py prepends unnumbered text that
   follows a sub-heading to the next numbered paragraph, so the block's first
   line is unnumbered and its `N.` sits on a later line. apply.py only reads a
   block's first line, so it would miss N. A blank line is inserted before the
   `N.` line; the unnumbered text becomes its own block (^<book>-U<k> on apply).

Every split is printed, so it can be recorded in the run report.
Usage: python3 -I prepare_ids.py <book> <file.md>
"""
import re
import sys

book, path = sys.argv[1], sys.argv[2]
lines = open(path, encoding="utf-8").read().split("\n")
NUM = re.compile(r"^\d+(?:-\d+)?(?:\.\s|$)")   # "149. ", a range "225-240. ", or a number-only line

h2 = [i for i, l in enumerate(lines) if l.startswith("## ")]
if len(h2) != 1:
    sys.exit(f"STOP: expected exactly one '##' line, found {len(h2)}")
lines[h2[0]] = re.sub(r"\s+\^[\w-]+\s*$", "", lines[h2[0]]).rstrip() + f" ^{book}-0"

out, splits = [], []
block_start = True
for i, line in enumerate(lines):
    blank_or_heading = (not line.strip()) or line.startswith("#")
    if not blank_or_heading and not block_start and NUM.match(line):
        splits.append((i + 1, line[:70]))
        out.append("")
    out.append(line)
    block_start = blank_or_heading

open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print(f"{path}: book set to {book}; {len(splits)} buried number(s) split")
for ln, txt in splits:
    print(f"   split before line {ln}: {txt}")
