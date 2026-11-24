#!/usr/bin/env python3
"""merge_volumes.py — join the per-volume files of one work into one file
(cscd-root-text-intake step 10 / cscd-commentary-intake step 9).

A nikāya (DN, MN, SN, AN) is one work printed by CSCD in several volumes; the
library holds it as one text whose chapters are the volumes, as the Vinaya and
Abhidhamma vaults do for multi-volume works. Each volume is first built and
verified on its own; this script then joins the verified files, losslessly:

- every block of every volume is kept, in order, with its ID (IDs already
  carry the volume number `^<book>-…`, so they stay unique);
- the first volume's homage `^T-1` and `# <nikāya> ^0` stay the file's top;
- a later volume's opening lines (before its `## ^<book>-0`) are printed text,
  so they stay where printed, as plain blocks: the homage `^T-1` becomes
  `^<book>-T1` (then T2, …), and the `# <nikāya>` heading becomes the text line
  `<nikāya> ^<book>-T<k>` (the vault's "(aṭṭhakathā)" label is not printed and
  is dropped from it);
- transclusion targets are rewritten with --relink OLD=NEW (exact paths);
- the frontmatter is the first volume's, with the per-volume fields replaced
  (title, registered_id, root_text, commentary, source_*, other_ids) and the
  library ids of the old per-volume texts dropped.

`--split <merged.md> <part1.md> …` checks the reverse: undoing the boundary
changes and the relinks gives back exactly the bodies of the parts.

Usage:
  python3 -I merge_volumes.py <out.md> <part1.md> <part2.md> … --title T
         [--registered-id ID] [--root-text PATH] [--commentary PATH]
         [--relink OLD=NEW …] [--label "<volume label>"]
  python3 -I merge_volumes.py --split <merged.md> <part1.md> … [--relink OLD=NEW …]
"""
import re
import sys
from pathlib import Path

args = sys.argv[1:]


def take(flag, many=False):
    vals = []
    while flag in args:
        k = args.index(flag); vals.append(args[k + 1]); del args[k:k + 2]
    return vals if many else (vals[0] if vals else None)


relinks = [r.split("=", 1) for r in take("--relink", True)]
SPLIT = "--split" in args
if SPLIT: args.remove("--split")
title, reg, root_text, commentary, label = (take(f) for f in ("--title", "--registered-id", "--root-text", "--commentary", "--label"))
out, parts = args[0], args[1:]
# one part: a work whose first volume is ingested alone (the Khuddakanikāya-ṭīkā, the Netti's only):
# its body relinked, its frontmatter the work's; later volumes join it as usual
if not parts: sys.exit("STOP: give at least one part")

ID_END = re.compile(r"\s\^([\w-]+)\s*$")
LAYER_LABEL = re.compile(r"\s*\((aṭṭhakathā|ṭīkā|abhinavaṭīkā)\)\s*$")


def read(p):
    t = Path(p).read_text(encoding="utf-8")
    if not t.startswith("---\n"): sys.exit(f"STOP: {p} has no frontmatter")
    fm, body = t[4:].split("\n---\n", 1)
    return fm, body


def relink(body):
    for old, new in relinks:
        body = body.replace(f"![[{old}#", f"![[{new}#")
    return body


def opening(body):
    """(lines before the first '## ', rest) of a part body."""
    lines = body.split("\n")
    k = next(i for i, l in enumerate(lines) if l.startswith("## "))
    return lines[:k], lines[k:]


def book_of(rest):
    m = ID_END.search(rest[0])
    if not m or not re.fullmatch(r"\d+-0", m.group(1)): sys.exit(f"STOP: first ## has no ^<book>-0 id: {rest[0]!r}")
    return m.group(1)[:-2]


def convert_opening(head, book):
    """Later volume: '^T-n' -> '^<book>-T<k>', '# X ^0' -> 'X ^<book>-T<k>'."""
    out, k = [], 0
    for l in head:
        if not l.strip(): out.append(l); continue
        m = ID_END.search(l)
        if not m: sys.exit(f"STOP: unexpected opening line without id: {l!r}")
        k += 1
        text = l[:m.start()]
        if l.startswith("# "):
            if m.group(1) != "0": sys.exit(f"STOP: h1 id is not ^0: {l!r}")
            text = LAYER_LABEL.sub("", text[2:])
        elif not re.fullmatch(r"T-\d+", m.group(1)):
            sys.exit(f"STOP: unexpected opening block {l!r}")
        out.append(f"{text} ^{book}-T{k}")
    return out


bodies = [read(p) for p in parts]

if SPLIT:
    fm, merged = read(out)
    # Rebuild the merged body from the parts and compare: the transform is
    # deterministic, so equality proves nothing was lost, added or moved.
    pieces = []
    for i, (_, b) in enumerate(bodies):
        b = relink(b).rstrip("\n")
        if i == 0: pieces.append(b); continue
        head, rest = opening(b)
        pieces.append("\n".join(convert_opening(head, book_of(rest)) + rest))
    want = "\n\n".join(p.strip("\n") for p in pieces) + "\n"
    got = merged.lstrip("\n")
    if got.strip("\n") != want.strip("\n"):
        a, b = got.split("\n"), want.split("\n")
        i = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))
        sys.exit(f"SPLIT MISMATCH at line {i}: merged {a[i] if i < len(a) else None!r} | parts {b[i] if i < len(b) else None!r}")
    # And the reverse direction, block by block: every part's IDs, in order.
    ids = re.findall(r"\s\^([\w-]+)\s*$", got, re.M)
    n = sum(len(re.findall(r"\s\^([\w-]+)\s*$", b, re.M)) for _, b in bodies)
    if len(ids) != n or len(set(ids)) != len(ids):
        sys.exit(f"SPLIT ID PROBLEM: merged {len(ids)} ids ({len(set(ids))} unique), parts {n}")
    print(f"SPLIT OK: {len(parts)} parts, {n} block IDs, all unique, bodies identical after the documented boundary changes")
    sys.exit(0)

# ---------- merge ----------
pieces, conv = [], []
for i, (_, b) in enumerate(bodies):
    b = relink(b).rstrip("\n")
    if i == 0: pieces.append(b); continue
    head, rest = opening(b)
    book = book_of(rest)
    new = convert_opening(head, book)
    conv += [l for l in new if l.strip()]
    pieces.append("\n".join(new + rest))
body = "\n\n".join(p.strip("\n") for p in pieces) + "\n"
ids = re.findall(r"\s\^([\w-]+)\s*$", body, re.M)
dup = sorted({x for x in ids if ids.count(x) > 1})
if dup: sys.exit(f"STOP: duplicate ids after merge: {dup[:10]}")
left = [t for t, _ in re.findall(r"!\[\[([^#\]]+)#\^([\w-]+)\]\]", body) if any(t == o for o, _ in relinks)]
if left: sys.exit(f"STOP: {len(left)} transclusions still point at old files")

# ---------- frontmatter ----------
fms = [f for f, _ in bodies]


def field(fm, key):
    m = re.search(rf"^{key}:[ \t]*(.*)$", fm, re.M)
    return m.group(1).strip() if m else None


def block(fm, key):
    """A key and its indented continuation lines (lists)."""
    m = re.search(rf"^{key}:.*(?:\n[ \t]+.*)*", fm, re.M)
    return m.group(0) if m else None


def unq(v): return v.strip().strip('"')


srcfiles, urls, others = [], [], []
for f in fms:
    for s in unq(field(f, "source_filename")).strip("[]").split(","):
        s = s.strip()
        if s and s not in srcfiles: srcfiles.append(s)
    # a volume built from several XML parts (merge_parts.py) lists them under `source:` itself
    vols = block(f, "source_volumes") or block(f, "source")
    for u in re.findall(r'"(https?://[^"]+)"', vols or "") or [unq(field(f, "source"))]:
        if u and u not in urls: urls.append(u)
    for o in re.findall(r"^  - (.+)$", block(f, "other_ids") or "", re.M):
        if o not in others: others.append(o)

first = fms[0]
nikaya = unq(field(first, "nikaya"))
layer = unq(field(first, "layer"))
stems = ", ".join(s.replace(".xml", "") for s in srcfiles)
how = ("Converted XML → segment JSON → json-to-source-text (tipitaka_org_book.py or tree mode) → block IDs, via the cscd-root-text-intake skill"
       if field(first, "file_type") == "root-text" else
       "Converted XML → segment JSON → commentary converter → block IDs, via the cscd-commentary-intake skill; each paragraph that opens with a printed paragraph number links to those root paragraphs (transclusions), and the printed number is kept")
desc = (f"VRI Chaṭṭha Saṅgāyana (CSCD) romanised XML, {len(srcfiles)} volume file{'s' if len(srcfiles) > 1 else ''} ({stems}), {nikaya}{', ' + label if label else ''}. "
        f"{how}. Each volume was built and verified on its own, then the volumes were joined in order with merge_volumes.py: "
        f"every block and ID kept; a later volume's opening homage and nikāya line kept as plain text blocks ^<book>-T<k>. "
        f"Variant readings inline in [ ]; bold kept as **…**; page markers dropped; printed heading numbers kept in the headings, as in the XML.")

keep_before = ["language", "script", "file_type"]
keep_mid = ["lang_tag", "verse_id_format", "pitaka", "nikaya", "layer"]
lines = ["---", f"title: {title or unq(field(first, 'title'))}"]
lines += [f"{k}: {field(first, k)}" for k in keep_before if field(first, k) is not None]
if reg: lines.append(f"registered_id: {reg}")
lines += [f"{k}: {field(first, k)}" for k in keep_mid if field(first, k) is not None]
if root_text: lines.append(f"root_text: {root_text}")
if commentary: lines.append(f"commentary: {commentary}")
lines.append(f'source_description: "{desc}"')
lines.append(f"source_filename: [{', '.join(srcfiles)}]")
lines.append(f'source: "{urls[0]}"')
lines.append("source_volumes:"); lines += [f'  - "{u}"' for u in urls]
lines.append("other_ids:"); lines += [f"  - {o}" for o in others]
for k in ("license", "tag_ids", "category_id"):
    if field(first, k) is not None: lines.append(f"{k}: {field(first, k)}")
lines.append("---")
Path(out).write_text("\n".join(lines) + "\n" + body, encoding="utf-8")
print(f"{out}: {len(parts)} volumes, {len(ids)} block IDs, {body.count(chr(10) + '![[')} transclusions; opening lines kept as text: {len(conv)}")
for l in conv: print("   ", l[:90])
