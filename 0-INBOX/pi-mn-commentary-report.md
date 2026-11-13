# Majjhimanikāya — root texts and commentaries: intake report

**Date:** 2026-11-13
**Built with:** `4-SYSTEM/Skills/cscd-root-text-intake/` and `4-SYSTEM/Skills/cscd-commentary-intake/`
**Checked against:**
- VipassanaTech/tipitaka-xml `romn/`, in `0-INBOX/raw-data/mn/`. All 9 files are byte-identical to the repo's current versions (git blob SHA). The repo's `romn/` was last changed 2024-08-25.
- tipitaka.app `/api/children`, `/api/text` and `/api/links`, fetched 2026-11-13 into `0-INBOX/tipitaka-app/`.

This note is for someone opening the project cold. Pāli only: nothing is translated, uploaded or committed.

The nine files are in `1-SOURCES/`. They were moved there with approval and checked again in place. The logs of unlinked citations stay in `0-INBOX/temp/mn-comm/*.unresolved.json`. The structure analysis that came before the intake is in `pi-mn-structure-report.md`.

---

## The nine files

| File | ID | Work | CSCD source | tipitaka.app | Root |
|---|---|---|---|---|---|
| `Text/pi-mn-1.md` | book 1 | Mūlapaṇṇāsapāḷi | `s0201m.mul.xml` | `mn-1` | — |
| `Text/pi-mn-2.md` | book 2 | Majjhimapaṇṇāsapāḷi | `s0202m.mul.xml` | `mn-2` | — |
| `Text/pi-mn-3.md` | book 3 | Uparipaṇṇāsapāḷi | `s0203m.mul.xml` | `mn-3` | — |
| `Commentaries/pi-mn-1-atthakatha.md` | `mn-1-atthakatha` | Mūlapaṇṇāsa-aṭṭhakathā | `s0201a.att.xml` | `atta-mn-1` | `pi-mn-1.md` |
| `Commentaries/pi-mn-2-atthakatha.md` | `mn-2-atthakatha` | Majjhimapaṇṇāsa-aṭṭhakathā | `s0202a.att.xml` | `atta-mn-2` | `pi-mn-2.md` |
| `Commentaries/pi-mn-3-atthakatha.md` | `mn-3-atthakatha` | Uparipaṇṇāsa-aṭṭhakathā | `s0203a.att.xml` | `atta-mn-3` | `pi-mn-3.md` |
| `Commentaries/pi-mn-1-tiika.md` | `mn-1-tiika` | Mūlapaṇṇāsa-ṭīkā | `s0201t.tik.xml` | `tika-mn-1` | `pi-mn-1.md` |
| `Commentaries/pi-mn-2-tiika.md` | `mn-2-tiika` | Majjhimapaṇṇāsaṭīkā | `s0202t.tik.xml` | `tika-mn-2` | `pi-mn-2.md` |
| `Commentaries/pi-mn-3-tiika.md` | `mn-3-tiika` | Uparipaṇṇāsa-ṭīkā | `s0203t.tik.xml` | `tika-mn-3` | `pi-mn-3.md` |

- Book numbers, file names and heading levels are registered in annex §1–§2.
- The `registered_id`s are in annex §3.
- Each ṭīkā names its aṭṭhakathā in `commentary:`.

## Structure

```
## <paṇṇāsa> ^<b>-0
### <vagga> ^<b>-<v>-0
#### <sutta> ^<b>-<v>-<n>-0          (commentary: <sutta>vaṇṇanā, same ID)
##### <sub-heading> ^<b>-<v>-<n>-<m>-0
```

- Root content IDs are the printed paragraph numbers: `^1-1`…`^1-513`, `^2-1`…`^2-486`, `^3-1`…`^3-463`. There are no `U` blocks and no duplicates.
- Commentary content IDs are a continuous run. A paragraph that cites root paragraphs is preceded by one transclusion per cited paragraph.
- Every vagga and sutta heading ID in all six commentaries equals the root's (5 + 50, 5 + 50, 5 + 52).

## Results

| File | XML: words, IDs, bold | XML: every heading, in order | Citations | tipitaka.app |
|---|---|---|---|---|
| pi-mn-1 | PASS (513 IDs, 84,765 words) | 80 / 80 | — | PASS |
| pi-mn-2 | PASS (486 IDs, 94,472 words) | 56 / 56 | — | PASS |
| pi-mn-3 | PASS (463 IDs, 74,204 words) | 57 / 57 | — | PASS |
| mn-1 aṭṭhakathā | PASS (5,999 bold spans) | 141 / 141 | 438 linked, 0 wrong, 1 logged | explained (a, b) |
| mn-2 aṭṭhakathā | PASS | 56 / 56 | 354 linked, 0 wrong | PASS |
| mn-3 aṭṭhakathā | PASS | 65 / 65 | 306 linked, 0 wrong | explained (c) |
| mn-1 ṭīkā | PASS (12,361 bold spans) | 168 / 168 | 427 linked, 0 wrong, 1 logged, 16 section numbers unlinked | explained (a, d, e) |
| mn-2 ṭīkā | PASS | 56 / 56 | 333 linked, 0 wrong | PASS |
| mn-3 ṭīkā | PASS | 64 / 64 | 307 linked, 0 wrong | PASS |

Explained differences from tipitaka.app. Each is a site artefact; the files follow the XML.
- **(a)** CSCD prints a paragraph number `01` with no dot: `s0201a` "01 Bahinagareti …" and `s0201t` "01 Tesaṃ lābhāti …". The site does not show it. The file keeps it as printed, and the citation is logged as unresolved, not linked.
- **(b)** The site lists `Ganthārambhakathā` twice: once for the front-matter `<div>`, which has no head, and once for the real heading.
- **(c)** The site has no contents node for `5. Saḷāyatanavaggo` in the Uparipaṇṇāsa-aṭṭhakathā; it lists 4 vaggas.
- **(d)** After the ṭīkā's two `title` groups (Soḷasahāravaṇṇanā, Pañcavidhanayavaṇṇanā), the site nests the rest of the vagga one level too deep. For example, `2. Sabbāsavasuttavaṇṇanā` sits at depth 6, not at sutta depth 5.
- **(e)** The site pairs the ṭīkā's own front-matter numbers 1–16 with the aṭṭhakathā paragraphs that carry the same numbers, mostly its comments on root ¶2–16. That is a blind number match: the Ganthārambhakathāvaṇṇanā comes before any sutta. Here they are left unlinked.
- **Other site notes:** some bold spans are joined on the site but kept apart in the XML; the XML is followed. Two ṭīkā/aṭṭhakathā pairs print a single number on one side and a range on the other.

## Judgment calls (confirmed 2026-11-13)

1. **Number-only paragraphs** (`<p rend="hangnum">`, 10 paragraphs) are joined to the gāthā line that follows, as on tipitaka.app:
   - MN 1 ¶513
   - MN 2 ¶76, 456–460
   - MN 3 ¶135, 237, 382
2. **Front matter, MN 1:** `--frontmatter "Ganthārambhakathā"` in the aṭṭhakathā (IDs `^1-I-0`, `^1-I-I-0`), and `--frontmatter "Ganthārambhakathāvaṇṇanā"` in the ṭīkā.
3. **Unlinked section numbers:** `--unlinked "Ganthārambhakathāvaṇṇanā"` in the MN 1 ṭīkā. Its numbers 1.–16. are logged under `unlinked_section_numbers`.
4. **Two-part printing:** the MN 1 aṭṭhakathā and ṭīkā each contain "(Paṭhamo bhāgo)" … "(Dutiyo bhāgo)" with a reprinted nikāya and book title. These are kept as plain text blocks, not headings.
5. **ṭīkā lists under a `title`:** the 16 hāras and the 4 nayas are `######` under their `#####` title. The `title` heading is a sibling of `Nettinayavaṇṇanā`.

## Source misprints kept as printed

- **`01`**, printed with no dot, in `s0201a` and `s0201t`: logged as unresolved.
- **`14.` printed twice** in the ṭīkā's hāra list (`14. Adhiṭṭhāna-`, `14. Parikkhāra-`; the second should be 15). Heading numbers are stripped, so this does not affect any ID.
- **Abbreviated ranges**, expanded for linking only and logged:
  - mn-1 aṭṭhakathā: `380-1.`, `410-4.`
  - mn-1 ṭīkā: 3 ranges
  - mn-2 ṭīkā: 1
  - mn-3 aṭṭhakathā: 1
  - mn-3 ṭīkā: 1

## Uploaded to library-prod.webuddhist.com (2026-11-13)

Run with `0-INBOX/temp/mn/upload-mn.sh`. For each file: dry run with live checks, `--execute`, `--verify`; the log is in `0-INBOX/temp/mn/upload-mn.log`. The library IDs are in each file's frontmatter and in the two upload ledgers. The library fields are the same as for the DN: `license: cc0`, `tag_ids: [296WZOr8MXWteSqBBI7pl]`, `category_id: MZUUxphQ0yFwLBon3Vng8`.

| File | text_id | edition_id | toc_id | Live segments | TOC nodes | Alignment pairs → root edition |
|---|---|---|---|---|---|---|
| pi-mn-1 | `ueaCpKSILFcgtJA3zp13X` | `aIXWlhR2vxkSUwyqXqAnU` | `x6dwLsBb1kge00FYyuwAf` | 514 | 82 headings | — |
| pi-mn-2 | `cw3QYWhLrtIU8jetxrDee` | `68MEFcllavnajd7qASNqk` | `rN3ppPClLrviz2PLeUq0q` | 487 | 58 headings | — |
| pi-mn-3 | `a16eguWjXslgsEZhMFjl0` | `rkEFE9YLpfHvBHgNvuqce` | `FHYhpcqRsrgwagkwmEw5N` | 464 | 59 headings | — |
| pi-mn-1-atthakatha | `Mj9cj3d5W5ktwlHkRAfSO` | `bHOTCntkTvuSAIoRhEuCg` | `o7tb3f1r4gsidK5Ke5EJk` | 2512 | 143 | 2508 → `aIXWlhR2vxkSUwyqXqAnU` |
| pi-mn-1-tiika | `GS4wMUiDBQjJMEjTAoCss` | `d6bCxrZFwvPCYF1oRLLpt` | `sk1XKBmYNSmAFZOtcFY27` | 2135 | 170 | 2084 → `aIXWlhR2vxkSUwyqXqAnU` |
| pi-mn-2-atthakatha | `euqbubzMlDaKQp5IJAWEH` | `UWkXUKDWDLCFOgXXYUUNd` | `o2XAjwMIVbH2wNbofRXRO` | 1164 | 58 | 1187 → `68MEFcllavnajd7qASNqk` |
| pi-mn-2-tiika | `sf0zN5sjqk2ar3jgKzfxy` | `FT11ObI0eH2tQlICtKvV8` | `tqGTm5kNl18Q2dOnoTShX` | 832 | 58 | 855 → `68MEFcllavnajd7qASNqk` |
| pi-mn-3-atthakatha | `6yFc3ln7NQDkWjVwjFN08` | `8rxq510IzxDwAVIuHlC9a` | `fVOuXRNdsmXqsewguUouq` | 989 | 67 | 990 → `rkEFE9YLpfHvBHgNvuqce` |
| pi-mn-3-tiika | `GEPIm3uxAuISZRlht4OfR` | `0ivKf5QtTznqR8sT0x2YM` | `fxcpIM0T4NFXLJKgJxF4K` | 787 | 66 | 788 → `rkEFE9YLpfHvBHgNvuqce` |

What was checked:
- **Segments:** live segments = the file's content blocks + the homage `T-1`.
- **TOC nodes:** live TOC nodes = the file's headings.
- **Alignment pairs:** the live pairs equal the parser's pairs, built from the file's transclusions. Every target was present in the live root segmentation before the upload.
- **Commentary links:** each commentary's live `commentary_of` is its root's `text_id`, and it is aligned to its root's edition.
- **Ledgers:** the IDs in the files equal the ledgers.

## Not done

- No commit or push, at your request; no translation.
- The skill fixes in `4-SYSTEM/Skills/` are vault copies. Per CLAUDE.md §14 they should also go to the shared skill library.
