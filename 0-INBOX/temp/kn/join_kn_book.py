"""Join a verified KN book draft (0-INBOX/temp/kn/pi-kn-<book>.md) onto 1-SOURCES/Text/pi-kn.md
(cscd-root-text-intake step 12): merge_volumes.py, its --split proof, then the joined file is
checked line for line against every XML in order; only if all pass is pi-kn.md replaced.

usage: python join_kn_book.py <book>[,<book>…] "<label for the frontmatter>"
  (several books at once when they share a CSCD file: 10,11 = s0510m1 + s0510m2)
"""
import re, subprocess, sys, shutil
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
book, label = sys.argv[1], sys.argv[2]
MV = "4-SYSTEM/Skills/cscd-root-text-intake/scripts/merge_volumes.py"
books = book.split(",")
D = Path("0-INBOX/temp/kn"); parts = [str(D / f"pi-kn-{b}.md") for b in books]; out = D / "pi-kn.join.md"
cur = Path("1-SOURCES/Text/pi-kn.md")
def run(*a):
    r = subprocess.run([sys.executable, *a], capture_output=True, text=True, encoding="utf-8")
    o = (r.stdout + r.stderr).strip()
    print("\n".join("   " + l for l in o.splitlines()[-6:]))
    if r.returncode: sys.exit(f"STOP: {a[0]} exited {r.returncode}")
    return o
for b in books:
    assert f"^{b}-0" not in cur.read_text(encoding="utf-8"), f"book {b} is already in pi-kn.md"
run("-I", "-X", "utf8", MV, str(out), str(cur), *parts, "--title", "Khuddakanikāya", "--label", label)
s = run("-I", "-X", "utf8", MV, "--split", str(out), str(cur), *parts)
assert s.strip().startswith("SPLIT OK") or "SPLIT OK" in s
fm = out.read_text(encoding="utf-8").split("\n---\n", 1)[0]
stems = re.findall(r"(s05\w+\.\w+)\.xml", fm.split("source_filename:")[1].split("\n")[0])
xmls = [str(next(Path("0-INBOX/raw-data/kn").glob(f"{st}.xml"))) for st in stems]
c = run("0-INBOX/xml-verification/compare_sutta.py", str(out), str(D / "pi-kn.join-detail.md"), *xmls)
m = re.search(r"xmlLines=(\d+) vaultLines=(\d+) equal=(\d+) .*?hunks=(\d+) idMismatch=(\d+).*?idProblems=(\d+) headIdBad=(\d+)", c)
x, v, eq, hunks, idm, idp, hb = map(int, m.groups())
if not (x == eq and hunks == 0 and idm == 0 and idp == 0 and hb == 0):
    sys.exit("STOP: the joined file does not match the XMLs line for line — not replacing pi-kn.md")
shutil.copyfile(out, cur)
print(f"== joined book {book}: pi-kn.md now {x} lines = XML ({len(xmls)} files), all IDs clean")
