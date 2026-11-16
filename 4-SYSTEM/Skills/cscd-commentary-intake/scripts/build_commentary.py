#!/usr/bin/env python3
"""
build_commentary.py — steps 4–6 of cscd-commentary-intake, for one work.

  segment JSON --commentary_converter.py--> draft (root links from printed citations)
               --frontmatter-------------> registered_id, root_text, sources
               --apply_commentary_ids.py--> ^T-1, ^0, headings, ^<book>-<N>

Writes <out.md> and <out>.unresolved.json (citations with no root block, and
expanded truncated-tail ranges) for the report.

Usage:
  python3 -I build_commentary.py <segments.json> <root.md> <out.md>
      --registered-id ID --layer LAYER --layer-label LABEL --nikaya NAME
      [--commentary PATH] [--frontmatter "<heading text>"] [--unlinked "<heading text>" …]

  LAYER        atthakatha | tiika | abhinavatiika   (frontmatter `layer:`)
  LABEL        shown in the h1, e.g. aṭṭhakathā, ṭīkā, abhinavaṭīkā
  --commentary the aṭṭhakathā file a ṭīkā explains (frontmatter `commentary:`)
  --unlinked   (repeatable) a heading whose own text numbers its paragraphs for
               itself — those numbers are not root citations and get no links
               (e.g. the Mūlapaṇṇāsa-ṭīkā's "Ganthārambhakathāvaṇṇanā", 1.–16.).
               A human decision; the run stops if the heading is not found.
"""
import argparse
import json
import re
import subprocess
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = "https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn/"

ap = argparse.ArgumentParser()
ap.add_argument("json_path"); ap.add_argument("root_md"); ap.add_argument("out_md")
ap.add_argument("--registered-id", required=True)
ap.add_argument("--layer", required=True)
ap.add_argument("--layer-label", required=True)
ap.add_argument("--nikaya", required=True)
ap.add_argument("--commentary")
ap.add_argument("--frontmatter", action="append", default=[])   # repeatable
ap.add_argument("--unlinked", action="append", default=[])
a = ap.parse_args()

root = Path(a.root_md)
m = re.search(r"-(\d+)\.md$", root.name)
if not m:
    sys.exit(f"STOP: root file name {root.name} has no trailing book number")
book = int(m.group(1))
root_ids = set(re.findall(r"\s\^([\w-]+)\s*$", root.read_text(encoding="utf-8"), re.M))

# 4. convert
conv = types.ModuleType("commentary_converter")
exec(compile((HERE / "commentary_converter.py").read_text(encoding="utf-8"), "commentary_converter", "exec"), conv.__dict__)
conv.ROOT_TEXT_PATH = root.as_posix()
conv.BOOK_ID = book
conv.ROOT_IDS = root_ids
conv.UNLINKED_HEADINGS = set(a.unlinked)
data = json.loads(Path(a.json_path).read_text(encoding="utf-8"))
conv.LAYER_DISPLAY_MAP = {k: a.layer_label for k in ("atthakatha", "tika", "other", data.get("layer", ""))}
out = Path(a.out_md)
conv.convert_json_to_commentary(a.json_path, out,
                                chapter_context={s["chapter"]: "main" for s in data["segments"]})

missing = set(a.unlinked) - conv.UNLINKED_MATCHED
if missing:
    sys.exit(f"STOP: --unlinked heading(s) not found: {sorted(missing)} — check the exact heading text")

# 5. frontmatter (before IDs: apply_commentary_ids.py reads root_text from it)
text = out.read_text(encoding="utf-8")
body = text.split("\n---\n", 1)[1]
title = re.search(r"^## (.+?)(?:\s+\^[\w-]+)?\s*$", body, re.M).group(1).strip()
fnames = data["source_filename"] if isinstance(data["source_filename"], list) else [data["source_filename"]]
stems = data["id"] if isinstance(data["id"], list) else [data["id"]]
parts = " + ".join(fnames)
lines = [
    "---",
    f"title: {title}",
    "language: Pali",
    "script: Roman (PTS diacritics)",
    "file_type: commentary",
    f"registered_id: {a.registered_id}",
    "lang_tag: pi",
    "verse_id_format: book-verse",
    "pitaka: sutta",
    f"nikaya: {a.nikaya}",
    f"layer: {a.layer}",
    f"root_text: {root.as_posix()}",
]
if a.commentary:
    lines.append(f"commentary: {a.commentary}")
lines += [
    f'source_description: "VRI Chaṭṭha Saṅgāyana (CSCD) romanised XML, {parts}. Converted XML → segment JSON'
    + (" → volumes joined" if len(fnames) > 1 else "")
    + ' → commentary converter → block IDs, via the cscd-commentary-intake skill. Each paragraph that opens with a printed'
      ' paragraph number links to those root paragraphs (transclusions); the printed number is kept. Variant readings'
      ' inline in [ ]; bold kept as **…**; page markers dropped; chapter numbers stripped from headings."',
    "source_filename: " + (fnames[0] if len(fnames) == 1 else "[" + ", ".join(fnames) + "]"),
]
if len(fnames) == 1:
    lines.append(f'source: "{RAW}{fnames[0]}"')
else:
    lines.append("source:")
    lines += [f'  - "{RAW}{f}"' for f in fnames]
lines.append("other_ids:")
lines += [f"  - tipitaka.org: {s}" for s in stems]
lines.append("---")
out.write_text("\n".join(lines) + "\n" + body, encoding="utf-8")

# 6. block IDs
cmd = ["python3", "-I", str(HERE / "apply_commentary_ids.py"), "apply", str(out)]
for fm_heading in a.frontmatter:
    cmd += ["--frontmatter", fm_heading]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stdout + r.stderr)
for ln in r.stdout.splitlines():
    if "WARNING" in ln or "front" in ln.lower():
        print("   " + ln.strip())

log = {"unresolved": conv.UNRESOLVED, "abbreviated_ranges": conv.ABBREVIATED}
if a.unlinked or conv.UNLINKED:
    log["unlinked_section_numbers"] = conv.UNLINKED
Path(str(out)[:-3] + ".unresolved.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
txt = out.read_text(encoding="utf-8")
n_content = len(re.findall(r"\s\^" + str(book) + r"-(?!0\s*$)\d+\s*$", txt, re.M))
print(f"{out.name}: book {book}, title '{title}', transclusions {txt.count('![[')}, "
      f"content blocks {n_content}, "
      f"unresolved {len(conv.UNRESOLVED)}, abbreviated ranges {len(conv.ABBREVIATED)}"
      + (f", numbers left unlinked {len(conv.UNLINKED)}" + (f" (under {sorted(a.unlinked)})" if a.unlinked else "") if conv.UNLINKED else ""))
