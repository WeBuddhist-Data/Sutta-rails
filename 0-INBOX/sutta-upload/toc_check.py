"""Read-only: is every TOC difference on prod only a restored heading number?
Walks the live and built TOC trees in parallel; every other field must be equal,
and a differing title must be the built title with a leading printed number
removed. Also prints SN ṭīkā's alignment pairs that differ.
Run from the vault root:  python -X utf8 0-INBOX/sutta-upload/toc_check.py <kind> <notes...>"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path("4-SYSTEM/Skills/library-upload/scripts").resolve()))
from webuddhist import envs, text as T                      # noqa: E402
from webuddhist.api import Client                            # noqa: E402
from webuddhist.ledger import Ledger                         # noqa: E402

NUM = re.compile(r"^(?:\(?\d+[\d\-–.,()]*\.?\)?\s*)+(?=\D)")
kind, notes = sys.argv[1], sys.argv[2:]
env = envs.get("prod")
ctx = T.Ctx(env=env, client=Client(env), ledger=Ledger(env.name, "texts"))


def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            out["other"].append(f"{path}: keys {sorted(a.keys() ^ b.keys())}")
        for k in a.keys() & b.keys():
            walk(a[k], b[k], f"{path}.{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out["other"].append(f"{path}: {len(a)} vs {len(b)} items")
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]", out)
    elif a != b:
        if isinstance(a, str) and isinstance(b, str) and NUM.sub("", b, count=1) == a and b != a:
            out["num"] += 1
        elif isinstance(a, str) and isinstance(b, str) and NUM.sub("", b, count=1).strip() == a.strip():
            out["num_space"].append(f"{path}: {a!r} -> {b!r}")
        else:
            out["other"].append(f"{path}: {str(a)[:70]!r} -> {str(b)[:70]!r}")


for it in T.assess_all(kind, notes, ctx, progress=False):
    if it.live_content is None:
        print(f"{it.key}: not on prod")
        continue
    have = T.ann_sets("toc", T._live_toc_sections(it))
    want = T.ann_sets("toc", it.p.get("toc"))
    out = {"num": 0, "num_space": [], "other": []}
    walk(have, want, "toc", out)
    print(f"{it.key}: {sorted(it.flags)}  number-only title changes={out['num']}  "
          f"other={len(out['other'])}  spacing={len(out['num_space'])}")
    for x in (out["other"] + out["num_space"])[:8]:
        print("    " + x)
    if it.pairs is not None and it.live_pairs is not None and set(it.pairs) != set(it.live_pairs):
        w, h = set(it.pairs), set(it.live_pairs)
        print(f"    pairs only in note: {sorted(w - h)[:10]}  only on prod: {sorted(h - w)[:10]}")
