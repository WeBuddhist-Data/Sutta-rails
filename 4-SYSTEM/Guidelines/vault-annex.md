# Vault Annex — sutta-rails conventions

The methodology guidelines (`0-VAULT-Structure.md`, `../../1-SOURCES/About Sources.md`, `../../2-RAILS/About Rails.md`, `../../3-TRANSFORMATIONS/About Transformations.md`) are **text-agnostic**: they apply to any Railroads vault built on any classical text. This annex records the conventions specific to *this* vault, the **Pāli Sutta Piṭaka**.

When the Guidelines and this annex disagree on a vault-specific detail, this annex wins, **for the points it actually states**. Everything it does not state follows the defaults unchanged.

---

## 1. The text

This vault serves the **Pāli Sutta Piṭaka**, the second basket of the Pāli Canon, in the Chaṭṭha Saṅgāyana (CSCD) edition published by the Vipassana Research Institute.

Source-text files in `1-SOURCES/Text/` are **one file per CSCD volume**. Ingested so far:

| Nikāya | Volume | `book` | CSCD source | tipitaka.app key | Filename |
| ------ | ------ | ------ | ----------- | ---------------- | -------- |
| Dīghanikāya | Sīlakkhandhavaggapāḷi | 1 | `s0101m.mul.xml` | `dn-1` | `pi-dn-1.md` |
| Dīghanikāya | Mahāvaggapāḷi | 2 | `s0102m.mul.xml` | `dn-2` | `pi-dn-2.md` |
| Dīghanikāya | Pāthikavaggapāḷi | 3 | `s0103m.mul.xml` | `dn-3` | `pi-dn-3.md` |
| Majjhimanikāya | Mūlapaṇṇāsapāḷi | 1 | `s0201m.mul.xml` | `mn-1` | `pi-mn-1.md` |
| Majjhimanikāya | Majjhimapaṇṇāsapāḷi | 2 | `s0202m.mul.xml` | `mn-2` | `pi-mn-2.md` |
| Majjhimanikāya | Uparipaṇṇāsapāḷi | 3 | `s0203m.mul.xml` | `mn-3` | `pi-mn-3.md` |
| Saṃyuttanikāya | Sagāthāvaggo | 1 | `s0301m.mul.xml` | `sn-1` | `pi-sn-1.md` |
| Saṃyuttanikāya | Nidānavaggo | 2 | `s0302m.mul.xml` | `sn-2` | `pi-sn-2.md` |
| Saṃyuttanikāya | Khandhavaggo | 3 | `s0303m.mul.xml` | `sn-3` | `pi-sn-3.md` |
| Saṃyuttanikāya | Saḷāyatanavaggo | 4 | `s0304m.mul.xml` | `sn-4` | `pi-sn-4.md` |
| Saṃyuttanikāya | Mahāvaggo | 5 | `s0305m.mul.xml` | `sn-5` | `pi-sn-5.md` |

Only volumes that have been ingested are present in the folder. The Dīgha-, Majjhima- and Saṃyuttanikāya are in, in Pāli: root text and commentaries (§3), no translations yet. MN registered 2026-11-13, SN 2026-11-14.

**Other nikāyas** (Aṅguttara, Khuddaka) are registered in this table **before** they are ingested, with their book numbers and file names.

`cscd-root-text-intake` supports three shapes:
- book → sutta `<div>`s (Dīgha);
- book → vagga `<div>`s whose suttas are numbered sub-headings (Majjhima);
- book → saṃyutta `<div>`s, with vaggas as `title` and suttas as `subhead` paragraphs (Saṃyutta).

Aṅguttaranikāya volumes are split over several files and nest by nipāta; the skill must be checked against that shape before they are ingested. It stops rather than flattening.

---

## 2. Addressing scheme

**`verse_id_format`:** `book-verse`

**Format example:** `^1-149` (Sīlakkhandhavagga, printed paragraph 149)

- **Nikāya collection:** the abbreviation in the file name: `dn` for Dīghanikāya, `mn` for Majjhimanikāya, `sn` for Saṃyuttanikāya. The collection is given by the file, not by the ID.
- **`book`:** the position of the CSCD volume within its nikāya (`1`–`3` for the Dīghanikāya's three vaggas, `1`–`3` for the Majjhimanikāya's three paṇṇāsas, `1`–`5` for the Saṃyuttanikāya's five vaggas).

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

Each heading segment is the heading's **sibling position** under its parent. It is not the number printed in the source. Printed sutta and vagga numbers, and printed ranges, are stripped from the heading text (`1. Brahmajālasuttaṃ` → `Brahmajālasuttaṃ`, `1-10. Tathāgatādisuttaṃ` → `Tathāgatādisuttaṃ`).

### Verse numbering rule

- The content ID is the **paragraph number printed in CSCD**, copied verbatim: never renumbered, padded or invented.
- CSCD restarts paragraph numbers at 1 in **each volume**: Sīlakkhandhavagga 1–559, Mahāvagga 1–441, Pāthikavagga 1–360; Mūlapaṇṇāsa 1–513, Majjhimapaṇṇāsa 1–486, Uparipaṇṇāsa 1–463; Sagāthāvagga 1–271, Nidānavagga 1–246, Khandhavagga 1–716, Saḷāyatanavagga 1–420, Mahāvagga 1–1201. One file per volume therefore gives each file a single unbroken run, and content IDs need no zone segment.
- The number does **not** restart at sutta or sub-heading boundaries.
- A paragraph's unnumbered continuation lines, gāthā lines and closing lines (`… niṭṭhitaṃ`) stay in its block. The ID goes on the block's last line.
- CSCD sometimes prints a paragraph number on a line of its own (`<p rend="hangnum">`), with the paragraph's gāthā on the next line. The number is joined to that gāthā line, as tipitaka.app shows it. This happens in 10 MN paragraphs (MN 1 ¶513; MN 2 ¶76, 456–460; MN 3 ¶135, 237, 382) and 48 in SN 1.
- **Printed ranges** (Saṃyuttanikāya): a paragraph printed as `225-240.` is one block, and its ID is the range as printed, `^3-225-240`. There are 27 in SN 3, 16 in SN 4 and 50 in SN 5. A commentary citation of any number in the range links to that block.
- **Gaps as printed** (SN Mahāvagga): one paragraph number can cover a run of abbreviated suttas, so the next printed number jumps (`270.` → `280.`). The IDs keep the gap. The 11 gaps are 270→280, 280→292, 292→302, 302→311, 552→587-596, 608→641-650, 662→673-684, 716→749-758, 770→792-802, 856→889-898 and 934→967-976.
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

#### ⚑ Pre-title `^T-N` and collection heading `^0` — overrides `annotation-conventions.md` §2 (registered 2026-11-13)

**Default:** the `#` title takes no ID, and pre-chapter material goes under `## 0. Introduction ^0-0` as `^0-N`.

**This vault:** the homage before the first heading is `^T-1` (then `^T-2`, …), and the `#` nikāya heading is `^0`. There is no chapter 0.

**Why:** the homage is part of the printed text but precedes all structure. A synthetic "Introduction" heading would add editorial structure the source does not have.

#### ⚑ Unnumbered blocks `^<book>-U<k>` and duplicates `^<book>-<N>x<k>` (registered 2026-11-13)

A paragraph that the source sets apart without a printed number (e.g. directly after a sub-heading) is its own block `^<book>-U<k>`, with `k` in document order within the file. A printed number repeated within one run takes `x1`, `x2`, … on its later copies.

Currently used:
- `^2-U1`: Mahāsudassanasutta.
- `^3-U1`: Pāsādikasutta, before paragraph 165.
- Saṃyuttanikāya: `^1-U1` (Sagāthāvagga closing line); `^2-U1`, `^2-U2` (Nidānasaṃyutta peyyāla and closing); `^5-U1`…`^5-U12` (Mahāvagga, unnumbered abbreviated suttas and closing lines).

No duplicates occur in the Dīgha-, Majjhima- or Saṃyuttanikāya, and the Majjhimanikāya has no `U` blocks.

**Why:** this keeps the invariant that every `^<book>-<N>` is a real printed number.

---

## 3. Registered commentary IDs

No `registered_id` may be used in any rail until it is added to this roster.

| `registered_id` | Title | Tier | Language | Root text | File |
| --------------- | ----- | ---- | -------- | --------- | ---- |
| `dn-1-atthakatha` | Sīlakkhandhavaggaṭṭhakathā | commentary | Pāli | `pi-dn-1.md` | `1-SOURCES/Commentaries/pi-dn-1-atthakatha.md` |
| `dn-2-atthakatha` | Mahāvaggaṭṭhakathā | commentary | Pāli | `pi-dn-2.md` | `1-SOURCES/Commentaries/pi-dn-2-atthakatha.md` |
| `dn-3-atthakatha` | Pāthikavaggaṭṭhakathā | commentary | Pāli | `pi-dn-3.md` | `1-SOURCES/Commentaries/pi-dn-3-atthakatha.md` |
| `dn-1-tiika` | Sīlakkhandhavaggaṭīkā | sub-commentary | Pāli | `pi-dn-1.md` | `1-SOURCES/Commentaries/pi-dn-1-tiika.md` |
| `dn-2-tiika` | Mahāvaggaṭīkā | sub-commentary | Pāli | `pi-dn-2.md` | `1-SOURCES/Commentaries/pi-dn-2-tiika.md` |
| `dn-3-tiika` | Pāthikavaggaṭīkā | sub-commentary | Pāli | `pi-dn-3.md` | `1-SOURCES/Commentaries/pi-dn-3-tiika.md` |
| `dn-1-abhinavatiika` | Sīlakkhandhavaggaabhinavaṭīkā | sub-commentary (second) | Pāli | `pi-dn-1.md` | `1-SOURCES/Commentaries/pi-dn-1-abhinavatiika.md` |

| `mn-1-atthakatha` | Mūlapaṇṇāsa-aṭṭhakathā | commentary | Pāli | `pi-mn-1.md` | `1-SOURCES/Commentaries/pi-mn-1-atthakatha.md` |
| `mn-2-atthakatha` | Majjhimapaṇṇāsa-aṭṭhakathā | commentary | Pāli | `pi-mn-2.md` | `1-SOURCES/Commentaries/pi-mn-2-atthakatha.md` |
| `mn-3-atthakatha` | Uparipaṇṇāsa-aṭṭhakathā | commentary | Pāli | `pi-mn-3.md` | `1-SOURCES/Commentaries/pi-mn-3-atthakatha.md` |
| `mn-1-tiika` | Mūlapaṇṇāsa-ṭīkā | sub-commentary | Pāli | `pi-mn-1.md` | `1-SOURCES/Commentaries/pi-mn-1-tiika.md` |
| `mn-2-tiika` | Majjhimapaṇṇāsaṭīkā | sub-commentary | Pāli | `pi-mn-2.md` | `1-SOURCES/Commentaries/pi-mn-2-tiika.md` |
| `mn-3-tiika` | Uparipaṇṇāsa-ṭīkā | sub-commentary | Pāli | `pi-mn-3.md` | `1-SOURCES/Commentaries/pi-mn-3-tiika.md` |

Registered 2026-11-13. Sources: CSCD `s0101a`–`s0103a.att`, `s0101t`–`s0103t.tik`, and `s0104t` + `s0105t.nrf` (one work over two volumes, joined).

MN registered 2026-11-13. Sources: CSCD `s0201a`–`s0203a.att`, `s0201t`–`s0203t.tik`. CSCD has no abhinavaṭīkā on the Majjhimanikāya.

MN 1 front matter (`--frontmatter`): `Ganthārambhakathā` in the aṭṭhakathā, `Ganthārambhakathāvaṇṇanā` in the ṭīkā. The ṭīkā numbers its Ganthārambhakathāvaṇṇanā paragraphs 1.–16. for itself. Those numbers are not root citations, so they are left unlinked (`--unlinked`).

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
