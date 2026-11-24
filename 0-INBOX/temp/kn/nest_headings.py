"""Nest the N sibling headings that follow an empty heading under it (human decision), with
their whole sub-trees. Only heading lines change: one '#' more and the new path ID. Later
siblings move up by N. Text and content IDs are untouched.

  python nest_headings.py <file.md> <parent-id> <N>
  e.g. python nest_headings.py 1-SOURCES/Text/pi-kn.md 15-1 16
       ### Aṭṭhakavaggo ^15-1-0 (empty) + the 16 '###' niddesas ^15-2-0 … ^15-17-0
       -> the niddesas become '####' ^15-1-1-0 … ^15-1-16-0

Checks: the parent is empty before and has its children right under it after; every heading's
'#' count = its ID path length + 1 (headings deeper than '######' keep the **bold** rule:
refused here); all block IDs unique; the line count is unchanged.
"""
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
path, parent, n = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
raw = path.read_bytes().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
lines = raw.split(nl)
H = re.compile(r"^(#+) (.*) \^([\d-]+)-0$")
P = [int(x) for x in parent.split("-")]

heads = [(i, H.match(l)) for i, l in enumerate(lines) if H.match(l)]
pi = next(k for k, (i, m) in enumerate(heads) if m.group(3) == parent)
lvl = len(heads[pi][1].group(1))
assert lvl == len(P) + 1, "parent level does not match its ID"
nxt = next(l for l in lines[heads[pi][0] + 1:] if l.strip())
assert H.match(nxt) and len(H.match(nxt).group(1)) <= lvl, f"parent is not empty: {nxt[:80]}"

# siblings after the parent: same level, same prefix, until the prefix's sub-tree ends
pre = P[:-1]
sib = []
for i, m in heads[pi + 1:]:
    q = [int(x) for x in m.group(3).split("-")]
    if q[:len(pre)] != pre or len(q) < len(P):
        break                                      # left the parent's own parent
    if len(q) == len(P):
        sib.append(q[-1])
assert len(sib) >= n and sib[:n] == list(range(P[-1] + 1, P[-1] + 1 + n)), f"siblings after {parent}: {sib[:n + 2]}"
adopt = {P[-1] + k: k for k in range(1, n + 1)}     # old ordinal -> child number

changed = 0
for i, m in heads[pi + 1:]:
    q = [int(x) for x in m.group(3).split("-")]
    if q[:len(pre)] != pre or len(q) < len(P):
        break
    o = q[len(P) - 1]
    if o in adopt:
        new = P + [adopt[o]] + q[len(P):]
    else:
        new = pre + [o - n] + q[len(P):]
    level = len(new) + 1
    assert level <= 6, "deeper than ###### needs the **bold** form: not handled here"
    line = f"{'#' * level} {m.group(2)} ^{'-'.join(map(str, new))}-0"
    if line != lines[i]:
        print(f"  {lines[i]}  ->  {line}")
        lines[i] = line
        changed += 1

nxt = next(l for l in lines[heads[pi][0] + 1:] if l.strip())
assert len(H.match(nxt).group(1)) == lvl + 1, "parent did not get its children"
for l in lines:
    m = H.match(l)
    if m and not m.group(3).isdigit():
        assert len(m.group(1)) == m.group(3).count("-") + 2, f"level/ID mismatch: {l}"
out = nl.join(lines)
assert out.count(nl) == raw.count(nl)
ids = re.findall(r"\s\^([\w-]+)\s*$", out, re.M)
assert len(ids) == len(set(ids)), "duplicate block IDs"
path.write_bytes(out.encode("utf-8"))
print(f"{path}: {changed} heading lines changed; {len(ids)} block IDs, all unique; text untouched")
