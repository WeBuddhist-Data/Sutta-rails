"""Jātaka-aṭṭhakathā (KN book 14): the shape decided by a human, 2026-11-24. Headings only, no text.

  prep <segments.json>   before build_commentary.py (the seven volumes joined by merge_parts.py):
     - the Nidāna nested as the Apadāna's:  ### Nidānakathā > #### Dūrenidānakathā > ##### Sumedhakathā;
       #### Avidūrenidānakathā; #### Santikenidānakathā   (front matter: --fm=Nidānakathā);
     - each of the 547 jātaka titles, printed as a plain paragraph ("[11] 1. Lakkhaṇamigajātakavaṇṇanā";
       the first ten without "[N]"), is a heading one level below its vagga, or below its nipāta where
       the nipāta has no vaggas, as in the root; it keeps its printed numbers (keep_number), so the
       words stay those of the XML. A jātaka's own sub-sections (the Mahānipāta's kaṇḍas) go one
       level below it;
     - mis-tagging corrected: "2. Pucimandavaggo" and "3. Kuṭidūsakavaggo", tagged like the nikāya line
       (<p rend="nikaya">) and so kept as text by the converter, are vagga headings like their siblings;
       "Catuttho bhāgo", a volume label printed without brackets, is text; "22. Mahānipāto" reprinted
       at the start of volume 7 (the Mahānipāta runs on from volume 6) is text (skill Rule 4).
     Writes <segments>.shape.json: the titles turned into headings and into text, for the checks.
  post <draft.md> <segments.json>   after the build:
     - a jātaka's sub-sections take the root's IDs for the same sections. The build numbers them
       1, 2, … in the order the commentary has headings, but the Vessantara-aṭṭhakathā has none
       for the root's first four kaṇḍas (Dasavarakathā … Vanapavesanaṃ), so its Jūjakapabbavaṇṇanā
       would be ^14-22-10-1-0, the root's Dasavarakathā. Each sub-section whose name matches one of
       the root's under the same jātaka takes that ID; one the root lacks goes after the root's last
       (Nagarakaṇḍavaṇṇanā ^14-22-10-13-0). A jātaka the root gives no sub-sections (Bhūridatta)
       keeps the build's numbers, which claim no root section.
"""
import json
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
mode, path = sys.argv[1], Path(sys.argv[2])
NIP = re.compile(r"^\s*\d+\.\s*\S*nipāto\s*$")
VAG = re.compile(r"^\s*\d+\.\s*\S+vaggo\s*$")
# "jātaka(va)ṇṇanā": [174] is misprinted "Dubbhiyamakkaṭajātakaṇṇanā" (kept as printed)
JAT = re.compile(r"^\s*(?:\[\d+\]\s*)?\d+\.\s*\S.*jātaka(?:va)?ṇṇanā\s*$")

if mode == "prep":
    data = json.loads(path.read_text(encoding="utf-8"))
    segs = data["segments"]
    to_heading, to_text = [], []
    names = {"Nidānakathā": 3, "Dūrenidānakathā": 4, "Sumedhakathā": 5, "Avidūrenidānakathā": 4, "Santikenidānakathā": 4}
    for s in segs:
        bare = re.sub(r"^\s*\d+\.\s*", "", s["content"]).strip()     # "1. Dūrenidānakathā"
        if s["css_class"] == "heading" and bare in names:
            s["level"] = names[bare]
    seen_nip, in_nip, vagga_open, jat_level = set(), False, False, None
    for s in segs:
        c, css = s["content"].strip(), s["css_class"]
        if css == "heading" and c == "Catuttho bhāgo":
            s["css_class"] = "centered"; s.pop("level", None); to_text.append(c); continue
        if css == "heading" and NIP.match(c):
            if c in seen_nip:                                   # volume 7's reprint
                s["css_class"] = "centered"; s.pop("level", None); to_text.append(c); continue
            seen_nip.add(c); s["level"] = 3; in_nip, vagga_open, jat_level = True, False, None
            continue
        if not in_nip:
            continue
        if VAG.match(c) and css in ("heading", "centered"):
            if css != "heading":
                to_heading.append(c)
            s["css_class"], s["level"] = "heading", 4
            vagga_open, jat_level = True, None
            continue
        if JAT.match(c) and css in ("heading", "bodytext"):
            if css != "heading":
                to_heading.append(c); s["keep_number"] = True
            jat_level = 5 if vagga_open else 4
            s["css_class"], s["level"] = "heading", jat_level
            continue
        if css == "heading" and jat_level is not None and not c.startswith("Nigamana"):
            s["level"] = jat_level + 1                          # a jātaka's own sub-section
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    Path(str(path) + ".shape.json").write_text(json.dumps({"to_heading": to_heading, "to_text": to_text},
                                                          ensure_ascii=False, indent=1), encoding="utf-8")
    jt = sum(1 for s in segs if s["css_class"] == "heading" and JAT.match(s["content"].strip()))
    print(f"   jataka prep: {jt} jātaka headings ({sum(1 for t in to_heading if JAT.match(t))} from title lines), "
          f"vaggas from mis-tagged lines {[t for t in to_heading if VAG.match(t)]}, as text {to_text}")

elif mode == "post":
    book = "14"
    H = re.compile(r"^(#+) (.*) \^([\w-]+)$")
    stem = lambda s: re.sub(r"[^a-z]", "", s.lower().replace("ṃ", "m").replace("ā", "a").replace("ī", "i").replace("ū", "u"))[:4]
    root = Path(f"0-INBOX/temp/kn/pi-kn-{book}.md").read_text(encoding="utf-8").split("\n")
    rsub = {}                                    # jātaka ID -> [(sub-section ID, name)]
    for m in map(H.match, root):
        if m and re.fullmatch(rf"{book}(-\d+)+-0", m.group(3)):
            parent = m.group(3)[:-2].rsplit("-", 1)[0] + "-0"
            rsub.setdefault(parent, []).append((m.group(3), m.group(2)))
    lines = path.read_text(encoding="utf-8").split("\n")
    jat = {i: H.match(l).group(3) for i, l in enumerate(lines) if H.match(l) and JAT.match(H.match(l).group(2))}
    ren = {}
    cur = None
    for i, l in enumerate(lines):
        if i in jat:
            cur = jat[i]; continue
        m = H.match(l)
        if not m or cur is None:
            continue
        hid = m.group(3)
        if hid.rsplit("-", 2)[0] + "-0" != cur:   # not a direct sub-section of the open jātaka
            if not hid.startswith(cur[:-2] + "-"):
                cur = None
            continue
        subs = rsub.get(cur)
        if not subs:
            continue                              # the root gives this jātaka no sub-sections
        # the whole name, less "-vaṇṇanā" and a final "ṃ" (Jūjakapabbavaṇṇanā = Jūjakapabbaṃ):
        # four letters cannot tell Mahāvana- from Mahārājapabba-
        key = lambda s: re.sub(r"(?:vaṇṇanā|ṃ)$", "", s.strip())
        hit = [rid for rid, name in subs if key(name) == key(m.group(2))]
        if hit:
            new = hit[0]
        else:
            last = max(int(rid.split("-")[-2]) for rid, _ in subs) + sum(1 for v in ren.values() if v.startswith(cur[:-2] + "-") and v not in {r for r, _ in subs})
            new = f"{cur[:-2]}-{last + 1}-0"
        if new != hid:
            ren[i] = new
    for i, new in ren.items():
        m = H.match(lines[i])
        print(f"   jataka post: {m.group(2)}  ^{m.group(3)} -> ^{new}")
        lines[i] = f"{m.group(1)} {m.group(2)} ^{new}"
    ids = [H.match(l).group(3) for l in lines if H.match(l)]
    dup = sorted({x for x in ids if ids.count(x) > 1})
    assert not dup, f"duplicate heading IDs after the jātaka post step: {dup[:10]}"
    path.write_text("\n".join(lines), encoding="utf-8")
