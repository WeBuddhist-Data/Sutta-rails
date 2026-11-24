"""Probe (Netti-ṭīkā): tipitaka.app pairs each numbered ṭīkā paragraph with an aṭṭhakathā paragraph
(paranum links, kind atta-tika). For each pair, the root blocks the ṭīkā draft links should be the
ones the aṭṭhakathā draft links for its paragraph. A draft's lines (all but the frontmatter and the
transclusion lines) are 1:1 with the site's paragraphs (compare_site_commentary.py checked that);
a paragraph's links are the transclusion lines just before it."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
site = lambda k: json.load(open(f"0-INBOX/tipitaka-app/{k}.text.json", encoding="utf-8"))["paras"]
TP, AP = site("tika-kn-nett"), site("atta-kn-nett")
L = [l for l in json.load(open("0-INBOX/tipitaka-app/tika-kn-nett.links.json", encoding="utf-8")) if l["src"] == "paranum"]


def paras(path):
    body = Path(path).read_text(encoding="utf-8").split("\n---\n", 1)[1]
    out, pend = [], []
    for ln in body.split("\n"):
        if not ln.strip():
            continue
        ids = re.findall(r"^!\[\[[^\]#]+#\^([\w-]+)\]\]$", ln.strip())
        if ids:
            pend += ids; continue
        out.append((ln, pend)); pend = []
    return out


TD, AD = paras(sys.argv[1]), paras(sys.argv[2])
print(f"tika lines {len(TD)} / site {len(TP)}; atta lines {len(AD)} / site {len(AP)}")
assert len(TD) == len(TP) and len(AD) == len(AP)
agree, ranged, rows = 0, 0, []
for l in L:
    ti, ai = TD[l["i"]][1], AD[l["t"]][1]
    if ti and ti == ai:
        agree += 1
    # the ṭīkā cites a range ("73-4.") opening on the block its aṭṭhakathā paragraph cites alone
    elif ti and ai and ti[0] == ai[0] and set(ai) <= set(ti) and re.match(r"\d+-\d+\.", TD[l["i"]][0]):
        ranged += 1
        print(f"   range: tika {TD[l['i']][0][:40]!r} -> {ti} | atta -> {ai}")
    else:
        rows.append(f"tika {l['i']} {TD[l['i']][0][:60]!r} -> {ti} | atta {l['t']} {AD[l['t']][0][:60]!r} -> {ai}")
print("\n".join(rows))
print(f"aṭṭhakathā check: of {len(L)} site paranum links, {agree} agree, {ranged} a range opening on the same block, {len(rows)} differ")
sys.exit(1 if rows else 0)
