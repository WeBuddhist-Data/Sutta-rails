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
