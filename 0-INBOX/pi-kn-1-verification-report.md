# Khuddakapāṭha (`pi-kn-1`) — independent verification of structure, hierarchy and alignment

**Checked:** 2026-11-16, on the files in `1-SOURCES/` as built by the KN intake (`pi-kn-structure-report.md`).
**Against:**
- VipassanaTech/tipitaka-xml `romn/`;
- tipitaka.app `kn-khp` and `atta-kn-khp`: text, contents tree, and paragraph links.

**Scope:**
- `1-SOURCES/Text/pi-kn-1.md`;
- `1-SOURCES/Commentaries/pi-kn-1-atthakatha.md`.

**Edits:** none remain. The Tirokuṭṭa re-link (§3) was made, then undone the same day at the user's instruction: the files follow the website and the repo. The check scripts are scratch files and are not in the vault.

---

## 0. Verdict

- **Root text:** correct in every respect checked. Its structure, hierarchy, numbering and wording match the XML and the site.
- **Aṭṭhakathā:** its text, headings and hierarchy are correct.
- **Tirokuṭṭasutta: kept as the website and repo give it.**
  - The aṭṭhakathā's printed numbers do not follow the root's verse numbers, so linking by number sends 8 of its 13 paragraphs to a different or an extra verse, and leaves `13.` unlinked (§3).
  - The file links by number, exactly as tipitaka.app does. This is by the user's decision; it is recorded here for a reader.

## 1. Inputs are current

| Check | Result |
|---|---|
| `s0501m.mul.xml`, `s0501a.att.xml`, `s0501t.nrf.xml` vs upstream `romn/` (git blob SHA) | 3 / 3 identical |
| tipitaka.app `kn-khp`, `atta-kn-khp` fetched again today vs the copies in `0-INBOX/tipitaka-app/` | 6 / 6 identical |
| `s0501t.nrf.xml` | confirmed to be the **Nettivibhāvinī** (ṭīkā on the Nettippakaraṇa), not a Khuddakapāṭha ṭīkā. The Khuddakapāṭha has only an aṭṭhakathā. |

## 2. Results

### 2.1 The skill's own checkers, rerun in place (`--per-section`)

| Check | Result |
|---|---|
| `verify.py` (root vs XML) | PASS: 89 IDs + 2 `U`, 1,305 words identical |
| `compare_site.py` (root vs site) | PASS: 208 / 208 lines, 89 / 89 numbers in their block, contents tree 9 / 9 |
| `verify_commentary.py` (aṭṭhakathā vs XML) | PASS: 37,935 words identical, 68 citations: 67 linked, 1 logged |
| `compare_site_commentary.py` | 1,234 / 1,234 lines, contents tree 110 / 110. One difference: the site links `13.` to Maṅgala v. 13 (§3) |

### 2.2 Independent checks (no code shared with the skills)

**Root (`pi-kn-1.md`):**
- **Headings:** the 9 sections match the site's contents tree (title and depth) and a fresh parse of the XML. Heading IDs `^1-1-0` … `^1-9-0` equal the site's keys `kn-khp-1` … `-9`.
- **Blocks:** grouping the site's lines the way the file groups them (each printed number starts a block), all **91 blocks match exactly**: section, printed number and every word.
  - The two unnumbered sections, Saraṇattaya and Dvattiṃsākāra, are `^1-U1` and `^1-U2`.
- **Numbering:** verse numbers run 1…n with no gaps in every numbered section: 10, 10, 13, 18, 12, 16 and 10 verses.
- **Outline:** levels, parent and child IDs, and sibling numbering all pass; there are no duplicate IDs.

**Aṭṭhakathā (`pi-kn-1-atthakatha.md`):**
- **Headings:** 110 / 110 headings match the site (title and depth) and the XML.
  - Sections `1-1-0` … `1-9-0` correspond to the root's sections.
  - The front matter `Ganthārambhakathā` is `^1-I-0`, with sub-headings `^1-I-I-0` and `^1-I-II-0`; roman numerals are the vault's front-matter convention.
- **Text:** 37,867 words, identical to the site. The only difference is a site artefact: the site runs three bold spans together (`cittaṃyassana`), while the XML and the file keep the spaces.
- **Links by number:**
  - every link resolves;
  - every link stays inside its own section;
  - every link sits directly before its numbered paragraph;
  - the sequence equals the site's, apart from the logged `13.`.
- **No links in sections 2 and 4:** the aṭṭhakathā prints no paragraph numbers there (Sikkhāpada, Kumārapañha), so nothing is missing.
- **Links by meaning:** for each linked paragraph, the words it glosses in bold were compared with every root verse of its section.
  - **Maṅgala, Ratana, Metta:** all match.
  - **Nidhikaṇḍa:** all match except `5.`, which glosses verse 4 and verse 5 together. `4.` is a bridge with no glosses, so linking `5.` to verse 5 is defensible.
  - **Tirokuṭṭa:** see §3.

## 3. ⚑ Tirokuṭṭasutta: the aṭṭhakathā numbers its verses differently

**The cause:**
- Each aṭṭhakathā paragraph here is a bridge ("Evaṃ bhagavā … dassento –"), followed by the verse and its glosses.
- The aṭṭhakathā splits root **verse 3** (three lines) into two: `3.` glosses its first two lines, and `4.` its last line, "idaṃ vo ñātīnaṃ hotu, sukhitā hontu ñātayo".
- From there on, its numbers run one ahead of the root's 12 verses, which is why it has a `13.`.
- The intake (and tipitaka.app) link by number, so:

| Aṭṭhakathā | Glosses (bold) | Root verse by meaning | Linked now |
|---|---|---|---|
| `1.` `2.` `3.` | tirokuṭṭā…; pahūte annapānamhi…; evaṃ dadanti ñātīnaṃ… | v1, v2, v3 | ✅ v1, v2, v3 |
| `4.` | "idaṃ vo ñātīnaṃ hotu", "sukhitā hontu ñātayo" | v3 | ❌ v4 |
| `4-5.` | "te ca tattha", "pahūte annapānamhi", "anumodare" | v4 | ⚠ v4 + v5 |
| `5-6.` | "ciraṃ jīvantu", "amhākañca katā pūjā", "dāyakā ca anipphalā" | v5 | ⚠ v5 + v6 |
| `6-7.` | "na hi tattha kasi", "vaṇijjā tādisī", "ito dinnena yāpenti" | v6 | ⚠ v6 + v7 |
| `8-9.` | "unname udakaṃ vuṭṭhaṃ" … *gāthādvayamāha* ("spoke these two verses") | v7 + v8 | ❌ v8 + v9 |
| `10.` | "adāsi me", "petānaṃ dakkhiṇaṃ dajjā" | v9 | ❌ v10 |
| `11.` | "na hi ruṇṇaṃ vā", "soko", "paridevanā" | v10 | ❌ v11 |
| `12.` | "ayañca kho dakkhiṇā", "upakappati" | v11 | ❌ v12 |
| `13.` | "so ñātidhammo ca ayaṃ nidassito", "balañca bhikkhūnamanuppadinnaṃ" | v12 | — unlinked (logged as unresolved) |

**Effect:**
- 5 paragraphs link to the wrong verse;
- 3 link one extra verse;
- `13.` is unlinked although its verse exists.
- A reader following the transclusions in this section sees the commentary next to the wrong verse.
- The printed numbers are the source's own and stay as printed. Only the links are affected.

**Undone 2026-11-16 at the user's instruction ("keep it as it is with website and repo").**
- **What was undone:** the links, the `[Ed:]` note and the unresolved log are back as built.
- **How it was confirmed:** a fresh build from the XML (`build_kn_comm.sh` into a scratch folder) is identical to the file. The only difference is the three library-field lines added after the build.

What had been done, for the record:
- **Links:** the 9 paragraphs now link by meaning, as in the table's "by meaning" column. `13.` links to v12. The printed numbers and all wording are unchanged.
- **Note:** an `[Ed: …]` note at the end of `4.`, before `^1-762`, records the different count and the mapping.
- **Log:** in `0-INBOX/temp/kn-comm/pi-kn-1-atthakatha.unresolved.json`, `13.` is no longer unresolved. The 9 changes are listed under `corrections`, with the by-number and by-meaning targets of each.
- **Re-checked:**
  - In the meaning check, every Tirokuṭṭa paragraph now links to the verse whose words it glosses.
  - The outline check still passes.
  - Every link resolves and stays in its section.
- **Expected checker output from now on:**
  - `verify_commentary.py` reports exactly the 9 corrected links and the note's words as differences from the XML numbers, as with the SN 5 Daṇḍasutta fix.
  - `compare_site_commentary.py` likewise differs from the site's number-based links in this section.
- **Regeneration undoes it.** Rebuilding the file with `build_kn_comm.sh` would undo the fix, so reapply it after any rebuild. The KN session should be told before it uploads this file.

## 4. Library fields

The root and aṭṭhakathā carry:
- `license: cc0`;
- `tag_ids: [296WZOr8MXWteSqBBI7pl]` (Theravāda);
- `category_id: XfCwZpoJMtfO7s0laQkdK` (Discourses).

These are the values confirmed against library-prod for the Sutta texts. Neither file is uploaded.

## 5. Not checked

- **The Dhammapada (`pi-kn-2`)** was not part of this check. Its aṭṭhakathā links 436 verse citations by number, and those are worth the same meaning check.

---

## 6. Uploaded to library-prod.webuddhist.com (2026-11-16)

The files were uploaded **as the website and repo give them**: the Tirokuṭṭa links are by number (§3).

**Method:** for each file, a dry run with live checks, then `--execute`, then `--verify`, as for the DN, MN, SN and AN. The logs are in `0-INBOX/temp/kn-upload/`. Before the upload, library-prod held no Khuddakapāṭha text; 1,749 texts were searched.

| File | text_id | edition_id | toc_id | Live segments | TOC nodes | Alignment pairs → root edition |
|---|---|---|---|---|---|---|
| pi-kn-1 Khuddakapāṭhapāḷi | `MuwKRemR27jr6NkqjLnyl` | `yULAowUT247bjf8KSJ77D` | `1mlXm3dPsnQ6D9peeA6Bc` | 92 | 11 | — |
| pi-kn-1-atthakatha Khuddakapāṭha-aṭṭhakathā | `34v6YtfpXUmphlvsbwkK0` | `Rc6AC2Gudf3v88PwwELYU` | `mc0902hGLsD6zqdfTauHv` | 970 | 112 | 616 → `yULAowUT247bjf8KSJ77D` |

**What was checked:**
- **Segments:**
  - the root has 89 verses + 2 `U` + the homage `T-1`;
  - the aṭṭhakathā has its 969 content blocks + `T-1`.
- **TOC nodes:** they equal each file's headings.
- **Alignment:** 616 pairs, from 596 aṭṭhakathā segments to 68 root segments. Every target was present in the live root before the upload.
- **Commentary link:** the aṭṭhakathā is `commentary_of` the root text, and the root lists it as its commentary.
- **Library fields, read back live:**
  - both texts: category Discourses, tag Theravāda, licence `cc0`;
  - titles `Khuddakapāṭhapāḷi` and `Khuddakapāṭha-aṭṭhakathā`.
- **IDs:** they are in both files' frontmatter and in the two upload ledgers.
- **Side effect:** the linter's `languages.py` timestamp rewrites were restored with `git checkout`.

**Not done:**
- **Commit:** nothing is committed. The KN files are still uncommitted work of the KN intake.
- **The Dhammapada (`pi-kn-2`):** not uploaded. library-prod already has a Pāli "Dhammapada" (`UuRrxK8JmoqsfHBYYZDqs`, tagged Chants) with an English translation; how ours relates to it is a decision to take first.
