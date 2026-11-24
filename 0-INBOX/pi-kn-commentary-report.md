# Khuddakanikāya commentaries — books 3–20 (cscd-commentary-intake)

Each commentary is built against its book's verified root draft (`0-INBOX/temp/kn/pi-kn-<book>.md`, the same block IDs as in `pi-khuddakanikaya.md`). It is checked against its XML and tipitaka.app. Then it is joined onto `1-SOURCES/Commentaries/pi-khuddakanikaya-atthakatha.md` with `merge_volumes.py --relink 0-INBOX/temp/kn/pi-kn-<book>.md=1-SOURCES/Text/pi-khuddakanikaya.md`.

`verify_commentary.py` reads one book number from the root file name, so it verifies each book's draft, not the joined file. For the joined file, `merge_volumes.py --split` proves it splits back into the verified parts. Every link is then checked to resolve in `pi-khuddakanikaya.md`.

## Book 3 — Udāna-aṭṭhakathā (`s0503a.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs tipitaka.app `atta-kn-ud` | 1,676 = 1,676 |
| `verify_commentary.py` | PASS: content `^3-1`…`^3-1383`, 70,335 words = XML, 3,050 bold spans |
| Citations | 92 printed, 92 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | 90 = 90, ALL MATCH |
| `compare_site_commentary.py` | PASS: 1,676 paragraphs matched, 92 of 92 links agree with the site |
| Heading IDs vs root | 90 of 92 equal the root's (same titles); the other two are the front matter and the Nigamanakathā |

**Human decisions:**
- **`Ganthārambhakathā` is front matter, `^3-I-0`**, as in the vault's 11 other commentaries. It has 52 paragraphs: homage verses, the author's purpose, and an introduction to the Udāna as a whole (what an udāna is, 80 suttas in 8 vaggas). It ends with a lead-in to the Bodhivagga. It has no numbers of its own.
- **`Nigamanakathā` is its own `###`, `^3-9-0`**, after the eight vaggas. The XML prints it as a `subhead` right after "Niṭṭhitā ca pāṭaligāmiyavaggavaṇṇanā.", so it would otherwise sit inside the last vagga. This follows the skill's Dīghanikāya precedent and the Milindapañha's Nigamanaṃ. The XML-level draft is kept as `0-INBOX/temp/kn-comm/pi-kn-3-atthakatha.xmllevels.md`.

**Site differences, all explained:**
- The site joins two bold groups that the XML keeps apart.
- The site nests the Nigamanakathā under sutta 10. The vault places it after the vaggas (decision above).

**Join:**
- `merge_volumes.py`: book 3's opening homage and `Khuddakanikāye` are kept as text, `^3-T1`/`^3-T2`.
- Split proof OK. 6,315 block IDs, all unique.
- 599 links, all resolving in `pi-khuddakanikaya.md`: book 1 has 71, book 2 has 436, book 3 has 92.

From book 4 on, every book runs through `0-INBOX/temp/kn-comm/kn_comm_book.py`. It joins only if all of these pass:
- verify;
- headings;
- the site check;
- no unresolved citation;
- **tree vs root**: every `###` carries the root's ID and title, and at least 90% of all headings do.

## Book 4 — Itivuttaka-aṭṭhakathā (`s0504a.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-iti` | 1,759 = 1,759 |
| `verify_commentary.py` | PASS: `^4-1`…`^4-1407`, 60,345 words = XML, 2,549 bold spans |
| Citations | 108 printed, 108 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | 125 = 125, ALL MATCH |
| Site | PASS: 1,759 paragraphs, 108 of 108 links agree |
| Tree vs root | 112 of 122 headings carry the root's ID and title, and so do all `###`s |

**A tool error, caught and fixed before the join was kept.** The first run joined book 4 with a wrong contents tree: the vaggas sat beside their nipāta, and the Dukanipāta sat under the Ekakanipāta's last vagga.
- **Cause:** `cscd_shape.tree_levels` ranks `title` above `chapter` (an AN rule). The Itivuttaka-aṭṭhakathā uses them the other way round: `chapter` is the nipāta, `title` the vagga.
- **Fix:** in a file with no `<div>`s, the first real `title`/`chapter` (part labels excluded) is the outer level. Books 1–3 convert to identical heading levels.
- **The bad join was reverted** from the backup. The tree-vs-root gate was then added, so it cannot happen again.

**Human decisions:**
- `Ganthārambhakathā` → `^4-I-0` (standing).
- `Nidānavaṇṇanā` → second front matter `^4-II-0` (decided for this book). It is 125 paragraphs on the formula "vuttañhetaṃ bhagavatā …" that opens every sutta, before the Ekakanipāta.
- `Nigamanakathā` → `### ^4-5-0` (standing).

**Headings that differ from the root, all explained:** where the commentary groups suttas, its sibling numbers shift.
- "1-3. Mohapariññādisuttavaṇṇanā": 6 headings in the Ekakanipāta's second vagga.
- "Āsavasuttadvayavaṇṇanā": 3 headings in the Tikanipāta's first vagga.

The transclusions carry the exact alignment.

**Join:** 711 links, none broken; 7,850 block IDs, all unique.

## Book 5 — Suttanipāta-aṭṭhakathā (`s0505a.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-snp` | 2,686 = 2,686 |
| `verify_commentary.py --zones 1,2` | PASS: `^5-1`…`^5-2349`, 119,194 words = XML, 5,787 bold spans |
| Citations | 906 printed: 905 linked right, 0 wrong, 1 unresolved (below) |
| Transclusions | 1,106, all into the main verses `^5-1-N` (the commentary does not treat the Suttuddāna `^5-2-N`) |
| `check_headings.py` | 80 = 80, ALL MATCH |
| Site | 2,686 paragraphs matched; 905 of 905 links agree with tipitaka.app, zone included |
| Tree vs root | 74 of 78 headings carry the root's ID and title, and so do all `###`s |

**Unresolved citation, a source slip, left unlinked (Rule 2).** The note on "Asaṃhīraṃ asaṅkuppaṃ …" is printed `1156.`. In the root that verse is 1155, the last main verse, and 1156 does not exist. tipitaka.app does not link it either.

**Headings that differ from the root, all explained:**
- Two suttas go under their other names, at the right positions: `Aggikabhāradvājasuttavaṇṇanā` for the root's Vasalasutta, and `Pūraḷāsasutta-(sundarikabhāradvājasutta)` for the Sundarikabhāradvājasutta.
- The front matter and the Nigamanakathā (standing decisions).

**The second printed part.** The XML reprints a part opening after the Hirisutta: homage, `Khuddakanikāye`, the book title, "(Dutiyo bhāgo)", and "2. Cūḷavaggo" again, since that vagga is still running. Under Rule 4 all of these are kept as text.
- `cscd_shape.tree_levels` and `check_headings.py` now both treat a heading that repeats one still open, right after a reprinted book line, as a reprint. Without this the repeated vagga became a heading, and Maṅgala … Dhammika fell one level under it.
- tipitaka.app lists `Suttanipāta-aṭṭhakathā` and `Cūḷavaggo` there as contents nodes. That is the one site tree difference, accepted as explained.

**Tool changes for zoned roots:**
- **Linking:** the new `zone_link.py` is shared by the linker and `verify_commentary.py`. A citation goes to the zone whose blocks hold every cited number and lie next in the root's order.
- **Site check:** `compare_site_commentary.py --zones` takes each site link's zone from the root's run rules (`zones.py`).
- **Regression:** books 3–4 still PASS, and all 23 KN conversions so far (root and commentary) are identical.

**Join:** 1,817 links, none broken; 10,282 block IDs, all unique.

## Book 6 — Vimānavatthu-aṭṭhakathā (`s0506a.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-vv` | 3,114 = 3,114 |
| `verify_commentary.py` | PASS: `^6-1`…`^6-2046`, 50,674 words = XML, 2,235 bold spans |
| Citations | 1,381 printed: 1,375 linked right, 0 wrong, 7 logged as unresolved (below) |
| `check_headings.py` | 95 = 95, ALL MATCH |
| Site | PASS: 3,114 paragraphs matched; 1,375 of 1,375 links agree |
| Tree vs root | 91 of 93 headings carry the root's ID and title: Itthivimānaṃ `^6-1-0` and Purisavimānaṃ `^6-2-0` with their vaggas and vimānas. The other two are the front matter and the Nigamanakathā |

**Seven unresolved citations, left unlinked (Rule 2):** `229-231.` (231 only; 229 and 230 are linked), `248.`, `509.`, `549.`, `589.`, `721.`, `938.`.
- Each quotes a verse elided with "…pe…" that the root's XML counts but never prints. None of these numbers occurs in `s0506m`, and they are among the root's 101 recorded gaps.
- tipitaka.app does not link them either.

**A tool fix: quoted one-line verses.**
- **The problem:** the commentary quotes runs of one-line verses, each with its own printed number and no closing `gathalast` (for example "256. …", "258. …", "261. …", "262. …"). `commentary_converter.py` kept collecting the gāthā until a `gathalast`, so such a run became one block. Only its first citation could be linked; 47 citations had no block of their own.
- **The fix:** a numbered (`@n`) gāthā line now closes the gāthā that is still open.
- **Earlier books:** the pattern occurs 0 times in books 1–5 (counted in their XML), so they cannot change.

**Site notes:** the site nests Uposathāvimānavaṇṇanā and the Nigamanakathā differently, as with the earlier books.

**Join:** 3,252 links, none broken; 12,426 block IDs, all unique.

## Book 7 — Petavatthu-aṭṭhakathā (`s0507a.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-pv` | 2,532 = 2,532 |
| `verify_commentary.py` | PASS: `^7-1`…`^7-1659`, 43,967 words = XML, 2,106 bold spans |
| Citations | 1,067 printed, 1,067 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | 57 = 57, ALL MATCH |
| Site | PASS: 2,532 paragraphs matched; 1,067 of 1,067 links agree |
| Tree vs root | 54 of 55 headings carry the root's ID and title: the four vaggas `^7-1-0`…`^7-4-0` and their stories. The one other is the same story spelled `Ḍhubbaripetavatthuvaṇṇanā` against the root's `Ubbaripetavatthu` (`^7-2-13-0`) |

Front matter `^7-I-0` and `Nigamanakathā` `^7-5-0` (standing decisions). No tool change was needed.

**Join:** 4,511 links, none broken; 14,145 block IDs, all unique.

## Book 8 — Theragāthā-aṭṭhakathā (`s0508a1.att` + `s0508a2.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-thag` | 10,810 (the two volumes joined) = 10,810 non-empty site paragraphs (the site counts 2 empty ones as well) |
| `verify_commentary.py` | PASS: `^8-1`…`^8-6544`, 162,201 words = XML, 6,505 bold spans |
| Citations | 1,281 printed, 1,281 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | 304 = 304, ALL MATCH |
| Site | 10,810 paragraphs matched; 1,279 links agree, and the other 2 are the empty-paragraph case below |
| Tree vs root | **303 of 303** headings carry the root's ID and title: Nidānagāthāvaṇṇanā `^8-1-0` (as the root's `^8-1-0`, kept by human decision), then the 21 nipātas `^8-2-0`…`^8-22-0` |

**Two volumes.** `merge_parts.py` joins them, and volume 2's opening (homage, `Khuddakanikāye`, title, "(Dutiyo bhāgo)") is kept as text, as tipitaka.app shows it.

**A tool fix in `merge_parts.py`.** It ended a later volume's opening at the first segment tagged `chapter`. A `--tree` JSON tags headings `heading`, so the whole second volume (5,589 lines) would have been flattened to text. It now stops at either tag, and only the four opening lines are retyped.

**Empty numbered paragraphs, explained.** At 420 and 845 the XML prints the number on an empty `<p rend="gatha1"></p>`, with the verse in the next paragraph.
- **The vault** gives the number and its link to that verse, as in the root texts: `![[…#^8-420]]` stands above "420. Vedanānaṃ viññāpano …".
- **tipitaka.app** counts the empty paragraph and hangs its link there. Both point at the same root verse.

The book script accepts only this exact pattern: the site paragraph is empty, and the vault links the same number on the next verse.

No Nigamanakathā heading: the work ends with its colophon lines.

**Join:** 5,795 links, none broken; 20,996 block IDs, all unique.

## Book 9 — Therīgāthā-aṭṭhakathā (`s0509a.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-thig` | 4,024 = 4,024 |
| `verify_commentary.py` | PASS: `^9-1`…`^9-2381`, 47,195 words = XML, 1,875 bold spans |
| Citations | 524 printed, 524 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | 85 = 85, ALL MATCH |
| Site | PASS: 4,024 paragraphs matched; 524 of 524 links agree |
| Tree vs root | 76 of 84 headings carry the root's ID and title, and so do all 16 nipātas `^9-1-0`…`^9-16-0`. No front matter: the work opens with the Ekakanipāta |

**Headings that differ from the root, explained (reviewed, `--accept-tree`).** In the Ekakanipāta, "Tissāditherīgāthāvaṇṇanā" covers six therīs of the root at once: Aññatarā Tissā, Dhīrā, Vīrā, Mittā, Bhadrā and Upasamā. So the commentary has 13 headings there for the root's 18, and the 8 after the group are numbered one position off. The transclusions carry the exact verses.

**Closing section, a decision by analogy.** `Nigamanagāthā`, the author's closing verses for the whole work, naming it *Paramatthadīpanī* with its size and dedication, became its own `### ^9-17-0`. This applies the human decision for the Nigamanakathā. The XML has it inside the Mahānipāta (`#### ^9-16-2-0`). The book script now recognises both names.

**Join:** 6,319 links, none broken; 23,465 block IDs, all unique.

## Book 10 — Apadāna-aṭṭhakathā (`s0510a.att`, 2026-11-24)

It covers the Therāpadāna only (book 10). CSCD has no commentary on the Therīapadāna (book 11).

| Check | Result |
|---|---|
| Segments vs `atta-kn-ap` | 3,823 = 3,823 (one of the site's paragraphs is the number-only "314", shown empty) |
| `verify_commentary.py --per-section` | PASS: `^10-1`…`^10-2852`, 113,537 words = XML, 4,876 bold spans |
| Citations | 981 printed: 973 linked right, 0 wrong, 8 unresolved (below) |
| `check_headings.py` | 312 of 313: only "Therāpadānaṃ" differs (text by decision) |
| Site | accepted: all paragraphs matched; every link difference is the explained artefact below |
| Tree vs root | 263 of 280 headings carry the root's ID and title, and so do all vaggas (on their printed numbers) |

**Human decisions (2026-11-24), applied by `0-INBOX/temp/kn-comm/apadana_shape.py` (headings only, words unchanged):**
- **The Nidāna is front matter, nested:**
  - `### Nidānakathā ^10-II-0`
  - `#### Dūrenidānakathā ^10-II-I-0`, holding `##### Sumedhakathā` and one section per Buddha, `Dīpaṅkaro buddho` … `Gotamo buddho ^10-II-I-XXVI-0`
  - `#### Avidūrenidānakathā ^10-II-II-0` and `#### Santikenidānakathā ^10-II-III-0`

  The XML tags the Sumedhakathā and the Buddhas beside the Nidānakathā. The text tells the Sumedhakathā inside the Dūrenidāna ("imasmiṃ ṭhāne sumedhakathā kathetabbā").
- **"Therāpadānaṃ" is text** (`^10-531`, and the part-2 reprint `^10-1553`). As a heading it would push every vagga to `####`.
- **Vagga IDs follow the printed number.** The commentary has 42 vagga headings for the root's 56; "21-23", "34-38", "43-48" and "50-53" each cover several root vaggas. Each heading takes its first vagga's root ID (21-23 → `^10-21-0`, 24 → `^10-24-0` … 56 → `^10-56-0`), and the Nigamanakathā follows at `^10-57-0`.

**Unresolved citations, left unlinked (Rule 2):** `1.`, `2.`, `1.`, `30.`, `56.`, `61.`, `66.`, `72.`, all under "43-48. Sakiṃsammajjakādivaggo". That heading names no single vagga, and the root numbers each vagga from 1.
- **Evidence for a reviewer from the text:** "1. Pañcacattālīsamavagge paṭhamāpadāne …" (vagga 45), "1. Chacattālīsame vagge paṭhamāpadāne …" (vagga 46). The later ones name only the apadāna ("Tatiyāpadāne", "Chaṭṭhāpadāne" …).
- **From the site:** its gloss links point to vaggas 45, 46 and 48.

**Site differences, explained:**
- **533 number links in another vagga.** tipitaka.app resolves a printed number across the whole root book, not within its vagga. For example, commentary paragraph 939 ("11." on the Buddhāpadāna) has its number link at vagga 30's paragraph 11, while its own gloss links point into vagga 1, where the vault links it (`^10-1-11`). In 532 of these the site's gloss links name the vault's vagga; one has no gloss link, and the vault links the same number in its current vagga.
- **The number-only paragraph** "314" (`<p n="314">314</p>`, its dot opening the next paragraph). The site shows it empty. The vault links it (`^10-1-314`), and the site's gloss link names vagga 1 too.
- **Contents:** the site lists "Therāpadānaṃ" (twice) and the part-2 book title as contents nodes.

**Heading differences from the root, explained:**
- **Vagga 1** opens with an `Abbhantaranidānavaṇṇanā`, the commentary's own introduction to the Therāpadāna. It shifts the 12 apadāna headings after it by one.
- **Vaggas 39–40:** the commentary explains only selected apadānas (Soṇakoṭivīsa, the Pubbakammapilotika-buddhāpadāna, Bākula, Girimānanda).
- **Vagga 50:** "Kiṅkaṇipupphiyattheraapadānādi…" is the root's Tikiṅkaṇipupphiya apadāna under a slightly different name.

**Tool changes:**
- **`commentary_converter.py` (tree mode):** a number-only paragraph whose printed number is its `@n` is a citation. `verify_commentary.py` counts such a block as cited. The case occurs in none of books 1–9.
- **`compare_site_commentary.py --all`** prints every problem.
- **The book script** gained `--shape`, `--text-heading`, the per-vagga site acceptance, and a count check that allows either of the site's two counting habits.

**Join:** 7,399 links, none broken; 26,632 block IDs, all unique.

## Book 11 — Therīapadāna

There is no commentary: the Apadāna-aṭṭhakathā (`s0510a`) covers the Therāpadāna only.

## Book 12 — Buddhavaṃsa-aṭṭhakathā (`s0511a.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-bv` | 3,291 = 3,291 |
| `verify_commentary.py --per-section` | PASS: `^12-1`…`^12-2099`, 57,186 words = XML, 2,054 bold spans |
| Citations | 874 printed, 874 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | all but "Abbhantaranidānaṃ" (text by decision) |
| Site | all 3,291 paragraphs and all 874 links agree; the only difference is the site listing "Abbhantaranidānaṃ" as a contents node |
| Tree vs root | all 28 chapters `^12-1-0`…`^12-28-0` carry the root's ID and title. The other 8 headings are the commentary's own sub-sections, with no counterpart in the root: Dūre-, Avidūre- and Santikenidānakathā under Gotama, and five topics under Buddhapakiṇṇaka |

**Human decisions (2026-11-24), as for the Apadāna, applied by `0-INBOX/temp/kn-comm/buddhavamsa_shape.py` (headings only):**
- `### Nidānakathā ^12-II-0` (no text of its own), front matter, with `#### Bāhiranidānaṃ ^12-II-I-0` (2 paragraphs) under it.
- "Abbhantaranidānaṃ", a title with no text of its own printed above the 28 chapters, is text (`^12-…`). The chapters are `###` on the root's IDs.
- The closing Nigamanakathā is `^12-30-0`, after the root's 29 sections. The root's section 29, the Dhātubhājanīyakathā, has no commentary.

**Tool change:** the site acceptance also covers headings decided as text (`--text-heading`).

**Join:** 8,295 links, none broken; 28,774 block IDs, all unique.

## Book 13 — Cariyāpiṭaka-aṭṭhakathā (`s0512a.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-cp` | 2,011 = 2,011 |
| `verify_commentary.py --per-section --presection 1` | PASS: `^13-1`…`^13-1532`, 58,575 words = XML, 1,835 bold spans |
| Citations | 325 printed, 325 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | all but the Nigamanakathā, made a heading (below) |
| Site | all 2,011 paragraphs and all 325 links agree; the site has no contents node for the Nigamanakathā |
| Tree vs root | 37 of 40 headings carry the root's ID and title, and so do all three vaggas `^13-1-0`…`^13-3-0`. The other three: `Mahāsutasomacariyāvaṇṇanā` is the root's Sutasomacariyā under its fuller name; `Uddānagāthāvaṇṇanā` and `Pakiṇṇakakathā` are the commentary's own sections |

**Placements applied by analogy with earlier human decisions (easy to undo):**
- **`Nidānakathā`** is front matter `^13-II-0`, as for the Itivuttaka, Apadāna and Buddhavaṃsa.
- **`Nigamanakathā`** is its own `### ^13-4-0`. The XML prints it as a big title line (`<p rend="nikaya">`), as in the Milindapañha, so the converter kept it as text. It is made a heading (`--heading-from-text`), as you decided for the Milindapañha's Nigamanaṃ, and placed like every closing Nigamanakathā.

**Two citations in the front matter, linked by what they quote (`--presection 1`).** The Nidānakathā's "1." reads "Idāni '**kappe ca satasahasse**'tiādinayappavattāya cariyāpiṭakapāḷiyā atthasaṃvaṇṇanā". Its "2." ends "… '**atītakappe**'tiādimāha". These are the opening words of the root's verses 1 and 2, `^13-1-1` "Kappe ca satasahasse …" and `^13-1-2` "Atītakappe caritaṃ …". So citations before the first numbered section go to section 1. tipitaka.app links them to vagga 1 as well. The option acts only before the first numbered section, so a later heading without a single number (the Apadāna's "43-48") cannot inherit it.

**Kept as in the XML:** the `Pakiṇṇakakathā`, a general treatise on all the pāramīs that the text places at this point ("Imasmiṃ pana ṭhāne ṭhatvā … pakiṇṇakakathā kathetabbā"), stays under the Uddānagāthāvaṇṇanā in vagga 3.

**Tool changes:**
- `build_commentary.py`, `commentary_converter.py` and `verify_commentary.py` take `--presection`.
- The book script takes `--heading-from-text` and `--presection`, with matching acceptance in the heading and site checks.

**Join:** 8,644 links, none broken; 30,352 block IDs, all unique.

## Book 14 — Jātaka-aṭṭhakathā (`s0513a1`–`a4.att`, `s0514a1`–`a3.att`: seven volumes, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-jat` | 25,920 = 25,920 |
| `verify_commentary.py --per-section` | accepted: `^14-1`…`^14-17473`, 583,311 words against the XML's 583,312, 14,200 bold spans. The only word differences are three printed numbers of titles the shape moves (below) |
| Citations | 6,493 printed: 6,491 linked right, 0 wrong, 2 unresolved (below) |
| `check_headings.py` | accepted: the 89 XML headings all match. The differences are the 546 headings the shape adds (544 jātaka titles, 2 vaggas) and the 2 lines it makes text |
| Site | all 25,920 paragraphs match. Of the 6,493 number links, 2,193 agree with tipitaka.app outright. The other 4,300 are the per-section artefact seen before: tipitaka.app looks a number up across the whole root book. 4,271 of these are accepted because the site's own gloss links name the vault's nipāta. 28 are accepted because their gloss links name a parallel elsewhere (SN, another jātaka) while the vault's linked root verse has the paragraph's own words (text ratio ≥ 0.85; 0.88 to 1.00). 1 is the unresolved "3." |
| Tree vs root | 610 of 627 headings carry the root's ID and title, and so do all `###`s (below) |

**Human decisions (2026-11-24), applied by `0-INBOX/temp/kn-comm/jataka_shape.py` (headings only):**
- **The Nidāna is front matter, nested as in the Apadāna:** `### Nidānakathā ^14-II-0` › `#### Dūrenidānakathā ^14-II-I-0` › `##### Sumedhakathā ^14-II-I-I-0`; `#### Avidūrenidānakathā ^14-II-II-0`; `#### Santikenidānakathā ^14-II-III-0`. The Ganthārambhakathā is `^14-I-0` (standing decision).
- **All 547 jātakas are headings.** The XML prints 544 of the titles as plain paragraphs ("[11] 1. Lakkhaṇamigajātakavaṇṇanā"). Each is a heading one level below its vagga, or below its nipāta where the nipāta has no vaggas, as in the root. It keeps its printed numbers, so the words stay those of the XML. A jātaka's own sub-sections (the Mahānipāta's kaṇḍas) go one level below it.

**Mis-tagging corrected (Rule 4):**
- "2. Pucimandavaggo" and "3. Kuṭidūsakavaggo" are tagged like the nikāya line, so the converter kept them as text. They are made vagga headings like their siblings.
- "Catuttho bhāgo" is a volume label printed without brackets, so it is text.
- "22. Mahānipāto" is reprinted at the start of volume 7, where the Mahānipāta runs on from volume 6. It is text.
- These moves account for the three word differences: a heading's printed number is not text, so the XML's "2." and "3." drop out and the reprint's "22." comes in. The book script accepts exactly these numbers, once each.

**Vessantara kaṇḍas on the root's IDs.** The commentary has headings only from Jūjakapabbavaṇṇanā on. The root has headings from Dasavarakathā, so its Jūjakapabbaṃ is its fifth kaṇḍa.
- **The problem:** the build numbered the commentary's kaṇḍas 1, 2, …, so `^14-22-10-1-0` "Jūjakapabbavaṇṇanā" would have claimed the root's Dasavarakathā.
- **The fix:** the shape script's new `post` step gives each sub-section the root's ID for the kaṇḍa of the same name (name less "-vaṇṇanā" and a final "ṃ"): Jūjakapabba `-5-0` … Chakhattiyakamma `-12-0`. Nagarakaṇḍavaṇṇanā, which the root lacks, follows as `-13-0`.
- **Bhūridatta:** the root gives it no sub-sections, so its seven kaṇḍas keep the build's `^14-22-6-1-0`…`-7-0`. These claim no root section.

**Headings that differ from the root (17), all explained:**
- 8 are jātakas under another spelling at the same position: Bhojājānīya/Gojānīya, Kāḷakaṇṇi/Kālakaṇṇi, Vissāsa-/Visāsabhojana, Kuṇḍakapūva/Kuṇḍapūva, Vaṭṭa/Vaṭṭaka, Khandha/Khaṇḍa, Vīṇāthūṇa/Vīṇāguṇa, Rājakumbha/Gajakumbha.
- 1 is `[152] 2. Siṅgālajātakavaṇṇanā ^14-2-1-2-0`, where the root's heading is a verse line (next item).
- 8 are the commentary's own sub-sections: the 7 Bhūridatta kaṇḍas and the Vessantara's Nagarakaṇḍavaṇṇanā.

**Two unresolved citations, left unlinked (Rule 2):**
- **`3.` (Dukanipāta), "Asamekkhitakammantaṃ, turitābhinipātinaṃ".**
  - The root's XML (`s0513m.mul`) tags this verse's first line as the jātaka heading `<p rend="subhead">152. Asamekkhitakammantaṃ…</p>`, and prints no Siṅgālajātaka title.
  - So in `1-SOURCES/Text/pi-khuddakanikaya.md` the line is `##### … ^14-2-1-2-0`, its second line is the unnumbered `^14-U2`, and there is no `^14-2-3`.
  - tipitaka.app does not link it correctly either: its number link goes to Sattakanipāta.
  - Repairing the root is a separate decision on a committed `1-SOURCES` file.
- **`22.` (Ekādasakanipāta), "Phalā ca mūlā ca pahūtamettha …".** The root's XML prints 21 twice, so the second verse is `^14-18-21x1` and there is no `^14-18-22`.

**Tool changes:**
- **A doubled quote split by a bold tag.** The XML has ‘‘<b>pāpenti suggati’</b>’nti. The converter keeps the tag where it is (`suggati’**’nti`), so it does not turn ’’ into ". `verify_commentary.py` and `compare_site_commentary.py` now remove `**` before normalising quotes, on the md side too. This is the only such case in the vault (counted in every `1-SOURCES` file), so earlier books cannot change.
- **The book script now accepts these exceptions:**
  - verify word differences that are exactly the printed numbers of titles a `--shape` moved;
  - a site or heading "replace" that only pairs a reprinted or decided-text line with decided headings;
  - a per-section number link whose gloss links name a parallel, when the linked root verse has the paragraph's words.

**Join:** 15,278 links, none broken; 48,461 block IDs, all unique; split proof OK.

## Book 15 — Mahāniddesa-aṭṭhakathā (`s0515a.att`, 2026-11-24)

| Check | Result |
|---|---|
| Segments vs `atta-kn-mn` | 1,833 = 1,833 |
| `verify_commentary.py` | PASS: `^15-1`…`^15-1676`, 75,589 words = XML, 7,324 bold spans |
| Citations | 209 printed, 209 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | 19 = 19, ALL MATCH |
| Site | PASS: 1,833 paragraphs matched; 209 of 209 links agree |
| Tree vs root | 16 of 18 headings carry the root's ID and title, and so does the one `###`, Aṭṭhakavaggo `^15-1-0` (`--accept-tree`, below) |

**The two headings that differ from the root:**
- `Cūḷabyūhasuttaniddesavaṇṇanā ^15-1-12-0` is the root's Cūḷaviyūhasuttaniddeso, spelled differently, at the same ID. Mahābyūha/Mahāviyūha passes only because the 4-letter check sees "maha" in both.
- `Tividhakalyāṇaṃ ^15-1-2-1-0` is the commentary's own sub-section under the Guhaṭṭhakasuttaniddesavaṇṇanā. The root has no counterpart, and the ID claims no root section.

**Standing decision:** the Ganthārambhakathā is front matter `^15-I-0`. There is no Nigamanakathā.

**Join:** 15,487 links, none broken; 50,159 block IDs, all unique; split proof OK.

## Book 16 — Cūḷaniddesa-aṭṭhakathā (`s0516a.att`, 2026-11-24)

Run: `kn_comm_book.py 16 s0516a.att atta-kn-nc kn-nc … --per-section --presection=2 --shape=0-INBOX/temp/kn-comm/nc_shape.py`

| Check | Result |
|---|---|
| Segments vs `atta-kn-nc` | 749 = 749 |
| `verify_commentary.py` | accepted: `^16-1`…`^16-669`, 24,232 md words / 24,233 XML. The one difference is the "2." of the Dutiyavagga title made a heading (below). 2,071 bold spans |
| Citations | 146 printed, 146 linked right, 0 wrong, 0 unresolved (6 abbreviated ranges such as "35-7." read as 35–37) |
| `check_headings.py` | accepted: the only difference is the inserted `Dutiyavaggavaṇṇanā` |
| Site | accepted: 749 paragraphs matched. Of the 146 links, 40 agree directly and 106 are text-verified (below) |
| Tree vs root | 25 of 25 headings carry the root's ID and title |

**Root structure.** The root has three `###`:
- Pārāyanavaggo `^16-1-0`: the sutta text, with paragraph IDs `^16-1-N`.
- Pārāyanavagganiddeso `^16-2-0`.
- Khaggavisāṇasutto `^16-3-0`, containing `#### Khaggavisāṇasuttaniddeso ^16-3-1-0` and four vaggas.

The niddesa's paragraph numbers run from the Pārāyana on into the Khaggavisāṇa, so both have IDs `^16-2-N` (the Khaggavisāṇa starts at `^16-2-131`).

**Decisions (`nc_shape.py`, headings only):**
- **Section IDs.** The commentary explains the niddesa only and has no section for the root's Pārāyanavaggo `^16-1-0`. The build numbered its sections 1, 2 and Nigamana 3, one short of the root, so each heading's section number moves up by one:
  - Pārāyanavagganiddeso becomes `^16-2-0`, and its 18 suttas take the root's `^16-2-N-0`.
  - Khaggavisāṇasuttaniddeso becomes `^16-3-0`, Khaggavisāṇasuttaniddesavaṇṇanā `^16-3-1-0`, and the vaggas `^16-3-1-1-0`…`-4-0`.
  - Nigamanakathā becomes `^16-4-0`, after the root's last section (the standing decision).
- **Mis-tagging.** "2. Dutiyavaggavaṇṇanā" is tagged `<p rend="centre">`, a closing line's style, while its siblings 1, 3 and 4 are `<p rend="subhead">`. It is now a vagga heading at their level. The site lists no node for it either, because it follows the XML.
- **Citation section.** Neither commentary `###` prints a number, so per-section linking has no section to read. `--presection=2` sends every citation to the root's section 2, the niddesa.

**Site links, 106 text-verified.** The site numbers its root sections differently from the vault: its `kn-nc-1` is the niddesa (the vault's `^16-2-`) and its `kn-nc-2` is the Khaggavisāṇa. So its links for the Pārāyana commentary name section 1. Each of the 106 was accepted only when both of these hold:
- The vault's linked block has the same printed number as the site's root paragraph.
- The vault's block starts with that paragraph's words (difflib ≥ 0.85 over the shorter of the two, never fewer than 12 letters; the site's paragraph can be only a verse's first line).

The number is needed because the root prints each Pārāyana verse twice (Pārāyanavaggo `^16-1-57` = niddesa `^16-2-1`), so the words alone fit both blocks. An audit confirmed that for every site link, the number picks exactly the vault's block. This check was added to `kn_comm_book.py` (`same_root_para`).

**Join:** 15,645 links, none broken; 50,857 block IDs, all unique; split proof OK; no bare LFs.

## Book 17 — Paṭisambhidāmagga-aṭṭhakathā (`s0517a.att`, 2026-11-24)

Run: `kn_comm_book.py 17 s0517a.att atta-kn-ps kn-ps … --zones=M,1,2,3 --shape=0-INBOX/temp/kn-comm/ps_shape.py --accept-tree`

| Check | Result |
|---|---|
| Segments vs `atta-kn-ps` | 2,515 vs 2,514 non-empty site paragraphs (2,515 with the empty one) |
| `verify_commentary.py` | PASS: `^17-1`…`^17-2108`, 118,874 words = XML, 6,556 bold spans |
| Citations | 367 printed, 367 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | 177 = 177, ALL MATCH |
| Site | accepted. Text and tree match except the reprinted volume-2 title "Paṭisambhidāmagga-aṭṭhakathā", kept as text (Rule 4). Of the 367 links, 178 agree directly and 189 are ones the site resolves in the wrong run (below) |
| Tree vs root | 132 of 175 headings carry the root's ID and title; every `###` matches (`--accept-tree`; misses below) |

**Citations by zone.** The root numbers its paragraphs in four runs: the Mātikā `^17-M-1…73`, then each vagga from 1 (`^17-1-`, `^17-2-`, `^17-3-`). The commentary's citations restart at the same places: Mātikāvaṇṇanā 1–73, then Mahāvagga 1–240, Yuganaddha 1–48, Paññā 1–42. So the zone linker (`--zones=M,1,2,3`) links each citation in the run that follows the last one. Per-section linking would not work, because no commentary `###` prints the vagga's number.

**Human decisions (2026-11-24), applied by `ps_shape.py`, headings only:**
- **Vaggas.** The XML puts "(1) Mahāvaggo", "(2) Yuganaddhavaggo" and "(3) Paññāvaggo" at the kathās' level. Following the root, they are now `###` on its IDs, with the kathās as `####` under them.
- **Nesting follows the root.** A heading whose name pairs with a root heading takes that heading's ID and level. Pairing ignores "-vaṇṇanā"/"-niddeso", printed numbers, Ka./Kha. letters and a final vowel, and accepts a spelling variant (Sabbaññutaññāṇa). It searches in root order among not-yet-used headings under the commentary's parent, then up to the vagga. So these four XML nestings take the root's:
  - "9. Saṅkhārupekkhā…" (the XML nests it under Ādīnava) becomes `^17-1-2-9-0`.
  - "68. Indriyaparopariyatta…" becomes `^17-1-2-44-0`.
  - The three chakkas go under Upakkilesa: `^17-1-4-3-1-0`…`3-0`.
  - The Indriyakathā's Ka./Kha./Ga. become siblings of their suttantas (`^17-1-5-3-0`…).
- **Grouped titles** take their first section, as in the Apadāna:
  - "41-42. Khantiñāṇapariyogāhaṇa…" becomes Khanti `^17-1-2-32-0`.
  - "Gha-ṅa. pariyādānaṭṭhapatiṭṭhāpakaṭṭha…" becomes the root's Ṅa. pariyādānaṭṭha `^17-1-5-15-0`. It explains pariyādāna and patiṭṭhāpaka, the root's Ṅa./Ca.; the root's Gha. adhiṭṭhāna has no heading here.
  - "Balādivārattaya" becomes Balavāro `^17-2-4-2-0`.
  - "Satipaṭṭhānavārādi" and "Sattabodhisattavārādi" become `^17-2-6-2-0` and `-4-0`.
- **Four pairings read from the texts** (`ALIAS`):
  - Vimokkhuddesa = Uddeso
  - Vimokkhaniddesa = Niddeso
  - Balādivārattaya = Balavāro
  - Vivaṭṭañāṇachakka = Chavivaṭṭañāṇa
- **The commentary's own headings (38)** keep the commentary's nesting and are numbered after the root's headings under the same parent, so their IDs claim no root section. They are:
  - the Sutamaya's 13 sub-sections;
  - Pañcañāṇapakiṇṇakaṃ;
  - each kathā's "…kathāvaṇṇanā" introduction (e.g. Yuganaddhakathāvaṇṇanā `^17-2-1-3-0`, placed before the root's Suttantaniddeso `^17-2-1-1-0` because the commentary prints it first);
  - **Mātikāvaṇṇanā** `^17-1-2-49-0`. It is printed right after "1. Ñāṇakathā", so it sits inside the Ñāṇakathā rather than on the root's Mātikā `^17-1-1-0`. Its 73 citations still link to `^17-M-1…73`.
- **Nigamanakathā** is `^17-4-0`, after the root's last section (the standing decision).

**Tree misses (43 of 175), all reviewed:**
- 38 are the commentary's own headings above.
- 5 are pairings whose first letters differ from the root's title, so the driver's 4-letter check misses them: Vimokkhuddesa/Uddeso, Vimokkhaniddesa/Niddeso, Vivaṭṭa-/Chavivaṭṭa-, the Gha-ṅa. group/Ṅa., and Cāravihāra/"Ga. cāravihāra" (the commentary prints no "Ga.").

Root headings with no commentary heading include:
- the Mātikā;
- Pariyogāhaṇa (in the Khanti group);
- the four Ānāpāna catukkas;
- the Indriyakathā's Gha. and Ca.;
- several Paṭisambhidā- and Dhammacakkakathā vāras inside groups;
- the Suññakathā's Mātikā/Niddeso;
- Dasaiddhi, and the Vivekakathā's Indriyaniddeso.

**Site links resolved in the wrong run (189).** tipitaka.app resolves a printed number in another run of the root. For example, the Mātikāvaṇṇanā's "1." points to the Paññāvagga's "Aniccānupassanā" instead of the Mātikā's "Sotāvadhāne paññā sutamaye ñāṇaṃ". The driver now accepts such a link (`zone_link_ok`, zoned roots only; list in `pi-kn-17-atthakatha.site-zone-accepted.txt`) when the number is the same and either:
- **Lemmas (173):** the vault's root block holds more of the commentary paragraph's bold lemmas than the site's root paragraph does; or
- **Run (16):** neither holds more, and the vault's block lies in the same run as the vault's citations on either side. I read all 16, and the vault's block is the passage the paragraph explains in each (e.g. "Chando mūlaṭṭhena…", the Sammasana niddesa, "Sabbe sattā averino…" in the Mettākathā).

In no case does the site's paragraph hold more of the lemmas. `kn_comm_book.py` also applies the book-16 check (same number, same opening words) to zoned roots, where it finds none.

**Join:** 16,046 links, none broken; 53,145 block IDs, all unique; split proof OK; no bare LFs.

## Book 19 — Nettippakaraṇa-aṭṭhakathā (`s0519a.att`, 2026-11-24)

Run: `kn_comm_book.py 19 s0519a.att atta-kn-nett kn-nett … --zones=,1 --shape=0-INBOX/temp/kn-comm/nett_shape.py`

| Check | Result |
|---|---|
| Segments vs `atta-kn-nett` | 1,095 = 1,095 site paragraphs |
| `verify_commentary.py` | accepted: `^19-1`…`^19-995`, 50,157 words vs 50,160 in the XML (the three dropped printed numbers "5.", "7.", "8." of the titles made headings), 3,718 bold spans |
| Citations | 146 printed, 146 linked right, 0 wrong, 0 unresolved |
| `check_headings.py` | accepted: the only differences are the 3 titles made headings |
| Site | accepted. Text 1,095 = 1,095; all 146 paranum links agree; the tree differs only by the 3 titles made headings |
| Tree vs root | 36 of 38 headings carry the root's ID and title; every `###` matches. The 2 misses are the commentary's own headings (below) |

**Citations by zone.** The root keeps one main count, ¶1–4 then ¶5–124 (`^19-N`). Inside the Niddesavāra, the Hārasaṅkhepa and Dvādasapada verses carry their own count 1–26 (`^19-1-N`). The commentary cites 1–4, then the verses 5–26, then the main count again from 5 in the Paṭiniddesavāra. `--zones=,1` links each citation in the run that follows the last one.

**Linker bug fixed (`zone_link.py`).** The first dry run linked the Paṭiniddesavāra's 5–26 to the verses `^19-1-5…26` instead of `^19-5…26`. A plain zone's prefix `19-` also matched zone 1's IDs, and `19-1-5` read as the plain range 1–5. Verify passed, since it applies the same rule. tipitaka.app's links disagreed on 26 citations: 20 were left over, and 6 more had been wrongly accepted by the book-17 run rule, because their neighbours were wrong too. A plain zone now takes no ID of a labelled zone. After the fix all 146 links agree with the site. Books 5 and 17, the only other zoned roots, have no plain zone, so the fix does not change them.

**Human decisions (2026-11-24), applied by `nett_shape.py`, headings only:**
- **Vibhaṅga titles 5, 7, 8.** "5. Lakkhaṇa-", "7. Āvaṭṭa-" and "8. Vibhattihāravibhaṅgavaṇṇanā" are printed as big title lines (`<p rend="nikaya">`), which the converter keeps as text as if they were a volume's reprinted title. They are not reprints: each occurs once, opens its section and has its own "… niṭṭhitā." closing line, like its 13 siblings (`subhead`). They are now headings at their siblings' level.
- **Pairing with the root** works as in book 17. A heading whose name pairs with a root heading takes its ID and level, so the vibhaṅgas are `^19-4-1-0`…`16-0` and the sampātas keep the root's numbers. The commentary heads no Otaraṇa, Sodhana, Parikkhāra or Samāropana sampāta (it goes from 11. Paññatti to 14. Adhiṭṭhāna, then to its own Missaka section, and cites none of ¶74–75 or ¶77–78), so those root IDs (`^19-4-28-0`, `-29-0`, `-31-0`, `-32-0`) stay unused.
- **The commentary's own headings (2)** are numbered after the root's under the same parent (the standing decision):
  - Nayasaṅkhepo `^19-3-3-0`. In the root "Nayasaṅkhepo" is a text line (`^19-1-16`), not a heading. It is printed between Hārasaṅkhepo `^19-3-1-0` and Dvādasapadaṃ `^19-3-2-0`.
  - Missakahārasampātavaṇṇanā `^19-4-33-0`: the commentary's own run of all sixteen hāras over Dhp 2 ("Manopubbaṅgamā … pasannena"), which the root does not have.
- **Nigamanakathā** is `^19-7-0`, after the root's last section (the standing decision).

**The Netti ṭīkās (human decision).** The Nettippakaraṇa-ṭīkā (`s0519t.tik`) is to be built next into a new `pi-khuddakanikaya-tiika.md`. The Nettivibhāvinī (`s0501t.nrf`) is left out.

**Join:** 16,192 links, none broken; 54,183 block IDs, all unique; split proof OK; no bare LFs.

## Book 19 ṭīkā — Nettippakaraṇa-ṭīkā (`s0519t.tik`, 2026-11-24)

The first and only KN ṭīkā. It creates `1-SOURCES/Commentaries/pi-khuddakanikaya-tiika.md` (`kn-tiika`, `commentary:` the KN aṭṭhakathā), as the DN, MN, SN and AN ṭīkās have their own files. The Nettivibhāvinī (`s0501t.nrf`) is left out (human decision).

Run: `kn_comm_book.py 19 s0519t.tik tika-kn-nett kn-nett … --layer=tiika --zones=,1 --shape=0-INBOX/temp/kn-comm/nett_shape.py --fm=Ganthārambhakathāvaṇṇanā --fm=Nidānakathāvaṇṇanā --accept-unresolved=125.`

| Check | Result |
|---|---|
| Segments vs `tika-kn-nett` | 763 = 763 site paragraphs |
| `verify_commentary.py` | PASS: `^19-1`…`^19-717`, 24,149 words = XML, 2,417 bold spans |
| Citations | 130 printed: 129 linked right, 0 wrong, 1 left unlinked and logged ("125.", below) |
| `check_headings.py` | 33 = 33, ALL MATCH |
| Site | PASS: text and tree match |
| Aṭṭhakathā check (new, `tika_probe.py`) | of the site's 129 paranum links, 128 agree and 1 is a range opening on the same block; 0 differ |
| Tree vs root | 28 of 30 headings carry the root's ID and title; every `###` matches. The 2 misses are the commentary's own headings |

**The ṭīkā's citations, checked through the aṭṭhakathā.** tipitaka.app links the ṭīkā's numbered paragraphs to the aṭṭhakathā's paragraphs (`atta-tika`), not to the root. So `compare_site_commentary.py` finds no root links to compare. `tika_probe.py` (now a driver check for any ṭīkā) takes each pair the site gives. The root blocks the ṭīkā paragraph links must be the ones its aṭṭhakathā paragraph links (in the book's aṭṭhakathā draft). One accepted variant: the ṭīkā's "73-4." links `^19-73` and `^19-74`, while its aṭṭhakathā paragraph cites 73 only.

**"125." left unlinked (human decision: a source slip, Rule 2).** The ṭīkā's paragraph "125. Saccekadesato saccasamudāyo … ‘paramatthasaccaṃ vā hotū’ti āha. Caturo padāti …" explains the words of the aṭṭhakathā paragraph printed "170." ("Maggānaṭṭhaṅgiko … paramatthasaccaṃ vā hotu … caturo padā"), which links `^19-170`. The edition's root jumps from 124 to 170, and the ṭīkā keeps counting from 124. The root has no ¶125, so the printed "125." stays as printed, without a link. The site gives this paragraph no link either.

**Human decisions (2026-11-24):**
- **Front matter.** Ganthārambhakathāvaṇṇanā `^19-I-0` (on the aṭṭhakathā's opening verses) and Nidānakathāvaṇṇanā `^19-II-0` (on how the aṭṭhakathā introduces the Netti). Neither cites the root. This follows the AN ṭīkā's two opening sections and the Itivuttaka's `^4-II-0`.
- **Headings** by `nett_shape.py`, as in the aṭṭhakathā:
  - the vibhaṅgas take `^19-4-1-0`…`16-0`;
  - the grouped "4. Padaṭṭhānahārasampātādi-" takes its first section, `^19-4-20-0` (the standing decision); the sampātas after it have no heading here;
  - Nayasaṅkhepa is `^19-3-3-0` and Missaka `^19-4-33-0`, the same IDs as in the aṭṭhakathā.
- **Nigamanakathāvaṇṇanā** is `^19-7-0` (the standing decision; the driver now recognises the "-vaṇṇanā" form).

**Tooling changes:**
- `kn_comm_book.py --layer=tiika` builds a ṭīkā (registered id `kn-<book>-tiika`, `--commentary`) and joins it into `pi-khuddakanikaya-tiika.md`. The first ṭīkā book creates that file.
- `merge_volumes.py` takes one part (a work's first volume on its own), and reads a volume's source URLs when `source:` is a list (a book built from several XML parts).
- **A defect found, now repaired:** the joined KN aṭṭhakathā's `source_volumes` listed 15 URLs and missed the 9 multi-part volumes (`s0508a1/2`, `s0513a1–4`, `s0514a1–3`). Their drafts list them under `source:`, which merge_volumes did not read before this fix. With approval, `fix_source_volumes.py` rebuilt the list from `source_filename` (24 URLs, in source order): 9 lines added, nothing else changed, body byte-identical, CRLF kept. Backup in `0-INBOX/temp/kn-comm/backups/`.
- The new file's frontmatter took `license`, `tag_ids` and `category_id` from the KN aṭṭhakathā (the same values as the AN ṭīkā), and "1 volume file".

**Join (new file):** 130 links, none broken; 753 block IDs, all unique; split proof OK; no bare LFs.
