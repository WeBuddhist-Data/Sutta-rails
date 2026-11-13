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

---

## Rules

1. **Never edit wording or a printed number.** Mechanical changes only: page markers dropped, `<note>` as `[…]`, `‘‘ ’’` as `"`, the chapter number stripped from `###` headings, and the h1 layer label added. `verify_commentary.py` must show an identical word stream.
2. **Link exactly what is printed.** A printed range is expanded, and a truncated tail (`65-6.` = 65–66) is completed for linking only, with the text kept as printed. A citation that cannot be read, or that names no existing root block (`504-407.`, `292-3-6.`), is **not** linked: it is logged in `….unresolved.json` and reported for a reviewer, never guessed.
3. **Links only before cited paragraphs.** A transclusion group sits directly before the paragraph that opens with the citation, and it never sits before a heading.
4. **One work, one file.** A work that CSCD splits over volumes is joined (`merge_parts.py`). Every line is kept; a later volume's opening lines become plain text blocks, as tipitaka.app shows them.
5. **Front matter is a human decision.** `--frontmatter` is used only for an opening section that precedes the commentary on the first sutta. It must be confirmed with the human and recorded in the report.
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
     [--commentary 1-SOURCES/Commentaries/pi-$C-<book>-atthakatha.md] [--frontmatter "<heading>"]
   ```
   Read the printed summary: transclusions, content blocks, unresolved, abbreviated ranges.
5. **(in step 4)** IDs come from `apply_commentary_ids.py`. To preview the heading tree without writing, run it on its own with `audit`.
6. **(in step 4)** The unresolved log is written next to the draft.
7. **Verify against the XML**:
   ```bash
   python3 -I $S/verify_commentary.py $T/pi-$C-<book>-<layer>.md 1-SOURCES/Text/pi-$C-<book>.md 0-INBOX/raw-data/$C/<stem>.xml [<stem2>.xml]
   ```
   It must print `PASS`: IDs contiguous, words identical, and every printed citation linked right or logged as unresolved.
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
     - a site artefact, such as a synthetic contents node or a book-level section with no contents node.
   - Fix anything else in the scripts, and rerun from step 3.
9. **Report** (`0-INBOX/pi-$C-commentary-report.md`):
   - per file: content-ID range, headings, words, citations linked / unresolved, and site matches;
   - the front-matter decisions;
   - the joined volumes;
   - every unresolved citation, with the evidence (the ṭīkā's number, the site's link);
   - every explained site difference.
   
   Then ask for approval.
10. **On approval:** add the `registered_id`s to annex §3, then `mv -n $T/pi-$C-<book>-<layer>.md 1-SOURCES/Commentaries/`. Rerun steps 7–8 on the moved files, passing `--unresolved $T/pi-$C-<book>-<layer>.unresolved.json` to `verify_commentary.py` (the logs stay in `0-INBOX/`).

---

## Completion check

- [ ] Root file in `1-SOURCES/Text/` already verified
- [ ] Download approved before it ran
- [ ] Segment counts equal tipitaka.app's paragraph counts (joined works included)
- [ ] `verify_commentary.py` prints `PASS` for every file
- [ ] `compare_site_commentary.py`: text matches every site paragraph; every tree or link difference explained in the report
- [ ] Every unresolved citation reported with its evidence, unlinked, with the text as printed
- [ ] Front-matter heading choices confirmed and recorded
- [ ] `registered_id`s added to annex §3 before the move; files moved only after approval and re-verified there
- [ ] Nothing committed, pushed, translated or uploaded

---

## Notes

First run: Dīghanikāya, 2026-11-13. Seven works: aṭṭhakathā ×3, ṭīkā ×3, and the abhinavaṭīkā joined from s0104t + s0105t. All pass against the XML. On tipitaka.app the text matches line for line, and the only differences are the explained cases above.

CSCD shapes handled:
- A volume with no `<div>`s, where chapters are `<p rend="chapter">` (the abhinavaṭīkā).
- A heading after the last sutta `<div>` has closed (Nigamanakathā), which becomes its own `###`.
- No space after a printed range (`32-33.Text`).
- Truncated-tail ranges.
