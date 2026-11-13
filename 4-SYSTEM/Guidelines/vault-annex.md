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

Only volumes that have been ingested are present in the folder. The Dīghanikāya is the text currently being worked on, as Pāli root text only (no commentaries or translations yet).

**Other nikāyas** (Majjhima, Saṃyutta, Aṅguttara, Khuddaka) are registered in this table **before** they are ingested, with their book numbers and file names. Saṃyutta and Aṅguttara volumes nest deeper than book → sutta, which `cscd-root-text-intake` does not yet support (it stops rather than flattening).

---

## 2. Addressing scheme

**`verse_id_format`:** `book-verse`

**Format example:** `^1-149` (Sīlakkhandhavagga, printed paragraph 149)

- **Nikāya collection:** the abbreviation in the file name, `dn` for Dīghanikāya. The collection is given by the file, not by the ID.
- **`book`:** the position of the CSCD volume within its nikāya (`1`–`3` for the Dīghanikāya's three vaggas).

Block IDs always resolve as `file#^id`, so the same `^1-149` in two different files names two different blocks.

### Heading hierarchy

| Markdown | Role | Anchor | Example |
| -------- | ---- | ------ | ------- |
| (plain, before the first heading) | Homage (`Namo tassa…`) | `^T-1` | `Namo tassa bhagavato arahato sammāsambuddhassa ^T-1` |
| `#` | Nikāya, as printed | `^0` | `# Dīghanikāyo ^0` |
| `##` | Volume (vagga) | `^<book>-0` | `## Sīlakkhandhavaggapāḷi ^1-0` |
| `###` | Sutta | `^<book>-<n>-0` | `### Brahmajālasuttaṃ ^1-1-0` |
| `####` | Sub-heading within the sutta | `^<book>-<n>-<m>-0` | `#### Paribbājakakathā ^1-1-1-0` |

Each heading segment is the heading's **sibling position** under its parent. It is not the number printed in the source. Printed sutta numbers are stripped from the heading text (`1. Brahmajālasuttaṃ` → `Brahmajālasuttaṃ`).

### Verse numbering rule

- The content ID is the **paragraph number printed in CSCD**, copied verbatim: never renumbered, padded or invented.
- CSCD restarts paragraph numbers at 1 in **each volume**: Sīlakkhandhavagga 1–559, Mahāvagga 1–441, Pāthikavagga 1–360. One file per volume therefore gives each file a single unbroken run, and content IDs need no zone segment.
- The number does **not** restart at sutta or sub-heading boundaries.
- A paragraph's unnumbered continuation lines, gāthā lines and closing lines (`… niṭṭhitaṃ`) stay in its block. The ID goes on the block's last line.

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

No duplicates occur in the Dīghanikāya.

**Why:** this keeps the invariant that every `^<book>-<N>` is a real printed number.

---

## 3. Registered commentary IDs

**None ingested yet.** No `registered_id` may be used in any rail until it is added to this roster.

| `registered_id` | Title | Tier | Language | File |
| --------------- | ----- | ---- | -------- | ---- |
| — | — | — | — | — |

When commentaries are ingested, the tiers are **commentary** (aṭṭhakathā), **sub-commentary** (ṭīkā), **sub-sub-commentary** (anuṭīkā / abhinavaṭīkā). The tier order sets the order of the Traditional Interpretation sections in a verse package: aṭṭhakathā first, then the ṭīkā tiers in order.

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
