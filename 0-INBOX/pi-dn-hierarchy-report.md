# Dīghanikāya (`pi-dn-1` … `pi-dn-3`) — root text: structure and content

**Date:** 2026-11-13
**Texts:** the three Dīghanikāya root-text volumes, built with `4-SYSTEM/Skills/cscd-root-text-intake/`:

| File | Volume | CSCD source | tipitaka.app |
|---|---|---|---|
| `pi-dn-1.md` | Sīlakkhandhavaggapāḷi | `s0101m.mul.xml` | `dn-1` |
| `pi-dn-2.md` | Mahāvaggapāḷi | `s0102m.mul.xml` | `dn-2` |
| `pi-dn-3.md` | Pāthikavaggapāḷi | `s0103m.mul.xml` | `dn-3` |

**Checked against:** VipassanaTech/tipitaka-xml `romn/` (downloaded 2026-11-13 to `0-INBOX/raw-data/dn/`), and tipitaka.app's `/api/children` and `/api/text` (fetched 2026-11-13 to `0-INBOX/tipitaka-app/`).

This note is for someone opening the project cold. It records what was checked, what was fixed, and what differs from the website on purpose. Root text only: no commentaries, no translation, no upload.

---

## Status

The three files in `1-SOURCES/Text/` are the builds that pass every check below. They were checked again in place after the move.

They replaced copies from an earlier build the same day, with human approval. That earlier build differed in three ways only:

1. It kept CSCD's `‘‘ ’’`; the current files use `"`.
2. It had a stray `. ` at the start of `pi-dn-2.md` `^2-389` (see "What was fixed").
3. Its `source_description` was worded differently.

Block IDs and headings did not change. Nothing had cited the earlier copies.

---

## How IDs work

| Track | Shape | Example | Meaning |
|---|---|---|---|
| Pre-title | `^T-1` | homage line | content before the first heading |
| Collection | `^0` | `# Dīghanikāyo ^0` | the nikāya heading as printed |
| Volume | `^<book>-0` | `## Mahāvaggapāḷi ^2-0` | `<book>` = vagga position in DN (1–3) |
| Heading | path + `-0` | `### Mahāpadānasuttaṃ ^2-1-0` | sibling position under its parent |
| Content | `^<book>-<N>` | `^2-389` | `N` = printed CSCD paragraph number, verbatim |
| Unnumbered | `^<book>-U<k>` | `^2-U1` | a paragraph the source sets apart without a number |

Each volume is one numbering run (CSCD restarts at 1 in every vagga), so content IDs need no zone.

---

## Results

| | `pi-dn-1` | `pi-dn-2` | `pi-dn-3` |
|---|---:|---:|---:|
| Suttas (`###`) | 13 | 10 | 11 |
| Sub-headings (`####`) | 131 | 146 | 136 |
| Content IDs | `^1-1`…`^1-559` | `^2-1`…`^2-441` + `^2-U1` | `^3-1`…`^3-360` + `^3-U1` |
| Words (= XML) | 45,387 | 54,743 | 46,581 |
| tipitaka.app paragraphs matched | 1,074 / 1,074 | 1,559 / 1,559 | 1,910 / 1,910 |
| Printed numbers in the right block | 559 / 559 | 441 / 441 | 360 / 360 |
| Contents-tree nodes matched | 144 / 144 | 156 / 156 | 147 / 147 |

- **vs XML:** identical word stream. Content IDs equal the XML's paragraph numbers, with no gaps or duplicates. Every block has exactly one ID, on its last line.
- **vs tipitaka.app:** every md line matches one site paragraph, in order. Every site paragraph number `n` sits in block `^<book>-<n>`. Every contents-tree node matches in title, order and nesting.

## What was fixed (in the skill, then rebuilt)

| Issue | Where | Fix |
|---|---|---|
| Untagged dot after a paragraph number | `s0102m` paragraph 389 (`<hi rend="paranum">389</hi>. ‘‘Katamā`) | the converter had added its own dot and kept the plain one, leaving `. "Katamā…`; it now uses the source's dot either way |
| No space after the dot | `s0102m` paragraphs 335–342, 354, 370 (`370.‘‘Apariyositasaṅkappo`) | the number prefix is normalised before parsing; without it the 10 paragraphs merged into the one before |

Both were found by the tipitaka.app check. The XML check found the second, but not the first, because it read the XML the same way the converter did.

## Intentional differences from the website

| Item | Note |
|---|---|
| Printed paragraph numbers, sutta numbers on headings | stripped from the text and kept as block IDs; the site shows them |
| Variant readings | `[…]`; the site shows `{…}` |
| Double quotes | `"`; the site shows `‘‘ ’’` |
| Page markers | dropped; the site shows `|M1.0001|` etc. No stray space is left before punctuation (0 in all three files) |
| Tree depth | the site's depth is the md level + 1 on every node: the site counts the piṭaka as a level the source does not print. Nesting is identical |

## Judgment calls (for a reviewer)

| ID | Text | Why |
|---|---|---|
| `^2-U1` | "Bhūtapubbaṃ, ānanda, rājā mahāsudassano …" (Mahāsudassanasutta) | unnumbered paragraph directly after a sub-heading; kept as its own block |
| `^3-U1` | "Tena kho pana samayena nigaṇṭho nāṭaputto …" (Pāsādikasutta, before 165) | same; the converter had prepended it to paragraph 165, and it was split off |

## Not done

- No commentaries (`s0101a`… `.att`, `.tik`, `.nrf`).
- No lint, parse or upload, so no library IDs, `license` or `category_id` in the frontmatter.
- The vault annex does not yet record the `pi-dn-<book>` scheme.

## Related

- Skill: `4-SYSTEM/Skills/cscd-root-text-intake/SKILL.md`
- ID scheme and registered deviations: `4-SYSTEM/Guidelines/vault-annex.md` §2
