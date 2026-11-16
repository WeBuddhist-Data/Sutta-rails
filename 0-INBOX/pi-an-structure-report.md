# Aṅguttaranikāya — structure, hierarchy and alignment (pre-intake)

**Checked:** 2026-11-16.

**Sources:**
- VipassanaTech/tipitaka-xml `romn/`: 19 files in `0-INBOX/raw-data/an/`, byte-identical to the repo (git blob SHA).
- tipitaka.app: `an-1..11`, `atta-an-1..11`, `tika-an-1..11` (text, contents tree, links), in `0-INBOX/tipitaka-app/`.

**Status:** ingested 2026-11-16 (§7); intake committed and pushed (`d398506`, `fc3a38c`); uploaded to library-prod 2026-11-16 (§8).

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

## 8. Uploaded to library-prod.webuddhist.com (2026-11-16)

Run with `0-INBOX/temp/upload-an.sh`. For each file: lint, parse, dry run with live checks, `--execute`, `--verify`; the log is `0-INBOX/temp/upload-an.log`. The library IDs are in each file's frontmatter and in both upload ledgers.

**Titles:** none of the 33 clashes with a title in the Sutta, Vinaya or Abhidhamma vaults, and the library accepted all of them unchanged.

**Category:** every text is under **Discourses** (`XfCwZpoJMtfO7s0laQkdK`), the category fixed for the Sutta texts the same day, with tag Theravāda (`296WZOr8MXWteSqBBI7pl`). Read back on every root.

**Checked:** the IDs in the files equal the ledgers; each commentary's `commentary_of` is its root's `text_id`, and it is aligned to its root's edition; live segments equal the file's blocks.

| File | Library title | text_id | edition_id | toc_id | Segments | Alignment pairs → root edition |
|---|---|---|---|---|---|---|
| pi-an-1 | Ekakanipātapāḷi | `OzMkZ0SL8PTrPcoXdpS9a` | `UopigfzoTevjdwKcC00E7` | `Arxh4s7sKwjRalFJSh0hq` | 324 | — |
| pi-an-1-atthakatha | Ekakanipāta-aṭṭhakathā | `oRgGDx3qzIZrcir1j8wUD` | `wozxMmpIez2ypdBEX60LQ` | `iv1qYn45AlzP59UrIsFus` | 1320 | 1567 → `UopigfzoTevjdwKcC00E7` |
| pi-an-1-tiika | Ekakanipāta-ṭīkā | `3QeNbLO0blZkbeOPHhAy0` | `fxpXr8al20MDNf0UVu19j` | `bDsSduLICTdeSdrqE7Do3` | 921 | 1002 → `UopigfzoTevjdwKcC00E7` |
| pi-an-2 | Dukanipātapāḷi | `HXEj10ht3p5nATUuVDXkd` | `46AtxFI9d8nErnZHXOhuU` | `mwbpvu8Szfn2fh4IiXCBb` | 196 | — |
| pi-an-2-atthakatha | Dukanipāta-aṭṭhakathā | `zFTn4XRZh1Omqam772uKi` | `UFQXqHYVhyddmEdAtVUos` | `e6mwrHygQ82xxxM3bHiHa` | 271 | 271 → `46AtxFI9d8nErnZHXOhuU` |
| pi-an-2-tiika | Dukanipāta-ṭīkā | `tL4kgystH0OIt2XZ0LnPP` | `560GUHZjukbZOiiPAFgAN` | `yIP3vEOhxp3bbgOXjoml8` | 283 | 333 → `46AtxFI9d8nErnZHXOhuU` |
| pi-an-3 | Tikanipātapāḷi | `mE59gFTdeVZCfvsz3orEQ` | `O4QZlFUTwWqxBZfACNWQ4` | `ZVSifYzb9zkcfu0X3hLsh` | 160 | — |
| pi-an-3-atthakatha | Tikanipāta-aṭṭhakathā | `rJlmwQPTqR8oluok2cwtA` | `oMNgKUiiwzpFyH73kTWnq` | `N4S37ktSlplz3UAQQMUjU` | 504 | 519 → `O4QZlFUTwWqxBZfACNWQ4` |
| pi-an-3-tiika | Tikanipāta-ṭīkā | `xfxf31ISazEfdVfX9knVE` | `GsJwdTkrklAcl9ze6V1FT` | `RYTXCsVevGnmSINfKB9A6` | 565 | 717 → `O4QZlFUTwWqxBZfACNWQ4` |
| pi-an-4 | Catukkanipātapāḷi | `0mndr3Abu9iP0o6s9RU0e` | `umEBNmV2sng5zHjOT6Vgo` | `mfQf6wuvRvKUy2u3HUUM0` | 279 | — |
| pi-an-4-atthakatha | Catukkanipāta-aṭṭhakathā | `PcTOQ8CBYEwFLYpsH0cgW` | `HSlWiDWtygULLAdlTlUkw` | `A2PBE5108ZpMuYv2jDXZs` | 486 | 583 → `umEBNmV2sng5zHjOT6Vgo` |
| pi-an-4-tiika | Catukkanipāta-ṭīkā | `GQsHVsNT0iEhlbmOn9KS9` | `JCkVmx09MbqyBazXV40tS` | `lHFndrZk4G6meTHPn3n6Y` | 685 | 1041 → `umEBNmV2sng5zHjOT6Vgo` |
| pi-an-5 | Pañcakanipātapāḷi | `AbzuxZ1DTUcSvJdL42Xwk` | `7WeTyxp8yonAxsutbpazz` | `yibQ3GJJlaZrmA4WX58Qw` | 272 | — |
| pi-an-5-atthakatha | Pañcakanipāta-aṭṭhakathā | `W5C33S1nA6wS9MqWbHLqo` | `dVwsFl0qCIfFiqp96ZOb4` | `aScXIBuuKDlAFhA6EXEQf` | 293 | 326 → `7WeTyxp8yonAxsutbpazz` |
| pi-an-5-tiika | Pañcakanipāta-ṭīkā | `tV3TZvv1uZXbOwf1kdczY` | `yTFtrgUMi8JYdgTj7NTyt` | `MnaGcZAYDc3BCqnLjbfZh` | 334 | 804 → `7WeTyxp8yonAxsutbpazz` |
| pi-an-6 | Chakkanipātapāḷi | `3Dbr1UAVES5MkCdgjQIMB` | `4puW81Zi3uV9n04uCyf3E` | `XIGJoIBvNLo7y3XopdWrm` | 126 | — |
| pi-an-6-atthakatha | Chakkanipāta-aṭṭhakathā | `gIfCpoXnsThUrdnLFBmrz` | `0ExaQSzwctYWuqjLwA3sM` | `PL7odjvjQtyBI2TAXOjND` | 190 | 215 → `4puW81Zi3uV9n04uCyf3E` |
| pi-an-6-tiika | Chakkanipāta-ṭīkā | `U3JEgJJDFQn7CTNrHfRmN` | `devZnN7BmkuazUuHvMLec` | `toafTz1NqFf6xOjd3iAAZ` | 244 | 453 → `4puW81Zi3uV9n04uCyf3E` |
| pi-an-7 | Sattakanipātapāḷi | `DXM9m4bgTjB6dgK3wofpb` | `HKK8bv5u542EYQ12WboAe` | `DLgYRWmVTKTOYqLckoUL3` | 102 | — |
| pi-an-7-atthakatha | Sattakanipāta-aṭṭhakathā | `NewiyH4D6WO7g1w3dlnSs` | `f6VF9pHSJbuwVZFCVJl5y` | `UzIS60YgJCEF7a0Gz7rgs` | 134 | 147 → `HKK8bv5u542EYQ12WboAe` |
| pi-an-7-tiika | Sattakanipāta-ṭīkā | `a47iqPDr32dqXzlVsl1gS` | `WKxCphDefr1oBlEzR2N7q` | `V6dZ0vGwLbZQYcX5Hl25h` | 181 | 290 → `HKK8bv5u542EYQ12WboAe` |
| pi-an-8 | Aṭṭhakanipātapāḷi | `wzL4TQ6yPiU4EGfsmmfB0` | `ALrSAUIaVNeXPxO5rcnBX` | `iQQIc1kS9iTXRdAR3dEG5` | 97 | — |
| pi-an-8-atthakatha | Aṭṭhakanipāta-aṭṭhakathā | `2T1M0DFSnKQaoRDO2ncbb` | `Lh3f4vIiyybW6Z5R3HTZH` | `Hb24h4sJ7eRbh8I3urKfW` | 188 | 204 → `ALrSAUIaVNeXPxO5rcnBX` |
| pi-an-8-tiika | Aṭṭhakanipāta-ṭīkā | `twFt7NwwFCuY7a9vbWU60` | `Ynbvd0HkiAO1JfFYlUiUS` | `37CoFerj5dYfEESoyd2am` | 220 | 441 → `ALrSAUIaVNeXPxO5rcnBX` |
| pi-an-9 | Navakanipātapāḷi | `3lYAlAzmWa087hlGQJs0V` | `kQhhrP0whHnRCGRFrbhFp` | `Uz0RbwL8gUu0QtMSNVvYD` | 83 | — |
| pi-an-9-atthakatha | Navakanipāta-aṭṭhakathā | `n1Z4wAbdoBbTb7dJV4ObO` | `6NRooeGD0mSy12mX2bR15` | `IGIF9fDTig8eRaHNT8uFd` | 85 | 109 → `kQhhrP0whHnRCGRFrbhFp` |
| pi-an-9-tiika | Navakanipāta-ṭīkā | `5K8sF0xq4LzoDKtATrFRX` | `dBNeVwOLRDcJjuMhSNMYi` | `oaxty9r8pZNtHLIVf6TNR` | 144 | 209 → `kQhhrP0whHnRCGRFrbhFp` |
| pi-an-10 | Dasakanipātapāḷi | `je4Dvq2GBC6I3kI26pbYa` | `D3lxPOnirS5hYHLRznEMq` | `Jmlk2lvWoykyC6SOxJlHB` | 214 | — |
| pi-an-10-atthakatha | Dasakanipāta-aṭṭhakathā | `0nLTvITx8FdZK0nyHx8f0` | `JLGOEjKYHJGAZN1gzXvgO` | `mLb4JlIl5cdZSUXfTYnHn` | 186 | 221 → `D3lxPOnirS5hYHLRznEMq` |
| pi-an-10-tiika | Dasakanipāta-ṭīkā | `rcSvwctV4NOWYtbBZbYby` | `e1T0WXh4xYsMhd71qgahh` | `zPauA4uVynSl2D0nXzaf9` | 205 | 1107 → `D3lxPOnirS5hYHLRznEMq` |
| pi-an-11 | Ekādasakanipātapāḷi | `w6JEwfcPqkMpYMhPJga2V` | `56FsZ0Q64WTgDPNmEv2t1` | `JxKYjPuttcePNSOB0XyQc` | 36 | — |
| pi-an-11-atthakatha | Ekādasakanipāta-aṭṭhakathā | `peTE18nU7Zzar5NElAFIP` | `wzfADJAiFF1xW4ykjS767` | `93QcQ7jdQ5EmElrToau2b` | 66 | 72 → `56FsZ0Q64WTgDPNmEv2t1` |
| pi-an-11-tiika | Ekādasakanipāta-ṭīkā | `22ENMzxJH19wHWorIzPhr` | `JxmJLUh7YTAR4rpsVcR5v` | `ACG1oVQxIDMT2bS5ZP2rw` | 69 | 101 → `56FsZ0Q64WTgDPNmEv2t1` |
