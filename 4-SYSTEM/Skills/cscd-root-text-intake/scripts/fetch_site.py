"""fetch_site.py — step 9 of cscd-root-text-intake.
Fetch a tipitaka.app book's contents tree and full text (same API calls as
Vinaya-rails 0-INBOX/tipitaka-app/fetch_toc.py + fetch_text.py, links omitted).
Writes <out>/<key>.toc.json and <out>/<key>.text.json.
Usage: python3 -I fetch_site.py <out-dir> <key> [<key> ...]"""
import json, sys, time, urllib.request
from pathlib import Path

V = "7d17987e5be3e268"


def get(path):
    req = urllib.request.Request(f"https://tipitaka.app/api/{path}&v={V}",
                                 headers={"User-Agent": "rails-toc-check"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def walk(key, acc):
    for k in get(f"children?key={key}"):
        acc.append({x: k.get(x) for x in ("key", "depth", "rend", "start", "end", "title")})
        if k.get("children"):
            walk(k["key"], acc)
        time.sleep(0.1)


out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
for key in sys.argv[2:]:
    toc = []; walk(key, toc)
    first = get(f"text?key={key}&from=0&to=150")
    n = first["book"]["paraCount"]
    paras = list(first["paras"])
    for start in range(150, n, 150):
        paras += get(f"text?key={key}&from={start}&to={start + 150}")["paras"]
        time.sleep(0.2)
    (out / f"{key}.toc.json").write_text(json.dumps(toc, ensure_ascii=False, indent=0), encoding="utf-8")
    (out / f"{key}.text.json").write_text(json.dumps({"book": first["book"], "paras": paras}, ensure_ascii=False, indent=0), encoding="utf-8")
    print(key, "toc nodes", len(toc), "paras", len(paras), "of", n)
