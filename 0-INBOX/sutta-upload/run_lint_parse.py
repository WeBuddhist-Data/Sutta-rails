"""Run the vault's updated linter + parser (4-SYSTEM/scripts/) on the 5 Sutta roots
and their 11 commentaries, exactly as library-upload does (linter, then parser on
its output), restoring each note byte for byte afterwards (the linter may fill in
frontmatter). Nothing is sent anywhere.

Writes 0-INBOX/sutta-upload/lint-parse/<stem>.log (full stdout/stderr) and
prints a summary line per file.
Run from the vault root:  python -X utf8 0-INBOX/sutta-upload/run_lint_parse.py"""
import json
import re
import subprocess
import sys
from pathlib import Path

VAULT = Path.cwd()
S = VAULT / "4-SYSTEM/scripts"
LOGS = VAULT / "0-INBOX/sutta-upload/lint-parse"
LOGS.mkdir(parents=True, exist_ok=True)
NK = ["dighanikaya", "majjhimanikaya", "samyuttanikaya", "anguttaranikaya", "khuddakanikaya"]
FILES = []
for nk in NK:
    FILES.append(("root", VAULT / f"1-SOURCES/Text/pi-{nk}.md"))
    for c in sorted((VAULT / "1-SOURCES/Commentaries").glob(f"pi-{nk}-*.md")):
        FILES.append(("commentary", c))

rows = []
for kind, path in FILES:
    lint_dir, parse_dir = ("linter-commentary", "parser-commentary") if kind == "commentary" \
        else ("linter-root-text", "parser-root-text")
    linter, parser = S / lint_dir / "lint_text_input.py", S / parse_dir / "parser.py"
    snap = path.read_bytes()
    log = [f"# {path.relative_to(VAULT).as_posix()}  ({kind})\n"]
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", str(linter), str(path)], cwd=VAULT,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        log += ["## linter (exit %d)\n" % r.returncode, r.stdout, r.stderr]
        ok = S / lint_dir / "output" / f"{path.stem}.lint.json"
        bad = S / lint_dir / "output" / f"{path.stem}.lint.errors.json"
        lint_failed = r.returncode != 0 or not ok.exists() or (bad.exists() and bad.stat().st_mtime > ok.stat().st_mtime)
        p_rc, p_out = None, ""
        if not lint_failed:
            p = subprocess.run([sys.executable, "-X", "utf8", str(parser), str(path), str(ok)], cwd=VAULT,
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            p_rc, p_out = p.returncode, p.stdout + p.stderr
            log += ["## parser (exit %d)\n" % p.returncode, p.stdout, p.stderr]
    finally:
        changed = path.read_bytes() != snap
        if changed:
            path.write_bytes(snap)
    (LOGS / f"{path.stem}.log").write_text("\n".join(log), encoding="utf-8")
    text = "\n".join(log)
    warns = [l for l in text.splitlines() if re.search(r"\bWARN|WARNING|ERROR", l)]
    out = S / parse_dir / "output" / path.stem
    stats = {}
    if out.is_dir():
        ed = json.loads((out / f"{path.stem}.edition.json").read_text(encoding="utf-8"))
        segs = ed["segmentation"]["segments"]
        stats["segs"] = len(segs)
        stats["types"] = {t: sum(1 for s in segs if s["type"] == t) for t in sorted({s["type"] for s in segs})}
        stats["**"] = ed["content"].count("**")
        al = out / f"{path.stem}.alignment.json"
        if al.exists():
            stats["pairs"] = len(json.loads(al.read_text(encoding="utf-8"))["alignments"])
        fn = out / f"{path.stem}.footnotes.json"
        if fn.exists():
            stats["footnotes"] = len(json.loads(fn.read_text(encoding="utf-8"))["footnotes"])
    status = "LINT-FAIL" if lint_failed else ("PARSE-FAIL" if p_rc else "ok")
    print(f"{status:10} {path.stem:38} {stats}  warn-lines={len(warns)}  restored={changed}")
    for w in warns[:6]:
        print("            " + w.strip()[:200])
