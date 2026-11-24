"""compare_site.py — step 9 of cscd-root-text-intake.
Compare a converted root-text .md with tipitaka.app (text + contents tree).

Text: every md line (heading or text) is matched in order to one site paragraph,
after normalising site display markup (page markers |X0.0000|, **bold**,
{notes} -> [notes], ‘‘ ’’ -> ") and dropping printed leading numbers on both sides.
Paragraph numbers: every site paragraph that starts with a printed N. must sit
in the md block whose ID is ^<book>-N.
Tree: md '###'+ headings vs site nodes: same titles (leading numbers and
[variant readings] ignored, as the site's contents titles omit them),
same order, md level == site depth.
Bold: the md's **…** spans equal the site's, in order (bold_check.py), compared
with edge spaces/punctuation trimmed. Text is compared with
the ** removed on both sides.
Usage: python3 -I compare_site.py <book> <file.md> <key.text.json> <key.toc.json>"""
import difflib, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bold_check  # noqa: E402

PER_SECTION = "--per-section" in sys.argv   # IDs ^<book>-<section>-<N> (Khuddakapāṭha)
_args = sys.argv[1:]
ZONE_LABELS = None   # --zone-labels M,1,2,3: run k's zone label (Paṭisambhidāmagga); implies --zoned
if "--zone-labels" in _args:
    _k = _args.index("--zone-labels"); ZONE_LABELS = _args[_k + 1].split(","); del _args[_k:_k + 2]
ZONED = "--zoned" in _args or ZONE_LABELS is not None   # IDs ^<book>-<run>-<N>, run = k-th restart at 1 (Suttanipāta)
book, md, textp, tocp = [x for x in _args if x not in ("--per-section", "--zoned")][:4]
# printed numbers dropped before comparing: "1. ", "1-10. ", "(6) 1. " (AN vaggas)
LEAD = re.compile(r"^\s*(?:\(\d+\)\s*)?(\d+(?:-\d+)*|\(\d+\))\s*\.\s*")


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
    txt = bold_check.strip_bold(h.group(2) if h else re.sub(r"\s\^[\w-]+$", "", ln))
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
site_merges = []
problems += bold_check.compare(bold_check.site_spans(paras), bold_check.md_spans(lines)[0], "site", site_merges)
if site_merges:
    print(f"   note: {len(site_merges)} bold group(s) the site joins into one span (XML and md keep them apart), e.g. "
          f"site {site_merges[0][0]} vs md {site_merges[0][1]}")
# compared without whitespace (the site drops spaces next to some marks, e.g. its
# ".Namo" for the XML's ". Namo"); exact spacing is verify.py's check against the XML
a = [re.sub(r"\s+", "", LEAD.sub("", site_norm(p["t"]))) for p in paras]
b = [re.sub(r"\s+", "", LEAD.sub("", it["text"])) for it in items]
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
zone, zprev = 0, None
import zones  # noqa: E402  (the run rules shared with apply.py and verify.py)
head_since, numbered = False, []
for i, p in enumerate(paras):
    if p.get("r") in ("chapter", "title", "subhead", "subsubhead", "book"):
        head_since = True
    elif p.get("n"):
        numbered.append((i, p["n"], head_since))
        head_since = False
run_of = dict(zip((i for i, _, _ in numbered), zones.assign((n, hs) for _, n, hs in numbered))) if ZONED else {}
for i, p in enumerate(paras):
    n = p.get("n")              # the site keeps the printed paragraph number here
    if not n:
        continue
    j = pairs.get(i)
    want = f"{book}-{n}"
    if ZONED:
        zone = run_of[i]
        lab = ZONE_LABELS[zone - 1] if ZONE_LABELS and zone <= len(ZONE_LABELS) else str(zone)
        want = f"{book}-{lab}-{n}" if lab else f"{book}-{n}"
    if PER_SECTION:                     # the site's node key "<book-key>-<section>[-…]" gives the section
        # the book's own key, from its contents tree ("kn-thiap-1" -> "kn-thiap"): the text
        # file's book.root names the site's source file, which may hold two books (kn-ap)
        root = json.loads(Path(tocp).read_text(encoding="utf-8"))[0]["key"].rsplit("-", 1)[0]
        rest = p.get("k", "")[len(root):].strip("-").split("-")
        want = f"{book}-{rest[0]}-{n}" if rest and rest[0].isdigit() else want
    if j is not None and items[j].get("block") == want:
        num_ok += 1
    else:
        num_bad += 1
        problems.append(f"paranum {n}: md block {items[j].get('block') if j is not None else None}")

# contents tree
toc = json.loads(Path(tocp).read_text(encoding="utf-8"))
site_h = [(LEAD.sub("", n["title"]).strip(), n["depth"]) for n in toc]
# The site's contents titles leave out variant readings (`Pañcattayasuttaṃ`
# for the md's `Pañcattayasuttaṃ [pañcāyatanasutta (ka.)]`), so [..] is dropped here.
md_h = [(re.sub(r"\s*\[[^\]]*\]", "", LEAD.sub("", it["text"])).strip(), it["level"])
        for it in items if it["head"] and it["level"] >= 3]
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
