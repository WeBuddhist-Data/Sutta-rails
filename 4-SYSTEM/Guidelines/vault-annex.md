# Vault Annex — sutta-rails conventions

The methodology guidelines (`0-VAULT-Structure.md`, `../../1-SOURCES/About Sources.md`, `../../2-RAILS/About Rails.md`, `../../3-TRANSFORMATIONS/About Transformations.md`) are **text-agnostic**: they apply to any Railroads vault built on any classical text. This annex records the conventions specific to *this* vault, the **Pāli Sutta Piṭaka**.

When the Guidelines and this annex disagree on a vault-specific detail, this annex wins, **for the points it actually states**. Everything it does not state follows the defaults unchanged.

---

## 1. The text

This vault serves the **Pāli Sutta Piṭaka**, the second basket of the Pāli Canon, in the Chaṭṭha Saṅgāyana (CSCD) edition published by the Vipassana Research Institute.

Source-text files in `1-SOURCES/Text/` are **one file per work**, as in the Vinaya and Abhidhamma vaults: a work CSCD prints in several volumes is one file, and each volume is a `##` chapter in it. The Dīgha-, Majjhima-, Saṃyutta- and Aṅguttaranikāya are each one work (`pi-dn.md`, `pi-mn.md`, `pi-sn.md`, `pi-an.md`). Each Khuddakanikāya book is a work of its own (`pi-kn-<book>.md`). Each volume is still built and verified on its own (`cscd-root-text-intake`), then the volumes are joined with `merge_volumes.py` (merged 2026-11-20). Ingested so far:

| Nikāya | Volume = chapter | `book` | CSCD source | tipitaka.app key | Filename |
| ------ | ---------------- | ------ | ----------- | ---------------- | -------- |
| Dīghanikāya | Sīlakkhandhavaggapāḷi | 1 | `s0101m.mul.xml` | `dn-1` | `pi-dn.md` |
| Dīghanikāya | Mahāvaggapāḷi | 2 | `s0102m.mul.xml` | `dn-2` | `pi-dn.md` |
| Dīghanikāya | Pāthikavaggapāḷi | 3 | `s0103m.mul.xml` | `dn-3` | `pi-dn.md` |
| Majjhimanikāya | Mūlapaṇṇāsapāḷi | 1 | `s0201m.mul.xml` | `mn-1` | `pi-mn.md` |
| Majjhimanikāya | Majjhimapaṇṇāsapāḷi | 2 | `s0202m.mul.xml` | `mn-2` | `pi-mn.md` |
| Majjhimanikāya | Uparipaṇṇāsapāḷi | 3 | `s0203m.mul.xml` | `mn-3` | `pi-mn.md` |
| Saṃyuttanikāya | Sagāthāvaggo | 1 | `s0301m.mul.xml` | `sn-1` | `pi-sn.md` |
| Saṃyuttanikāya | Nidānavaggo | 2 | `s0302m.mul.xml` | `sn-2` | `pi-sn.md` |
| Saṃyuttanikāya | Khandhavaggo | 3 | `s0303m.mul.xml` | `sn-3` | `pi-sn.md` |
| Saṃyuttanikāya | Saḷāyatanavaggo | 4 | `s0304m.mul.xml` | `sn-4` | `pi-sn.md` |
| Saṃyuttanikāya | Mahāvaggo | 5 | `s0305m.mul.xml` | `sn-5` | `pi-sn.md` |
| Aṅguttaranikāya | Ekakanipātapāḷi | 1 | `s0401m.mul.xml` | `an-1` | `pi-an.md` |
| Aṅguttaranikāya | Dukanipātapāḷi | 2 | `s0402m1.mul.xml` | `an-2` | `pi-an.md` |
| Aṅguttaranikāya | Tikanipātapāḷi | 3 | `s0402m2.mul.xml` | `an-3` | `pi-an.md` |
| Aṅguttaranikāya | Catukkanipātapāḷi | 4 | `s0402m3.mul.xml` | `an-4` | `pi-an.md` |
| Aṅguttaranikāya | Pañcakanipātapāḷi | 5 | `s0403m1.mul.xml` | `an-5` | `pi-an.md` |
| Aṅguttaranikāya | Chakkanipātapāḷi | 6 | `s0403m2.mul.xml` | `an-6` | `pi-an.md` |
| Aṅguttaranikāya | Sattakanipātapāḷi | 7 | `s0403m3.mul.xml` | `an-7` | `pi-an.md` |
| Aṅguttaranikāya | Aṭṭhakanipātapāḷi | 8 | `s0404m1.mul.xml` | `an-8` | `pi-an.md` |
| Aṅguttaranikāya | Navakanipātapāḷi | 9 | `s0404m2.mul.xml` | `an-9` | `pi-an.md` |
| Aṅguttaranikāya | Dasakanipātapāḷi | 10 | `s0404m3.mul.xml` | `an-10` | `pi-an.md` |
| Aṅguttaranikāya | Ekādasakanipātapāḷi | 11 | `s0404m4.mul.xml` | `an-11` | `pi-an.md` |
| Khuddakanikāya | Khuddakapāṭhapāḷi | 1 | `s0501m.mul.xml` | `kn-khp` | `pi-kn-1.md` |
| Khuddakanikāya | Dhammapadapāḷi | 2 | `s0502m.mul.xml` | `kn-dhp` | `pi-kn-2.md` |

**Before 2026-11-20** each volume was its own file (`pi-dn-1.md` … `pi-an-11.md`) and its own library text. Those files are in git history; the verification reports in `0-INBOX/` dated before the merge refer to them.

Only volumes that have been ingested are present in the folder. The Dīgha-, Majjhima-, Saṃyutta- and Aṅguttaranikāya are in, in Pāli: root text and commentaries (§3), no translations yet. The Khuddakanikāya is being added book by book. MN registered 2026-11-13, SN 2026-11-14, AN 2026-11-16, KN books 1–2 2026-11-16.

**Khuddakanikāya:** one file per book, `pi-kn-<book>`. `book` is the book's position in tipitaka.app's list of the 20 books: 1 Khuddakapāṭha, 2 Dhammapada, 3 Udāna, 4 Itivuttaka, 5 Suttanipāta, 6 Vimānavatthu, 7 Petavatthu, 8 Theragāthā, 9 Therīgāthā, 10 Therāpadāna, 11 Therīapadāna, 12 Buddhavaṃsa, 13 Cariyāpiṭaka, 14 Jātaka, 15 Mahāniddesa, 16 Cūḷaniddesa, 17 Paṭisambhidāmagga, 18 Milindapañha, 19 Nettippakaraṇa, 20 Peṭakopadesa. Each book is registered in this table **before** it is ingested. Converted in tree mode.

`cscd-root-text-intake` supports four shapes:
- book → sutta `<div>`s (Dīgha);
- book → vagga `<div>`s whose suttas are numbered sub-headings (Majjhima);
- book → saṃyutta `<div>`s, with vaggas as `title` and suttas as `subhead` paragraphs (Saṃyutta);
- **tree mode** (Aṅguttara), where divisions nest in more than one way. Each heading's level is read from the XML's own nesting.

**Aṅguttaranikāya:** each nipāta is built as its own volume file, as CSCD prints the root and tipitaka.app shows all three layers, then the eleven are joined into `pi-an.md`. `book` is the nipāta number. A CSCD commentary volume holds several nipātas as separate books (`s0402a` = Duka-, Tika-, Catukkanipāta); each is built on its own (tree mode, `--book K`) and the eleven are joined into `pi-an-atthakatha.md` / `pi-an-tiika.md`.

**Joining volumes (`merge_volumes.py`, in `cscd-root-text-intake/scripts/`):** every block of every volume is kept in order with its ID. The first volume's homage `^T-1` and `# <nikāya> ^0` open the file. A later volume's own opening lines are printed text, so they stay where printed, as plain blocks: its homage becomes `^<book>-T1` and its printed nikāya line `^<book>-T2` (see the deviation in §2). Transclusions are pointed at the joined root. The join is checked word for word against the XML volumes in order.

---

## 2. Addressing scheme

**`verse_id_format`:** `book-verse`

**Format example:** `^1-149` (Sīlakkhandhavagga, printed paragraph 149)

- **Nikāya collection:** the abbreviation in the file name: `dn` for Dīghanikāya, `mn` for Majjhimanikāya, `sn` for Saṃyuttanikāya, `an` for Aṅguttaranikāya, `kn` for Khuddakanikāya. The collection is given by the file, not by the ID.
- **`book`:** the position of the CSCD volume within its nikāya (`1`–`3` for the Dīghanikāya's three vaggas, `1`–`3` for the Majjhimanikāya's three paṇṇāsas, `1`–`5` for the Saṃyuttanikāya's five vaggas, `1`–`11` for the Aṅguttaranikāya's eleven nipātas, `1`–`20` for the Khuddakanikāya's books).

Block IDs always resolve as `file#^id`, so the same `^1-149` in two different files names two different blocks.

### Heading hierarchy

| Markdown | Role | Anchor | Example |
| -------- | ---- | ------ | ------- |
| (plain, before the first heading) | Homage (`Namo tassa…`) | `^T-1` | `Namo tassa bhagavato arahato sammāsambuddhassa ^T-1` |
| `#` | Nikāya, as printed | `^0` | `# Dīghanikāyo ^0` |
| `##` | Volume (vagga) | `^<book>-0` | `## Sīlakkhandhavaggapāḷi ^1-0` |
| `###` | Sutta | `^<book>-<n>-0` | `### Brahmajālasuttaṃ ^1-1-0` |
| `####` | Sub-heading within the sutta | `^<book>-<n>-<m>-0` | `#### Paribbājakakathā ^1-1-1-0` |

**Majjhimanikāya:** each paṇṇāsa holds vaggas, and the sutta is one level deeper:

| Markdown | Role | Anchor | Example |
| -------- | ---- | ------ | ------- |
| `##` | Volume (paṇṇāsa) | `^<book>-0` | `## Mūlapaṇṇāsapāḷi ^1-0` |
| `###` | Vagga | `^<book>-<v>-0` | `### Mūlapariyāyavaggo ^1-1-0` |
| `####` | Sutta | `^<book>-<v>-<n>-0` | `#### Sabbāsavasuttaṃ ^1-1-2-0` |
| `#####` | Sub-heading within the sutta | `^<book>-<v>-<n>-<m>-0` | `##### Dassanā pahātabbāsavā ^1-1-2-1-0` |

A commentary's vagga and sutta headings carry the same IDs as the root's (`#### Sabbāsavasuttavaṇṇanā ^1-1-2-0`). A ṭīkā's own numbered list under a `title` heading is one level deeper again (`###### Desanāhāravaṇṇanā`, the 16 hāras of the Mūlapaṇṇāsa-ṭīkā).

**Saṃyuttanikāya:** each volume holds saṃyuttas. A saṃyutta with vaggas nests the sutta under its vagga; a saṃyutta without vaggas (about half) holds its suttas directly:

| Markdown | Role | Anchor | Example |
| -------- | ---- | ------ | ------- |
| `##` | Volume (vagga) | `^<book>-0` | `## Sagāthāvaggo ^1-0` |
| `###` | Saṃyutta | `^<book>-<s>-0` | `### Devatāsaṃyuttaṃ ^1-1-0` |
| `####` | Vagga (`title`) | `^<book>-<s>-<v>-0` | `#### Naḷavaggo ^1-1-1-0` |
| `#####` | Sutta (`subhead`) | `^<book>-<s>-<v>-<n>-0` | `##### Oghataraṇasuttaṃ ^1-1-1-1-0` |
| `####` | Sutta, in a saṃyutta without vaggas | `^<book>-<s>-<n>-0` | `#### Āḷavikāsuttaṃ ^1-5-1-0` |

A section after the last saṃyutta (`Sagāthāvaggo paṭhamo.` with its uddāna) is a `###` of its own. In the commentaries, saṃyutta IDs equal the root's. Vagga and sutta IDs often do not, because a commentary leaves out the vaggas and suttas it does not comment on and heading IDs are sibling positions. The transclusions carry the alignment.

**Aṅguttaranikāya (tree mode):** a `<div>`'s head is one level under its parent's. A heading paragraph, or a further `<head>` in the same container, sits under the innermost open heading of a higher rank (title > chapter > subhead > subsubhead):

| Markdown | Role | Anchor | Example |
| -------- | ---- | ------ | ------- |
| `##` | Nipāta | `^<book>-0` | `## Dukanipātapāḷi ^2-0` |
| `###` | Paṇṇāsaka | `^<book>-<p>-0` | `### Paṭhamapaṇṇāsakaṃ ^2-1-0` |
| `####` | Vagga in a paṇṇāsaka | `^<book>-<p>-<v>-0` | `#### Kammakaraṇavaggo ^2-1-1-0` |
| `#####` | Sutta | `^<book>-<p>-<v>-<n>-0` | `##### Vajjasuttaṃ ^2-1-1-1-0` |
| `###` | Vagga outside the paṇṇāsakas, or in a nipāta without them (Ekaka, Ekādasaka) | `^<book>-<v>-0` | `### Acelakavaggo ^3-4-0` |

The ṭīkās have no divisions inside a book, so nothing marks where a paṇṇāsaka ends. A ṭīkā vagga printed after the last paṇṇāsaka therefore nests under it (`#### Acelakavaggavaṇṇanā ^3-3-5-0`), as the XML gives it. The transclusions carry the alignment.

**Khuddakanikāya (tree mode):** the levels come from each book's own XML. Dhammapada: `## Dhammapadapāḷi ^2-0` → `### Yamakavaggo ^2-1-0`, with the verses under the vagga. Khuddakapāṭha: `## Khuddakapāṭhapāḷi ^1-0` → `### Ratanasuttaṃ ^1-6-0`, the nine sections.

Each heading segment is the heading's **sibling position** under its parent. It is not the number printed in the source. Printed sutta and vagga numbers, and printed ranges, are stripped from the heading text (`1. Brahmajālasuttaṃ` → `Brahmajālasuttaṃ`, `1-10. Tathāgatādisuttaṃ` → `Tathāgatādisuttaṃ`, `(6) 1. Puggalavaggo` → `Puggalavaggo`).

### Verse numbering rule

- The content ID is the **paragraph number printed in CSCD**, copied verbatim: never renumbered, padded or invented.
- CSCD restarts paragraph numbers at 1 in **each volume**: Sīlakkhandhavagga 1–559, Mahāvagga 1–441, Pāthikavagga 1–360; Mūlapaṇṇāsa 1–513, Majjhimapaṇṇāsa 1–486, Uparipaṇṇāsa 1–463; Sagāthāvagga 1–271, Nidānavagga 1–246, Khandhavagga 1–716, Saḷāyatanavagga 1–420, Mahāvagga 1–1201; the eleven nipātas 1–611, 1–246, 1–184, 1–783, 1–1151, 1–649, 1–1132, 1–626, 1–432, 1–746 and 1–671. The `book` segment keeps the runs apart, so a joined nikāya file holds one unbroken run per chapter (`^1-…`, `^2-…`, …) and content IDs need no zone segment.
- The number does **not** restart at sutta or sub-heading boundaries.
- A paragraph's unnumbered continuation lines, gāthā lines and closing lines (`… niṭṭhitaṃ`) stay in its block. The ID goes on the block's last line.
- CSCD sometimes prints a paragraph number on a line of its own (`<p rend="hangnum">`), with the paragraph's gāthā on the next line. The number is joined to that gāthā line, as tipitaka.app shows it. This happens in 10 MN paragraphs (MN 1 ¶513; MN 2 ¶76, 456–460; MN 3 ¶135, 237, 382) and 48 in SN 1, and in AN 8 ¶32.
- **Printed ranges** (Saṃyuttanikāya): a paragraph printed as `225-240.` is one block, and its ID is the range as printed, `^3-225-240`. There are 27 in SN 3, 16 in SN 4 and 50 in SN 5, and 90 across the AN (long peyyāla ranges such as `^4-304-783`). A commentary citation of any number in the range links to that block.
- **Gaps as printed** (SN Mahāvagga): one paragraph number can cover a run of abbreviated suttas, so the next printed number jumps (`270.` → `280.`). The IDs keep the gap. The 11 gaps are 270→280, 280→292, 292→302, 302→311, 552→587-596, 608→641-650, 662→673-684, 716→749-758, 770→792-802, 856→889-898 and 934→967-976.
- **KN Dhammapada:** verses 1–423 as printed, `^2-1` … `^2-423`. Each verse number is a line of its own (`hangnum`), joined to its gāthā (423).
- **KN Khuddakapāṭha: section + verse.** See the deviation below.
- **AN gap:** Catukkanipāta 105 → 107. Sutta 6 of the Ambavagga (Dutiyaambasutta) prints no text, only an editorial note (`^4-U1`).
- **Homage with `n="0"`** (four AN files): an attribute only, with no printed number. The homage stays the pre-title `^T-1`, with its text as printed (`. Namo tassa…`).
- **Number-only paragraphs before a heading** (SN Mahāvagga `312-323`, `324-333`, `334-345`, `346-356`, `357-366`): a vagga of fully abbreviated suttas prints only the number and a heading. The number stays where it is printed, as a block holding just the number (`312-323 ^5-312-323`).

### Text form

These are mechanical changes only; no wording changes. `verify.py` and `compare_site.py` in `cscd-root-text-intake` check the result against the XML and tipitaka.app.

- The printed `N.` prefix is stripped from the paragraph (it lives in the block ID).
- Variant readings (`<note>`) are inline as `[…]`.
- CSCD's doubled quotes `‘‘ ’’` are written `"`; single `‘ ’` are kept.
- Page markers are dropped, with no space left in their place.

### ⚑ Registered deviations — overrides of the default conventions

#### ⚑ Bible-style `book-verse` — overrides `annotation-conventions.md` §1a (registered 2026-11-13)

**Default:** `^chapter-verse`, numbers restarting in each chapter.

**This vault:** `^<book>-<N>`, with `N` the source's printed paragraph number and one run per volume. It applies to every file in `1-SOURCES/Text/`.

**Why:** the canon is cited by its printed paragraph numbers, and CSCD numbers paragraphs per volume, not per sutta. This is the recognised `book-verse` deviation (`annotation-conventions.md` §7).

#### ⚑ Section + verse `^<book>-<section>-<N>` for the Khuddakapāṭha — overrides the one-run-per-volume rule above (registered 2026-11-16)

**Default here:** `^<book>-<N>`, one run of printed numbers per file.

**Khuddakapāṭha (`pi-kn-1`):** the book numbers each of its 9 sections from 1, so `N` alone would repeat. Its IDs are `^1-<section>-<N>`, where `section` is the section's position (1–9) and `N` the printed verse number (Ratanasutta v. 3 = `^1-6-3`). All 89 printed numbers are kept. Saraṇattaya and Dvattiṃsākāra print no numbers and are `^1-U1`, `^1-U2`. The aṭṭhakathā's citations link within their own section (`6. Ratanasuttavaṇṇanā` → `^1-6-…`).

**Why:** the printed numbers stay the IDs, as everywhere else, and every ID is unique in the file. Built with `apply.py --zone-per-section`; checked with `--per-section`.

#### ⚑ Pre-title `^T-N` and collection heading `^0` — overrides `annotation-conventions.md` §2 (registered 2026-11-13)

**Default:** the `#` title takes no ID, and pre-chapter material goes under `## 0. Introduction ^0-0` as `^0-N`.

**This vault:** the homage before the first heading is `^T-1` (then `^T-2`, …), and the `#` nikāya heading is `^0`. There is no chapter 0.

**Why:** the homage is part of the printed text but precedes all structure. A synthetic "Introduction" heading would add editorial structure the source does not have.

**In a joined file** (registered 2026-11-20), only the first volume's opening lines are `^T-1` and `^0`. Each later volume's homage and printed nikāya line stay where printed, just before its `##` chapter heading, as plain text blocks `^<book>-T1` and `^<book>-T2` (e.g. `Dīghanikāyo ^2-T2` before `## Mahāvaggapāḷi ^2-0`). The vault's `(aṭṭhakathā)` / `(ṭīkā)` label is not printed, so it is not in these lines.

#### ⚑ Unnumbered blocks `^<book>-U<k>` and duplicates `^<book>-<N>x<k>` (registered 2026-11-13)

A paragraph that the source sets apart without a printed number (e.g. directly after a sub-heading) is its own block `^<book>-U<k>`, with `k` in document order within the file. A printed number repeated within one run takes `x1`, `x2`, … on its later copies.

Currently used:
- `^2-U1`: Mahāsudassanasutta.
- `^3-U1`: Pāsādikasutta, before paragraph 165.
- Saṃyuttanikāya: `^1-U1` (Sagāthāvagga closing line); `^2-U1`, `^2-U2` (Nidānasaṃyutta peyyāla and closing); `^5-U1`…`^5-U12` (Mahāvagga, unnumbered abbreviated suttas and closing lines).

- Aṅguttaranikāya: `^4-U1` (Catukkanipāta, the editorial note in place of the Dutiyaambasutta).

No duplicates occur in the Dīgha-, Majjhima-, Saṃyutta- or Aṅguttaranikāya, and the Majjhimanikāya has no `U` blocks.

**Why:** this keeps the invariant that every `^<book>-<N>` is a real printed number.

---

## 3. Registered commentary IDs

No `registered_id` may be used in any rail until it is added to this roster.

| `registered_id` | Title | Tier | Language | Root text | File |
| --------------- | ----- | ---- | -------- | --------- | ---- |
| `dn-atthakatha` | Dīghanikāya-aṭṭhakathā | commentary | Pāli | `pi-dn.md` | `1-SOURCES/Commentaries/pi-dn-atthakatha.md` |
| `dn-tiika` | Dīghanikāya-ṭīkā | sub-commentary | Pāli | `pi-dn.md` | `1-SOURCES/Commentaries/pi-dn-tiika.md` |
| `dn-1-abhinavatiika` | Sīlakkhandhavaggaabhinavaṭīkā | sub-commentary (second) | Pāli | `pi-dn.md` | `1-SOURCES/Commentaries/pi-dn-1-abhinavatiika.md` |
| `mn-atthakatha` | Majjhimanikāya-aṭṭhakathā | commentary | Pāli | `pi-mn.md` | `1-SOURCES/Commentaries/pi-mn-atthakatha.md` |
| `mn-tiika` | Majjhimanikāya-ṭīkā | sub-commentary | Pāli | `pi-mn.md` | `1-SOURCES/Commentaries/pi-mn-tiika.md` |
| `sn-atthakatha` | Saṃyuttanikāya-aṭṭhakathā | commentary | Pāli | `pi-sn.md` | `1-SOURCES/Commentaries/pi-sn-atthakatha.md` |
| `sn-tiika` | Saṃyuttanikāya-ṭīkā | sub-commentary | Pāli | `pi-sn.md` | `1-SOURCES/Commentaries/pi-sn-tiika.md` |
| `an-atthakatha` | Aṅguttaranikāya-aṭṭhakathā | commentary | Pāli | `pi-an.md` | `1-SOURCES/Commentaries/pi-an-atthakatha.md` |
| `an-tiika` | Aṅguttaranikāya-ṭīkā | sub-commentary | Pāli | `pi-an.md` | `1-SOURCES/Commentaries/pi-an-tiika.md` |
| `kn-1-atthakatha` | Khuddakapāṭha-aṭṭhakathā | commentary | Pāli | `pi-kn-1.md` | `1-SOURCES/Commentaries/pi-kn-1-atthakatha.md` |
| `kn-2-atthakatha` | Dhammapada-aṭṭhakathā | commentary | Pāli | `pi-kn-2.md` | `1-SOURCES/Commentaries/pi-kn-2-atthakatha.md` |

**Retired 2026-11-20** (per-volume IDs, never reused). Each volume's commentary was its own file until the volumes were joined per nikāya. Each ID below is now a `##` chapter of the joined file:

| Retired `registered_id` | Title (now a chapter) | Joined into |
| --- | --- | --- |
| `dn-1-atthakatha` | Sīlakkhandhavaggaṭṭhakathā | `dn-atthakatha` |
| `dn-2-atthakatha` | Mahāvaggaṭṭhakathā | `dn-atthakatha` |
| `dn-3-atthakatha` | Pāthikavaggaṭṭhakathā | `dn-atthakatha` |
| `dn-1-tiika` | Sīlakkhandhavaggaṭīkā | `dn-tiika` |
| `dn-2-tiika` | Mahāvaggaṭīkā | `dn-tiika` |
| `dn-3-tiika` | Pāthikavaggaṭīkā | `dn-tiika` |
| `mn-1-atthakatha` | Mūlapaṇṇāsa-aṭṭhakathā | `mn-atthakatha` |
| `mn-2-atthakatha` | Majjhimapaṇṇāsa-aṭṭhakathā | `mn-atthakatha` |
| `mn-3-atthakatha` | Uparipaṇṇāsa-aṭṭhakathā | `mn-atthakatha` |
| `mn-1-tiika` | Mūlapaṇṇāsa-ṭīkā | `mn-tiika` |
| `mn-2-tiika` | Majjhimapaṇṇāsaṭīkā | `mn-tiika` |
| `mn-3-tiika` | Uparipaṇṇāsa-ṭīkā | `mn-tiika` |
| `sn-1-atthakatha` | Sagāthāvagga-aṭṭhakathā | `sn-atthakatha` |
| `sn-2-atthakatha` | Nidānavagga-aṭṭhakathā | `sn-atthakatha` |
| `sn-3-atthakatha` | Khandhavagga-aṭṭhakathā | `sn-atthakatha` |
| `sn-4-atthakatha` | Saḷāyatanavagga-aṭṭhakathā | `sn-atthakatha` |
| `sn-5-atthakatha` | Mahāvagga-aṭṭhakathā | `sn-atthakatha` |
| `sn-1-tiika` | Sagāthāvaggaṭīkā | `sn-tiika` |
| `sn-2-tiika` | Nidānavaggaṭīkā | `sn-tiika` |
| `sn-3-tiika` | Khandhavaggaṭīkā | `sn-tiika` |
| `sn-4-tiika` | Saḷāyatanavaggaṭīkā | `sn-tiika` |
| `sn-5-tiika` | Mahāvaggaṭīkā | `sn-tiika` |
| `an-1-atthakatha` | Ekakanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-2-atthakatha` | Dukanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-3-atthakatha` | Tikanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-4-atthakatha` | Catukkanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-5-atthakatha` | Pañcakanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-6-atthakatha` | Chakkanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-7-atthakatha` | Sattakanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-8-atthakatha` | Aṭṭhakanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-9-atthakatha` | Navakanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-10-atthakatha` | Dasakanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-11-atthakatha` | Ekādasakanipāta-aṭṭhakathā | `an-atthakatha` |
| `an-1-tiika` | Ekakanipāta-ṭīkā | `an-tiika` |
| `an-2-tiika` | Dukanipāta-ṭīkā | `an-tiika` |
| `an-3-tiika` | Tikanipāta-ṭīkā | `an-tiika` |
| `an-4-tiika` | Catukkanipāta-ṭīkā | `an-tiika` |
| `an-5-tiika` | Pañcakanipāta-ṭīkā | `an-tiika` |
| `an-6-tiika` | Chakkanipāta-ṭīkā | `an-tiika` |
| `an-7-tiika` | Sattakanipāta-ṭīkā | `an-tiika` |
| `an-8-tiika` | Aṭṭhakanipāta-ṭīkā | `an-tiika` |
| `an-9-tiika` | Navakanipāta-ṭīkā | `an-tiika` |
| `an-10-tiika` | Dasakanipāta-ṭīkā | `an-tiika` |
| `an-11-tiika` | Ekādasakanipāta-ṭīkā | `an-tiika` |

Registered 2026-11-13. Sources: CSCD `s0101a`–`s0103a.att`, `s0101t`–`s0103t.tik`, and `s0104t` + `s0105t.nrf` (one work over two volumes, joined).

MN registered 2026-11-13. Sources: CSCD `s0201a`–`s0203a.att`, `s0201t`–`s0203t.tik`. CSCD has no abhinavaṭīkā on the Majjhimanikāya.

MN 1 front matter (`--frontmatter`): `Ganthārambhakathā` in the aṭṭhakathā, `Ganthārambhakathāvaṇṇanā` in the ṭīkā. The ṭīkā numbers its Ganthārambhakathāvaṇṇanā paragraphs 1.–16. for itself. Those numbers are not root citations, so they are left unlinked (`--unlinked`).

SN registered 2026-11-14. Sources: CSCD `s0301a`–`s0305a.att`, `s0301t`–`s0305t.tik`. CSCD has no abhinavaṭīkā on the Saṃyuttanikāya. SN 1 front matter is handled as in the MN: `--frontmatter "Ganthārambhakathā"` (aṭṭhakathā), and `--frontmatter` plus `--unlinked "Ganthārambhakathāvaṇṇanā"` (ṭīkā, its own numbers 1.–19.).

AN registered 2026-11-16. Sources: CSCD `s0401a`–`s0404a.att` and `s0401t`–`s0404t.tik`, four volumes per layer, cut into one file per nipāta with `--book K` (tree mode). CSCD has no abhinavaṭīkā on the Aṅguttaranikāya. AN 1 front matter: `--frontmatter "Ganthārambhakathā"` (aṭṭhakathā → `^1-I-0`). For the ṭīkā, `--frontmatter "Ganthārambhakathā"` and `--frontmatter "Ganthārambhakathāvaṇṇanā"` (→ `^1-I-0`, `^1-II-0`), plus `--unlinked "Ganthārambhakathāvaṇṇanā"` (its own numbers 1.–19.). The Dasaka-ṭīkā's own verse list `1.`–`12.` carries no `@n` in the XML; it is not linked to the root.

KN books 1–2 registered 2026-11-16. Sources: CSCD `s0501a.att` (Khuddakapāṭha-aṭṭhakathā, `--frontmatter "Ganthārambhakathā"` → `^1-I-0`, `--per-section`: its citations link within their own section) and `s0502a.att` (Dhammapada-aṭṭhakathā, one file printed in two parts; every verse it quotes links to the root verse). Both are div-less files, converted in tree mode. These two books have no ṭīkā in CSCD. One Khuddakapāṭha-aṭṭhakathā citation stays unlinked and logged: its `13.` in the Tirokuṭṭasutta, whose root prints only verses 1–12.

Tier labels: **commentary** (aṭṭhakathā) and **sub-commentary** (ṭīkā). The abhinavaṭīkā is a second sub-commentary on the same aṭṭhakathā: tipitaka.app pairs its paragraphs with the aṭṭhakathā's, as it does for the ṭīkā. A ṭīkā names the aṭṭhakathā it explains in its `commentary:` frontmatter. The tier order sets the order of the Traditional Interpretation sections in a verse package: aṭṭhakathā first, then the ṭīkā, then the abhinavaṭīkā.

Once assigned, a `registered_id` never changes.

---

## 4. Language tracks

| Tag | Language | Translation track | Plan stream |
| --- | -------- | ----------------- | ----------- |
| `pi` | Pāli (source) | — (source) | — |

**No translation tracks yet.** New tracks are added by creating `3-TRANSFORMATIONS/Translations/<lang>-<descriptor>/` and running the `bilingual-glossary` skill from the consolidated `2-RAILS/Bilingual-Glossaries/pi-<lang>.md`.

### Analysis language per rail section

The default, unchanged: Traditional Interpretation paraphrases and Translation Notes are in English. Everything else (AI Overview, Disambiguated Restatement, Local-Wiki articles, Key Concepts) is in Pāli.

---

## 5. Bilingual glossary pairs

None yet.

---

## 6. Active transformation tracks

None yet.

---

## 7. Source-language tags used in this vault

| Tag | Script / System | Use in this vault |
| --- | --------------- | ----------------- |
| `-pi` | Pāli romanisation (PTS diacritics), as in the CSCD `romn` edition | all root texts, **default** |

The default for every Pāli source is `-pi`.

---

## 8. Where to look next

- [`0-VAULT-Structure.md`](0-VAULT-Structure.md): the architecture in full.
- [`../../1-SOURCES/About Sources.md`](../../1-SOURCES/About%20Sources.md): source-file rules.
- [`../../2-RAILS/About Rails.md`](../../2-RAILS/About%20Rails.md): rails schema.
- [`../../3-TRANSFORMATIONS/About Transformations.md`](../../3-TRANSFORMATIONS/About%20Transformations.md): track and output rules.
- [`annotation-conventions.md`](annotation-conventions.md): the default block-ID conventions this annex registers deviations from.
- [`vault-variants.md`](vault-variants.md) §2: the multi-book canon variant this vault follows.
- [`../Skills/cscd-root-text-intake/SKILL.md`](../Skills/cscd-root-text-intake/SKILL.md): how a CSCD volume is brought into `1-SOURCES/Text/`.
- [`../CLAUDE.md`](../CLAUDE.md): the operational quick-reference. *This annex overrides it on the points recorded above.*
- [Top-level `README.md`](../../README.md): pipeline overview and reading paths.
