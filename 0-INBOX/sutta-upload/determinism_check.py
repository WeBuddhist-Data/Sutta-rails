"""Rebuild the linter + parser output twice from the current notes and compare
checksums: run 1 vs what was on disk (what went stale), run 2 vs run 1 (is the
output deterministic?). Uses run_lint_parse.py, which restores every note.
Run from the vault root:  python -X utf8 0-INBOX/sutta-upload/determinism_check.py"""
import hashlib
import subprocess
import sys
from pathlib import Path

OUT = sorted(Path("4-SYSTEM/scripts").glob("*/output"))


def snapshot():
    return {p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for d in OUT for p in sorted(d.rglob("*")) if p.is_file()}


def run():
    r = subprocess.run([sys.executable, "-X", "utf8", "0-INBOX/sutta-upload/run_lint_parse.py"],
                       capture_output=True, text=True, encoding="utf-8")
    bad = [l for l in r.stdout.splitlines() if l[:2] != "ok" and not l.startswith(" ")]
    if r.returncode or bad:
        sys.exit("build failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])


def compare(a, b, label):
    changed = sorted(k for k in a.keys() & b.keys() if a[k] != b[k])
    print(f"{label}: {len(changed)} changed, {len(b.keys() - a.keys())} new, {len(a.keys() - b.keys())} gone")
    for k in changed + sorted(b.keys() - a.keys()) + sorted(a.keys() - b.keys()):
        print("   ", k)


s0 = snapshot()
run()
s1 = snapshot()
compare(s0, s1, "run 1 vs disk")
run()
s2 = snapshot()
compare(s1, s2, "run 2 vs run 1")
