# Aṅguttaranikāya — structure, hierarchy and alignment (pre-intake)

**Checked:** 2026-11-16.

**Sources:**
- VipassanaTech/tipitaka-xml `romn/`: 19 files in `0-INBOX/raw-data/an/`, byte-identical to the repo (git blob SHA).
- tipitaka.app: `an-1..11`, `atta-an-1..11`, `tika-an-1..11` (text, contents tree, links), in `0-INBOX/tipitaka-app/`.

**Status:** ingested 2026-11-16 (§7). Nothing is committed, pushed or uploaded.

---

## 1. The files: one per nipāta, as on tipitaka.app

| Vault file (proposed) | Nipāta | Root XML | Aṭṭhakathā XML (book in the volume) | Ṭīkā XML (book) |
|---|---|---|---|---|
| `pi-an-1` | Ekakanipāta | `s0401m` | `s0401a` | `s0401t` |
| `pi-an-2` | Dukanipāta | `s0402m1` | `s0402a` (1 of 3) | `s0402t` (1 of 3) |
| `pi-an-3` | Tikanipāta | `s0402m2` | `s0402a` (2) | `s0402t` (2) |
| `pi-an-4` | Catukkanipāta | `s0402m3` | `s0402a` (3) | `s0402t` (3) |
| `pi-an-5` | Pañcakanipāta | `s0403m1` | `s0403a` (1 of 3) | `s0403t` (1 of 3) |
| `pi-an-6` | Chakkanipāta | `s0403m2` | `s0403a` (2) | `s0403t` (2) |
| `pi-an-7` | Sattakanipāta | `s0403m3` | `s0403a` (3) | `s0403t` (3) |
| `pi-an-8` | Aṭṭhakanipāta | `s0404m1` | `s0404a` (1 of 4) | `s0404t` (1 of 4) |
| `pi-an-9` | Navakanipāta | `s0404m2` | `s0404a` (2) | `s0404t` (2) |
| `pi-an-10` | Dasakanipāta | `s0404m3` | `s0404a` (3) | `s0404t` (3) |
| `pi-an-11` | Ekādasakanipāta | `s0404m4` | `s0404a` (4) | `s0404t` (4) |

Commentaries would be `pi-an-N-atthakatha.md` and `pi-an-N-tiika.md`, so 33 files in all. CSCD has no abhinavaṭīkā on the Aṅguttara.

**Why per nipāta:**
- CSCD prints the root one file per nipāta, and paragraph numbers restart at 1 in each.
- tipitaka.app shows each nipāta as its own book in all three layers. Its commentary books are slices of the volume file (`atta-an-3` = paragraphs 321–992 of `s0402a`).
- The `book` number in every ID is the nipāta number (`^4-149` = Catukkanipāta ¶149).

## 2. Hierarchy

The XML nests three ways, sometimes inside one nipāta:
- `book → paṇṇāsaka <div> → vagga <div> → sutta`;
- `book → vagga <div> → sutta`, for vaggas outside any paṇṇāsaka and for the Ekaka- and Ekādasakanipāta;
- `peyyāla <div>`s at either level.

The commentaries vary too:
- **Aṭṭhakathās** mostly follow the root's divs. In `s0404a` books 2–4, though, the vaggas are `<head rend="chapter">` elements straight inside the book.
- **Ṭīkās** have no inner divs at all. They use `title` (paṇṇāsaka) > `chapter` (vagga) > `subhead` (sutta) paragraphs.

**Tree mode** (new, `--tree`) reads every heading's level from that nesting:

```
## Dukanipātapāḷi ^2-0
### Paṭhamapaṇṇāsakaṃ ^2-1-0            paṇṇāsaka
#### Kammakaraṇavaggo ^2-1-1-0          vagga
##### Vajjasuttaṃ ^2-1-1-1-0            sutta
### Acelakavaggo ^3-4-0                 (Tikanipāta) a vagga outside the paṇṇāsakas
```

Printed numbers are stripped from headings, including the cumulative form `(6) 1. Puggalavaggo` → `Puggalavaggo`.

## 3. Paragraph numbers

- **Root:** 1,877 content IDs across the 11 nipātas, including 90 printed ranges, for example the long peyyāla ranges `^4-304-783`, `^7-653-1132` and `^11-512-671`.
- **Gaps:** one, Catukkanipāta 105 → 107. It is as printed in the XML.
- **Number-only paragraphs:** one root `hangnum` is joined to its gāthā (Aṭṭhakanipāta ¶32).
- **Homage:** in four XML files the homage carries `n="0"` with no printed number, and its text starts `. Namo tassa…` (as printed). It stays the pre-title `^T-1`.

## 4. Results

| | XML: words, IDs, bold | Every heading (level + text) | Citations | tipitaka.app |
|---|---|---|---|---|
| 11 root texts | PASS ×11 | ALL MATCH ×11 | — | PASS ×11 |
| 11 aṭṭhakathās | PASS ×11 | ALL MATCH ×11 | linked right, 0 wrong | PASS ×8; 3 explained (a) |
| 11 ṭīkās | PASS ×11 | ALL MATCH ×11 | linked right, 0 wrong | PASS ×10; 1 explained (b) |

- **Citations:** 2,103 linked right and 0 wrong. 30 numbers are the commentaries' own numbering, left unlinked and logged:
  - the Ekaka-ṭīkā's own front-matter numbers 1.–19. (18 paragraphs);
  - the Dasaka-ṭīkā's own verse list `1.`–`12.`, which the XML does not mark as paragraph numbers (no `@n`).
- **Lines outside a volume's books** go with the nearest book, as on tipitaka.app. For example, `s0402t`'s closing `Dutiyo bhāgo niṭṭhito.` goes in the Catukka-ṭīkā.
- **Front matter, Ekakanipāta:**
  - aṭṭhakathā: `Ganthārambhakathā` → `^1-I-0`;
  - ṭīkā: `Ganthārambhakathā` → `^1-I-0` and `Ganthārambhakathāvaṇṇanā` → `^1-II-0`.

  In both, the first vagga is `^1-1-0`, as in the root.

Explained differences from tipitaka.app (site artefacts; the files follow the XML):
- **(a)** The site has no contents nodes for vaggas the XML gives as `<head>`s straight in the book: Navaka-, Dasaka- and Ekādasaka-aṭṭhakathā.
- **(b)** The site pairs the Dasaka-ṭīkā's own verse number `12.` with the aṭṭhakathā's comment on root ¶12, by number alone.
- **Notes only:** a paragraph printed as a single number on one side and as a range on the other; and, in the ṭīkās, site nesting that differs on paṇṇāsaka headings.

## 5. Decisions for a human

1. **Ṭīkā vaggas after the last paṇṇāsaka.**
   - A ṭīkā has no divs, so nothing marks where a paṇṇāsaka ends.
   - Its vaggas printed after the last paṇṇāsaka therefore nest under that paṇṇāsaka. Tikanipāta example: `#### Acelakavaggavaṇṇanā ^3-3-5-0`, against the root's `### Acelakavaggo ^3-4-0`.
   - Either keep this, which is what the XML gives, or place those vaggas at the root's level by matching their names to the root's vaggas.
   - The links (transclusions) are correct either way.
2. **Commentary heading IDs** are sibling positions, as for the SN, so they differ from the root's wherever a commentary skips a vagga or sutta.
3. **Annex entries:**
   - books 1–11 → `pi-an-1..11.md` (keys `an-1..11`), tree mode;
   - the 22 commentary IDs `an-1..11-atthakatha`, `an-1..11-tiika`;
   - the Ekakanipāta front matter.

## 6. Skill changes made (vault copies)

- **`cscd_xml_to_json.py`:**
  - `--tree`;
  - `--book K`;
  - lines outside books go to the first or last book.
- **`cscd_shape.py`:** `tree_levels`, `strip_heading_number`.
- **New:**
  - `tree_to_md.py`, the root converter in tree mode;
  - `check_headings.py`, the independent heading check, now part of the skill.
- **`verify.py`:**
  - `--tree`;
  - counts only printed paragraph numbers.
- **`compare_site.py`:**
  - `(N) N.` headings;
  - compares lines without whitespace.
- **`fetch_site.py`:**
  - pages over a book's own slice;
  - retries HTTP 5xx.
- **`commentary_converter.py`:**
  - tree branch;
  - numbers without `@n` are never citations.
- **`build_commentary.py` / `apply_commentary_ids.py`:**
  - repeatable `--frontmatter`;
  - the unlinked log is always written.
- **`verify_commentary.py`:**
  - `--book K`;
  - printed citations only;
  - the text's own numbering recognised.
- **`compare_site_commentary.py`:** matches site paragraphs by index `i`.

**DN, MN and SN regression:** 33 of 34 files regenerate byte-identical. The only difference is `pi-sn-5-tiika`'s hand-made `[Ed:]` correction. All checkers report the same results on them as before.

## 7. Ingested (2026-11-16)

- **Annex:**
  - §1–§2: the 11 nipātas (`pi-an-1..11`, `book` = nipāta number), tree mode, the heading levels, the paragraph runs, the 90 printed ranges, the Catukkanipāta gap, the `n="0"` homage and `^4-U1`;
  - §3: the 22 commentary IDs `an-1..11-atthakatha`, `an-1..11-tiika` and the Ekakanipāta front matter.
- **Files:** `1-SOURCES/Text/pi-an-1..11.md` and `1-SOURCES/Commentaries/pi-an-1..11-atthakatha.md`, `pi-an-1..11-tiika.md`.
  - Built in `0-INBOX/temp/an/` and `0-INBOX/temp/an-comm/` (scripts `build_an_roots.sh`, `build_an_comm.sh`), moved with `mv -n`, and checked again in place.
  - Against the XML: all 33 PASS, with every heading matching.
  - Citations: 2,103 linked right, 0 wrong.
  - tipitaka.app: 29 PASS; the 4 others differ only by the site artefacts in §4.
- **Unresolved logs:** they stay in `0-INBOX/temp/an-comm/*.unresolved.json`.
- **Library fields:** `license: cc0`, `tag_ids: [296WZOr8MXWteSqBBI7pl]` and `category_id: MZUUxphQ0yFwLBon3Vng8`, as for the DN, MN and SN. They are not uploaded; check the titles against the library before any upload.
- **Decisions §5.1–5.2:** kept as built. Ṭīkā vaggas after the last paṇṇāsaka stay nested under it, and commentary heading IDs are sibling positions.
