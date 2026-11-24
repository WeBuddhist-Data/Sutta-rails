"""After the rename: every [[path#^id]] link and every root_text:/commentary: line in 1-SOURCES
points at an existing file and (for links) an existing block ID; no exact old name is left in
1-SOURCES or vault-annex.md.   usage: python check_links.py   (from the vault root)"""
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
OLD = re.compile(r"(?<![\w-])pi-(dn|mn|sn|an|kn)(-1-abhinavatiika|-atthakatha|-tiika)?(?![\w-])")
ids_of = {}


def ids(path):
    if path not in ids_of:
        t = Path(path).read_text(encoding="utf-8")
        ids_of[path] = set(re.findall(r"\s\^([\w-]+)\s*$", t, re.M))
    return ids_of[path]


links = bad = fm = 0
problems = []
for f in sorted(Path("1-SOURCES").rglob("*.md")):
    t = f.read_text(encoding="utf-8")
    for m in re.finditer(r"\[\[([^\]#|]+\.md)#\^([\w-]+)", t):
        links += 1
        path, bid = m.group(1), m.group(2)
        if not Path(path).exists():
            bad += 1; problems.append(f"{f.name}: missing file {path}")
        elif bid not in ids(path):
            bad += 1; problems.append(f"{f.name}: {path} has no ^{bid}")
    for m in re.finditer(r"^(root_text|commentary): (\S+)", t, re.M):
        fm += 1
        if not Path(m.group(2)).exists():
            problems.append(f"{f.name}: {m.group(1)} -> missing {m.group(2)}")
    if OLD.search(t):
        problems.append(f"{f.name}: old name left: {OLD.search(t).group(0)}")
a = Path("4-SYSTEM/Guidelines/vault-annex.md").read_text(encoding="utf-8")
if OLD.search(a):
    problems.append(f"vault-annex.md: old name left: {OLD.search(a).group(0)}")
print(f"links {links} (broken {bad}), frontmatter paths {fm}, problems {len(problems)}")
for p in problems[:20]:
    print("  ", p)
sys.exit(1 if problems else 0)
