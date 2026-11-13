# Dīghanikāya commentaries — structure, content and root alignment

**Date:** 2026-11-13
**Built with:** `4-SYSTEM/Skills/cscd-commentary-intake/`
**Root texts:** `1-SOURCES/Text/pi-dn-1.md`, `pi-dn-2.md`, `pi-dn-3.md` (see `pi-dn-hierarchy-report.md`)
**Checked against:**
- VipassanaTech/tipitaka-xml `romn/`, downloaded 2026-11-13 to `0-INBOX/raw-data/dn/`;
- tipitaka.app `/api/children`, `/api/text` and `/api/links`, fetched 2026-11-13 to `0-INBOX/tipitaka-app/`.

This note is for someone opening the project cold. Pāli only: nothing translated or uploaded. The seven files are in `1-SOURCES/Commentaries/`, moved with approval and checked again there. Their logs of unlinked citations stay in `0-INBOX/temp/dn-comm/*.unresolved.json`.

---

## The seven works

| File | `registered_id` | Work | CSCD source | tipitaka.app | Root |
|---|---|---|---|---|---|
| `pi-dn-1-atthakatha.md` | `dn-1-atthakatha` | Sīlakkhandhavaggaṭṭhakathā | `s0101a.att.xml` | `atta-dn-1` | `pi-dn-1.md` |
| `pi-dn-2-atthakatha.md` | `dn-2-atthakatha` | Mahāvaggaṭṭhakathā | `s0102a.att.xml` | `atta-dn-2` | `pi-dn-2.md` |
| `pi-dn-3-atthakatha.md` | `dn-3-atthakatha` | Pāthikavaggaṭṭhakathā | `s0103a.att.xml` | `atta-dn-3` | `pi-dn-3.md` |
| `pi-dn-1-tiika.md` | `dn-1-tiika` | Sīlakkhandhavaggaṭīkā | `s0101t.tik.xml` | `tika-dn-1` | `pi-dn-1.md` |
| `pi-dn-2-tiika.md` | `dn-2-tiika` | Mahāvaggaṭīkā | `s0102t.tik.xml` | `tika-dn-2` | `pi-dn-2.md` |
| `pi-dn-3-tiika.md` | `dn-3-tiika` | Pāthikavaggaṭīkā | `s0103t.tik.xml` | `tika-dn-3` | `pi-dn-3.md` |
| `pi-dn-1-abhinavatiika.md` | `dn-1-abhinavatiika` | Sīlakkhandhavaggaabhinavaṭīkā | `s0104t.nrf.xml` + `s0105t.nrf.xml` (joined) | `tika2-dn-1` | `pi-dn-1.md` |

The `registered_id`s are registered in annex §3. Each ṭīkā names its aṭṭhakathā in `commentary:`.

---

## How IDs and links work

| Track | Shape | Example | Meaning |
|---|---|---|---|
| Homage | `^T-1` | | before the first heading |
| Collection | `^0` | `# Dīghanikāye (aṭṭhakathā) ^0` | nikāya as printed; the layer label is editorial |
| Work | `^<book>-0` | `## Sīlakkhandhavaggaṭṭhakathā ^1-0` | `<book>` = the root volume's number |
| Front matter | Roman path + `-0` | `### Ganthārambhakathā ^1-I-0` | opening section of the vagga 1 works only |
| Heading | path + `-0` | `### Brahmajālasuttavaṇṇanā ^1-1-0` | sibling position; sutta *k* of the vagga is `^<book>-k-0`, the same as in the root |
| Content | `^<book>-<k>` | `^1-37` | the *k*-th paragraph of **this file**, a running counter |
| Root link | transclusion | `![[1-SOURCES/Text/pi-dn-1.md#^1-149]]` | the root paragraph a printed citation names |

- A paragraph that opens with a printed number or range is preceded by one link per root paragraph it cites, and the number stays in the text.
- The link's scope runs to the next link group or heading.

## Results

| File | Content IDs | Headings | Words (= XML) | Printed citations | Linked right | Unlinked (logged) |
|---|---|---:|---:|---:|---:|---:|
| `pi-dn-1-atthakatha` | `^1-1`…`^1-1231` | 123 | 61,275 | 320 | 319 | 1 |
| `pi-dn-2-atthakatha` | `^2-1`…`^2-1455` | 154 | 74,217 | 345 | 345 | 0 |
| `pi-dn-3-atthakatha` | `^3-1`…`^3-958` | 149 | 44,337 | 293 | 293 | 0 |
| `pi-dn-1-tiika` | `^1-1`…`^1-1162` | 153 | 67,889 | 305 | 305 | 0 |
| `pi-dn-2-tiika` | `^2-1`…`^2-1290` | 169 | 60,193 | 336 | 336 | 0 |
| `pi-dn-3-tiika` | `^3-1`…`^3-962` | 155 | 49,323 | 292 | 292 | 0 |
| `pi-dn-1-abhinavatiika` | `^1-1`…`^1-2405` | 158 | 166,357 | 326 | 325 | 1 |
| **Total** | | | **523,591** | **2,217** | **2,215** | **2** |

**vs XML** (`verify_commentary.py`, all PASS):
- the word stream is identical;
- content IDs are contiguous;
- every printed citation is linked to exactly the root paragraphs it names, ranges included;
- every link resolves to an existing root block.

CSCD's 29 truncated-tail ranges (`65-6.` = 65–66, `354-8.` = 354–358, …) are linked in full and kept as printed.

**vs tipitaka.app** (`compare_site_commentary.py`):

| File | Site paragraphs matched | Contents tree (site / ours) | Site paranum links agreeing |
|---|---:|---|---:|
| `pi-dn-1-atthakatha` | 1,506 / 1,506 | 121 / 121 | 319 / 320 |
| `pi-dn-2-atthakatha` | 1,712 / 1,712 | 152 / 152 | 345 / 345 |
| `pi-dn-3-atthakatha` | 1,131 / 1,131 | 146 / 147 | 293 / 293 |
| `pi-dn-1-tiika` | 1,391 / 1,391 | 152 / 151 | 256 / 276 |
| `pi-dn-2-tiika` | 1,495 / 1,495 | 167 / 167 | 318 / 318 |
| `pi-dn-3-tiika` | 1,132 / 1,132 | 152 / 153 | 285 / 285 |
| `pi-dn-1-abhinavatiika` | 2,940 / 2,940 | 156 / 156 | 275 / 298 |

For the aṭṭhakathā, a site link is aṭṭhakathā paragraph → root paragraph. For the ṭīkās, it pairs a ṭīkā paragraph with an aṭṭhakathā paragraph, and the two must carry the same root links. The site's much larger set of "gloss" links are its own word matches, not printed citations, and were not used. Every difference is explained below.

---

## Unlinked citations — for a reviewer

The text is kept as printed. The paragraph gets no link of its own, so it stays in the scope of the previous link group.

| File | Block | Printed | Root heading | Evidence | Likely reading |
|---|---|---|---|---|---|
| `pi-dn-1-atthakatha` | the paragraph "Rosikaṃ nhāpitaṃ āmantesīti …" | `504-407.` | Lohiccasutta | The ṭīkā and the abhinavaṭīkā print `504.` there and `508.` next. tipitaka.app links this paragraph to root 504. Root 504–507 is the Rosikā the barber episode. | 504–507 |
| `pi-dn-1-abhinavatiika` | the paragraph "Kittako pana soti …" (Pokkharasātibuddhūpasaṅkamanavaṇṇanā) | `292-3-6.` | Ambaṭṭhasutta | The aṭṭhakathā prints `292-296.` there, and the ṭīkā prints `293-6.`. | 292–296 |

The site differences these cause (1 aṭṭhakathā link and 3 ṭīkā pairs) are counted in the table above.

## Explained differences from tipitaka.app

| Item | Files | Why |
|---|---|---|
| Ṭīkā link pairs: 19 (ṭīkā), 21 (abhinavaṭīkā) | `pi-dn-1-tiika`, `pi-dn-1-abhinavatiika` | Same root paragraph, printed as a single number on one side (`45.`) and as a range on the other (`45-46.`). Each file follows its own printed numbers. |
| `Nigamanakathā` / `Nigamanakathāvaṇṇanā` is a `###` here; the site has no contents node | `pi-dn-3-atthakatha`, `pi-dn-3-tiika` | In the XML it follows the work's own closing line, outside the last sutta and outside the book `<div>`. The site keeps it at book level with no node. Here it is its own top-level section (`^3-12-0`) rather than part of the 34th sutta. |
| One site node fewer | `pi-dn-1-tiika` | The site adds a chapter node "Ganthārambhakathāvaṇṇanā" for the XML's first `<div>`, which has no heading, above the printed heading of the same name. Here there is only the printed heading. |
| Opening headings nested | `pi-dn-1-abhinavatiika` | The XML of this work has no `<div>`s, so the site shows its four opening headings at one level. Here Ganthārambhakathāvaṇṇanā, Nidānakathāvaṇṇanā and Paṭhamamahāsaṅgītikathāvaṇṇanā sit under Ganthārambhakathā. That is how the site itself nests the same sections in the aṭṭhakathā and ṭīkā. |
| Site depth = our level + 1 | all | The site counts the piṭaka as a level the source does not print (as for the root). |
| Printed numbers, notes, quotes, page markers | all | As in the root texts: the number is kept here, the site keeps it in a separate field; `[…]` here, `{…}` on the site; `"` here, `‘‘ ’’` on the site; no page markers here. |

## Judgment calls

| Decision | Where | Why |
|---|---|---|
| Front matter in Roman (`--frontmatter`) | `Ganthārambhakathā` (aṭṭhakathā, abhinavaṭīkā) and `Ganthārambhakathāvaṇṇanā` (ṭīkā) in the three vagga 1 works | The opening account (Ganthārambha, Nidāna, First Council) precedes the commentary on the first sutta. Marking it keeps sutta *k* at `^1-k-0` in every DN file. The vagga 2 and 3 works open directly with sutta 1 and have no front matter. |
| Abhinavaṭīkā joined into one file | `s0104t` (root paragraphs 1–149) + `s0105t` (150–559) | One work over two CSCD volumes. tipitaka.app shows one book of 2,940 paragraphs, the exact sum. Volume 2's opening lines (homage, *Dīghanikāye*, *Sīlakkhandhavaggaabhinavaṭīkā*, *(Dutiyo bhāgo)*) are kept as plain text blocks, as on the site. Nothing is dropped. |

## Not done

- No lint, parse or upload.

## Related

- Skill: `4-SYSTEM/Skills/cscd-commentary-intake/SKILL.md`
- Root texts: `0-INBOX/pi-dn-hierarchy-report.md`
- ID scheme: `4-SYSTEM/Guidelines/vault-annex.md` §2

---

## Update 2026-11-13 — bold kept

The XML's `<hi rend="bold">` (the word being explained) was being dropped. It is now kept as `**…**`, copied tag for tag from the XML, which is the data tipitaka.app displays.

| File | Bold spans (= XML) |
|---|---:|
| `pi-dn-1-atthakatha` | 2,519 |
| `pi-dn-2-atthakatha` | 2,852 |
| `pi-dn-3-atthakatha` | 2,892 |
| `pi-dn-1-tiika` | 5,614 |
| `pi-dn-2-tiika` | 6,845 |
| `pi-dn-3-tiika` | 5,783 |
| `pi-dn-1-abhinavatiika` | 13,418 |

- **Exact copy.** Each `**` sits where the XML has a bold tag; spaces and punctuation inside a tag stay inside (`**‘jātaka’**nti`, `**passatā. ** Sabba`). Nothing is moved, merged or dropped, so a few thousand spans that start or end with punctuation or a space will not render as bold in Obsidian. `verify_commentary.py` compares every span's exact text with the XML: PASS for all seven.
- **Text unchanged.** IDs, headings, links and line count are as before. With `**` removed, the only difference from the earlier build is spacing at the 283 tags that hold a space at their edge.
- **vs tipitaka.app.** About 95% of the lines with bold are character-for-character identical to the site (after its own display forms: page markers, `{ }`, `‘‘ ’’`, numbers). The rest differ only where the site departs from the XML: it drops a space next to a bold marker, joins two spans the XML keeps apart (144 cases, e.g. XML `<hi>Āyasmato</hi> <hi>mahākassapassa</hi>` → site `**Āyasmatomahākassapassa**`), or drops a bold tag that holds only a space (2 cases) together with the space. Here the XML is followed.
- The unresolved-citation logs in `0-INBOX/temp/dn-comm/` were refreshed (their text excerpts now show bold).
