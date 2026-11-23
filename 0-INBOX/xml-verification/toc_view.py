"""Print a heading tree (TOC only) with, per heading, the number of text blocks directly
under it (before its first sub-heading or next heading), or EMPTY if it has neither text
nor sub-headings.

usage: python toc_view.py <file.md> <heading-id-or-title-prefix> [--depth N]
  prints the subtree of the first heading whose ID or title matches.
"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
path, key = sys.argv[1], sys.argv[2]
maxd = int(sys.argv[sys.argv.index("--depth") + 1]) if "--depth" in sys.argv else 99
L = open(path, encoding="utf-8").read().replace("\r\n", "\n").split("\n")
H = re.compile(r"^(#+)\s+(.*?)\s+\^([\w-]+)\s*$")
heads, blocks_under, cur, in_block = [], {}, None, False
for i, l in enumerate(L):
    m = H.match(l)
    if m:
        cur = len(heads)
        heads.append((len(m.group(1)), re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2)), m.group(3), i + 1))
        blocks_under[cur] = 0; in_block = False
        continue
    if cur is None or l.startswith("---"):
        continue
    if l.strip() and not in_block:
        if not l.startswith("![["):
            blocks_under[cur] += 1
        in_block = True
    elif not l.strip():
        in_block = False
start = next(i for i, h in enumerate(heads) if h[2] == key.lstrip("^") or h[1].startswith(key))
d0 = heads[start][0]
for i in range(start, len(heads)):
    d, t, hid, ln = heads[i]
    if i > start and d <= d0:
        break
    if d - d0 > maxd:
        continue
    has_kids = i + 1 < len(heads) and heads[i + 1][0] > d
    n = blocks_under[i]
    mark = "EMPTY" if n == 0 and not has_kids else (f"{n} block{'s' if n != 1 else ''}" if n else "—")
    flag = "   <<< EMPTY" if mark == "EMPTY" else ""
    print(f"{'    ' * (d - d0)}{'#' * d} {t}  ^{hid}   [{mark}]{flag}")
