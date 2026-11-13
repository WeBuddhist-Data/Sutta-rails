"""compare_site.py — step 9 of cscd-root-text-intake.
Compare a converted root-text .md with tipitaka.app (text + contents tree),
the way Vinaya-rails' compare_md_site.py / compare_toc.py do.

Text: every md line (heading or text) is matched in order to one site paragraph,
after normalising site display markup (page markers |X0.0000|, **bold**,
{notes} -> [notes], ‘‘ ’’ -> ") and dropping printed leading numbers on both sides.
Paragraph numbers: every site paragraph that starts with a printed N. must sit
in the md block whose ID is ^<book>-N.
Tree: md '###'+ headings vs site nodes: same titles (leading numbers ignored),
same order, md level == site depth.
Usage: python3 -I compare_site.py <book> <file.md> <key.text.json> <key.toc.json>"""
import difflib, json, re, sys
from pathlib import Path

book, md, textp, tocp = sys.argv[1:5]
LEAD = re.compile(r"^\s*(\d+(?:-\d+)*|\(\d+\))\s*\.\s*")


def site_norm(s):
    s = re.sub(r"\|[A-Z]\d+\.\d+\|", " ", s)
    s = s.replace("‘‘", '"').replace("’’", '"').replace("**", "")
    s = s.replace("{", "[").replace("}", "]")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\[\s+", "[", re.sub(r"\s+\]", "]", s))
    s = re.sub(r"\s+([,.;:?!])", r"\1", s)   # page marker before punctuation
    return s


lines = Path(md).read_text(encoding="utf-8").split("\n---\n", 1)[1].split("\n")
items, cur = [], []
for ln in lines:
    if not ln.strip():
        continue
    h = re.match(r"^(#+) (.*?) \^[\w-]+$", ln)
    bid = re.search(r"\s\^([\w-]+)$", ln)
    txt = h.group(2) if h else re.sub(r"\s\^[\w-]+$", "", ln)
    items.append({"text": txt, "head": bool(h), "level": len(h.group(1)) if h else None,
                  "id": bid.group(1) if bid else None})
blk = None
for it in reversed(items):          # block ID of each text line = ID at end of its block
    if it["head"]:
        blk = None; continue
    if it["id"]:
        blk = it["id"]
    it["block"] = blk

paras = json.loads(Path(textp).read_text(encoding="utf-8"))["paras"]
problems = []
a = [LEAD.sub("", site_norm(p["t"])) for p in paras]
b = [LEAD.sub("", it["text"]) for it in items]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
pairs = {}
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal":
        for k in range(i2 - i1):
            pairs[i1 + k] = j1 + k
    else:
        problems.append(f"text {op}: site {[p[:70] for p in a[i1:i2]][:3]} | md {[x[:70] for x in b[j1:j2]][:3]}")

# printed paragraph numbers -> block IDs
num_ok = num_bad = 0
for i, p in enumerate(paras):
    n = p.get("n")              # the site keeps the printed paragraph number here
    if not n:
        continue
    j = pairs.get(i)
    if j is not None and items[j].get("block") == f"{book}-{n}":
        num_ok += 1
    else:
        num_bad += 1
        problems.append(f"paranum {n}: md block {items[j].get('block') if j is not None else None}")

# contents tree
toc = json.loads(Path(tocp).read_text(encoding="utf-8"))
site_h = [(LEAD.sub("", n["title"]).strip(), n["depth"]) for n in toc]
md_h = [(LEAD.sub("", it["text"]).strip(), it["level"]) for it in items if it["head"] and it["level"] >= 3]
if [t for t, _ in site_h] != [t for t, _ in md_h]:
    problems.append("tree titles/order differ")
# The site counts the piṭaka as a level the source text does not print, so its
# depth may be a constant offset from the md level; nesting must be identical.
offsets = {s[1] - m[1] for s, m in zip(site_h, md_h)}
if len(offsets) != 1:
    problems.append(f"tree nesting differs (depth offsets {sorted(offsets)})")
depth_note = f"site depth = md level + {offsets.pop()}" if len(offsets) == 1 else ""

print(f"== {Path(md).name}: site paras {len(paras)}, md lines {len(items)}, matched {len(pairs)}; "
      f"printed numbers in the right block {num_ok}/{num_ok + num_bad}; tree nodes site {len(site_h)} / md {len(md_h)}; {depth_note}")
print("   PASS" if not problems else "   PROBLEMS (" + str(len(problems)) + "):\n   - " + "\n   - ".join(problems[:15]))
sys.exit(1 if problems else 0)
