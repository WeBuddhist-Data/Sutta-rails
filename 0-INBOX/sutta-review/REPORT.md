# Sutta — completeness review, one nikāya at a time

Begun 2026-11-25, the way the Vinaya was re-checked on 2026-11-23 (`Vinaya-rails/0-INBOX/vinaya-redo/REPORT.md`).

**What [`review_nikaya.py`](review_nikaya.py) checks, for every file of a nikāya** (detail per file in `<file>-detail.md`):

1. **Completeness:** the XML files named in `source_filename`, read in order, against the vault file, line by line. Both sides are normalised as in the Vinaya check: notes become `[ ]`, `‘‘ ’’` becomes `"`, spaces are collapsed and none is left before punctuation, and a `hangnum` line is joined to the next. On the vault side, transclusions, footnote definitions, `**bold**`, `[^ref]` and block IDs are dropped. Heading markers are dropped, and printed heading numbers are stripped on both sides.
   - A root text carries its printed paragraph number in the block ID (`^1-1`), not in the text, so each such number is checked against its ID instead.
2. **XML copies:** each XML file in `0-INBOX/raw-data/` must be byte-identical to `tipitaka-xml/romn/`. In the local tipitaka-xml clone, `romn/` was last changed in `0854d11` (2024-08-25), the same commit the vault was built from.
3. **Block IDs:** every block has one, and all are unique. Heading IDs end in `-0`, and their path length agrees with the `#` count.
4. **Transclusions:** every `![[file#^id]]` points at an existing block of that file.

## Finding: printed heading numbers are dropped (all nikāyas) ⚠️

At first the review stripped printed heading numbers on both sides, as the intake did, so the sections below were marked ✅ on that basis. On review the user said not to strip them. A heading's printed number (`1.`, `(1) 1.`) cannot be read back from its block ID: `^1-1-0` is a structural path, not the printed number. The Vinaya files keep it (`### 1. Pārājikakaṇḍaṃ ^1-2-0`); the Sutta intake strips it ("chapter numbers stripped from headings" in every `source_description`).

The review now compares headings as printed, and lists each heading whose number is missing in its `-detail.md`. In every case the heading matches the XML once the number is removed, so the number is the only thing lost.

| Nikāya | Root | Aṭṭhakathā | Ṭīkā | Abhinavaṭīkā |
|---|---|---|---|---|
| Dīgha | 34 | 34 | 34 | 13 |
| Majjhima | 167 | 167 | 187 | |
| Saṃyutta | 2,040 | 1,125 | 1,104 | |
| Aṅguttara | 1,533 | 1,048 | 738 | |
| Khuddaka | 2,700 | 1,763 | 24 | |

**Total: 12,711 headings in 16 files.** (12,706 found first; 5 more in KN when the review learned two more cases: `subsubhead` headings, and an XML paragraph the vault made a heading. See §5.)

### Fixed (approved by the user, 2026-11-25) ✅

- **Restore:** `review_nikaya.py <nk> --restore` put each number back exactly as the XML prints it, for example `### 1. Rūpādivaggo ^1-1-0` and `##### 1.Sattisuttavaṇṇanā ^1-1-3-1-0` (no space, as printed). Heading levels, block IDs, `**…**` wrappers and every other line are unchanged. All were restored (12,706, then the 5 KN ones), and none was skipped. The previous versions are in `backups/`.
- **Checked against git HEAD** ([`verify_restore.py`](verify_restore.py)): every file has the same number of lines, and each changed line is a heading whose only change is the added number. 0 problems.
- **Re-run of the review:** 0 headings without their number in all 16 files, and every other count is unchanged.
- **`source_description`:** in all 16 files, "chapter numbers stripped from headings" now reads "printed heading numbers kept in the headings, as in the XML" ([`fix_description.py`](fix_description.py)).
- **Not done yet:** the prod library still shows the old, unnumbered headings. A re-upload needs approval.

### The intake now keeps the numbers (2026-11-25) ✅

**What changed.** These are this vault's copies of the shared skills:

| File | Change |
|---|---|
| `cscd-root-text-intake/scripts/cscd_shape.py` | new `printed_heading()`: the heading as printed, number kept; `strip_heading_number()` stays, for matching by name only |
| `cscd-root-text-intake/scripts/cscd_xml_to_json.py` | no space added after a heading's `N.`, so `1.Sattisuttavaṇṇanā` stays as printed (paragraphs unchanged) |
| `json-to-source-text/converters/tipitaka_org_book.py` | headings written with `printed_heading()` |
| `cscd-root-text-intake/scripts/tree_to_md.py` | the same, in tree mode |
| `cscd-commentary-intake/scripts/commentary_converter.py` | the same. The stripped name is still used for the h3 de-duplication and `--unlinked` matching |
| `verify.py`, `check_headings.py`, `verify_commentary.py` | headings compared **with** their number, so a dropped number is now an error |
| `build_commentary.py`, `merge_volumes.py`, `set_frontmatter.py`, both `SKILL.md` | the `source_description` wording and the rule ("A heading keeps its printed number exactly as printed"); the SKILL examples now show numbered headings |

**Tested** ([`test_build.py`](test_build.py)): three volumes were rebuilt from the XML through the skill's own steps, in `test/`.

| Build | Converter | Checks | Headings vs the corrected vault |
|---|---|---|---|
| DN root vol 1 `s0101m` | `tipitaka_org_book.py` | `verify.py` PASS, `check_headings.py` ALL MATCH | 144 = 144, identical |
| AN root vol 1 `s0401m` | `tree_to_md.py` (tree mode) | `verify.py --tree` PASS, `check_headings.py` ALL MATCH | 34 = 34, identical |
| DN aṭṭhakathā vol 1 `s0101a` | `commentary_converter.py` | `verify_commentary.py` PASS (319 citations right, 0 wrong), `check_headings.py` ALL MATCH | 121 = 121, identical |

**Negative test:** with the number removed from one heading (`1. Rūpādivaggo` → `Rūpādivaggo`), `check_headings.py` and `verify.py` both fail and name that heading.

**Still to note:**
- **Shared library:** the fix is in this vault's copies, and the shared skill library still drops the numbers. It belongs upstream with the other script fixes. `tipitaka_org_book.py` is also used for Abhidhamma (`abh…m`) roots, so a sync carries the change there too.
- **KN build scripts:** the shape scripts in `0-INBOX/temp/kn-comm/` pair commentary headings with root headings by name. Before any re-run, they would need to strip numbers when matching.

## 1. Dīghanikāya ✅ (apart from the heading numbers)

| File | XML | XML lines | Not matched (XML / vault) | Block IDs | ID problems | Transclusions (unresolved) |
|---|---|---|---|---|---|---|
| `pi-dighanikaya` | `s0101m`–`s0103m` | 4,543 | 0 / 0 | 1,818 | 0 | — |
| `pi-dighanikaya-atthakatha` | `s0101a`–`s0103a` | 4,349 | 0 / 0 | 4,073 | 0 | 1,159 (0) |
| `pi-dighanikaya-tiika` | `s0101t`–`s0103t` | 4,018 | 0 / 0 | 3,894 | 0 | 1,051 (0) |
| `pi-dighanikaya-1-abhinavatiika` | `s0104t`, `s0105t` | 2,940 | 0 / 0 | 2,564 | 0 | 442 (0) |

- **Every XML line is in the vault, and nothing is added.**
- **Root paragraph numbers:** the root carries 1,360 printed paragraph numbers in its block IDs, and every one agrees with its ID.
- **XML copies:** all 11 are byte-identical to `romn/`.
- **Line endings:** all four files are LF, like every Sutta source file.
- **Known items:** the aṭṭhakathā's `504-407.` misprint, documented 2026-11-16, is unchanged: the printed number is kept and a footnote explains it.
- **Books:** the books match tipitaka.app's (3 root, 3 aṭṭhakathā, 3 ṭīkā, and the DN 1 abhinavaṭīkā), as checked on 2026-11-20. The DN files have not changed since, apart from the rename.

## 2. Majjhimanikāya ✅

| File | XML | XML lines | Not matched (XML / vault) | Block IDs | ID problems | Transclusions (unresolved) |
|---|---|---|---|---|---|---|
| `pi-majjhimanikaya` | `s0201m`–`s0203m` | 4,940 | 0 / 0 | 1,664 | 0 | — |
| `pi-majjhimanikaya-atthakatha` | `s0201a`–`s0203a` | 5,357 | 0 / 0 | 4,933 | 0 | 1,110 (0) |
| `pi-majjhimanikaya-tiika` | `s0201t`–`s0203t` | 4,151 | 0 / 0 | 4,048 | 0 | 1,088 (0) |

- **Every XML line is in the vault, and nothing is added.**
- **Root paragraph numbers:** the root carries 1,462 printed paragraph numbers in its block IDs, and every one agrees with its ID.
- **XML copies:** all 9 are byte-identical to `romn/`.
- **Line endings:** all three files are LF.
- **Known items:** the `01` placeholder paragraph number (no dot) in `s0201a` and `s0201t` is unchanged: kept as printed and unlinked (`pi-mn-commentary-report.md`).
- **Books:** the books match tipitaka.app's (3 root, 3 aṭṭhakathā, 3 ṭīkā), as checked on 2026-11-20.

## 3. Saṃyuttanikāya ✅

| File | XML | XML lines | Not matched (XML / vault) | Block IDs | ID problems | Transclusions (unresolved) |
|---|---|---|---|---|---|---|
| `pi-samyuttanikaya` | `s0301m`–`s0305m` | 11,211 | 5 / 10 (known, below) | 3,942 | 0 | — |
| `pi-samyuttanikaya-atthakatha` | `s0301a`–`s0305a` | 4,761 | 0 / 0 | 4,514 | 0 | 1,698 (0) |
| `pi-samyuttanikaya-tiika` | `s0301t`–`s0305t` | 4,830 | 0 / 0 | 4,770 | 0 | 1,648 (0) |

- **Every XML line is in the vault, and nothing is added.**
- **Root paragraph numbers:** the root carries 1,856 printed paragraph numbers in its block IDs, and every one agrees with its ID. A printed range is carried whole (`225-240.` → `^3-225-240`).
- **The 5 root differences** are the SN 5 abbreviated suttas `312-323` … `357-366`. The XML prints each range with the sutta title, as one hangnum + heading. The vault keeps the range as its own block (`^5-312-323`) and puts the title in the heading under it. The words are the same, only split. This is documented in the 2026-11-20 verification and `pi-sn-structure-report.md`.
- **Printed heading numbers:** four commentary headings print the number with no space (`1.Sattisuttavaṇṇanā`). Like every other heading number, it is not kept in the vault heading.
- **Known item:** the ṭīkā's `[Ed:]` note on `1101.`, a CSCD misprint linked to `^5-1103`, is unchanged (`pi-sn-verification-report.md`).
- **XML copies:** all 15 are byte-identical to `romn/`.
- **Line endings:** all three files are LF.
- **Books:** the books match tipitaka.app's (5 root, 5 aṭṭhakathā, 5 ṭīkā), as checked on 2026-11-20.

## 4. Aṅguttaranikāya ✅

| File | XML | XML lines | Not matched (XML / vault) | Block IDs | ID problems | Transclusions (unresolved) |
|---|---|---|---|---|---|---|
| `pi-anguttaranikaya` | `s0401m`, `s0402m1`–`m3`, `s0403m1`–`m3`, `s0404m1`–`m4` | 10,674 | 0 / 0 | 3,446 | 0 | — |
| `pi-anguttaranikaya-atthakatha` | `s0401a`–`s0404a` | 5,126 | 1 / 1 (known, below) | 4,871 | 0 | 1,427 (0) |
| `pi-anguttaranikaya-tiika` | `s0401t`–`s0404t` | 4,980 | 0 / 0 | 4,684 | 0 | 1,654 (0) |

- **Every XML line is in the vault, and nothing is added.**
- **Root paragraph numbers:** the root carries 1,877 printed paragraph numbers in its block IDs, and every one agrees with its ID.
- **The 1 aṭṭhakathā difference** is a heading moved, not text. `### Rūpādivaggavaṇṇanā` stands 3 paragraphs later than in the XML (`^1-20`–`^1-22`, the summary of the 11 nipātas), so that `Saṃkhepakathā` holds them instead of being empty. It is fix E of the AN structure review (`0-INBOX/xml-verification/an-verification.md`), commit `a822251`.
- **Printed heading numbers:** many AN headings print two numbers (`(1) 1. Puggalavaggo`). Both are dropped from the vault heading, as everywhere else.
- **XML copies:** all 19 are byte-identical to `romn/`.
- **Line endings:** all three files are LF.
- **Books:** the books match tipitaka.app's (11 nipātas as 11 root books, 11 aṭṭhakathā, 11 ṭīkā), as checked on 2026-11-20.

## 5. Khuddakanikāya ✅

| File | XML | XML lines | Not matched (XML / vault) | Block IDs | ID problems | Transclusions (unresolved) |
|---|---|---|---|---|---|---|
| `pi-khuddakanikaya` | `s0501m`–`s0520m` (21 files; `s0510m1`+`m2`; `s0518m`, `s0520m` are `.nrf`) | 63,290 | 1 / 0 (known, below) | 25,945 | 0 | — |
| `pi-khuddakanikaya-atthakatha` | 24 files, `s0501a`–`s0519a` | 73,869 | 0 / 0 | 54,183 | 0 | 16,192 (0) |
| `pi-khuddakanikaya-tiika` | `s0519t` | 763 | 0 / 0 | 753 | 0 | 130 (0) |

- **Every XML line is in the vault, and nothing is added.**
- **Root paragraph numbers:** the root carries 22,985 printed paragraph numbers in its block IDs, and every one agrees with its ID. Zoned and per-section books keep the zone or section before the number (`^5-1-474`, Khuddakapāṭha `^1-6-3`; annex §4).
- **The 1 root difference is `474.` (Suttanipāta).** The XML prints the number alone in its own paragraph. The vault opens the next verse with it, and that verse's ID is `^5-1-474`. This is by design (`tree_to_md.py`), and nothing is lost.
- **36 Vimānavatthu blocks `^6-U1`–`^6-U36`** keep a printed `N.` as text (`1. Vatthuttamadāyikāvimānavatthu`). The number titles a sub-story and is not a paragraph number, so the block takes a `U` ID. This is by design (`tree_to_md.py`).
- **12 lines are a heading on one side and text on the other, with the same words and number:**
  - Two are a later part's reprinted title kept as text: `2. Cūḷavaggo` (Suttanipāta-aṭṭhakathā part 2) and `22. Mahānipāto` (Jātaka-aṭṭhakathā part 7).
  - Ten are Jātaka titles the XML prints as paragraphs and the vault makes headings (`##### 1. Apaṇṇakajātakavaṇṇanā` … `10.`), as decided for book 14.
- **5 more heading numbers restored, found only in this step:**
  - Root: `### 1. Bāhirakathā` (Milindapañha). The XML has it as a `subsubhead`, a heading type the first pass did not list.
  - Aṭṭhakathā: the Apadāna Nidāna's `1. Dūrenidānakathā`, `2. Avidūrenidānakathā`, `3. Santikenidānakathā` (also `subsubhead`).
  - Aṭṭhakathā: the Cūḷaniddesa's `2. Dutiyavaggavaṇṇanā`, an XML paragraph the shape script made a heading without its number.
  - Restored and checked like the others; the other nikāyas have no such case.
- **XML copies:** all 46 are byte-identical to `romn/`.
- **Line endings:** all three files are LF.
- **Books:** all 20 KN root books; aṭṭhakathās for every book CSCD comments on (none for 11, 18, 20); the Nettippakaraṇa-ṭīkā only, the Nettivibhāvinī left out by decision (annex).
- **Before any KN rebuild:** the shape scripts in `0-INBOX/temp/kn-comm/` pair headings by name, and the one that turns a paragraph into a heading must keep its number (the `Dutiyavaggavaṇṇanā` case). The intake skill scripts already do.

## Second pass: page breaks, bold, structure and links (2026-11-25) ✅

[`review_more.py`](review_more.py), a `<file>-more.md` per text. These were checked at build time; this pass re-runs them on today's files.

| Nikāya | Page markers | Spacing differences | Bold spans (XML = vault) | Structure problems | Citations | Wrong links |
|---|---|---|---|---|---|---|
| Dīgha (4 files) | 10,959 | 0 | 40,166 ✓ | 0 | 2,216 | 1 known |
| Majjhima (3) | 11,132 | 0 | 31,794 ✓ | 0 | 2,181 | 0 |
| Saṃyutta (3) | 10,793 | 0 | 24,819 ✓ | 0 | 1,902 | 1 known |
| Aṅguttara (3) | 12,581 | 0 | 25,523 ✓ | 0 | 2,133 | 0 |
| Khuddaka (3) | 44,497 | 0 | 78,108 ✓ | 0 | 15,535 | 0 |
| **All 16** | **89,962** | **0** | **200,410 ✓** | **0** | **23,967** | **2 known** |

**A. Page breaks.** Lines are aligned by their letters, then compared with exact spacing and punctuation. Each `<pb/>` is tracked, and the editions' markers at the same spot count as one.
- **No page break became a space and none joined two words.** The Vinaya's problem (`word<pb/>.` → `word .`, 3,111 cases) does not occur here. A marker with spaces around it is one space in the vault (`me <pb/> sutaṃ` → `me sutaṃ`), and one with none is no space (`dhammaṃ<pb/>.` → `dhammaṃ.`).
- **No other spacing or punctuation difference** exists in any aligned line.
- The only lines that cannot be aligned are the first pass's known ones: SN 5's 5 ranges, the AN Saṃkhepakathā heading move and KN's `474.`.

**B. Bold.** All 200,410 `<hi rend="bold">` spans are `**…**` spans with exactly the same text, in order (`bold_check.py`). No `**` is unpaired.

**C. Structure.** In all 16 files:
- each heading sits under the heading one level up whose ID path is its own minus one segment;
- no level is skipped;
- no heading is empty.

The "sibling restarts" listed in the detail files are the source's own numbering. A ṭīkā skips suttas it does not comment on (`7. …` after `3. …`), titles repeat (`14. Etadaggavaggo` ×6, as in the AN structure review), and grouped marks such as `(3-5)` are not counted.

**D. Links.** Each printed citation was checked against its links: the linked root blocks must hold exactly the cited numbers.
- **0 wrong links**, apart from the 2 known misprints: DN aṭṭhakathā `504-407.` → 504–507 and SN ṭīkā `1101.` → `^5-1103`.
- **Cited numbers the root does not print (9 citations):** SN `531-650.`, `651-704.`, `705-812.` (aṭṭhakathā and ṭīkā) span the documented SN Mahāvagga gaps; AN `105-6.` (aṭṭhakathā and ṭīkā; the root has no 4-106); KN `229-231.` (no 6-231). Every number the root does print is linked.
- **Citations with no links, all documented:**
  - the MN, SN and AN ṭīkās' own Ganthārambhakathāvaṇṇanā numbers 1.–16. and 1.–19., and the AN Dasaka-ṭīkā's verse list 1.–12. (annex, `--unlinked`);
  - KN aṭṭhakathā (20): the Tirokuṭṭa `13.`, the reprinted `2. Cūḷavaggo`, `1156.`, the 7 Vimānavatthu `…pe…` verses, the 8 under Apadāna "43-48", and 3 Jātaka items, all in the build logs (`0-INBOX/temp/kn-comm/*.unresolved.json`) and the annex;
  - KN ṭīkā `125.`, a source slip.
- **One false alarm:** KN aṭṭhakathā `314` (printed without a dot) is a citation the check did not recognise. It links `^10-1-314`, which is right.

## Shelf coverage

[`shelf_coverage.py`](shelf_coverage.py) lists every Sutta-shelf XML file in `romn/` (`s01*`–`s05*`, 101 files) against the `source_filename` lists in `1-SOURCES/`. **100 of the 101 are in the vault.** The one left out is `s0501t.nrf.xml`, the Nettivibhāvinī, by decision (annex). No vault file names an XML file that is not in `romn/`.

## Summary

All five nikāyas, 16 files, are complete against tipitaka-xml: every XML line is in the vault and nothing is added. The only differences are documented choices: SN 5's 5 range blocks, the AN Saṃkhepakathā heading move, KN's `474.` and the heading↔text lines. All block IDs are unique and agree with their printed numbers, and every transclusion resolves. The one defect, printed heading numbers dropped from 12,711 headings, is fixed in the vault and in the intake scripts. Not done: the prod re-upload and syncing the shared skill library.
