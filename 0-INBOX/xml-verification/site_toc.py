"""Compare a vault file's heading tree with tipitaka.app's contents tree.

usage: python site_toc.py <vault.md> <site.toc.json> <key-prefix>
  e.g. python site_toc.py 1-SOURCES/Text/pi-dn-1.md 0-INBOX/tipitaka-app/dn-1.toc.json dn-

A site key `dn-1-1-2` is the vault heading `^1-1-2-0` (key minus prefix, plus -0).
Checks: every site node exists in the vault and vice versa, same title (heading
numbers stripped), same relative depth, and same parent.
"""
import re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
md, js, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
id_prefix = sys.argv[4] if len(sys.argv) > 4 else ""   # e.g. "1-" when the site key has no book number (kn-khp-1 -> ^1-1-0)

text = open(md, encoding="utf-8").read().replace("\r\n", "\n")
vh = {}
order = []
for m in re.finditer(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$", text, flags=re.M):
    t = re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2))
    vh[m.group(3)] = (len(m.group(1)), t)
    order.append(m.group(3))

site = json.load(open(js, encoding="utf-8"))
strip = lambda t: re.sub(r"^\s*[\d\-–]+\.\s*", "", re.sub(r"^\s*\(\d+\)\s*(?=\d+\.)", "", t)).replace("‘‘", '"').replace("’’", '"').strip()
problems, offs = [], {}
sk = set()
for n in site:
    vid = id_prefix + n["key"][len(prefix):] + "-0"
    sk.add(vid)
    if vid not in vh:
        problems.append(f"site node {n['key']} `{n['title']}` → ^{vid} missing in vault"); continue
    lvl, t = vh[vid]
    if strip(n["title"]) != strip(t):
        problems.append(f"^{vid}: site `{n['title']}` vs vault `{t}`")
    offs.setdefault(n["depth"] - lvl, []).append(vid)
extra = [v for v in order if v.endswith("-0") and v not in sk and v != "0"]
main = max(offs, key=lambda k: len(offs[k])) if offs else 0
for o, ids in offs.items():
    if o != main:
        for v in ids:
            problems.append(f"^{v} `{vh[v][1]}`: depth differs from the site by {o - main}")
print(f"site nodes: {len(site)}; vault headings: {len(order)}; vault headings not on site: {len(extra)} {extra[:12]}")
print(f"problems: {len(problems)}")
for p in problems[:80]:
    print("  - " + p)
