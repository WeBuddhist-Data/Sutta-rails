"""Meaning check of commentary->root links: for each link group, does the
commentary text in its scope (until the next link group or heading) share more
words with the linked root block(s) than with a nearby block (+-window)?
Prints the groups where another block scores clearly higher. A heuristic: in
prose a numbered commentary paragraph often runs on into the following root
paragraphs, so a flag there is usually a false positive; read each one.
Usage: python3 -I content_links.py <comm.md> <root.md> [window]"""
import re, sys
from collections import Counter

comm, rootp = sys.argv[1], sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 3
WORD = re.compile(r"[^\W\d_]+", re.U)
STOP = set("ca vā pi hi tu pana ti iti na ettha tattha evaṃ ayaṃ idaṃ taṃ so sā te ye yo yaṃ kho atha ādi".split())


def toks(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)
    out = []
    for w in WORD.findall(s.lower()):
        w = re.sub(r"(nti|ti)$", "", w) if len(w) > 5 else w
        if len(w) >= 4 and w not in STOP: out.append(w[:7])
    return out


root = open(rootp, encoding="utf-8").read().split("\n---\n", 1)[1]
order, rtext = [], {}
for b in re.split(r"\n\s*\n", root):
    m = re.search(r"\^([\w-]+)\s*$", b.strip())
    if m and not b.lstrip().startswith("#"):
        order.append(m.group(1)); rtext[m.group(1)] = Counter(toks(b))
pos = {k: i for i, k in enumerate(order)}

lines = open(comm, encoding="utf-8").read().split("\n---\n", 1)[1].split("\n")
groups, cur, scope = [], None, []
for ln in lines + ["#"]:
    m = re.match(r"!\[\[[^#]+#\^([\w-]+)\]\]", ln)
    if m:
        if cur is not None and scope:
            groups.append((cur, " ".join(scope))); cur, scope = None, []
        if cur is None: cur = []
        cur.append(m.group(1)); continue
    if ln.startswith("#"):
        if cur is not None: groups.append((cur, " ".join(scope)))
        cur, scope = None, []; continue
    if cur is not None: scope.append(re.sub(r"\s\^[\w-]+\s*$", "", ln))


def score(c, k):
    r = rtext[k]
    return sum(min(c[w], 1) for w in r) / max(1, len(r)) if r else 0


flag = 0
for links, text in groups:
    links = [k for k in links if k in pos]
    if not links: continue
    c = Counter(toks(text))
    lo, hi = min(pos[k] for k in links) - W, max(pos[k] for k in links) + W
    sc = {k: score(c, k) for k in order[max(0, lo):hi + 1]}
    best = max(sc, key=sc.get); lk = max(sc[k] for k in links)
    if best not in links and sc[best] >= 0.5 and sc[best] > lk + 0.25:
        flag += 1
        print(f"  linked {links} ({lk:.2f})  best ^{best} ({sc[best]:.2f})  | {text.strip()[:70]!r}")
print(f"{comm.split('/')[-1]}: {len(groups)} link groups, {flag} flagged")
