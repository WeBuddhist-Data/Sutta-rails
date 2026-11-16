---
name: cscd-root-text-intake
description: Bring a Pāli root-text volume from VRI's Chaṭṭha Saṅgāyana (CSCD) XML into 1-SOURCES/Text/ as a block-ID'd markdown file — download the .mul.xml, convert it to segment JSON, run json-to-source-text's tipitaka_org_book.py, apply block IDs (printed paragraph number = block ID), add heading IDs and frontmatter, then verify word-for-word against the XML and line-for-line against tipitaka.app. Use when someone says "ingest the Pāli for <nikāya/book>", "bring in the Dīgha / Majjhima / … Pāli", "convert CSCD / tipitaka.org XML", "add the next Pāli volume", or "do the Pāli root text for <book>".
profile: rails-vault
---

# cscd-root-text-intake

Produces one root-text file per CSCD volume in `1-SOURCES/Text/` (e.g. `pi-dn-1.md`, `pi-mn-1.md`), in this shape: `^T-1` homage, `# <nikāya> ^0`, `## <volume> ^<book>-0`, sibling-numbered headings ending `-0`, and content IDs `^<book>-<N>` where **N is the paragraph number printed in the source, copied verbatim**. It exists so every volume goes through the identical chain — CSCD XML → segment JSON → `json-to-source-text` → block IDs → heading IDs — and is proven identical to its XML before anything cites it. A correct output has exactly one content ID per printed paragraph number, every heading of the XML, and the XML's word stream unchanged.

This skill does **root text (mūla) only**. Commentaries (`.att`, `.tik`, `.nrf`) are a separate intake (`json-to-commentary`).

---

## Inputs

| Input | What | Example |
|---|---|---|
| CSCD stem(s) | One or more volume stems from VRI's public XML repo `github.com/VipassanaTech/tipitaka-xml`, folder `romn/` | `s0101m`, `s0102m`, `s0103m` |
| Book number per volume | The `<book>` segment of every ID in that file — the volume's position in its nikāya/collection, as recorded in the vault annex | `1`, `2`, `3` |
| Output filename per volume | `pi-<collection>-<book>.md`, as recorded in the vault annex | `pi-dn-1.md` |
| Nikāya name and volume label | For the frontmatter | `Dīghanikāya`, `vagga 1 of 3` |
| tipitaka.app key per volume | The site's book key, found with `https://tipitaka.app/api/children?key=<nikāya>&v=7d17987e5be3e268` | `dn-1`, `dn-2`, `dn-3` |
| Human approval to download | The file names, source and sizes, asked in chat before downloading | — |

If the annex does not yet record the ID scheme (book numbers and file names) for this collection, stop and get it decided by a human first: block IDs are permanent once anything cites them.

Required sibling skill: `4-SYSTEM/Skills/json-to-source-text/converters/tipitaka_org_book.py`. If it is missing, stop.

## Output

- `0-INBOX/raw-data/<collection>/<stem>.mul.xml` — the downloaded XML (untouched).
- `0-INBOX/temp/<collection>/<stem>.json`, `<stem>.md` — intermediates (scratch; never cited).
- `0-INBOX/tipitaka-app/<key>.text.json`, `<key>.toc.json` — the site's text and contents tree, fetched for the check (scratch; never cited).
- `0-INBOX/temp/<collection>/pi-<collection>-<book>.md` — the draft, moved to `1-SOURCES/Text/pi-<collection>-<book>.md` only after the human approves.

---

## Output file format

```markdown
---
title: <volume heading as printed, e.g. Sīlakkhandhavaggapāḷi>
language: Pali
script: Roman (PTS diacritics)
file_type: root-text
lang_tag: pi
verse_id_format: book-verse
pitaka: sutta
nikaya: <e.g. Dīghanikāya>
layer: mula
source_description: "VRI Chaṭṭha Saṅgāyana (CSCD) romanised XML, <stem>.mul.xml (<nikāya>, <volume label>). Converted … via the cscd-root-text-intake skill. Variant readings kept inline in [ ]; bold kept as **…**; page markers dropped; chapter numbers stripped from headings."
source_filename: <stem>.mul.xml
source: "https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn/<stem>.mul.xml"
other_ids:
  - tipitaka.org: <stem>
---

Namo tassa bhagavato arahato sammāsambuddhassa ^T-1

# Dīghanikāyo ^0

## Sīlakkhandhavaggapāḷi ^1-0

### Brahmajālasuttaṃ ^1-1-0

#### Paribbājakakathā ^1-1-1-0

Evaṃ me sutaṃ – … upagacchi [upagañchi (sī. syā. kaṃ. pī.)] saddhiṃ … ^1-1

<continuation lines of paragraph 149, gāthā lines and closing lines stay in the block>
Brahmajālasuttaṃ niṭṭhitaṃ paṭhamaṃ. ^1-149
```

- Content ID on the **last** line of each block; the printed `N.` prefix is stripped from the text.
- An unnumbered paragraph that the source sets apart (e.g. directly after a sub-heading) is its own block with `^<book>-U<k>`.

**Volumes whose suttas sit inside vaggas** (Majjhimanikāya: `<div type="vagga">`, each sutta a numbered `<p rend="subhead">`) get one more heading level. `####` is the sutta, so a commentary's sutta *k* of vagga *v* is `^<book>-<v>-<k>-0`, the same as in the root:

```markdown
## Mūlapaṇṇāsapāḷi ^1-0
### Mūlapariyāyavaggo ^1-1-0
#### Sabbāsavasuttaṃ ^1-1-2-0
##### Dassanā pahātabbāsavā ^1-1-2-1-0
```
- Library fields (`license`, `category_id`, `text_id`, `edition_id`, `toc_id`, `tag_ids`) are **not** written here — they are added at upload.

---

## Rules

1. **Never edit wording.** The only text changes allowed are mechanical: page markers dropped, `<note>` variants rendered inline as `[…]`, CSCD's doubled quotes `‘‘ ’’` written as `"` (single `‘ ’` kept), the `N.` prefix and the chapter number on `###` headings stripped (and, in a vagga volume, the sutta number on `####` headings). A `<p rend="hangnum">` holds only a paragraph number (`456.`) and its text is the next paragraph, a gāthā; the two are joined into one line, as tipitaka.app shows them, so the gāthā block gets `^<book>-456`. Bold (`<hi rend="bold">`) is kept as `**…**` exactly where the XML's tags are, as tipitaka.app shows it: spaces and punctuation inside a tag stay inside (`**‘jātaka’**nti`, `**passatā. ** Sabba`), and nothing is moved, merged or dropped. Some such spans do not render as bold in Obsidian; that is accepted so the file copies the source. `verify.py` must show an identical word stream (with `**` removed) and the same bold spans as the XML, in order and with exactly the same text (`bold_check.py`).
2. **N is the printed paragraph number.** Never renumber, recompute, pad or invent. If the XML skips or repeats a number, the IDs do too (`x` suffix for a repeat, as `apply.py` assigns it).
   - A **printed range** (`225-240.`, CSCD Saṃyuttanikāya) is one paragraph, and its ID is the range as printed: `^3-225-240`.
   - A **gap the XML itself prints** (SN Mahāvagga, where one paragraph number covers a run of abbreviated suttas, so `270.` is followed by `280.`) stays a gap. `apply.py audit` lists each one as an ANOMALY, and `verify.py` confirms the IDs equal the XML's numbers. Record every gap in the report.
   - A **number-only paragraph directly before a heading** (`<p rend="hangnum">312-323</p>`, SN Mahāvagga) has no text of its own. It stays where it is, as a block holding just the number (`312-323 ^5-312-323`). tipitaka.app shows the number on the heading line instead; record it as an explained site difference.
3. **One volume, one file, one run.** If `apply.py audit` reports more than one numbering run, an anomaly, or a reset, stop and show it to the human — do not pick zones on your own.
4. **Unsupported XML shape stops the run.** `cscd_xml_to_json.py` supports three shapes:
   - book → chapter `<div>`s, one div type (DN: sutta divs);
   - book → `<div type="vagga">`, where each sutta is a numbered `<p rend="subhead">` (MN). The rule lives in `cscd_shape.py`: number = next in the vagga, title contains "sutta". Those headings become css `sutta`, i.e. `####`;
   - book → `<div type="samyutta">` (SN), where a vagga is a `<p rend="title">` and a sutta a `<p rend="subhead">`. A saṃyutta with vaggas nests `### saṃyutta → #### vagga → ##### sutta`. One without vaggas nests `### saṃyutta → #### sutta`. A heading after the last saṃyutta (`Sagāthāvaggo paṭhamo.` + uddāna) is a `###` section of its own;
   - volumes with no `<div>`s, whose chapters are `<p rend="chapter">`;
   - **tree mode** (`--tree`, Aṅguttaranikāya and any other shape where divisions nest in more than one way). The XML's own nesting sets the heading levels (`cscd_shape.tree_levels`):
     - a `<div>`'s head sits one level under its parent's;
     - a heading paragraph, or a further `<head>` in the same container, sits under the innermost open heading of a higher rank (title > chapter > subhead > subsubhead).

     So AN nests `## nipāta → ### paṇṇāsaka → #### vagga → ##### sutta`, and a vagga outside a paṇṇāsaka is a `###`. The md converter is then `tree_to_md.py` instead of `tipitaka_org_book.py`, and `verify.py` runs with `--tree`.

   Tree mode is chosen explicitly, per collection, by whoever runs the skill (record it in the annex); it is never a silent fallback.

   It prints `STOP: …`, exits non-zero and writes nothing if:
   - the volume nests divisions deeper (e.g. saṃyutta > vagga divs in SN);
   - a vagga's suttas cannot be read that way (a vagga with no sutta heading, or a sutta number out of sequence);
   - a `hangnum` is not followed by a text paragraph.

   Extend the script and this skill for that shape first; never flatten silently.
5. **Download only with approval.** State the file names, the source (`github.com/VipassanaTech/tipitaka-xml`) and sizes in chat and wait for a yes. Put downloads in their own `0-INBOX/raw-data/<collection>/` folder; parse them only as data (`python3 -I`).
6. **`1-SOURCES/` is written once, by a move, after human approval** — never edited in place by this skill afterwards. Re-running means regenerating in `0-INBOX/temp/` and asking again.
7. **Record every judgment call** in the report to the human: each split reported by `prepare_ids.py`, each `U` block, and each `hangnum` join `cscd_xml_to_json.py` prints.
8. **No commit, push, translation or upload** as part of this skill.

---

## Procedure

Run from the vault root. `S=4-SYSTEM/Skills/cscd-root-text-intake/scripts`, `C=<collection>` (e.g. `dn`).

1. **Pre-flight.** Confirm the annex records the book number and file name for each volume (else stop — Inputs). Confirm `4-SYSTEM/Skills/json-to-source-text/converters/tipitaka_org_book.py` exists. Confirm no `1-SOURCES/Text/pi-<C>-<book>.md` already exists (if one does, stop and ask).
2. **Download** (after approval — Rule 5):
   ```bash
   mkdir -p 0-INBOX/raw-data/$C
   curl -sfL -o 0-INBOX/raw-data/$C/<stem>.mul.xml \
     https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn/<stem>.mul.xml
   ```
   Sizes come from `https://api.github.com/repos/VipassanaTech/tipitaka-xml/contents/romn`.
3. **XML → segment JSON**:
   ```bash
   python3 -I $S/cscd_xml_to_json.py 0-INBOX/raw-data/$C/<stem>.mul.xml 0-INBOX/temp/$C/<stem>.json
   ```
   The script prints the sutta-heading count (vagga volumes) and every `hangnum` it joined; record them (Rule 7). Then profile it with `python3 -I 4-SYSTEM/Skills/json-to-source-text/json_inspector.py 0-INBOX/temp/$C/<stem>.json` and confirm the `css_class` set is only `centered, nikaya, book, chapter, subhead, bodytext, gatha1–3, gathalast` (plus `unindented`/`indent`, and `sutta` in a vagga volume). Any other class: stop and decide its role with the human.
4. **Segment JSON → markdown** (json-to-source-text's existing converter; in tree mode `python3 -I $S/tree_to_md.py <stem>.json <stem>.md` instead), then make the working copy:
   ```bash
   python3 4-SYSTEM/Skills/json-to-source-text/converters/tipitaka_org_book.py 0-INBOX/temp/$C/<stem>.json 0-INBOX/temp/$C/<stem>.md
   cp 0-INBOX/temp/$C/<stem>.md 0-INBOX/temp/$C/pi-$C-<book>.md
   python3 -I $S/prepare_ids.py <book> 0-INBOX/temp/$C/pi-$C-<book>.md
   ```
   `prepare_ids.py` sets `## … ^<book>-0` and splits every block whose `N.` is not on its first line; note each split it prints (Rule 7).
5. **Content IDs** (`apply.py`):
   a. `python3 -I $S/apply.py audit 0-INBOX/temp/$C/pi-$C-<book>.md` — expect `Detected book number: <book>`, **one** run `1→max`, no ANOMALY. Otherwise stop (Rule 3).
   b. `python3 -I $S/apply.py apply 0-INBOX/temp/$C/pi-$C-<book>.md --zones "1=@<line of the ## heading>"` — the empty label gives `^<book>-<N>`; the heading ID it sets is temporary.
6. **Heading IDs and pre-title**: `python3 -I $S/heading_ids.py <book> 0-INBOX/temp/$C/pi-$C-<book>.md`.
7. **Frontmatter**: `python3 -I $S/set_frontmatter.py 0-INBOX/temp/$C/pi-$C-<book>.md <stem> "<Nikāya>" "<volume label>"`.
8. **Verify**: `python3 -I $S/verify.py <book> 0-INBOX/temp/$C/pi-$C-<book>.md 0-INBOX/raw-data/$C/<stem>.mul.xml` — must print `PASS` (in a vagga volume it also checks that the `####` headings are exactly the sutta headings). On any problem, fix the cause (script or source handling), regenerate from step 3, and verify again; never hand-patch the draft.
   Then the independent heading check: `python3 -I $S/check_headings.py 0-INBOX/temp/$C/pi-$C-<book>.md 0-INBOX/raw-data/$C/<stem>.mul.xml` must print `ALL MATCH` (every XML heading, in order, with the same text).
9. **Check against tipitaka.app** (the website reading of the same CSCD edition):
   ```bash
   python3 -I $S/fetch_site.py 0-INBOX/tipitaka-app <key> [<key> …]
   python3 -I $S/compare_site.py <book> 0-INBOX/temp/$C/pi-$C-<book>.md 0-INBOX/tipitaka-app/<key>.text.json 0-INBOX/tipitaka-app/<key>.toc.json
   ```
   Must print `PASS`: every md line matches one site paragraph in order, every site paragraph number (`n`) sits in block `^<book>-<n>`, and every contents-tree node matches in title, order and nesting. Contents titles are compared without `[variant readings]`, which the site leaves out of them. The site counts the piṭaka as a level the source does not print, so a **constant** depth offset (e.g. `site depth = md level + 1`) is expected; anything else is a problem. On a mismatch, find the cause in the scripts, regenerate from step 3, and rerun steps 8–9.
10. **Report** to the human: per file — content-ID range, `U` blocks, heading count, chapter count, word count, the site match counts, every split from step 4. Ask for approval to move into `1-SOURCES/Text/`.
11. **Move on approval**: `mv -n 0-INBOX/temp/$C/pi-$C-<book>.md 1-SOURCES/Text/`, then rerun steps 8–9 on the moved file. (Replacing an existing `1-SOURCES/` file needs the human's explicit approval for that file.)

---

## Completion check

- [ ] Download approved in chat before it ran; XML stored in `0-INBOX/raw-data/<collection>/`
- [ ] `apply.py audit` showed one run, no anomaly, correct book number
- [ ] Every content ID is `^<book>-<N>` or `^<book>-U<k>`, equal to the XML's printed paragraph numbers, contiguous wherever the source is
- [ ] Every heading ends `-0`; `#` is `^0`, `##` is `^<book>-0`, homage is `^T-1`
- [ ] `verify.py` prints `PASS` (IDs, `###`/`####` structure, identical word stream, bold spans equal to the XML's)
- [ ] `compare_site.py` prints `PASS` against tipitaka.app (text, paragraph numbers, contents tree)
- [ ] Every split / `U` block reported to the human
- [ ] File moved into `1-SOURCES/Text/` only after approval, and re-verified there
- [ ] Nothing committed, pushed, translated or uploaded

---

## Notes

`apply.py` reads the book number from the `##` line's `^<book>-0`, which step 4 sets. The scripts were first run on the Dīgha Nikāya (s0101m–s0103m, 2026-11-13, all PASS against the XML and tipitaka.app).

**Aṅguttaranikāya** (11 nipātas, s0401m … s0404m4, one file per nipāta) dry run, 2026-11-16, in a scratch folder, in tree mode.
- All 11 PASS `verify.py --tree` and `check_headings.py`; all 11 PASS `compare_site.py`.
- 1,877 content IDs, including 90 printed ranges. Catukkanipāta's gap 105 → 107 is as printed.
- The homage carries `n="0"` in four files; it is not a printed number and stays `^T-1`.
- `fetch_site.py` pages over a book's own slice of its volume (`start`/`end` from the parent listing) and retries HTTP 5xx.
- After the AN changes, the DN, MN and SN files regenerate byte-identical (except `pi-sn-5-tiika`'s hand-made `[Ed:]` note).

**Saṃyuttanikāya** (s0301m–s0305m) dry run, 2026-11-14, in a scratch folder.
- All five PASS `verify.py`: 271 / 246 / 362 / 361 / 621 content IDs, including 93 printed ranges; the Mahāvagga's 11 gaps are as printed.
- Segment counts equal the site's: 3450 / 1427 / 1467 / 2020 / 2847, with 48 + 5 `hangnum`s handled.
- Volumes 1, 2 and 4 PASS `compare_site.py`. Volumes 3 and 5 differ only in site artefacts: the site nests unnumbered or misprinted sutta headings one level deeper (`9.Khayadhammasuttaṃ`; five abbreviated suttas in Bojjhaṅgasaṃyutta), and it shows the five number-only paragraphs on their heading lines.
- After the SN changes, the DN and MN files regenerate byte-identical.

**Majjhimanikāya** (s0201m–s0203m) dry run, 2026-11-13, in a scratch folder: all three PASS `verify.py` and `compare_site.py`.
- 513 / 486 / 463 content IDs and 50 / 50 / 52 suttas.
- Segment counts equal the site's: 1796 / 1684 / 1460.
- The 10 `hangnum` paragraphs were joined: ¶513; ¶76, 456–460; ¶135, 237, 382.
- After the MN changes, the DN files regenerate byte-identical and still PASS.

CSCD quirks already handled:
- an untagged dot after a paragraph number (DN Mahāvagga 389);
- no space after the dot (DN Mahāvagga 335–342, 354, 370);
- number-only `hangnum` paragraphs (MN);
- `<note>`s inside sutta headings (MN Uparipaṇṇāsa 2, 5). The skill is generic to any CSCD Pāli vault and should be contributed to the shared skill library.
