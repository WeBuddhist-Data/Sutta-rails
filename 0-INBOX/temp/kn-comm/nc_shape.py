"""Cūḷaniddesa-aṭṭhakathā (KN book 16): headings only, no text.

  prep <segments.json>   before build_commentary.py:
     - mis-tagging corrected: "2. Dutiyavaggavaṇṇanā" is tagged <p rend="centre"> (a closing line's
       style) while its siblings "1. Paṭhama…", "3. Tatiya…", "4. Catutthavaggavaṇṇanā" are
       <p rend="subhead">; it is a vagga heading like them, at their level. Its printed "2." goes
       the way of theirs (a heading's number is not text).
     Writes <segments>.shape.json: the titles turned into headings, for the checks.
  post <draft.md> <segments.json>   after the build:
     - the commentary's sections take the root's IDs. The root has three '###': Pārāyanavaggo
       ^16-1-0 (the sutta text the niddesa explains), Pārāyanavagganiddeso ^16-2-0, Khaggavisāṇasutto
       ^16-3-0 (> #### Khaggavisāṇasuttaniddeso ^16-3-1-0 > ##### the four vaggas). The commentary
       explains the niddesa only, so it has no section for the root's ^16-1-0, and the build's
       numbers (1, 2, Nigamana 3) are one short: each heading's section number goes up by one
       (Pārāyanavagganiddeso ^16-2-0, its eighteen suttas ^16-2-N-0 as the root's; Khaggavisāṇa-
       suttaniddeso ^16-3-0 > Khaggavisāṇasuttaniddesavaṇṇanā ^16-3-1-0 > vaggas ^16-3-1-N-0;
       Nigamanakathā ^16-4-0, after the root's last section).
"""
import json
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
mode, path = sys.argv[1], Path(sys.argv[2])
BOOK = "16"

if mode == "prep":
    data = json.loads(path.read_text(encoding="utf-8"))
    segs = data["segments"]
    vlevel = {s["level"] for s in segs if s["css_class"] == "heading" and re.match(r"\d+\.\s*\S+vaggavaṇṇanā$", s["content"].strip())}
    assert len(vlevel) == 1, vlevel
    to_heading = []
    for s in segs:
        if s["css_class"] == "centered" and s["content"].strip() == "2. Dutiyavaggavaṇṇanā":
            s["css_class"], s["level"] = "heading", vlevel.pop() if vlevel else s["level"]
            to_heading.append(s["content"].strip())
    assert to_heading == ["2. Dutiyavaggavaṇṇanā"], to_heading
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    Path(str(path) + ".shape.json").write_text(json.dumps({"to_heading": to_heading, "to_text": []},
                                                          ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"   nc prep: as headings {to_heading}")

elif mode == "post":
    H = re.compile(r"^(#+) (.*) \^([\w-]+)$")
    lines = path.read_text(encoding="utf-8").split("\n")
    n = 0
    for i, l in enumerate(lines):
        m = H.match(l)
        if m and len(m.group(1)) >= 3:
            parts = m.group(3).split("-")
            assert parts[0] == BOOK and parts[-1] == "0" and parts[1].isdigit(), m.group(3)
            parts[1] = str(int(parts[1]) + 1)
            lines[i] = f"{m.group(1)} {m.group(2)} ^{'-'.join(parts)}"
            n += 1
    ids = [H.match(l).group(3) for l in lines if H.match(l)]
    assert len(ids) == len(set(ids)), "duplicate heading IDs"
    tops = [(H.match(l).group(3), H.match(l).group(2)) for l in lines if H.match(l) and H.match(l).group(1) == "###"]
    print(f"   nc post: {n} heading IDs moved one section up; '###' now {tops}")
    path.write_text("\n".join(lines), encoding="utf-8")
