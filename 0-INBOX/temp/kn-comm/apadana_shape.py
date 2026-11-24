"""Apadāna-aṭṭhakathā (KN book 10): the shape decided by a human, 2026-11-24. Headings only, no text.

  prep <segments.json>   before build_commentary.py:
     - the Nidāna, nested:  ### Nidānakathā > #### Dūrenidānakathā > ##### Sumedhakathā,
       Dīpaṅkaro buddho … Gotamo buddho;  #### Avidūrenidānakathā;  #### Santikenidānakathā
       (the XML tags Sumedhakathā and the Buddhas as subheads beside the Nidānakathā; the text
       tells the Sumedhakathā inside the Dūrenidāna: "imasmiṃ ṭhāne sumedhakathā kathetabbā");
     - "Therāpadānaṃ" (printed above the vaggas, and again in part 2) is text, not a heading,
       and everything after it moves up one level, so the vaggas are '###' as in the root.
  post <draft.md>        after build_commentary.py (heading IDs only):
     - each vagga takes the root ID of its printed (first) number, with everything under it:
       21-23. Kaṇikārapupphiyādivaggo -> ^10-21-0, 24. Udakāsanavaggo -> ^10-24-0 …;
       the Nigamanakathā follows the last vagga (^10-57-0).
"""
import json
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
mode, path = sys.argv[1], Path(sys.argv[2])
LEAD = re.compile(r"^\s*(\d+)(?:-\d+)?\.\s*")

if mode == "prep":
    data = json.loads(path.read_text(encoding="utf-8"))
    segs = data["segments"]
    heads = [s for s in segs if s["css_class"] == "heading"]
    names = [LEAD.sub("", s["content"]).strip() for s in heads]
    i_nid, i_dure = names.index("Nidānakathā"), names.index("Dūrenidānakathā")
    i_avi, i_san = names.index("Avidūrenidānakathā"), names.index("Santikenidānakathā")
    assert i_nid < i_dure < i_avi < i_san
    heads[i_nid]["level"] = 3
    heads[i_dure]["level"] = 4
    for k in range(i_dure + 1, i_avi):                 # Sumedhakathā, the Buddhas
        heads[k]["level"] = 5
    heads[i_avi]["level"] = heads[i_san]["level"] = 4
    n_text, after = 0, False
    for s in segs:
        if s["css_class"] == "heading" and s["content"].strip() == "Therāpadānaṃ":
            s["css_class"] = "centered"; s.pop("level", None); n_text += 1; after = True
            continue
        if after and s["css_class"] == "heading":
            s["level"] -= 1
    assert n_text == 1, n_text          # the part-2 reprint is already text (reprint rule)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    vag = [s for s in segs if s["css_class"] == "heading" and s.get("level") == 3]
    print(f"   apadana prep: Nidāna nested; 'Therāpadānaṃ' as text; level-3 headings now: "
          f"{[LEAD.sub('', s['content']).strip() for s in vag][:4]} … ({len(vag)})")

elif mode == "post":
    raw = path.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(nl)
    jpath = Path(sys.argv[3])                           # the prepped JSON: printed vagga numbers
    segs = json.loads(jpath.read_text(encoding="utf-8"))["segments"]
    printed = [int(LEAD.match(s["content"]).group(1)) for s in segs
               if s["css_class"] == "heading" and s.get("level") == 3 and LEAD.match(s["content"])]
    H = re.compile(r"^(#+) (.*) \^10-(\d+)((?:-[\dIVXLC]+)*)-0$")
    pos = [m.group(3) for m in map(H.match, lines) if m and len(m.group(1)) == 3 and m.group(3).isdigit()]
    assert len(pos) == len(printed) + 1, (len(pos), len(printed))   # + the Nigamanakathā
    remap = {p: str(n) for p, n in zip(pos, printed)}
    remap[pos[-1]] = str(printed[-1] + 1)
    changed = 0
    for k, l in enumerate(lines):
        m = H.match(l)
        if m and m.group(3) in remap and remap[m.group(3)] != m.group(3):
            lines[k] = f"{m.group(1)} {m.group(2)} ^10-{remap[m.group(3)]}{m.group(4)}-0"
            changed += 1
    out = nl.join(lines)
    ids = re.findall(r"\s\^([\w-]+)\s*$", out, re.M)
    assert len(ids) == len(set(ids)), "duplicate IDs"
    path.write_bytes(out.encode("utf-8"))
    print(f"   apadana post: vagga IDs by printed number ({len(printed)} vaggas, {changed} heading lines renumbered)")
