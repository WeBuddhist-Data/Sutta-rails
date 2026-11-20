#!/usr/bin/env python3
"""replace_segmentation.py — re-apply a changed parser rule to a commentary that
is already live, keeping its text, edition and contents ids (as the Vinaya vault
did on 2026-11-12: DELETE + POST /v2/editions/{id}/segmentation, then PUT the
alignment).

For one commentary file that carries text_id / edition_id / toc_id:
  1. parse the file with parser-commentary (edition payload + alignment);
  2. GET the live segments, alignment pairs and contents tree, and save them
     as a backup (<backup-dir>/<stem>.live.json);
  3. STOP unless the new segmentation has exactly the live references and
     spans, in the same order: only segment types may change, so the text and
     the contents tree stay valid;
  4. report what changes: segment types (live -> new) and alignment pairs
     (removed / added);
  with --execute (after human confirmation):
  5. DELETE the segmentation (this also drops the alignment hanging off it),
     POST the new one, PUT the new alignment;
  6. read back: references, spans and types == parser; pairs == parser; the
     contents tree still present (re-POSTed from the parser output if the
     backend dropped it); a receipt goes into the upload ledger.

Usage: python3 replace_segmentation.py <commentary.md> <backup-dir> [--execute]
Env: WEBUDDHIST_API_KEY, WEBUDDHIST_API_BASE, WEBUDDHIST_APP (optional)
"""
import json, os, subprocess, sys, urllib.error, urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = Path(sys.argv[1]); bdir = Path(sys.argv[2]); EXECUTE = "--execute" in sys.argv
BASE = os.environ.get("WEBUDDHIST_API_BASE", "https://library.webuddhist.com").rstrip("/")
KEY = os.environ.get("WEBUDDHIST_API_KEY") or sys.exit("STOP: WEBUDDHIST_API_KEY not set")
H = {"X-API-Key": KEY, "Content-Type": "application/json"}
if os.environ.get("WEBUDDHIST_APP"): H["X-Application"] = os.environ["WEBUDDHIST_APP"]
LEDGER = HERE / "upload_ledger.json"


def call(method, path, body=None, timeout=900):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(); return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:800]


def paged(path):
    out, off = [], 0
    while True:
        st, d = call("GET", f"{path}{'&' if '?' in path else '?'}limit=500&offset={off}", timeout=300)
        if st != 200: sys.exit(f"STOP: GET {path} -> {st} {d}")
        items = d.get("items") if isinstance(d, dict) else d
        items = items or []
        out += items
        if not (isinstance(d, dict) and d.get("has_more")) or not items: return out
        off += len(items)


def fm_of(p):
    t = p.read_text(encoding="utf-8").split("\n---\n", 1)[0]
    return {l.split(":", 1)[0]: l.split(":", 1)[1].strip().strip('"') for l in t.split("\n")[1:] if ":" in l and not l.startswith(" ")}


fm = fm_of(src)
eid, tid, toc_id = fm.get("edition_id"), fm.get("text_id"), fm.get("toc_id")
root = fm_of(Path(fm["root_text"]))
reid = root.get("edition_id")
if not (eid and tid and reid): sys.exit("STOP: file or root has no library ids")

# 1. parse (lint output must be current: the upload script's dry run writes it)
stem = src.stem
r = subprocess.run([sys.executable, str(HERE / "upload_commentary.py"), str(src), "--no-live"], capture_output=True, text=True)
if r.returncode: sys.exit(f"STOP: dry run failed:\n{r.stdout[-1500:]}{r.stderr[-1500:]}")
out = HERE / "parser-commentary" / "output" / stem
edition = json.loads((out / f"{stem}.edition.json").read_text(encoding="utf-8"))
align = json.loads((out / f"{stem}.alignment.json").read_text(encoding="utf-8"))
toc_payload = json.loads((out / f"{stem}.toc.json").read_text(encoding="utf-8"))
new_segs = edition["segmentation"]["segments"]
new_pairs = [(a["source_segment_reference"], a["target_segment_reference"]) for a in align["alignments"]]

# 2. live state + backup
live = paged(f"/v2/editions/{eid}/segmentation/segments")
live_pairs = [(i["source_segment"]["reference"], i["target_segment"]["reference"]) for i in paged(f"/v2/editions/{eid}/alignments/{reid}")]
st, live_toc = call("GET", f"/v2/editions/{eid}/table-of-contents", timeout=300)
bdir.mkdir(parents=True, exist_ok=True)
(bdir / f"{stem}.live.json").write_text(json.dumps({"edition_id": eid, "segments": live, "pairs": live_pairs, "toc": live_toc}, ensure_ascii=False), encoding="utf-8")


def spans(s):
    ls = s.get("lines") or s.get("spans") or []
    return [(x["start"], x["end"]) for x in ls]


# 3. same references and spans, in order
lv = [(s["reference"], spans(s)) for s in live]
nw = [(s["reference"], spans(s)) for s in new_segs]
if lv != nw:
    i = next((k for k in range(min(len(lv), len(nw))) if lv[k] != nw[k]), min(len(lv), len(nw)))
    sys.exit(f"STOP {stem}: references/spans differ from live at #{i}: live {lv[i] if i < len(lv) else None} | new {nw[i] if i < len(nw) else None}")

# 4. report
tchg = Counter((a.get("type"), b.get("type")) for a, b in zip(live, new_segs) if a.get("type") != b.get("type"))
rm, add = set(live_pairs) - set(new_pairs), set(new_pairs) - set(live_pairs)
print(f"{stem}: {len(new_segs)} segments, refs+spans identical to live; type changes {dict(tchg) or 'none'}; "
      f"pairs live {len(live_pairs)} -> new {len(new_pairs)} (removed {len(rm)}, added {len(add)})")
if not EXECUTE:
    print("  dry run: nothing sent. Backup written:", bdir / f"{stem}.live.json"); sys.exit(0)
if not tchg and not rm and not add:
    print("  nothing to change"); sys.exit(0)

# 5. replace
receipt = {"step": "resegment", "ts": datetime.now().isoformat(timespec="seconds"), "backup": str(bdir / f"{stem}.live.json")}
if tchg:
    st, b = call("DELETE", f"/v2/editions/{eid}/segmentation"); receipt["delete_segmentation"] = st
    if st not in (200, 204): sys.exit(f"STOP {stem}: DELETE segmentation {st} {b}")
    st, b = call("POST", f"/v2/editions/{eid}/segmentation", edition["segmentation"]); receipt["post_segmentation"] = st
    if st not in (200, 201): sys.exit(f"STOP {stem}: POST segmentation {st} {b} — live edition has NO segmentation now; restore from the backup")
st, b = call("PUT", f"/v2/editions/{eid}/alignments/{reid}", {"alignments": align["alignments"]}); receipt["put_alignment"] = st
if st not in (200, 201, 204): sys.exit(f"STOP {stem}: PUT alignment {st} {b}")

# 6. read back
live2 = paged(f"/v2/editions/{eid}/segmentation/segments")
ok_segs = [(s["reference"], spans(s), s.get("type")) for s in live2] == [(s["reference"], spans(s), s.get("type")) for s in new_segs]
pairs2 = [(i["source_segment"]["reference"], i["target_segment"]["reference"]) for i in paged(f"/v2/editions/{eid}/alignments/{reid}")]
ok_pairs = set(pairs2) == set(new_pairs) and len(pairs2) == len(new_pairs)
st, toc2 = call("GET", f"/v2/editions/{eid}/table-of-contents", timeout=300)
has_toc = st == 200 and bool(toc2)
if not has_toc:
    st, b = call("POST", f"/v2/editions/{eid}/table-of-contents", toc_payload); receipt["toc_reposted"] = st
    if st in (200, 201) and isinstance(b, dict) and b.get("id"): receipt["toc_id"] = b["id"]
    st, toc2 = call("GET", f"/v2/editions/{eid}/table-of-contents", timeout=300); has_toc = st == 200 and bool(toc2)
receipt.update(segments=len(live2), types=dict(Counter(s.get("type") for s in live2)), pairs=len(pairs2), readback_segments=ok_segs, readback_pairs=ok_pairs, toc_present=has_toc)
L = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {}
L.setdefault(stem, {}).setdefault("log", []).append(receipt)
LEDGER.write_text(json.dumps(L, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"  replaced: segments {len(live2)} {dict(Counter(s.get('type') for s in live2))}, read back {'OK' if ok_segs else 'MISMATCH'}; "
      f"pairs {len(pairs2)} read back {'OK' if ok_pairs else 'MISMATCH'}; toc {'present' if has_toc else 'MISSING'}"
      + (f" (re-posted, new toc_id {receipt.get('toc_id')})" if "toc_reposted" in receipt else ""))
if not (ok_segs and ok_pairs and has_toc): sys.exit(1)
