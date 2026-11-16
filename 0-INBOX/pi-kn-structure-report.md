# Khuddakanikāya — structure, hierarchy and alignment

**Checked:** 2026-11-16.

**Sources:**
- VipassanaTech/tipitaka-xml `romn/`: all 47 KN files in `0-INBOX/raw-data/kn/`, byte-identical to the repo (git blob SHA).
- tipitaka.app: `kn-khp`, `atta-kn-khp`, `kn-dhp`, `atta-kn-dhp` (text, contents tree, links), in `0-INBOX/tipitaka-app/`.

**Status:** books 1–2 (Khuddakapāṭha, Dhammapada) are **ingested** into `1-SOURCES/` and registered in the annex (§7). Nothing is committed, pushed or uploaded yet. The other 18 books follow one by one.

---

## 1. The Khuddakanikāya at a glance

- **Books:** 20 on tipitaka.app, in this order: Khuddakapāṭha, Dhammapada, Udāna, Itivuttaka, Suttanipāta, Vimānavatthu, Petavatthu, Theragāthā, Therīgāthā, Therāpadāna, Therīapadāna, Buddhavaṃsa, Cariyāpiṭaka, Jātaka, Mahāniddesa, Cūḷaniddesa, Paṭisambhidāmagga, Milindapañha, Nettippakaraṇa, Peṭakopadesa.
- **Repo files:** 47 (19 root, 24 aṭṭhakathā, 1 ṭīkā, 3 other).
- **Proposed naming:** `pi-kn-<book>`, where `book` is the book's position in that list, as the ID prefix. So the Khuddakapāṭha is `pi-kn-1` and the Dhammapada `pi-kn-2`. Their CSCD files are `s0501`, `s0502`.
- **`s0501t.nrf.xml`** is the **Nettivibhāvinī**, a ṭīkā on the Nettippakaraṇa (book 19). It is not a Khuddakapāṭha commentary; tipitaka.app shows it as `tika2-kn-nett`.
- **Ṭīkās:** the Khuddakapāṭha and Dhammapada have only an aṭṭhakathā.

## 2. Khuddakapāṭha (`pi-kn-1`)

- **Structure:** the book holds 9 sections (`<div type="chapter">`): Saraṇattaya, Dasasikkhāpada, Dvattiṃsākāra, Kumārapañha, Maṅgala-, Ratana-, Tirokuṭṭa-, Nidhikaṇḍa- and Mettasutta.
- **Numbering:** each section numbers its verses from 1, and Saraṇattaya and Dvattiṃsākāra print no numbers.
- **IDs (your decision, 2026-11-16):** section + verse, `^1-<section>-<N>`. For example, Ratanasutta v. 3 = `^1-6-3`. All 89 printed numbers are kept; the two unnumbered sections are `^1-U1`, `^1-U2`.
- **Aṭṭhakathā:**
  - It numbers its sections the same way (`6. Ratanasuttavaṇṇanā`), so a citation links within its own section.
  - Its front matter is `Ganthārambhakathā` (→ `^1-I-0`); the sections 1–9 then get the root's IDs.

## 3. Dhammapada (`pi-kn-2`)

- **Structure:** 26 vaggas (`<div type="vagga">`). The 423 verses are numbered straight through, so the standard verse numbering applies: Dhp 1 = `^2-1` … Dhp 423 = `^2-423`.
- **Number lines:** each verse number is a line of its own before its gāthā (`hangnum`). The 423 are joined to their gāthās, as tipitaka.app shows them: 971 paragraphs on both sides.
- **Aṭṭhakathā:**
  - It is printed in two parts in one file. `(Paṭhamo bhāgo)`, `(Dutiyo bhāgo)` and the reprinted title lines are kept as text.
  - It quotes every verse with its number. Those 436 citations each link to the root verse.

## 4. Results

| | XML: words, IDs, bold | Every heading | Citations | tipitaka.app |
|---|---|---|---|---|
| pi-kn-1 Khuddakapāṭha | PASS (89 IDs + 2 U) | 9 / 9 | — | PASS (89 / 89 numbers in their block) |
| pi-kn-1-atthakatha | PASS | 110 / 110 | 67 linked, 0 wrong, 1 logged | 1 explained (a) |
| pi-kn-2 Dhammapada | PASS (423 IDs) | 26 / 26 | — | PASS |
| pi-kn-2-atthakatha | PASS | 333 / 333 | 436 linked, 0 wrong | 1 explained (b) |

- **(a)** The aṭṭhakathā's `13.` comments on a 13th verse of the Tirokuṭṭasutta, whose root prints only verses 1–12. It is unresolved and logged for a reviewer. tipitaka.app links it to Maṅgalasutta v. 13, in another section, by number alone.
- **(b)** The site adds a contents node for the book title reprinted at the start of part 2; the file keeps that line as text.

## 5. Skill changes made (vault copies)

- **Per-section numbering:**
  - `apply.py --zone-per-section`;
  - `verify.py` / `compare_site.py --per-section`;
  - `--per-section` in `build_commentary.py`, `verify_commentary.py` and `compare_site_commentary.py`.
- **Div-less files in tree mode:** the body is the book.
- **Unnumbered sections:** text after a heading in a section that prints no numbers is a `U` block.
- **Cited gāthās:** in tree mode, a gāthā opening with a real citation links to the root.
- **Number tags:** `8 .` (the number and dot as two tags) is rendered `8.`.
- **Site check:** `compare_site_commentary.py` takes the book number from `root_text`.

**Regression:** the DN, MN, SN and AN files (67) regenerate byte-identical. The one exception is `pi-sn-5-tiika`'s hand-made `[Ed:]` note.

## 6. For the annex (done, see §7)

- **KN book numbers:** by tipitaka.app's order (above).
- **Khuddakapāṭha:** registered as a deviation, section + verse IDs `^1-<section>-<N>`.
- **Commentary IDs:** `kn-1-atthakatha`, `kn-2-atthakatha`.
- **Library fields:** `category_id` **Discourses** (`XfCwZpoJMtfO7s0laQkdK`) and tag Theravāda, as corrected for the Sutta texts.

## 7. Ingested (2026-11-16)

| File | Built with | Checks in place |
|---|---|---|
| `1-SOURCES/Text/pi-kn-1.md` | tree mode, `apply.py --zone-per-section` | XML PASS (`--per-section`), headings 9 / 9, tipitaka.app PASS |
| `1-SOURCES/Text/pi-kn-2.md` | tree mode | XML PASS, headings 26 / 26, tipitaka.app PASS |
| `1-SOURCES/Commentaries/pi-kn-1-atthakatha.md` | `--per-section --frontmatter "Ganthārambhakathā"` | XML PASS: 67 linked, 0 wrong, 1 logged; site: only (a) |
| `1-SOURCES/Commentaries/pi-kn-2-atthakatha.md` | tree mode | XML PASS: 436 linked, 0 wrong; site: only (b) |

- **The builds match the dry run.** The only change is `verse_id_format: book-chapter-verse` on the Khuddakapāṭha and its aṭṭhakathā. Their IDs have three parts, so `book-verse` would be wrong.
- **Annex:**
  - §1: both books are listed, with the KN book order, the `kn` collection and the tree-mode note.
  - §2: the Dhammapada numbering, plus the deviation "Section + verse `^<book>-<section>-<N>`" for the Khuddakapāṭha.
  - §3: `kn-1-atthakatha` and `kn-2-atthakatha`, with a sources paragraph.
- **Library fields:** `license: cc0`, tag Theravāda, `category_id` Discourses (`XfCwZpoJMtfO7s0laQkdK`). The text, edition and TOC IDs are added at upload.
- **Unresolved log:** `0-INBOX/temp/kn-comm/pi-kn-1-atthakatha.unresolved.json` holds one entry: Tirokuṭṭa `13.`, looked for at `^1-7-13`, which the root does not have.
- **Re-runnable:**
  - `bash 0-INBOX/temp/build_kn_roots.sh <dir>`;
  - `bash 0-INBOX/temp/build_kn_comm.sh <dir>`, built against the `1-SOURCES` roots.
