# Sutta vault — verification against tipitaka-xml, tipitaka.app and the commentaries

**Date:** 2026-11-20 (first run 2026-11-17, rerun today from saved scripts)
**Files:** all 71 files in `1-SOURCES/`: 24 root texts and 47 commentaries.

| Nikāya | Root texts | Commentaries |
|---|---|---|
| Dīghanikāya | `pi-dn-1` … `pi-dn-3` | aṭṭhakathā ×3, ṭīkā ×3, abhinavaṭīkā (DN 1) |
| Majjhimanikāya | `pi-mn-1` … `pi-mn-3` | aṭṭhakathā ×3, ṭīkā ×3 |
| Saṃyuttanikāya | `pi-sn-1` … `pi-sn-5` | aṭṭhakathā ×5, ṭīkā ×5 |
| Aṅguttaranikāya | `pi-an-1` … `pi-an-11` | aṭṭhakathā ×11, ṭīkā ×11 |
| Khuddakanikāya | `pi-kn-1` Khuddakapāṭha, `pi-kn-2` Dhammapada | aṭṭhakathā ×2 |

**References, fetched fresh:**

- [VipassanaTech/tipitaka-xml](https://github.com/VipassanaTech/tipitaka-xml) `romn/`, at HEAD `9c15eee`. The newest commits (2026-11-20) change only `site-deploy.ps1`. The last change to `romn/` is still `0854d11` (August 2024), so the source has not changed since the vault was built.
- [tipitaka.app](https://tipitaka.app/latn/sp): its API (data version `7d17987e5be3e268`, the one the live site requests) gave the full text, contents tree and cross-layer links of 71 books (24 Mūla, 24 Aṭṭhakathā, 23 Ṭīkā).

**Six checks, scripts and output in `tipitaka-xml-check/2026-11-20/`** (run with `bash run_all.sh <scratch-dir>`; output in `out/`):

1. `fetch_github.sh`: downloads the 58 XML files named in the frontmatter and compares them byte for byte with `0-INBOX/raw-data/`.
2. `verify_xml_all.sh`: the intake skills' own checks (`verify.py`, `verify_commentary.py`, `check_headings.py`): IDs, text, headings, bold, citations.
3. `indep.py`: a second check that uses no vault code. It compares the letter-word sequence of each file with the XML's and counts spaces before punctuation. It also checks that block IDs are unique, that every transclusion resolves, and that the frontmatter IDs (`commentary_of`, `aligned_to_edition_id`) match the root's.
4. `fetch_site.py` + `fetch_tika2.py`: a fresh download of tipitaka.app, compared with the cache in `0-INBOX/tipitaka-app/`.
5. `site_all.sh`: the skills' site comparisons (`compare_site.py`, `compare_site_commentary.py`): text paragraph by paragraph, contents tree, paranum links, bold.
6. `content_links.py`: a meaning check. For each commentary link, it tests whether the commentary's words match the linked root block better than a neighbouring one.

---

## Verdict

**Everything matches. There is no defect to fix.** The few differences are two corrected XML misprints, one alignment kept by number on your instruction, and gaps on tipitaka.app's side.

| Area | Result |
|---|---|
| XML files vs GitHub | **58/58 byte-identical** to `romn/` at HEAD |
| Words vs XML | **identical in all 71 files** (≈ 2.97 million words; roots ≈ 1.0 million). The only extra text is the two `[Ed:]` notes below. For AN commentaries, the volume's opening homage and closing colophon, which sit outside the nipāta `<div>`, are in the first / last nipāta's file, as they should be |
| Skills' XML checks | **69/71 PASS.** The other two report exactly the two `[Ed:]` corrections below, and nothing else. All headings match the XML in all files |
| Spacing | **no extra spaces** (unlike the Vinaya vault's 3,100). Page breaks are dropped without leaving a space before punctuation. The one `word .` in the vault (`pāpa"nti . (saṃ`, DN 1 aṭṭhakathā) is in the XML itself |
| Block IDs | 54,616 IDs, unique in every file (11,425 in the roots) |
| Transclusions | **11,784**, every one pointing to an existing block of the right root file |
| Frontmatter | every commentary's `root_text`, `commentary`, `commentary_of`, `aligned_to_edition_id` and category match its root. `pi-kn-2` and its aṭṭhakathā have no library IDs yet (not uploaded) |
| Books vs tipitaka.app | same books, same titles. DN, MN, SN, AN complete (every root, aṭṭhakathā and ṭīkā the site has, plus the DN abhinavaṭīkā). KN: 2 of 20 books |
| tipitaka.app download vs cache | identical (see §Site data) |
| Text, tree, links vs tipitaka.app | 55/71 PASS. The 16 others are all explained below: site-side gaps or the deliberate items |
| Commentary ↔ root, by meaning | 4,730 link groups checked. 13 flagged: 5 are the Tirokuṭṭa item below; 8 are false positives (a prose commentary paragraph running on into the next root paragraphs, with the printed number agreeing with both XML and site) |

## Deliberate items (documented, not errors)

| Item | What | Where documented |
|---|---|---|
| DN 1 aṭṭhakathā `504-407.` | CSCD misprint for 504–507 (next paragraph is 508; the ṭīkā and abhinavaṭīkā cite 504). Linked to ^1-504–^1-507, printed number kept, `[^ed-504]` footnote. tipitaka.app links it to 504 | commit `08aab36`, `pi-dn-commentary-report.md` |
| SN 5 ṭīkā `1101.` | CSCD misprint: the paragraph sits under *Daṇḍasuttavaṇṇanā* and glosses the Daṇḍasutta (root 1103; 1101 is the Sīsapāvanasutta). Linked to ^5-1103, printed number kept, `[Ed:]` note | `pi-sn-verification-report.md` |
| Khuddakapāṭha aṭṭhakathā, Tirokuṭṭasutta | The aṭṭhakathā counts 13 verses where the root has 12 (it splits root verse 3), so from `4.` to `13.` the by-number links point up to one verse off, and `13.` (root v12) is unlinked. **Kept by number on your instruction (2026-11-16): "keep it as it is with website and repo".** Every other Khuddakapāṭha section, including the Nidhikaṇḍa, is aligned verse for verse | `pi-kn-1-verification-report.md` §3 |
| MN 1 aṭṭhakathā / ṭīkā `01` | CSCD placeholder paragraph number. Kept as printed, logged unresolved, no link | `pi-mn-commentary-report.md` |

## Differences from tipitaka.app (site-side; the vault follows the XML)

| File(s) | Site difference | Why the vault is right |
|---|---|---|
| DN 1 ṭīkā, MN 1 aṭṭhakathā, KN 2 aṭṭhakathā | the front-matter heading (*Ganthārambhakathā(vaṇṇanā)*, *Dhammapada-aṭṭhakathā*) sits at a different level on the site | the heading is in the XML; only the nesting differs |
| DN 3 aṭṭhakathā and ṭīkā, MN 3 aṭṭhakathā | the site's contents tree lacks *Nigamanakathā(vaṇṇanā)* and *Saḷāyatanavaggo* | they are XML headings (`subhead`, `chapter`) |
| AN 9, 10, 11 aṭṭhakathā | the site's tree lists only each nipāta's first vagga (e.g. AN 9: *Sambodhivaggo*; *Sīhanāda-*, *Sattāvāsa-*, *Mahā-*, *Sāmaññavaggo* missing) | all are `<head rend="chapter">` in `s0404a.att.xml`. **New: not in any earlier report** |
| SN 3, SN 5 roots | tree nesting offset by one or two levels | structure follows the XML (`pi-sn-structure-report.md`) |
| SN 5 root | five range-only lines (`312-323` … `357-366`) the site does not display | XML `hangnum` paragraphs with @n (abbreviated suttas), kept with their IDs |
| AN 10 ṭīkā | the site treats the numbered verses `1.` `2.` … of the Pubbakammapiloti as citations of AN 10.1, 10.2 … (9 pairs) | XML prints them as `hangnum` without @n: the passage's own numbering, logged as such, unlinked |
| KN 1 aṭṭhakathā | the site links Tirokuṭṭa `13.` to a Maṅgalasutta paragraph | wrong on the site; see the Tirokuṭṭa item above |
| Bold, many files | the site joins adjacent bold spans (`samagganandī,samaggakaraṇiṃ`) | the XML keeps them apart, and so do the files |

## Site data

- A fresh download of all 71 books is identical to `0-INBOX/tipitaka-app/`, so every site comparison above reflects the live site. The cache lacked only the DN roots' links files, which the fresh download adds.
- **Bug in `fetch_site.py` (not fixed):** for a key like `tika2-dn-1`, it derives the parent as `tika2-dn`. That key doesn't exist on the site, which answers 404, and the run stops. The real parent is `tika-dn`. `fetch_tika2.py` here fetches such books with the parent given. The same will hit `tika2-kn-nett`.

## Note: bold that strict Markdown does not render

- **What:** about 18,000 bold pairs in 41 files do not render as bold under strict CommonMark. Most are the Pāli pattern `**"…"**ti`, where the closing `**` sits between a quote mark and a letter. About 360 more have a space just inside the `**`, copied from the XML (`<hi rend="bold"> vesāliya</hi>`).
- **Text:** faithful to the XML; the checks require exactly that.
- **Library:** not affected. The upload parser strips `**` (`parser-commentary/parser.py` `_strip_bold`).
- **Effect:** only how the files look in Obsidian or another Markdown viewer.

## Not covered

- Readings and variant notes were checked against the XML only, not against printed editions.
- The library-prod uploads were not re-read in this run. The upload commits record byte-for-byte verification at upload time.
- KN books 3–20 are not in the vault yet. Their XML sits in `0-INBOX/raw-data/kn/` (untracked).

---

## After the check: merged per nikāya and re-uploaded (2026-11-20, same day)

On your instruction ("take reference from Abhidhamma and Vinaya"), the vault and the library now hold **one text per work**. A work CSCD prints in several volumes is one file, and each volume is a chapter in it.

**Vault.**
- **Joined files:** `pi-dn`, `pi-mn`, `pi-sn`, `pi-an`, and an aṭṭhakathā and a ṭīkā for each, 12 files built with `cscd-root-text-intake/scripts/merge_volumes.py` from the 66 verified per-volume files. The per-volume files are removed from `1-SOURCES/`; they are in git history.
- **Abhinavaṭīkā:** `pi-dn-1-abhinavatiika` stays one work (it covers DN 1 only) and now links to `pi-dn.md`.
- **KN:** the Khuddakanikāya books stay one file per book.
- **Block IDs:** every block ID is unchanged. A later volume's homage and nikāya line stay where printed, as text blocks `^<book>-T1`, `^<book>-T2`.
- **Checked:** all 17 files are identical word for word to the XML volumes in order (`indep.py`: 17/17 OK), and every transclusion resolves.
- **Rules:** annex §1–§3, both intake skills, the catalog and the `/` commands are updated. The 44 per-volume commentary IDs are retired, never reused.

**Library-prod.**
- **Deleted:** the 67 per-volume texts, commentaries first and then roots, each read back as gone (`4-SYSTEM/scripts/library-delete/delete_texts.py`; log `0-INBOX/temp/merge/delete-log.jsonl`). The Khuddakapāṭha root and aṭṭhakathā were left as they were.
- **Uploaded:** 13 texts, each read back:

| File | Title | text_id | Chapters (TOC top level) |
|---|---|---|---|
| `pi-dn` | Dīghanikāya | `O4D2mIIgVEMj82ljsKBth` | 3 vaggas |
| `pi-mn` | Majjhimanikāya | `u9MLgrwMkk8Z4bwlazQyP` | 3 paṇṇāsas |
| `pi-sn` | Saṃyuttanikāya | `uzZmqn2gy3nFauQi3A1Jc` | 5 vaggas |
| `pi-an` | Aṅguttaranikāya | `ZV0nnyNrdAs5qCMr4u30C` | 11 nipātas |
| `pi-dn-atthakatha` | Dīghanikāya-aṭṭhakathā | `oA84xA2Nu7W0COntGWr0x` | |
| `pi-dn-tiika` | Dīghanikāya-ṭīkā | `ORdr2bUpQtertVv9eonn4` | |
| `pi-dn-1-abhinavatiika` | Sīlakkhandhavaggaabhinavaṭīkā | `CJ7pS7bHxqTvkaDD4HrQb` | |
| `pi-mn-atthakatha` | Majjhimanikāya-aṭṭhakathā | `ZtYqURlKWImiQ25Bvz8om` | |
| `pi-mn-tiika` | Majjhimanikāya-ṭīkā | `YkkkB0D992UkiVjrXykeR` | |
| `pi-sn-atthakatha` | Saṃyuttanikāya-aṭṭhakathā | `RtWhT5zmeG7NhZ9j51z73` | |
| `pi-sn-tiika` | Saṃyuttanikāya-ṭīkā | `gA2PitXY0qqWiXVS0FVp1` | |
| `pi-an-atthakatha` | Aṅguttaranikāya-aṭṭhakathā | `d7wgj6qGg2QFUWWEBN09F` | |
| `pi-an-tiika` | Aṅguttaranikāya-ṭīkā | `srnX4lidUR7rnV0YlE7hK` | |

**Upload rules brought in line with Vinaya and Abhidhamma** (`parser-commentary/parser.py`, ported from the Vinaya parser):

1. **A heading ends a link group.** Commentary after a heading needs its own citation to be aligned.
2. **Every commentary block is a `paragraph`,** gāthās included.
3. **Volume openings:** a later volume's opening blocks `^<book>-T<k>` also end a link group, so the join adds no pair the per-volume files did not have.

**Proof the join changed nothing:** before rules 1–2 were applied, the merged alignments were checked pair for pair against the old per-volume alignment files, and all 9 were identical.

**Applying rules 1–2 to the live texts:** `commentary-upload/scripts/replace_segmentation.py` applied them to all 10 live commentaries, the 9 above plus `pi-kn-1-atthakatha`. It changed only segment types and alignment pairs; references, spans, text and contents trees are unchanged.
- **Changes:** 1,705 gāthā segments changed from verse to paragraph, and 1,207 run-on pairs were removed, with none added. For example, DN aṭṭhakathā `^1-805`, the start of the *Saraṇagamanakathā* excursus, is no longer tied to root ^1-250.
- **Backups:** `0-INBOX/temp/merge/live-backup/`.
- **AN ṭīkā:** its alignment PUT answered `504 Gateway Time-out`, but the read-back shows all 6,411 pairs equal to the parser output. The ledger records this.

**Checks in this folder that still read the old per-volume files:** `verify_xml_all.sh` and `site_all.sh` were run on 2026-11-17/20 before the merge, so their results above refer to the per-volume files. The merged files are covered by `indep.py`. The fresh tipitaka.app download (213 files) is identical to the cache, so the site results stand.

**Not done:**
- Dhammapada (`pi-kn-2`) and its aṭṭhakathā are not uploaded, as before.
- `fetch_site.py`'s `tika2-` parent bug is not fixed.
