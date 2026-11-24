"""Rename the Sutta files pi-<nikāya abbreviation> to pi-<nikāya name> (human decision
2026-11-24, as Vinaya's pi-N -> pi-<book>pali) and repoint everything that names them.

  root texts    pi-dn.md -> pi-dighanikaya.md, pi-mn -> pi-majjhimanikaya, pi-sn -> pi-samyuttanikaya,
                pi-an -> pi-anguttaranikaya, pi-kn -> pi-khuddakanikaya       (CLAUDE.md §4: no diacritics)
  commentaries  same prefix, layer part unchanged: pi-dn-atthakatha -> pi-dighanikaya-atthakatha,
                pi-dn-tiika -> pi-dighanikaya-tiika, pi-dn-1-abhinavatiika -> pi-dighanikaya-1-abhinavatiika, …

- git mv the 15 files, and tracked linter/parser output named exactly after one of them;
- 1-SOURCES (transclusions, root_text:, commentary:) and vault-annex.md: every exact current name.
  Only exact names change: the annex's historical per-volume names (pi-dn-1.md … pi-an-11.md,
  pi-kn-1.md) are not current names and stay. Library ids (registered_id: dn-tiika …) are not
  file names and stay. The upload ledgers are not edited (the upload skills forbid hand edits).
Bytes other than the replaced names are untouched (line endings kept).

usage: python rename_sutta.py [--write]      (from the vault root)
"""
import re
import subprocess
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
GIT = r"C:\Users\Uzumaki Sither\AppData\Local\GitHubDesktop\app-3.6.11\resources\app\git\cmd\git.exe"
NIK = {"dn": "dighanikaya", "mn": "majjhimanikaya", "sn": "samyuttanikaya", "an": "anguttaranikaya", "kn": "khuddakanikaya"}
W = "--write" in sys.argv
git = lambda *a: subprocess.run([GIT, *a], capture_output=True, text=True, check=True, encoding="utf-8").stdout

roots = {f"pi-{k}": f"pi-{v}" for k, v in NIK.items()}
comms = {}
for f in sorted(Path("1-SOURCES/Commentaries").glob("pi-*.md")):
    m = re.fullmatch(r"pi-(dn|mn|sn|an|kn)(-.+)", f.stem)
    assert m, f
    comms[f.stem] = f"pi-{NIK[m.group(1)]}{m.group(2)}"
NEW = {**roots, **comms}
for old in roots:
    assert Path(f"1-SOURCES/Text/{old}.md").exists(), old

# an exact current name: not part of a longer name on either side (pi-dn-1.md is not pi-dn)
names = sorted(NEW, key=len, reverse=True)
TOK = re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, names)) + r")(?![\w-])")

edits, counts = {}, {}
targets = sorted(str(p) for p in Path("1-SOURCES").rglob("*.md")) + ["4-SYSTEM/Guidelines/vault-annex.md"]
for f in targets:
    s = Path(f).read_bytes().decode("utf-8")
    s2, n = TOK.subn(lambda m: NEW[m.group(1)], s)
    if n:
        edits[f], counts[f] = s2, n

moves = [(f"1-SOURCES/Text/{o}.md", f"1-SOURCES/Text/{n}.md") for o, n in roots.items()]
moves += [(f"1-SOURCES/Commentaries/{o}.md", f"1-SOURCES/Commentaries/{n}.md") for o, n in comms.items()]
for f in git("ls-files", "4-SYSTEM").splitlines():
    if "/output/" not in f:
        continue
    head, tail = f.split("/output/", 1)
    parts = tail.split("/")              # e.g. pi-an-atthakatha/pi-an-atthakatha.text.json
    new = []
    for i, part in enumerate(parts):
        stem = part.split(".", 1)[0] if i == len(parts) - 1 else part
        new.append(NEW[stem] + part[len(stem):] if stem in NEW else part)
    if new != parts:
        moves.append((f, f"{head}/output/{'/'.join(new)}"))

for f, n in counts.items():
    print(f"{n:6}  {f}")
print(f"files to move: {len(moves)}")
for a, b in moves:
    print(f"   {a}  ->  {b}")
if W:
    for f, s in edits.items():
        Path(f).write_bytes(s.encode("utf-8"))
    for a, b in moves:
        Path(b).parent.mkdir(parents=True, exist_ok=True)
        git("mv", a, b)
    print("written")
else:
    print("dry run; pass --write to apply")
