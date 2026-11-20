---
name: cscd-commentary-intake
description: Bring a Pāli commentary (aṭṭhakathā, ṭīkā, abhinavaṭīkā …) from VRI's Chaṭṭha Saṅgāyana (CSCD) XML into 1-SOURCES/Commentaries/ as a block-ID'd markdown file whose paragraphs link to the root paragraphs they cite — download the .att/.tik/.nrf XML, convert to segment JSON (joining multi-volume works), convert with root links from the printed citations, add frontmatter and block IDs, then verify word-for-word and citation-for-citation against the XML and against tipitaka.app's text, contents tree and links. Use when someone says "ingest the commentaries for <nikāya/vagga>", "bring in the aṭṭhakathā / ṭīkā", "align the commentary with the root", or "do the Pāli commentaries next".
profile: rails-vault
---

# cscd-commentary-intake

Produces one commentary file per CSCD commentary work in `1-SOURCES/Commentaries/` (e.g. `pi-dn-1-atthakatha.md`), aligned to a root text that `cscd-root-text-intake` already brought in.

Each commentary paragraph is one block with an internal running ID `^<book>-<k>`. A paragraph that opens with a printed number or range (`149.`, `32-33.`) is preceded by one transclusion per root paragraph it cites (`![[1-SOURCES/Text/pi-dn-1.md#^1-149]]`), and the printed number stays in the text. Those transclusions are the commentary↔root alignment.

The skill exists so that every work goes through the same chain and is proven, before anything cites it, to have:
- the XML's exact words;
- one correct set of links per printed citation;
- the same text, contents and links as tipitaka.app's reading of the same edition, apart from differences that are explained.

**Root text first.** The commentary links to a root file's block IDs, so that root file must already be in `1-SOURCES/Text/`. **Pāli only:** no translation, upload or commit.

---

## Inputs

| Input | What | Example |
|---|---|---|
| CSCD stem(s) per work | One stem, or several for a work CSCD splits over volumes, from `github.com/VipassanaTech/tipitaka-xml` `romn/` | `s0101a.att`; `s0104t.nrf` + `s0105t.nrf` |
| Root file | The root volume it comments on, in `1-SOURCES/Text/` | `1-SOURCES/Text/pi-dn-1.md` |
| File name and `registered_id` | From the vault annex §3 (registered there before use) | `pi-dn-1-atthakatha.md`, `dn-1-atthakatha` |
| Layer and label | `layer:` value and the h1 label | `atthakatha` / `aṭṭhakathā`, `tiika` / `ṭīkā`, `abhinavatiika` / `abhinavaṭīkā` |
| Aṭṭhakathā file | For a ṭīkā: the aṭṭhakathā it explains (`commentary:` field) | `1-SOURCES/Commentaries/pi-dn-1-atthakatha.md` |
| Front-matter heading | Only if the work opens with a section that stands apart from the commentary on the first sutta (a human judgment) | `Ganthārambhakathā` |
| Unlinked heading(s) | Only if a section numbers its own paragraphs, so that its leading numbers are **not** root citations (a human judgment) | `Ganthārambhakathāvaṇṇanā` (Mūlapaṇṇāsa-ṭīkā, 1.–16.) |
| Book in the volume | Only for a CSCD volume that holds several works as separate `<div type="book">`s (AN: `s0402a` = Duka-, Tika-, Catukkanipāta): `--book K` to `cscd_xml_to_json.py` and `verify_commentary.py`, one vault file per book | `--book 2` |
| Tree mode | When the root was converted with `--tree`: pass `--tree` to `cscd_xml_to_json.py` for the commentary too | AN |
| Per-section | When the root has per-section IDs `^<book>-<section>-<N>`: `--per-section` to `build_commentary.py`, `verify_commentary.py` and `compare_site_commentary.py`. A citation links within the section that the last numbered `###` heading names (`6. Ratanasuttavaṇṇanā` → `^1-6-…`). | Khuddakapāṭha |
| tipitaka.app keys | The commentary's key, and the root's | `atta-dn-1`, `tika-dn-1`, `tika2-dn-1`; root `dn-1` |
| Human approval | Download (names, source, sizes), and the move into `1-SOURCES/` | — |

Required sibling skill: `4-SYSTEM/Skills/cscd-root-text-intake/` (its `cscd_xml_to_json.py` and `fetch_site.py`). If it is missing, stop.

## Output

- `0-INBOX/raw-data/<collection>/<stem>.xml` — downloaded XML (untouched).
- `0-INBOX/temp/<collection>-comm/<stem>.json` — segment JSON (scratch); `<a>-<b>.json` for a joined work.
- `0-INBOX/temp/<collection>-comm/pi-<collection>-<book>-<layer>.md` — the draft, plus `….unresolved.json` (citations not linked, abbreviated ranges expanded).
- `0-INBOX/tipitaka-app/<key>.text.json`, `.toc.json`, `.links.json` — site data for the check.
- After approval: `1-SOURCES/Commentaries/pi-<collection>-<book>-<layer>.md`.

---

## Output file format

```markdown
---
title: Sīlakkhandhavaggaṭṭhakathā
language: Pali
script: Roman (PTS diacritics)
file_type: commentary
registered_id: dn-1-atthakatha
lang_tag: pi
verse_id_format: book-verse
pitaka: sutta
nikaya: Dīghanikāya
layer: atthakatha
root_text: 1-SOURCES/Text/pi-dn-1.md
commentary: <only for a ṭīkā: the aṭṭhakathā file>
source_description: "VRI Chaṭṭha Saṅgāyana (CSCD) romanised XML, s0101a.att.xml. …"
source_filename: s0101a.att.xml
source: "https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn/s0101a.att.xml"
other_ids:
  - tipitaka.org: s0101a
---

Namo tassa bhagavato arahato sammāsambuddhassa ^T-1

# Dīghanikāye (aṭṭhakathā) ^0

## Sīlakkhandhavaggaṭṭhakathā ^1-0

### Ganthārambhakathā ^1-I-0          ← front matter: Roman, own counter

#### Nidānakathā ^1-I-I-0

### Brahmajālasuttavaṇṇanā ^1-1-0    ← sutta k of the vagga = ^<book>-k-0, as in the root

#### Paribbājakakathāvaṇṇanā ^1-1-1-0

![[1-SOURCES/Text/pi-dn-1.md#^1-1]]

1. Evaṃ me sutanti … ^1-37

Tattha evanti … ^1-38                 ← in the scope of the link above until the next link group or heading
```

- `# <nikāya> (<layer label>) ^0` carries the layer label; it is the one editorial addition to the text.
- Content IDs `^<book>-<k>` count every content block in document order. Transclusion lines carry no ID.
- Headings: sibling position, Arabic; Roman only inside the named front-matter subtree.
- **Volumes whose suttas sit inside vaggas** (Majjhimanikāya) nest one level deeper:
  - `### <vagga> ^<book>-<v>-0`
  - `#### <sutta>vaṇṇanā ^<book>-<v>-<k>-0`, the same IDs as the root's suttas
  - `#####` sub-headings
  - `######` for a numbered list a ṭīkā gives under a `title` (e.g. the 16 hāras under `Soḷasahāravaṇṇanā`), until the next unnumbered heading.

---

## Rules

1. **Never edit wording or a printed number.** Mechanical changes only: page markers dropped, `<note>` as `[…]`, `‘‘ ’’` as `"`, the chapter number stripped from `###` headings, and the h1 layer label added. Bold (`<hi rend="bold">`) is kept as `**…**` exactly where the XML's tags are, as tipitaka.app shows it: spaces and punctuation inside a tag stay inside (`**‘jātaka’**nti`, `**passatā. ** Sabba`), and nothing is moved, merged or dropped. Some such spans do not render as bold in Obsidian; that is accepted so the file copies the source. In the commentaries the bold marks the word being explained. `verify_commentary.py` must show an identical word stream (with `**` removed) and the same bold spans as the XML (`cscd-root-text-intake/scripts/bold_check.py`).
2. **Link exactly what is printed.** A printed range is expanded, and a truncated tail (`65-6.` = 65–66) is completed for linking only, with the text kept as printed. Each cited number links to the root block that holds it. That is `^b-N`, or a root range block `^b-A-B` that holds A–B (SN). Each block is linked once, in order. A cited number no root block holds is logged as unresolved. A citation that cannot be read, or that names no existing root block (`504-407.`, `292-3-6.`, `01` printed with no dot), is **not** linked: it is logged in `….unresolved.json` and reported for a reviewer, never guessed. Numbers in a section named with `--unlinked` are the section's own numbering. They are not linked and are logged under `unlinked_section_numbers`.
3. **Links only before cited paragraphs.** A transclusion group sits directly before the paragraph that opens with the citation, and it never sits before a heading.
4. **One work, one file.** A work that CSCD splits over volumes is joined (`merge_parts.py`). Every line is kept; a later volume's opening lines become plain text blocks, as tipitaka.app shows them. The same holds inside one file. Some files reprint homage, nikāya and book title partway through, with `(Paṭhamo bhāgo)` / `(Dutiyo bhāgo)` (MN Mūlapaṇṇāsa aṭṭhakathā and ṭīkā). `cscd_xml_to_json.py` keeps those lines as plain text, never as headings, so the vagga IDs stay equal to the root's.
5. **Front matter is a human decision.** `--frontmatter` is repeatable, for a work that opens with two front-matter sections (AN Ekaka-ṭīkā: `Ganthārambhakathā`, `Ganthārambhakathāvaṇṇanā` → `^1-I-0`, `^1-II-0`). A number that the XML does not mark as a paragraph number (no `@n`, e.g. the Dasaka-ṭīkā's own verse list `1.`–`12.`) is never a citation: it is not linked and is logged under `unlinked_section_numbers`. **The rest of this rule:** `--frontmatter` is used only for an opening section that precedes the commentary on the first sutta. It must be confirmed with the human and recorded in the report. The heading text can differ per layer: MN uses `Ganthārambhakathā` in the aṭṭhakathā and `Ganthārambhakathāvaṇṇanā` in the ṭīkā. `--frontmatter` changes heading IDs only, not links. If that section numbers its own paragraphs, also pass `--unlinked "<heading>"`, which is confirmed and recorded the same way. The run stops if the heading is not found.
6. **Unsupported XML shape stops the run.** If `cscd_xml_to_json.py` stops, extend it; never flatten.
7. **Every difference from tipitaka.app is explained in the report,** or the cause is fixed and the run repeated.
8. **Download, and move into `1-SOURCES/`, only with approval.** `registered_id`s go into annex §3 before the files move.
9. **No commit, push, translation or upload** as part of this skill.

---

## Procedure

Run from the vault root. `R=4-SYSTEM/Skills/cscd-root-text-intake/scripts`, `S=4-SYSTEM/Skills/cscd-commentary-intake/scripts`, `C=<collection>` (e.g. `dn`), `T=0-INBOX/temp/$C-comm`.

1. **Pre-flight.** The root file exists in `1-SOURCES/Text/` and passes `cscd-root-text-intake`'s checks. The file names and `registered_id`s are agreed with the human. No target file already exists in `1-SOURCES/Commentaries/` (if one does, stop and ask).
2. **Download** (after approval) into `0-INBOX/raw-data/$C/`: `curl -sfL -o … https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn/<stem>.xml`. Sizes come from `https://api.github.com/repos/VipassanaTech/tipitaka-xml/contents/romn`.
3. **XML → segment JSON**, per volume:
   ```bash
   python3 -I $R/cscd_xml_to_json.py 0-INBOX/raw-data/$C/<stem>.xml $T/<stem-without-ext>.json
   ```
   - The segment count must equal tipitaka.app's paragraph count for the book (`/api/children` `end`).
   - For a multi-volume work, also run:
     ```bash
     python3 -I $S/merge_parts.py $T/<a>-<b>.json $T/<a>.json $T/<b>.json
     ```
     The joined count must equal the site book's count. Note the opening lines it re-types.
4. **Convert, frontmatter, IDs** (steps 4–6 in one run):
   ```bash
   python3 -I $S/build_commentary.py $T/<json> 1-SOURCES/Text/pi-$C-<book>.md $T/pi-$C-<book>-<layer>.md \
     --registered-id <id> --layer <layer> --layer-label <label> --nikaya "<Nikāya>" \
     [--commentary 1-SOURCES/Commentaries/pi-$C-<book>-atthakatha.md] [--frontmatter "<heading>"] [--unlinked "<heading>"]
   ```
   Read the printed summary: transclusions, content blocks, unresolved, abbreviated ranges.
5. **(in step 4)** IDs come from `apply_commentary_ids.py`. To preview the heading tree without writing, run it on its own with `audit`.
6. **(in step 4)** The unresolved log is written next to the draft.
7. **Verify against the XML**:
   ```bash
   python3 -I $S/verify_commentary.py $T/pi-$C-<book>-<layer>.md 1-SOURCES/Text/pi-$C-<book>.md 0-INBOX/raw-data/$C/<stem>.xml [<stem2>.xml]
   ```
   It must print `PASS`: IDs contiguous, words identical, and every printed citation linked right or logged as unresolved. The log is matched occurrence by occurrence, so a logged `1.` exempts one unlinked `1.`, not every `1.` in the file.
8. **Check against tipitaka.app**:
   ```bash
   python3 -I $R/fetch_site.py 0-INBOX/tipitaka-app <key> [<key> …] --links
   python3 -I $S/compare_site_commentary.py $T/pi-…-atthakatha.md 0-INBOX/tipitaka-app <atta-key> <root-key>
   python3 -I $S/compare_site_commentary.py $T/pi-…-tiika.md 0-INBOX/tipitaka-app <tika-key> <root-key> $T/pi-…-atthakatha.md <atta-key>
   ```
   - Text must match every site paragraph.
   - For each listed difference (tree, links), find the cause:
     - a source misprint that is logged as unresolved;
     - a printed single number against a printed range of the same paragraph;
     - a site artefact. Examples:
       - a synthetic contents node: MN atta-mn-1 lists `Ganthārambhakathā` twice;
       - a section with no contents node: atta-mn-3 has no `Saḷāyatanavaggo`;
       - a printed number the site does not show (`01`);
       - nesting the site gets wrong after a ṭīkā's `title` groups: tika-mn-1 puts `Sabbāsavasuttavaṇṇanā` one level too deep.
   - Fix anything else in the scripts, and rerun from step 3.
9. **Report** (`0-INBOX/pi-$C-commentary-report.md`):
   - per file: content-ID range, headings, words, citations linked / unresolved, and site matches;
   - the front-matter decisions;
   - the joined volumes;
   - every unresolved citation, with the evidence (the ṭīkā's number, the site's link);
   - every explained site difference.
   
   Then ask for approval.
10. **On approval:** add the `registered_id`s to annex §3. A single-volume work (a KN book) moves as is. For a multi-volume work (DN, MN, SN, AN), build each volume against its per-volume root draft in `0-INBOX/temp/$C/`, verify it, then join the volumes with `cscd-root-text-intake/scripts/merge_volumes.py <out> <parts…> --title "<Nikāya>-<layer label>" --registered-id $C-<layer> --root-text 1-SOURCES/Text/pi-$C.md [--commentary 1-SOURCES/Commentaries/pi-$C-atthakatha.md] --relink 1-SOURCES/Text/pi-$C-<book>.md=1-SOURCES/Text/pi-$C.md …` (one `--relink` per volume), check it word for word against the XML volumes, and move the joined file. Otherwise `mv -n $T/pi-$C-<book>-<layer>.md 1-SOURCES/Commentaries/`. Rerun steps 7–8 on the moved files, passing `--unresolved $T/pi-$C-<book>-<layer>.unresolved.json` to `verify_commentary.py` (the logs stay in `0-INBOX/`).

---

## Completion check

- [ ] Root file in `1-SOURCES/Text/` already verified
- [ ] Download approved before it ran
- [ ] Segment counts equal tipitaka.app's paragraph counts (joined works included)
- [ ] `verify_commentary.py` prints `PASS` for every file
- [ ] `compare_site_commentary.py`: text matches every site paragraph; bold spans match the site's (the site's habit of joining two bold spans the XML keeps apart, and of dropping a bold tag that holds only a space, is printed as a note or ignored, not a problem; the XML is followed); every tree or link difference explained in the report
- [ ] Every unresolved citation reported with its evidence, unlinked, with the text as printed
- [ ] Front-matter heading choices confirmed and recorded
- [ ] `registered_id`s added to annex §3 before the move; files moved only after approval and re-verified there
- [ ] Nothing committed, pushed, translated or uploaded

---

## Notes

**Khuddakanikāya**, first two books, dry run 2026-11-16, tree mode. The two aṭṭhakathās have no `<div>`s at all.
- Khuddakapāṭha-aṭṭhakathā (per-section; `--frontmatter "Ganthārambhakathā"`) and Dhammapada-aṭṭhakathā (printed in two parts, kept as text) both PASS `verify_commentary.py` and `check_headings.py`.
- Citations: 67 and 436 linked right, 0 wrong.
- One citation is unresolved: the Khuddakapāṭha-aṭṭhakathā's `13.` on the Tirokuṭṭasutta, whose root prints only 12 verses. tipitaka.app links it to Maṅgalasutta v. 13 by number alone.
- In tree mode, a gāthā that opens with a real citation (a number-only line with `@n` joined to it) links to the root like prose.
- A paragraph number and its dot written as two tags with a space between them (`8 .`) are rendered `8.`.

**Aṅguttaranikāya** dry run, 2026-11-16. 22 works: an aṭṭhakathā and a ṭīkā per nipāta, cut from the four commentary volumes per layer with `--book K`, in tree mode.
- All 22 PASS `verify_commentary.py --book K` and `check_headings.py --book K`.
- Every citation is linked right or logged: 2,103 linked, 0 wrong, and 30 own section or verse numbers left unlinked.
- Lines outside a volume's books belong to the first book (before it) or the last (after it), as tipitaka.app has them. An example is `s0402t`'s closing `Dutiyo bhāgo niṭṭhito.`, which belongs to the Catukka-ṭīkā.
- tipitaka.app: 18 PASS; the other 4 differ only by site artefacts (no contents node for vaggas the XML gives as `<head>`s straight in the book; a ṭīkā verse number paired by number).
- tipitaka.app's commentary books are slices of their volume, so `compare_site_commentary.py` matches site paragraphs by their index `i`.

**Saṃyuttanikāya** dry run, 2026-11-14. Ten works: s0301a–s0305a, s0301t–s0305t.
- All ten PASS `verify_commentary.py`, with every heading present in order.
- Every citation is linked right or logged: 2,162, 0 wrong. That includes 256 cited ranges, linked to the root's range blocks.
- SN 1 needed `--frontmatter`: `Ganthārambhakathā` for the aṭṭhakathā; `Ganthārambhakathāvaṇṇanā` for the ṭīkā, plus `--unlinked` for the same heading (its own numbers 1.–19.).
- All five aṭṭhakathās PASS `compare_site_commentary.py`.
- One XML bold tag is empty (`<hi rend="bold"></hi>`, s0301a); it is copied as `****` and counted by `bold_check.py`.
- The commentaries skip suttas and vaggas they do not comment on, so their vagga and sutta heading IDs (sibling positions) often differ from the root's; saṃyutta IDs always match. The transclusions carry the alignment.

First run: Dīghanikāya, 2026-11-13. Seven works: aṭṭhakathā ×3, ṭīkā ×3, and the abhinavaṭīkā joined from s0104t + s0105t. All pass against the XML. On tipitaka.app the text matches line for line, and the only differences are the explained cases above.

**Majjhimanikāya** dry run, 2026-11-13, in a scratch folder, against MN root drafts that pass. Six works: s0201a–s0203a, s0201t–s0203t. There is no abhinavaṭīkā.
- All six PASS `verify_commentary.py`.
- Links: 438 / 354 / 306 citations linked in the aṭṭhakathā, 427 / 333 / 307 in the ṭīkā.
- Every vagga and sutta heading ID equals the root's.
- MN 1 needed `--frontmatter`: `Ganthārambhakathā` for the aṭṭhakathā; `Ganthārambhakathāvaṇṇanā` for the ṭīkā, plus `--unlinked` for the same heading (16 self-numbers, 1.–16.).
- Each MN 1 file logs one `01` as unresolved.
- Site differences are only the explained artefacts above.
- After the MN changes, the seven DN files regenerate byte-identical. They still PASS, and the site check prints the same output as before.

CSCD shapes handled:
- Bold copied tag for tag: 40,166 spans in the DN, including 283 with a space inside the tag and 2 that hold only a space (`sāvaṇamāsassa** **kāḷapakkha`).
- A volume with no `<div>`s, where chapters are `<p rend="chapter">` (the abhinavaṭīkā).
- A heading after the last sutta `<div>` has closed (Nigamanakathā), which becomes its own `###`.
- Suttas as numbered subheads inside vagga `<div>`s, and a ṭīkā's own numbered sub-heads that are not suttas (MN).
- A front-matter `<div>` with no head, and a part label `(Paṭhamo bhāgo)` before it (MN).
- A volume printed in two parts inside one file (MN Mūlapaṇṇāsa aṭṭhakathā and ṭīkā).
- No space after a printed range (`32-33.Text`).
- Truncated-tail ranges.
