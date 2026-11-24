"""Check that the heading-number restore changed nothing else: each file against its
committed version (git HEAD): same number of lines, every changed line is a heading,
and the new heading is the old one with only a printed number added in front.

usage: python -I -X utf8 verify_restore.py <git.exe> <file> …
"""
import re, sys, subprocess

GIT, files = sys.argv[1], sys.argv[2:]
NUM = re.compile(r"^(?:\(?\d+[\d\-–.,()]*\.?\)?\s*)+(?=\D)")
H = re.compile(r"^(#+\s+)(\*\*)?(.*?)(\*\*)?(\s+\^[\w-]+\s*)$")
bad_total = 0
for f in files:
    old = subprocess.run([GIT, "show", f"HEAD:{f}"], capture_output=True, check=True).stdout.decode("utf-8").split("\n")
    new = open(f, encoding="utf-8", newline="").read().split("\n")
    bad, n = [], 0
    if len(old) != len(new):
        bad.append(f"line count {len(old)} -> {len(new)}")
    for i, (a, b) in enumerate(zip(old, new), 1):
        if a == b: continue
        if a.startswith("source_description:") and a.replace(
                "chapter numbers stripped from headings",
                "printed heading numbers kept in the headings, as in the XML") == b:
            continue   # fix_description.py, the one approved frontmatter change
        n += 1
        ma, mb = H.match(a), H.match(b)
        if not (ma and mb) or ma.group(1) != mb.group(1) or ma.group(5) != mb.group(5) \
           or (ma.group(2), ma.group(4)) != (mb.group(2), mb.group(4)) \
           or NUM.sub("", mb.group(3)) != NUM.sub("", ma.group(3)) or not NUM.match(mb.group(3)):
            bad.append(f"line {i}: {a!r} -> {b!r}")
    bad_total += len(bad)
    print(f"{f}: {n} lines changed, all heading-number additions" if not bad else f"{f}: {n} changed, {len(bad)} NOT a number addition")
    for x in bad[:10]: print("   ", x)
print("TOTAL problems:", bad_total)
