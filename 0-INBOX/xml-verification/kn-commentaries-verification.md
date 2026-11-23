# KN aṭṭhakathās vs tipitaka-xml, tipitaka.app and their roots — verification

- **Date:** 2026-11-23
- **Files:**
  - `pi-kn-1-atthakatha.md` (Khuddakapāṭha-aṭṭhakathā, `s0501a.att`);
  - `pi-kn-2-atthakatha.md` (Dhammapada-aṭṭhakathā, `s0502a.att`).
- **Note on the XML:** both files have no divs, only heading ranks.

## Result

| | KN 1 aṭṭhakathā | KN 2 aṭṭhakathā |
|---|---|---|
| Text vs XML | ✅ (1 verse number joined to its line) | ✅ (435 verse numbers joined to their lines: layout only) |
| Block IDs | ✅ | ✅ |
| Root links: all resolve and match the printed number | 71 ✅ (per-section links `^1-<section>-<n>`; Tirokuṭṭa kept by number, as decided 2026-11-16) | 436 ✅ |
| Heading titles vs tipitaka.app, in order | 110/110 ✅ | 333/333 ✅ (the site adds a node for the reprinted part-2 title, which the vault keeps as text) |
| Empty headings | none | none |
| **TOC structure** | ⚠️ Nigamana | ⚠️ Nigamana; vagga IDs one off from the root |

## Merged into one Khuddakanikāya text ✅ 2026-11-23, on the user's decision

tipitaka.app shows the Khuddakanikāya as one entry beside the other four nikāyas, its books inside, and DN–AN were already one file each. So the two KN books were joined like the DN–AN volumes on 2026-11-20 (`merge_volumes.py`):

- **New files:**
  - `pi-kn-1.md` + `pi-kn-2.md` became `1-SOURCES/Text/pi-kn.md`, title `Khuddakanikāya`;
  - the two aṭṭhakathās became `1-SOURCES/Commentaries/pi-kn-atthakatha.md`, title `Khuddakanikāya-aṭṭhakathā`, `registered_id: kn-atthakatha`.
- **IDs:** every block ID is unchanged. Each book is a `##` chapter (`^1-0` Khuddakapāṭhapāḷi, `^2-0` Dhammapadapāḷi). The Dhammapada's opening homage and nikāya line stay as text blocks, `^2-T1` and `^2-T2`.
- **Links:** all 507 transclusions now point at `pi-kn.md`.
- **Checks:**
  - `merge_volumes.py --split` proves both joins lossless (555 and 4,839 IDs, all unique);
  - the root has 1,179/1,179 lines identical to the two XMLs;
  - the aṭṭhakathā's 507/507 links resolve and match their printed numbers;
  - the trees match tipitaka.app book by book.
- **Annex updated:**
  - §1: the KN file rows and the layout paragraphs;
  - §2: the note on the Khuddakapāṭha's ID shape, now book 1 of the joined file;
  - §3: `kn-atthakatha` registered; `kn-1-atthakatha` and `kn-2-atthakatha` retired.
- **The old per-book files** are removed from `1-SOURCES/` and stay in git history.
- **Library:** `pi-kn-1` and its aṭṭhakathā are on prod as separate texts. The joined texts are not uploaded yet, and the old ones not retired (see the DN–AN procedure of 2026-11-20).

## Fixes ✅ APPLIED 2026-11-23 before the merge ([`fix_kn_comm.py`](fix_kn_comm.py); heading lines only)

1. **KN 1, Nigamana.** `#### Nigamanakathā ^1-9-13-0`, inside the Mettasuttavaṇṇanā, becomes `### Nigamanakathā ^1-10-0`, the book's last section. 1 heading line.
2. **KN 2, front matter and Nigamana.** 333 heading lines, IDs only, except the Nigamana's level.
   - **Front matter:** `Ganthārambhakathā` takes the Roman front-matter ID `^2-I-0`, as in KN 1 and the other commentaries. So the 26 vaggas get the root's numbers again: `Yamakavaggo ^2-1-0` … `Brāhmaṇavaggo ^2-26-0`, where today they run `^2-2-0` … `^2-27-0`. The earlier report (`pi-kn-2-verification-report.md` §4) already noted the offset.
   - **Nigamana:** `#### Nigamanakathā ^2-27-41-0`, after the last story of the Brāhmaṇavagga, becomes `### Nigamanakathā ^2-27-0`.

**Re-check on copies:** text, block IDs and links unchanged; titles identical to tipitaka.app in order; no empty heading.

## Left as it is (noted)

- **KN 2 front-matter verses:** the `Ganthārambhakathā` verses `1.`–`10.` are the commentator's own introduction, but they are linked to Dhammapada verses 1–10. tipitaka.app links them the same way, so they were kept, like the Tirokuṭṭa links (`pi-kn-2-verification-report.md` §4).
