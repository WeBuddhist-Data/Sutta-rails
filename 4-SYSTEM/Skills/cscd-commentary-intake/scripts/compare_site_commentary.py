#!/usr/bin/env python3
"""
compare_site_commentary.py — step 8 of cscd-commentary-intake: check a
commentary file against tipitaka.app (fetched with cscd-root-text-intake's
fetch_site.py --links).

Text   every non-link line of the file (headings included) matches one site
       paragraph, in order, after normalising the site's display markup
       (|X0.0000| page markers, **bold**, {notes} -> [notes], ‘‘ ’’ -> ")
       and dropping printed leading numbers and the h1's "(<layer>)" label.
Tree   the file's ### and deeper headings vs the site's contents nodes:
       same titles in the same order; nesting reported.
Links  aṭṭhakathā (kind mula-atta, src paranum): for each site link from
       commentary paragraph i to root paragraph t, the file's line for i must
       be in the scope of a link to the root block holding t.
       ṭīkā (kind atta-tika, src paranum): for each site pair ṭīkā i <->
       aṭṭhakathā t, the ṭīkā line's links must equal the aṭṭhakathā line's.
       A link's scope runs from the paragraph after it to the next link group
       or heading. The site's "gloss" links are its own word matches and are
       not a reference.
Bold   the file's **…** spans equal the site's, in order (bold_check.py in
       cscd-root-text-intake), compared with edge spaces/punctuation trimmed. Text is compared with the ** removed on both sides.
Usage:
  python3 -I compare_site_commentary.py <file.md> <site-dir> <key> <root-key> [<atthakatha.md> <atta-key>]
"""
import difflib, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "cscd-root-text-intake" / "scripts"))
import bold_check  # noqa: E402

md, sdir, key, root_key = sys.argv[1:5]
atta_md, atta_key = (sys.argv[5], sys.argv[6]) if len(sys.argv) > 6 else (None, None)
S = Path(sdir)
LEAD = re.compile(r"^\s*(\d+(?:-\d+)*|\(\d+\))\s*\.\s*")
TRANS = re.compile(r"^!\[\[[^#\]]+#\^([\w-]+)\]\]$")


def site_norm(s):
    s = re.sub(r"\|[A-Z]\d+\.\d+\|", " ", s)
    s = s.replace("‘‘", '"').replace("’’", '"').replace("**", "")
    s = s.replace("{", "[").replace("}", "]")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\[\s+", "[", re.sub(r"\s+\]", "]", s))
    s = re.sub(r"\s+([,.;:?!])", r"\1", s)
    return LEAD.sub("", s)


def md_items(path):
    body = Path(path).read_text(encoding="utf-8").split("\n---\n", 1)[1]
    items, group, scope, blockstart = [], [], [], True
    for ln in body.split("\n"):
        if not ln.strip():
            blockstart = True; continue
        m = TRANS.match(ln.strip())
        if m:
            if blockstart:
                group = []
            group.append(m.group(1)); scope = group; blockstart = False
            continue
        h = re.match(r"^(#+) (.*?) \^[\w-]+$", ln)
        if h:
            title = h.group(2)
            if len(h.group(1)) == 1:
                title = re.sub(r"\s*\([^)]*\)\s*$", "", title)
            items.append({"text": title, "head": True, "level": len(h.group(1)), "scope": []})
            scope, group = [], []
        else:
            items.append({"text": bold_check.strip_bold(re.sub(r"\s\^[\w-]+$", "", ln)), "head": False, "scope": list(scope)})
        blockstart = False
    return items


def align(items, paras):
    a = [re.sub(r"\s+", "", site_norm(p["t"])) for p in paras]
    b = [re.sub(r"\s+", "", LEAD.sub("", it["text"])) for it in items]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    pairs, diffs = {}, []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                pairs[i1 + k] = j1 + k
        else:
            diffs.append(f"text {op}: site {[paras[i]['t'][:60] for i in range(i1, i2)][:2]} | md {[items[j]['text'][:60] for j in range(j1, j2)][:2]}")
    return pairs, diffs


problems, notes = [], []
items = md_items(md)
paras = json.loads((S / f"{key}.text.json").read_text(encoding="utf-8"))["paras"]
pairs, diffs = align(items, paras)
problems += diffs
md_lines = Path(md).read_text(encoding="utf-8").split("\n---\n", 1)[1].split("\n")
site_merges = []
problems += bold_check.compare(bold_check.site_spans(paras), bold_check.md_spans(md_lines)[0], "site", site_merges)
if site_merges:
    print(f"   note: {len(site_merges)} bold group(s) the site joins into one span (XML and md keep them apart), e.g. "
          f"site {site_merges[0][0]} vs md {site_merges[0][1]}")

# tree
toc = json.loads((S / f"{key}.toc.json").read_text(encoding="utf-8"))
site_h = [(LEAD.sub("", n["title"]).strip(), n["depth"]) for n in toc]
md_h = [(LEAD.sub("", it["text"]).strip(), it["level"]) for it in items if it["head"] and it["level"] >= 3]
if [t for t, _ in site_h] != [t for t, _ in md_h]:
    sm = difflib.SequenceMatcher(None, [t for t, _ in site_h], [t for t, _ in md_h], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            problems.append(f"tree {op}: site {[t for t, _ in site_h[i1:i2]][:3]} | md {[t for t, _ in md_h[j1:j2]][:3]}")
offsets = {}
sm = difflib.SequenceMatcher(None, [t for t, _ in site_h], [t for t, _ in md_h], autojunk=False)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        s, m = site_h[blk.a + k], md_h[blk.b + k]
        offsets.setdefault(s[1] - m[1], []).append(m[0])
main_off = max(offsets, key=lambda k: len(offsets[k])) if offsets else 0
for off, titles in offsets.items():
    if off != main_off:
        notes.append(f"nesting differs from the site on {len(titles)} heading(s), e.g. {titles[:3]}")

# links
links = [l for l in json.loads((S / f"{key}.links.json").read_text(encoding="utf-8")) if l["src"] == "paranum"]
lk_ok = lk_bad = 0
if atta_md is None:
    root_paras = json.loads((S / f"{root_key}.text.json").read_text(encoding="utf-8"))["paras"]
    book = re.search(r"-(\d+)$", root_key).group(1)
    for l in links:
        if l["kind"] != "mula-atta":
            continue
        n = root_paras[l["t"]].get("n")
        j = pairs.get(l["i"])
        if j is not None and n and f"{book}-{n}" in items[j]["scope"]:
            lk_ok += 1
        else:
            lk_bad += 1
            problems.append(f"site link commentary para {l['i']} -> root {n}: md scope {items[j]['scope'][:4] if j is not None else None}")
else:
    a_items = md_items(atta_md)
    a_paras = json.loads((S / f"{atta_key}.text.json").read_text(encoding="utf-8"))["paras"]
    a_pairs, _ = align(a_items, a_paras)
    for l in links:
        if l["kind"] != "atta-tika" or not l.get("fwd"):
            continue
        j, ja = pairs.get(l["i"]), a_pairs.get(l["t"])
        if j is not None and ja is not None and items[j]["scope"] == a_items[ja]["scope"]:
            lk_ok += 1
            continue
        lk_bad += 1
        ts = items[j]["scope"] if j is not None else None
        as_ = a_items[ja]["scope"] if ja is not None else None
        if ts and as_ and ts[0] == as_[0] and (set(ts) <= set(as_) or set(as_) <= set(ts)):
            cat = "same root paragraph, printed as a single number on one side and a range on the other"
        elif not ts or not as_:
            cat = "one side has no link (an unresolved citation)"
        else:
            cat = "different root paragraphs"
            problems.append(f"ṭīkā para {l['i']} vs aṭṭhakathā para {l['t']}: {ts[:3]} vs {as_[:3]}")
        notes.append(f"[{cat}] ṭīkā para {l['i']} vs aṭṭhakathā para {l['t']}: {(ts or [])[:3]} vs {(as_ or [])[:3]}")

print(f"== {Path(md).name} vs {key}: site paras {len(paras)}, md lines {len(items)}, matched {len(pairs)}; "
      f"tree site {len(site_h)} / md {len(md_h)} (site depth = md level + {main_off}); "
      f"site paranum links agreeing {lk_ok}, not agreeing {lk_bad}")
cats = {}
for n_ in notes:
    c = n_[1:n_.index("]")] if n_.startswith("[") else n_
    cats[c] = cats.get(c, 0) + 1
for c, k in cats.items():
    print(f"   note: {k} × {c}")
print("   PASS" if not problems else "   PROBLEMS (%d):\n   - " % len(problems) + "\n   - ".join(problems[:15]))
sys.exit(1 if problems else 0)
