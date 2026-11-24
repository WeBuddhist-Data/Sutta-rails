"""For each printed citation with no links (from <file>-more.md), show the heading it sits under,
and, for KN, whether the build log (0-INBOX/temp/kn-comm/*.unresolved.json) lists it."""
import json, re, sys, glob
from pathlib import Path

name = sys.argv[1]
src = next(p for p in glob.glob(f"1-SOURCES/*/{name}.md"))
L = Path(src).read_text(encoding="utf-8").split("\n")
items = re.findall(r"^- line (\d+): `", Path(f"0-INBOX/sutta-review/{name}-more.md").read_text(encoding="utf-8")
                   .split("### Printed citations with no links", 1)[-1], re.M)
logged = {}
for j in glob.glob("0-INBOX/temp/kn-comm/*.unresolved.json"):
    d = json.loads(Path(j).read_text(encoding="utf-8"))
    for k, v in d.items():
        for e in v if isinstance(v, list) else []:
            p = (e[0] if isinstance(e, list) else e.get("printed") if isinstance(e, dict) else str(e))
            logged.setdefault(str(p).strip().rstrip("."), []).append(f"{Path(j).stem.split('.')[0]}:{k}")
for n in map(int, items):
    h = next((L[k] for k in range(n - 1, 0, -1) if L[k].startswith("#")), "")
    num = re.match(r"^\**(\d+(?:-\d+)?)", L[n - 1]).group(1)
    log = logged.get(num, [])
    print(f"{n:7}  {num:>8}  under {h[:60]!r}  {'LOGGED ' + ','.join(sorted(set(log)))[:60] if log else ''}")
