# Sutta root texts vs tipitaka-xml and tipitaka.app — verification

- **Date:** 2026-11-23
- **Files:** the 6 root texts in `1-SOURCES/Text/`, as merged on 2026-11-20 (`pi-dn`, `pi-mn`, `pi-sn`, `pi-an`, `pi-kn-1`, `pi-kn-2`).
- **Sources:**
  - `D:\Work\OpenPecha\tipitaka-xml\romn\` (22 `.mul.xml` volumes);
  - tipitaka.app contents trees in `0-INBOX/tipitaka-app/` (identical to a fresh download on 2026-11-20).
- **What this adds to `0-INBOX/sutta-verification-2026-11-20.md`:**
  - That report checked word sequences after the merge, but not headings, spacing or punctuation.
  - This one compares every line character by character (bold, variant notes, punctuation, spacing), every block ID with its printed paragraph number, and every heading's text and level with the XML.
  - It also runs a hierarchy review: numbering that restarts among siblings, and empty headings. This is the check that found the Vinaya problems.
- **Tools:** [`compare_sutta.py`](compare_sutta.py) and [`site_toc.py`](site_toc.py). Full output: `<file>-detail.md`.

## Result: ✅ correct, with 2 small items to fix

| | dn | mn | sn | an | kn-1 | kn-2 |
|---|---|---|---|---|---|---|
| Lines (XML ↔ vault, character for character) | 4,542/4,543 | 4,939/4,940 | 11,211 + 5 | 10,672/10,674 | 208/208 | 971/971 |
| Block ID = printed paragraph number | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Duplicate / missing IDs, stray whitespace | 0 | 0 | 0 | 0 | 0 | 0 |
| Headings: same text as the XML | ✅ | ✅ | ✅ | 1 ⚠️ | ✅ | ✅ |
| Heading IDs: depth, `-0`, siblings 1…n | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Flattened levels (Vinaya-style) | none | none | none | none | none | none |

### To fix (on approval)

1. **`pi-an.md` line 11122, `### (11). Rāgapeyyālaṃ ^8-3-0`.**
   - The XML prints this heading oddly as `(11). Rāgapeyyālaṃ`, with no local number, and the conversion's number-stripping missed that form.
   - The other 9 Rāgapeyyāla headings are plain `Rāgapeyyālaṃ`. **Fix:** `### Rāgapeyyālaṃ ^8-3-0`.
2. **`pi-an.md` line 11090, a variant note that lost a space.**
   - The XML note is `[ ] etthantare pāṭho …`: an empty bracket pair marking where the passage sits. The vault has `[[] etthantare …`.
   - **Fix:** `[[ ] etthantare …`.

### Differences that are correct as they are

- **DN ¶389 (Mahāvagga):** the XML's stray `. ` at the start of the paragraph was removed at intake (`pi-dn-hierarchy-report.md`).
- **SN 5, five range-only lines** (`312-323` … `357-366`): XML `hangnum` paragraphs with `@n`, kept with their IDs (2026-11-20 report).
- **MN line 430, `cāti]`:** the XML has `cāti ]` (a space before the end of the variant note). This is cosmetic, so leave it.
- **The nikāya title repeated at each later volume** (`Dīghanikāyo`, `Aṅguttaranikāyo`, …): a text block `^<book>-T<k>` since the merge.
- **Sub-sections of a sutta nested under it** (MN: 26, SN: about 1,500): for example the seven *pahātabbāsavā* of the Sabbāsavasutta and the eighteen *pabbas* of the Satipaṭṭhānasutta. The XML has them one level higher, as siblings of the suttas.
- **DN Lakkhaṇasutta headings `(1) …` – `(30) …`:** the mark numbers out of the 32 are content, so they stay.

### Hierarchy hints, all faithful to the source

- **SN Maggasaṃyutta peyyāla vaggas** (Sūriya-, Ekadhamma-, Gaṅgā-peyyāla …): each vagga prints the same 7-sutta (or 6-sutta) series twice, under different refrains, with no heading to group the series. There is nothing to nest it under without inventing a heading.
- **SN `2-12. Sikkhāsuttādi…` after `2-11. …`:** two parallel peyyāla series.
- **AN 2 and AN 5:** the peyyālas are numbered as their own series (`1. Kodhapeyyālaṃ`, `1. Sammutipeyyālaṃ`) after the paṇṇāsakas.
- **AN 10:** `(21) 1. Karajakāyavaggo` and `(22) 2. Sāmaññavaggo` sit directly under the book, beside the 4 paṇṇāsakas, in both the XML and tipitaka.app. Their numbers imply a 5th paṇṇāsaka, but the source has no heading for it.
- **AN 5 Sumanavagga:** `9. Bhojanasuttaṃ` comes before `8. Saddhasuttaṃ`. This is a CSCD misprint (for 7), shared by tipitaka.app, and invisible in the vault because it strips heading numbers.

### tipitaka.app trees

- **No problems:** DN 1–2, MN 1–2, SN 1, AN 1, 2, 6, 7, 8, 10, 11, KN 1–2.
- **The rest differ only because the site keys siblings by printed number where the vault keys by position**, e.g. `an-3-2-2-3` "3. Venāgapurasuttaṃ" is vault `^3-2-2-2-0`, after `1. Titthāyatanādisuttaṃ`, which covers suttas 1–2.
- **Every heading the site has is in the vault**, with the XML's text (checked one by one for AN 3, 4, 5, 9 and SN 2).
- **Also counted as differences, but not problems:**
  - DN 3 keys its group heading *Dvattiṃsamahāpurisalakkhaṇāni* as position 0.
  - MN 3 keeps a variant reading inside two headings, which the site drops.
