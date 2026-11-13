#!/usr/bin/env python3
"""
merge_parts.py — step 3b of cscd-commentary-intake.

Join the segment JSONs of one commentary work that CSCD splits over several
volumes (e.g. s0104t + s0105t) into one JSON, in order. tipitaka.app shows
such a work as a single book, with each later volume's opening lines (homage,
nikāya, book title, "(Dutiyo bhāgo)") kept as ordinary lines inside it.
The join does the same:

- every segment of every part is kept, in order (nothing dropped);
- a later part's opening lines (before its first chapter) are re-typed as
  "centered", so they become plain text blocks, not headings;
- chapter numbers continue from the previous part.

Usage: python3 -I merge_parts.py <out.json> <part1.json> <part2.json> [...]
"""
import json
import sys
from pathlib import Path

out, parts = sys.argv[1], sys.argv[2:]
if len(parts) < 2:
    sys.exit("STOP: give at least two parts")
merged, offset, retyped = None, 0, []
for k, path in enumerate(parts):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    segs = data["segments"]
    if merged is None:
        merged = dict(data)
        merged["segments"] = list(segs)
        merged["source_filename"] = [data["source_filename"]]
        merged["source_url"] = [data["source_url"]]
        merged["id"] = [data["id"]]
        offset = max(s["chapter"] for s in segs)
        continue
    before_first = True
    for s in segs:
        s = dict(s)
        if s["css_class"] == "chapter":
            before_first = False
        if before_first:
            retyped.append((Path(path).name, s["css_class"], s["content"]))
            s["css_class"] = "centered"
        s["chapter"] = s["chapter"] + offset
        merged["segments"].append(s)
    merged["source_filename"].append(data["source_filename"])
    merged["source_url"].append(data["source_url"])
    merged["id"].append(data["id"])
    offset = max(s["chapter"] for s in merged["segments"])
merged["total_segments"] = len(merged["segments"])
merged["retyped_opening_lines"] = retyped
Path(out).write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{out}: {len(parts)} parts, {merged['total_segments']} segments; "
      f"{len(retyped)} opening line(s) of later parts kept as plain text:")
for name, css, content in retyped:
    print(f"   {name} [{css}] {content}")
