# Saṃyuttanikāya — structure, hierarchy and alignment (pre-intake)

**Checked:** 2026-11-14.
**Sources:**
- VipassanaTech/tipitaka-xml `romn/`: 15 files in `0-INBOX/raw-data/sn/`, byte-identical to the repo by git blob SHA.
- tipitaka.app: `sn-1..5`, `atta-sn-1..5`, `tika-sn-1..5` (text, contents tree, links) in `0-INBOX/tipitaka-app/`.

**Status:** ingested 2026-11-14 (§7), uploaded to library-prod 2026-11-16 (§8). Not committed or pushed.

---

## 1. The files

| Vault file (proposed) | Volume | CSCD root | Aṭṭhakathā | Ṭīkā | Site key |
|---|---|---|---|---|---|
| `pi-sn-1.md` | Sagāthāvaggo | `s0301m.mul.xml` | `s0301a.att.xml` | `s0301t.tik.xml` | `sn-1` |
| `pi-sn-2.md` | Nidānavaggo | `s0302m.mul.xml` | `s0302a.att.xml` | `s0302t.tik.xml` | `sn-2` |
| `pi-sn-3.md` | Khandhavaggo | `s0303m.mul.xml` | `s0303a.att.xml` | `s0303t.tik.xml` | `sn-3` |
| `pi-sn-4.md` | Saḷāyatanavaggo | `s0304m.mul.xml` | `s0304a.att.xml` | `s0304t.tik.xml` | `sn-4` |
| `pi-sn-5.md` | Mahāvaggo | `s0305m.mul.xml` | `s0305a.att.xml` | `s0305t.tik.xml` | `sn-5` |

There is no abhinavaṭīkā on the Saṃyuttanikāya in the repo.

## 2. Hierarchy

The XML has: book `<div>` → `<div type="samyutta">` (head `chapter`) → vagga `<p rend="title">` → sutta `<p rend="subhead">`. The files keep that tree:

```
## Sagāthāvaggo ^1-0
### Devatāsaṃyuttaṃ ^1-1-0                 saṃyutta
#### Naḷavaggo ^1-1-1-0                     vagga
##### Oghataraṇasuttaṃ ^1-1-1-1-0           sutta
### Bhikkhunīsaṃyuttaṃ ^1-5-0               a saṃyutta with no vaggas:
#### Āḷavikāsuttaṃ ^1-5-1-0                 sutta directly under it
```

- **Saṃyuttas:** 11 / 10 / 13 / 10 / 12. About half have no vaggas; their suttas sit directly under the saṃyutta, as in the XML.
- **Every `subhead` in the root is a sutta.** The unnumbered ones are abbreviated (peyyāla) suttas, or the misprint `9.Khayadhammasuttaṃ`.
- **The one `title` that is not a vagga** is `9. Antarapeyyālaṃ` (Nidānasaṃyutta). It is kept at vagga level.
- **Closing section:** Sagāthāvagga ends with a section after its last saṃyutta, `Sagāthāvaggo paṭhamo.` + uddāna. It is its own `###`, like the DN's Nigamanakathā.

## 3. Paragraph numbers

| | Content IDs | Printed ranges | Gaps as printed | Number-only `hangnum` | `U` blocks |
|---|---|---|---|---|---|
| pi-sn-1 | `^1-1`…`^1-271` | 0 | 0 | 48 joined to their gāthā | 1 |
| pi-sn-2 | `^2-1`…`^2-246` | 0 | 0 | — | 2 |
| pi-sn-3 | `^3-1`…`^3-716` | 27 | 0 | — | 0 |
| pi-sn-4 | `^4-1`…`^4-420` | 16 | 0 | — | 0 |
| pi-sn-5 | `^5-1`…`^5-1201` | 50 | 11 | 5 kept as number-only blocks | 12 |

- **A printed range** (`225-240.`) is one paragraph, and its ID is the range as printed: `^3-225-240`. tipitaka.app gives the same paragraph `n: "225-240"`.
- **Mahāvagga gaps:**
  - The 11 gaps are the XML's own. One paragraph number covers a run of abbreviated suttas, so `270.` is followed by `280.`.
  - The gaps: 270→280, 280→292, 292→302, 302→311, 552→587-596, 608→641-650, 662→673-684, 716→749-758, 770→792-802, 856→889-898, 934→967-976.
- **Number-only paragraphs before a heading**, Mahāvagga `312-323`, `324-333`, `334-345`, `346-356`, `357-366`:
  - A vagga of fully abbreviated suttas prints only its number and a heading.
  - Each is kept where the XML has it, as a block holding just the number (`312-323 ^5-312-323`).
  - tipitaka.app puts the number on the heading line.
  - No commentary cites these numbers.
- **`U` blocks** hold paragraphs the source prints without a number: the uddāna and closing lines of a section with no numbered paragraph, and the texts of unnumbered abbreviated suttas.

## 4. Results

### Root texts

| File | XML: words, IDs, bold | XML: every heading in order | tipitaka.app |
|---|---|---|---|
| pi-sn-1 | PASS | 307 / 307 | PASS |
| pi-sn-2 | PASS | 281 / 281 | PASS |
| pi-sn-3 | PASS | 369 / 369 | explained (a) |
| pi-sn-4 | PASS | 381 / 381 | PASS |
| pi-sn-5 | PASS | 713 / 713 | explained (a, b) |

### Commentaries

| File | XML | Headings in order | Citations | tipitaka.app |
|---|---|---|---|---|
| sn-1 aṭṭhakathā | PASS | 291 / 291 | 270 linked, 0 wrong | PASS |
| sn-2 aṭṭhakathā | PASS | 221 / 221 | 188 linked, 0 wrong | PASS |
| sn-3 aṭṭhakathā | PASS | 138 / 138 | 112 linked, 0 wrong | PASS |
| sn-4 aṭṭhakathā | PASS | 188 / 188 | 156 linked, 0 wrong | PASS |
| sn-5 aṭṭhakathā | PASS | 289 / 289 | 233 linked, 0 wrong | PASS |
| sn-1 ṭīkā | PASS | 306 / 306 | 269 linked, 0 wrong; 18 own front-matter numbers unlinked | PASS (notes: its own front-matter numbers paired by the site; 1 nesting) |
| sn-2 ṭīkā | PASS | 224 / 224 | 188 linked, 0 wrong | PASS (notes: 4 nesting; 8 single number vs range) |
| sn-3 ṭīkā | PASS | 135 / 135 | 109 linked, 0 wrong | PASS (notes: 1 nesting; 1 single number vs range) |
| sn-4 ṭīkā | PASS | 181 / 181 | 149 linked, 0 wrong | PASS |
| sn-5 ṭīkā | PASS | 267 / 267 | 210 linked, 0 wrong | PASS (notes: 3 nesting; 2 single number vs range) |

- **Commentary segment counts** equal tipitaka.app's in all ten. All ten pass the site check: text line for line, the contents tree, and every site citation link (the notes are explained kinds).
- **Cited ranges** link to the root block or blocks that hold those numbers, each block once.
- **Mahāvagga, both layers:** three wide cited ranges (`531-650.`, `651-704.`, `705-812.`) span the root's printed gaps. They link to every root block in the range that exists; the numbers with no root block are logged as unresolved.
- **Truncated tails**, expanded for linking only: Mahāvagga `1004-5.`, `1008-9.`, `1017-18.`, `1073-75.` …
- **Bold:** one XML bold tag is empty (`<hi rend="bold"></hi>`, `s0301a`, "kāṇakuṇiādīnaṃ****nīharaṇena"). It is copied tag for tag; the site drops it.

### 4a. Explained differences from tipitaka.app

These are site artefacts; the files follow the XML.
- **(a)** The site nests an unnumbered or misprinted sutta heading one level under the sutta before it. This affects `9.Khayadhammasuttaṃ` (Rādhasaṃyutta; a numbered sutta with no space after its number) and five suttas in Bojjhaṅgasaṃyutta. The XML gives them the same class as every other sutta heading.
- **(b)** The five number-only paragraphs are shown on their heading lines (§3).

## 5. Decisions for a human

1. **The five Bojjhaṅga headings** after `1. Aṭṭhikamahapphalasuttaṃ` (Aññataraphala, Mahattha, Yogakkhema, Saṃvega, Phāsuvihāra) are unnumbered, and the next sutta is `2.`. They may be sub-suttas of sutta 1, as tipitaka.app nests them. The files keep them at sutta level, as the XML marks them.
2. **Commentary heading IDs:**
   - Saṃyutta IDs always equal the root's (111 / 111).
   - Vagga and sutta IDs often differ, because the commentaries skip vaggas and suttas they do not comment on, and heading IDs are sibling positions (annex §2).
   - The alignment is carried by the transclusions and is not affected.
   - The alternative is to number commentary vagga and sutta headings by their **printed** numbers, which equal the root's positions. That is a change to the annex rule.
3. **Annex entries:**
   - books 1–5 → `pi-sn-1..5.md`, keys `sn-1..5`;
   - range IDs `^<b>-<A>-<B>`;
   - number-only blocks;
   - commentary IDs `sn-1..5-atthakatha`, `sn-1..5-tiika`;
   - SN 1 front matter `Ganthārambhakathā` / `Ganthārambhakathāvaṇṇanā` with `--unlinked`.

## 6. Skill changes made (vault copies)

Shared by the DN and MN intake:
- **Paragraph ranges:** `tipitaka_org_book.py`, `prepare_ids.py`, `apply.py`, `verify.py`.
- **Number-only blocks:** `cscd_xml_to_json.py`.
- **Closing section as `###`:** `tipitaka_org_book.py`, `verify.py`.
- **Range heading numbers stripped** (`1-10.`, `4-5-6.`): both converters and both checkers.
- **Commentary links** to the root blocks that cover a cited number: `commentary_converter.py`, `verify_commentary.py`.
- **Empty bold spans counted:** `bold_check.py`.

**DN and MN regression:** all 19 files regenerate byte-identical from the XML, and every checker still passes on them.

## 7. Ingested (2026-11-14)

- **Annex:**
  - §1–§2: the five volumes, the heading levels, the paragraph runs, ranges, gaps, number-only blocks and `U` blocks;
  - §3: the ten commentary IDs `sn-1..5-atthakatha`, `sn-1..5-tiika` and the SN 1 front matter.
- **Files:** `1-SOURCES/Text/pi-sn-1..5.md` and `1-SOURCES/Commentaries/pi-sn-1..5-atthakatha.md`, `pi-sn-1..5-tiika.md`. They were built in `0-INBOX/temp/sn/` and `0-INBOX/temp/sn-comm/`, moved with `mv -n`, and checked again in place:
  - all 15 PASS against the XML;
  - every heading is present in order;
  - the commentaries link 2,162 citations right, 0 wrong;
  - tipitaka.app: all 10 commentaries and pi-sn-1, 2, 4 PASS; pi-sn-3 and 5 have only the site artefacts in §4a.
- **Unresolved logs:** they stay in `0-INBOX/temp/sn-comm/*.unresolved.json`.
- **Library fields:** `license: cc0`, `tag_ids: [296WZOr8MXWteSqBBI7pl]` and `category_id: MZUUxphQ0yFwLBon3Vng8`, the same as the DN and MN. They are not uploaded; confirm the category before any upload.
- **Decisions §5.1–5.2:** kept as built. The Bojjhaṅga headings are at sutta level, and commentary heading IDs are sibling positions.

## 8. Uploaded to library-prod.webuddhist.com (2026-11-16)

Uploaded 2026-11-16 to library-prod.webuddhist.com with `0-INBOX/temp/upload-dn23-sn.sh`. For each file: lint, parse, dry run with live checks, `--execute`, `--verify`; the logs are `0-INBOX/temp/upload-dn23-sn-batch1.log` and `upload-dn23-sn.log`. The library IDs are in each file's frontmatter and in both upload ledgers.

What was checked: the IDs in the files equal the ledgers; each commentary's live `commentary_of` is its root's `text_id`, and it is aligned to its root's edition; live segments equal the file's blocks.

**Library titles.** The library allows each title once per language, and "Mahāvagga" is a book name in all three piṭakas. Five titles were taken: by the Vinaya vault's uploaded `Mahāvaggapāḷi` and `Mahāvagga-aṭṭhakathā`, and by each other (`Mahāvaggaṭīkā` twice). They got the nikāya in brackets: `Mahāvaggapāḷi (Dīghanikāya)`, `Mahāvaggaṭṭhakathā (Dīghanikāya)`, `Mahāvaggaṭīkā (Dīghanikāya)`, `Mahāvagga-aṭṭhakathā (Saṃyuttanikāya)` and `Mahāvaggaṭīkā (Saṃyuttanikāya)`. Only the frontmatter `title` changed; the text and its printed headings are as in the source.

The upload ran with `SSL_CERT_FILE` set to certifi's bundle, because this Python (python.org 3.13) has no CA file of its own.

| File | Library title | text_id | edition_id | toc_id | Segments | Alignment pairs → root edition |
|---|---|---|---|---|---|---|
| pi-sn-1 | Sagāthāvaggo | `27iSZQ2XEEw9iZfgYqHTU` | `SxPJdoL6EYy69LzgosNl4` | `DCavYXa7s8nNZCQUPzmT7` | 273 | — |
| pi-sn-1-atthakatha | Sagāthāvagga-aṭṭhakathā | `KZTgptTudglEbV9dpo3AI` | `Ve7j7X1ooyXaW6Bl2sG8F` | `nv4t3f7cBwKbuHRQEPbGx` | 1077 | 1055 → `SxPJdoL6EYy69LzgosNl4` |
| pi-sn-1-tiika | Sagāthāvaggaṭīkā | `GZ0WUO1QJkBdFtspoNspw` | `83Nr7uuL1ELPuVZE7TMN8` | `071SUrtxO1ANlLfMFp9aB` | 1349 | 1284 → `SxPJdoL6EYy69LzgosNl4` |
| pi-sn-2 | Nidānavaggo | `DgA6j95JeMKK42tNQiGEc` | `YoJWvxGo8kWCHTlOVSowG` | `PtTs0dstXAoXFuygVykWw` | 249 | — |
| pi-sn-2-atthakatha | Nidānavagga-aṭṭhakathā | `kWsKgKlpZw4FwNF6EfEmS` | `nNeRVPtTCvRpVtDtDYWAz` | `fOywSoxrztCoO5SuXI9rh` | 719 | 872 → `YoJWvxGo8kWCHTlOVSowG` |
| pi-sn-2-tiika | Nidānavaggaṭīkā | `TcfuW82WDl0itrJxnok6Z` | `lVLQYi4TnEEaGOykJxyRJ` | `X1uQ4TekX5SGXHdGUcjCy` | 793 | 1003 → `YoJWvxGo8kWCHTlOVSowG` |
| pi-sn-3 | Khandhavaggo | `J2ZsEPJjQFrfo2CCDuNeP` | `vHMiuor2liUwl2rnB489Z` | `mowrLTLJhI7vqxQDJkqh9` | 363 | — |
| pi-sn-3-atthakatha | Khandhavagga-aṭṭhakathā | `4qJueCPxEzQYBzUgwVgVy` | `ystx56iHMcOBklV8Ouucg` | `6tY7c3bm6Fm1pjBbaHPfH` | 325 | 936 → `vHMiuor2liUwl2rnB489Z` |
| pi-sn-3-tiika | Khandhavaggaṭīkā | `P4NP58LfF0OTNbbtzjOkQ` | `937KiS1eArKQSR3XsmHFh` | `ej3ox6NIjvF6clBLKQOqM` | 382 | 1230 → `vHMiuor2liUwl2rnB489Z` |
| pi-sn-4 | Saḷāyatanavaggo | `RSvOaRm9QIE61XrVd5tiE` | `12ENMdnweU9YYf34m8ggh` | `GTcj4QEc4U7oukYSacCv2` | 362 | — |
| pi-sn-4-atthakatha | Saḷāyatanavagga-aṭṭhakathā | `Lx5BPtbdlcPfNMB61RSMG` | `YIImAHf7JPj4sDr2Gr4Gb` | `67CmwlXlXsuyaxCn63eCq` | 565 | 986 → `12ENMdnweU9YYf34m8ggh` |
| pi-sn-4-tiika | Saḷāyatanavaggaṭīkā | `5BkHu8zNjwH9BRQk6OFDw` | `7mPluYBnqPoRziahy6cW0` | `FHK2Xx9mCcEdLH7hOzNYW` | 544 | 1077 → `12ENMdnweU9YYf34m8ggh` |
| pi-sn-5 | Mahāvaggo | `b2JsBPaz7NdwPn2gmoCxI` | `a5fF7CygDzI4dI5hZ6qda` | `5GRtbTXvpWYAsxUH09e4G` | 634 | — |
| pi-sn-5-atthakatha | Mahāvagga-aṭṭhakathā (Saṃyuttanikāya) | `BSnbTY8ub0cqssPCzwAPT` | `6Loc3FMKaSQmbF2sFM8Zq` | `j7SrSSaC7xtZccL6t3I9X` | 691 | 1095 → `a5fF7CygDzI4dI5hZ6qda` |
| pi-sn-5-tiika | Mahāvaggaṭīkā (Saṃyuttanikāya) | `QSgUbNyjbrqsuYXZS84gz` | `fwvCHC4E47Q7tMKO6XnEf` | `m6ClCynLmn8GXaUIaSEe9` | 580 | 1085 → `a5fF7CygDzI4dI5hZ6qda` |
