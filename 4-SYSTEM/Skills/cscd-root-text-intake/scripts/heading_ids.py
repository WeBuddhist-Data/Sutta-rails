#!/usr/bin/env python3
"""heading_ids.py — step 6 of cscd-root-text-intake: heading IDs + pre-title
^T-N, after apply.py has set content IDs.

- content strictly before the first heading (after frontmatter) -> ^T-1, ^T-2 ...
- '#'  -> ^0
- '##' -> ^{book}-0
- deeper headings -> ^{book}-{sibling path}-0, Arabic, sibling counters reset
  under each new parent.
Existing IDs on headings / pre-title lines are replaced. Content IDs untouched.
Usage: python3 -I heading_ids.py <book> <file.md>
"""
import re
import sys

book, path = sys.argv[1], sys.argv[2]
lines = open(path, encoding="utf-8").read().split("\n")
ID = re.compile(r"\s+\^[\w-]+\s*$")

i = 0
if lines and lines[0].strip() == "---":
    i = lines.index("---", 1) + 1

out = lines[:i]
seen_heading = False
t_k = 0
counters = []          # counters[d] = sibling count at depth d (depth 0 = '###')
for line in lines[i:]:
    m = re.match(r"^(#+)\s+(.*)$", line)
    if m:
        seen_heading = True
        level = len(m.group(1))
        title = ID.sub("", m.group(2)).rstrip()
        if level == 1:
            hid = "0"
        elif level == 2:
            hid = f"{book}-0"
            counters = []
        else:
            depth = level - 3
            counters = counters[: depth + 1]
            while len(counters) < depth + 1:
                counters.append(0)
            counters[depth] += 1
            hid = f"{book}-" + "-".join(str(c) for c in counters) + "-0"
        out.append(f"{m.group(1)} {title} ^{hid}")
        continue
    if not seen_heading and line.strip():
        t_k += 1
        out.append(ID.sub("", line).rstrip() + f" ^T-{t_k}")
        continue
    out.append(line)

open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print(f"{path}: headings done, {t_k} pre-title block(s)")
