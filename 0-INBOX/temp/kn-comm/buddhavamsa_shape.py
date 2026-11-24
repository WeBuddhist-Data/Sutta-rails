"""Buddhavaṃsa-aṭṭhakathā (KN book 12): the shape decided by a human, 2026-11-24 (as the Apadāna).
Headings only, no text.

  prep <segments.json>   before build_commentary.py:
     - ### Nidānakathā (front matter, --fm=Nidānakathā) > #### Bāhiranidānaṃ;
     - "Abbhantaranidānaṃ", a title with no text of its own printed above the 28 chapters, is
       text, and every heading after it moves up one level: the chapters are '###', on the
       root's IDs ^12-1-0 … ^12-28-0 (the root's 29th section, the Dhātubhājanīyakathā, has no
       commentary).
  post <draft.md> <json> after build_commentary.py:
     - the closing Nigamanakathā is ^12-30-0, after the root's 29 sections (not ^12-29-0, the
       Dhātubhājanīyakathā's number).
"""
import json
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
mode, path = sys.argv[1], Path(sys.argv[2])

if mode == "prep":
    data = json.loads(path.read_text(encoding="utf-8"))
    segs = data["segments"]
    heads = [s for s in segs if s["css_class"] == "heading"]
    names = [s["content"].strip() for s in heads]
    i_nid, i_bah = names.index("Nidānakathā"), names.index("Bāhiranidānaṃ")
    assert i_bah == i_nid + 1
    heads[i_nid]["level"], heads[i_bah]["level"] = 3, 4
    after = False
    for s in segs:
        if s["css_class"] == "heading" and s["content"].strip() == "Abbhantaranidānaṃ":
            s["css_class"] = "centered"; s.pop("level", None); after = True
            continue
        if after and s["css_class"] == "heading":
            s["level"] -= 1
    assert after
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    ch = [s["content"] for s in segs if s["css_class"] == "heading" and s.get("level") == 3]
    print(f"   buddhavamsa prep: Bāhiranidāna under the Nidānakathā; 'Abbhantaranidānaṃ' as text; "
          f"level-3 headings {len(ch)}: {ch[:3]} … {ch[-2:]}")

elif mode == "post":
    raw = path.read_bytes().decode("utf-8")
    old = re.search(r"^### Nigamanakathā \^12-(\d+)-0(?=\r?$)", raw, re.M)
    assert old and old.group(1) == "29", old
    path.write_bytes(raw.replace(old.group(0), "### Nigamanakathā ^12-30-0").encode("utf-8"))
    print("   buddhavamsa post: Nigamanakathā ^12-29-0 -> ^12-30-0")
