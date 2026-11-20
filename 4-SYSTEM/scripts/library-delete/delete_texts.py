#!/usr/bin/env python3
"""delete_texts.py — permanently delete library texts listed in a TSV, one by one.

The API deletes a text only when it has no editions and no incoming text
relationships (a commentary's `commentary_of` points at its root). So, per text:

  commentary:  DELETE alignments (its edition -> root edition)
               DELETE every edition of the text
               DELETE the text            -> GET must then give 404
  root:        (only after every commentary that points at it is gone)
               DELETE every edition, DELETE the text -> GET 404

Commentaries run first, then roots. Before each text, a GET checks that the
live title equals the list's title, so a wrong id never deletes the wrong text.
Every call is appended to <log>.jsonl; a text already gone (404) is skipped,
so an interrupted run resumes.

List (TSV, no header): label, text_id, edition_id, title, [root_edition_id]
A row with a root_edition_id is a commentary.

Usage: python3 delete_texts.py <list.tsv> <log.jsonl>            # dry run: prints the plan, sends nothing
       python3 delete_texts.py <list.tsv> <log.jsonl> --execute  # needs WEBUDDHIST_API_KEY; human confirmation first
Env: WEBUDDHIST_API_KEY, WEBUDDHIST_API_BASE (default https://library.webuddhist.com), WEBUDDHIST_APP (optional)
"""
import json, os, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone

lst, logp = sys.argv[1], sys.argv[2]
EXECUTE = "--execute" in sys.argv
BASE = os.environ.get("WEBUDDHIST_API_BASE", "https://library.webuddhist.com").rstrip("/")
rows = []
for ln in open(lst, encoding="utf-8"):
    c = ln.rstrip("\n").split("\t")
    if len(c) >= 4 and c[1]:
        rows.append({"label": c[0], "text_id": c[1], "edition_id": c[2], "title": c[3], "root_edition_id": (c[4] if len(c) > 4 else "") or None})
comms = [r for r in rows if r["root_edition_id"]]
roots = [r for r in rows if not r["root_edition_id"]]
order = comms + roots

print(f"host: {BASE}\n{len(comms)} commentaries, then {len(roots)} roots = {len(order)} texts")
if not EXECUTE:
    for r in order:
        steps = (["DELETE alignments " + r["edition_id"] + " -> " + r["root_edition_id"]] if r["root_edition_id"] else []) + ["DELETE editions", "DELETE text " + r["text_id"]]
        print(f"  {r['label']:24s} {r['title']}: " + "; ".join(steps))
    sys.exit("dry run: nothing sent. Re-run with --execute after the human confirms this list.")

KEY = os.environ.get("WEBUDDHIST_API_KEY") or sys.exit("STOP: WEBUDDHIST_API_KEY not set")
H = {"X-API-Key": KEY, "Content-Type": "application/json"}
if os.environ.get("WEBUDDHIST_APP"): H["X-Application"] = os.environ["WEBUDDHIST_APP"]


def call(method, path):
    req = urllib.request.Request(BASE + path, method=method, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read(); return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:500]


def log(**kw):
    kw["at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(logp, "a", encoding="utf-8") as f: f.write(json.dumps(kw, ensure_ascii=False) + "\n")


def title_of(t):
    tt = t.get("title") if isinstance(t, dict) else None
    return (tt.get("pi") or next(iter(tt.values()), None)) if isinstance(tt, dict) else tt


done = failed = skipped = 0
for r in order:
    lab, tid = r["label"], r["text_id"]
    st, t = call("GET", f"/v2/texts/{tid}")
    if st == 404:
        print(f"  {lab}: already gone"); log(label=lab, text_id=tid, step="skip", status=404); skipped += 1; continue
    if st != 200 or title_of(t) != r["title"]:
        print(f"  STOP {lab}: GET {st}, live title {title_of(t) if st == 200 else t!r} != list title {r['title']!r}")
        log(label=lab, text_id=tid, step="title-check", status=st, live=title_of(t) if st == 200 else None); sys.exit(1)
    if r["root_edition_id"]:
        st, b = call("DELETE", f"/v2/editions/{r['edition_id']}/alignments/{r['root_edition_id']}")
        log(label=lab, text_id=tid, step="delete-alignment", status=st, body=b if st >= 300 else None)
        if st not in (200, 204, 404): print(f"  STOP {lab}: alignment delete {st} {b}"); sys.exit(1)
    st, eds = call("GET", f"/v2/texts/{tid}/editions")
    eds = eds if isinstance(eds, list) else (eds.get("items") or eds.get("data") or []) if isinstance(eds, dict) else []
    ids = [e.get("id") for e in eds if isinstance(e, dict) and e.get("id")] or ([r["edition_id"]] if r["edition_id"] else [])
    for eid in ids:
        st, b = call("DELETE", f"/v2/editions/{eid}")
        log(label=lab, text_id=tid, step="delete-edition", edition_id=eid, status=st, body=b if st >= 300 else None)
        if st not in (200, 204, 404): print(f"  STOP {lab}: edition {eid} delete {st} {b}"); sys.exit(1)
    st, b = call("DELETE", f"/v2/texts/{tid}")
    log(label=lab, text_id=tid, step="delete-text", status=st, body=b if st >= 300 else None)
    if st not in (200, 204):
        print(f"  STOP {lab}: text delete {st} {b}"); sys.exit(1)
    time.sleep(0.3)
    st, _ = call("GET", f"/v2/texts/{tid}")
    log(label=lab, text_id=tid, step="verify-gone", status=st)
    if st != 404: print(f"  STOP {lab}: still there after delete (GET {st})"); sys.exit(1)
    done += 1; print(f"  deleted {lab:24s} {r['title']} (editions {len(ids)}), GET now 404")
print(f"done: {done} deleted, {skipped} already gone, {failed} failed")
