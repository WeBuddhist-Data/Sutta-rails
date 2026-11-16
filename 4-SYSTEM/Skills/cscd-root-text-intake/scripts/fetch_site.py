"""fetch_site.py — step 9 of cscd-root-text-intake (also used by cscd-commentary-intake).
Fetch a tipitaka.app book's contents tree and full text, and with --links its
cross-layer links (commentary <-> root).
Writes <out>/<key>.toc.json, <key>.text.json [and <key>.links.json].
Usage: python3 -I fetch_site.py <out-dir> <key> [<key> ...] [--links]"""
import json, sys, time, urllib.error, urllib.request
from pathlib import Path

V = "7d17987e5be3e268"


def get(path, tries=5):
    """GET with retries: tipitaka.app occasionally answers a request with HTTP
    500 or drops it; wait and try again (2, 4, 8, 16 s) before giving up."""
    req = urllib.request.Request(f"https://tipitaka.app/api/{path}&v={V}",
                                 headers={"User-Agent": "rails-toc-check"})
    for k in range(tries):
        try:
            return json.load(urllib.request.urlopen(req, timeout=60))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if k == tries - 1 or (isinstance(e, urllib.error.HTTPError) and e.code < 500):
                raise
            time.sleep(2 ** (k + 1))


def walk(key, acc):
    for k in get(f"children?key={key}"):
        acc.append({x: k.get(x) for x in ("key", "depth", "rend", "start", "end", "title")})
        if k.get("children"):
            walk(k["key"], acc)
        time.sleep(0.1)


out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
for key in [a for a in sys.argv[2:] if not a.startswith("--")]:
    toc = []; walk(key, toc)
    # A book can be a slice of its volume file (CSCD AN commentaries: atta-an-3 is
    # paragraphs 321–992 of s0402a.att); the parent's listing gives start/end.
    # Paragraph indices `i` stay those of the volume.
    first = get(f"text?key={key}&from=0&to=1")
    lo, hi = 0, first["book"]["paraCount"]
    parent = key.rsplit("-", 1)[0]
    for node in (get(f"children?key={parent}") if parent != key else []):
        if node.get("key") == key and node.get("end") is not None:
            lo, hi = node.get("start") or 0, node["end"]
    paras = []
    for start in range(lo, hi, 150):
        paras += [p for p in get(f"text?key={key}&from={start}&to={min(start + 150, hi)}")["paras"] if lo <= p["i"] < hi]
        time.sleep(0.2)
    n = len(paras)
    links = []
    if "--links" in sys.argv:
        for start in range(lo, hi, 150):
            links += get(f"links?key={key}&from={start}&to={min(start + 150, hi)}")
            time.sleep(0.2)
        (out / f"{key}.links.json").write_text(json.dumps(links, ensure_ascii=False, indent=0), encoding="utf-8")
    (out / f"{key}.toc.json").write_text(json.dumps(toc, ensure_ascii=False, indent=0), encoding="utf-8")
    (out / f"{key}.text.json").write_text(json.dumps({"book": first["book"], "paras": paras}, ensure_ascii=False, indent=0), encoding="utf-8")
    print(key, "toc nodes", len(toc), "paras", len(paras), f"[{lo}, {hi})")
