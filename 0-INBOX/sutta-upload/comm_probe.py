"""Read-only: for commentaries on prod, show the content segments that differ and
the alignment pairs only on prod / only in the note. Uses library-upload's own
modules (GETs only).
Run from the vault root:  python -X utf8 0-INBOX/sutta-upload/comm_probe.py <notes...>"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path("0-INBOX/sutta-upload").resolve()))
sys.path.insert(0, str(Path("4-SYSTEM/Skills/library-upload/scripts").resolve()))
from webuddhist import envs, text as T                      # noqa: E402
from webuddhist.api import Client                            # noqa: E402
from webuddhist.ledger import Ledger                         # noqa: E402
import difflib                                               # noqa: E402


def seg_texts(content, segs):
    return [(str(s.get("reference")), "".join(content[l["start"]:l["end"]] for l in s["lines"]), None)
            for s in segs]


def show(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return " | ".join(f"…{a[max(0, i1 - 25):i1]}[{a[i1:i2]!r} -> {b[j1:j2]!r}]{a[i2:i2 + 25]}…"
                      for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")[:600]

env = envs.get("prod")
ctx = T.Ctx(env=env, client=Client(env), ledger=Ledger(env.name, "texts"))
for it in T.assess_all("commentary", sys.argv[1:], ctx, progress=False):
    print(f"\n=== {it.key}   flags: {sorted(it.flags)}")
    if it.live_content is None:
        continue
    new = it.p["edition"]
    if new["content"] != it.live_content:
        live = seg_texts(it.live_content, it.live_segs or [])
        built = seg_texts(new["content"], new["segmentation"]["segments"])
        n = 0
        for (lr, lt, _), (br, bt, _) in zip(live, built):
            if lr != br or lt != bt:
                n += 1
                if n <= 15:
                    print(f"  seg {lr}->{br}: {show(lt, bt)}")
        print(f"  {n} segment(s) differ")
    if it.pairs is not None:
        want, have = set(it.pairs), set(it.live_pairs or [])
        only_note, only_prod = sorted(want - have), sorted(have - want)
        print(f"  pairs: prod={len(have)} note={len(want)}  only in note={len(only_note)}  only on prod={len(only_prod)}")
        for lab, ps in (("note", only_note), ("prod", only_prod)):
            if ps:
                by_src = Counter(s for s, _ in ps)
                print(f"   only in {lab}, first: " + ", ".join(f"{s}->{t}" for s, t in ps[:12]))
                print(f"   ({len(by_src)} commentary blocks)")
