"""Look up root IDs and a commentary's context for the second-pass link items."""
import re, sys
from pathlib import Path

root = sys.argv[1]
ids = set(re.findall(r"\s\^([\w-]+)\s*$", Path(root).read_text(encoding="utf-8"), re.M))
for q in sys.argv[2:]:
    if q.startswith("@"):   # @file:line -> show the lines around
        f, n = q[1:].rsplit(":", 1); n = int(n)
        L = Path(f).read_text(encoding="utf-8").split("\n")
        print(f"--- {f}:{n}")
        for k in range(n - 6, n + 1): print("   ", L[k - 1][:150])
    else:                   # an ID prefix: list root IDs matching ^prefix(-|$)
        hits = sorted(i for i in ids if re.match(rf"{re.escape(q)}(?:$|[-x])", i))
        print(f"{q}: {hits[:12]}")
