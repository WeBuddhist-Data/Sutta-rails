#!/usr/bin/env python3
"""
set_frontmatter.py — step 7 of cscd-root-text-intake.

Replace the converter's frontmatter with the vault's root-text frontmatter.
The title is the file's own '##' heading (the volume title as printed).
Library fields (license, category_id, text_id, edition_id, toc_id, tag_ids)
are deliberately NOT written — they belong to the upload step.

Usage:
  python3 -I set_frontmatter.py <file.md> <cscd-stem> <nikaya> <volume-label>
  e.g.  ... pi-dn-1.md s0101m "Dīghanikāya" "vagga 1 of 3"
"""
import re
import sys

path, stem, nikaya, volume = sys.argv[1:5]
text = open(path, encoding="utf-8").read()
if not text.startswith("---\n"):
    sys.exit("STOP: file has no frontmatter block to replace")
body = text.split("\n---\n", 1)[1]
h2 = re.search(r"^## (.+?)(?:\s+\^[\w-]+)?\s*$", body, re.M)
if not h2:
    sys.exit("STOP: no '##' volume heading found")
title = h2.group(1).strip()
xml_name = f"{stem}.mul.xml"

fm = f'''---
title: {title}
language: Pali
script: Roman (PTS diacritics)
file_type: root-text
lang_tag: pi
verse_id_format: book-verse
pitaka: sutta
nikaya: {nikaya}
layer: mula
source_description: "VRI Chaṭṭha Saṅgāyana (CSCD) romanised XML, {xml_name} ({nikaya}, {volume}). Converted XML → segment JSON → json-to-source-text (tipitaka_org_book.py) → block IDs, via the cscd-root-text-intake skill. Variant readings kept inline in [ ]; bold kept as **…**; page markers dropped; chapter numbers stripped from headings."
source_filename: {xml_name}
source: "https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn/{xml_name}"
other_ids:
  - tipitaka.org: {stem}
---'''
open(path, "w", encoding="utf-8", newline="\n").write(fm + "\n" + body)
print(f"{path}: frontmatter set (title '{title}')")
