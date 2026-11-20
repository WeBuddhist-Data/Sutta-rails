"""Fetch one tipitaka.app book whose parent key is not its key minus the last
segment (tika2-dn-1 sits under tika-dn, not tika2-dn, which fetch_site.py
assumes and the site answers 404). Same output files as fetch_site.py --links.
Usage: python3 -I fetch_tika2.py <out-dir> <key> <parent-key>"""
import json, sys, time, urllib.request
from pathlib import Path
V = "7d17987e5be3e268"; out, key, parent = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
get = lambda p: json.load(urllib.request.urlopen(urllib.request.Request(
    f"https://tipitaka.app/api/{p}&v={V}", headers={"User-Agent": "rails-toc-check"}), timeout=60))
toc = []
def walk(k):
    for c in get(f"children?key={k}"):
        toc.append({x: c.get(x) for x in ("key", "depth", "rend", "start", "end", "title")})
        if c.get("children"): walk(c["key"])
walk(key)
first = get(f"text?key={key}&from=0&to=1"); lo, hi = 0, first["book"]["paraCount"]
for n in get(f"children?key={parent}"):
    if n["key"] == key and n.get("end") is not None: lo, hi = n.get("start") or 0, n["end"]
paras, links = [], []
for s in range(lo, hi, 150):
    paras += [p for p in get(f"text?key={key}&from={s}&to={min(s + 150, hi)}")["paras"] if lo <= p["i"] < hi]
    links += get(f"links?key={key}&from={s}&to={min(s + 150, hi)}"); time.sleep(0.2)
(out / f"{key}.toc.json").write_text(json.dumps(toc, ensure_ascii=False, indent=0), encoding="utf-8")
(out / f"{key}.text.json").write_text(json.dumps({"book": first["book"], "paras": paras}, ensure_ascii=False, indent=0), encoding="utf-8")
(out / f"{key}.links.json").write_text(json.dumps(links, ensure_ascii=False, indent=0), encoding="utf-8")
print(key, "toc nodes", len(toc), "paras", len(paras), f"[{lo}, {hi})")
