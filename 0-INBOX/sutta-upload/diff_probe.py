"""Read-only: why library-upload's prod status is not just toc-differs.
Uses library-upload's own modules (GETs only). For each note: the segments whose
text differs (live vs built), boundary moves, and a TOC summary.
Run from the vault root:  python -X utf8 0-INBOX/sutta-upload/diff_probe.py <kind> <notes...>"""
import difflib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path("4-SYSTEM/Skills/library-upload/scripts").resolve()))
from webuddhist import envs, text as T                      # noqa: E402
from webuddhist.api import Client                            # noqa: E402
from webuddhist.ledger import Ledger                         # noqa: E402

kind, notes = sys.argv[1], sys.argv[2:]
env = envs.get("prod")
ctx = T.Ctx(env=env, client=Client(env), ledger=Ledger(env.name, "texts"))
states = T.assess_all(kind, notes, ctx, progress=False)


def seg_texts(content, segs):
    out = []
    for s in segs:
        out.append((str(s.get("reference")), "".join(content[l["start"]:l["end"]] for l in s["lines"]),
                    (s["lines"][0]["start"], s["lines"][-1]["end"])))
    return out


def show(a, b, width=70):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    parts = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            ctxs = a[max(0, i1 - 25):i1]
            parts.append(f"…{ctxs}[{a[i1:i2]!r} -> {b[j1:j2]!r}]{a[i2:i2 + 25]}…")
    return " | ".join(parts)[:600]


for it in states:
    print(f"\n=== {it.key}   flags: {dict(it.flags)}")
    if it.live_content is None:
        continue
    new = it.p["edition"]
    live = seg_texts(it.live_content, it.live_segs or [])
    built = seg_texts(new["content"], new["segmentation"]["segments"])
    print(f"segments live={len(live)} built={len(built)}  content live={len(it.live_content)} built={len(new['content'])}")
    n = 0
    for (lr, lt, lsp), (br, bt, bsp) in zip(live, built):
        if lr != br or lt != bt:
            n += 1
            if n <= 25:
                print(f"  seg {lr}->{br}: {show(lt, bt)}")
    print(f"  {n} segment(s) differ")
    # TOC
    want = T.ann_sets("toc", it.p.get("toc"))
    have = T.ann_sets("toc", T._live_toc_sections(it))
    if want != have:
        w = json.dumps(want, ensure_ascii=False, indent=0).splitlines()
        h = json.dumps(have, ensure_ascii=False, indent=0).splitlines()
        d = [l for l in difflib.unified_diff(h, w, "live", "built", n=0, lineterm="") if l[:1] in "+-" and l[:3] not in ("+++", "---")]
        print(f"  toc differs: {len(d)} changed line(s); first ones:")
        for l in d[:12]:
            print("    " + l[:160])
