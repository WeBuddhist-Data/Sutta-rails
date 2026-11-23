# DN commentaries vs tipitaka-xml, tipitaka.app and `pi-dn.md` — verification

- **Date:** 2026-11-23
- **Files:**
  - `pi-dn-atthakatha.md` (`s0101a`–`s0103a.att`);
  - `pi-dn-tiika.md` (`s0101t`–`s0103t.tik`);
  - `pi-dn-1-abhinavatiika.md` (`s0104t` + `s0105t.nrf`).
- **Tools:**
  - [`compare_comm.py`](compare_comm.py) checks content character for character, block IDs and running counters, heading text and level against the XML with hierarchy hints, and every root-link group against the printed number after it.
  - [`site_toc.py`](site_toc.py) compares the heading trees with tipitaka.app.
- **Output:** `<file>-detail.md`.

## Result

| | aṭṭhakathā | ṭīkā | abhinavaṭīkā |
|---|---|---|---|
| Text vs XML | ✅ identical (only the `504-407` footnote line added) | ✅ (2 cosmetic spaces) | ✅ identical |
| Block IDs | ✅ running counters 1…N per book, no duplicates | ✅ | ✅ |
| Root links | 958 groups, 1,159 links, all resolve; 1 differs from its printed number: the documented `504-407.` → 504–507 | 933 / 1,051, all match | 325 / 442, all match |
| Headings: text vs XML | ✅ | ✅ | ✅ |
| Front matter vs tipitaka.app | ✅ same tree (`Ganthārambhakathā` → `Nidānakathā`, `Paṭhamamahāsaṅgītikathā`) | ✅ | ✅ |
| **TOC structure** | ✅ | ⚠️ 1 flattened section | ⚠️ 1 flattened section, Nigamana misplaced |

## TOC fixes ✅ APPLIED 2026-11-23 on the user's approval ([`fix_dn_comm.py`](fix_dn_comm.py); heading lines only)

> **Applied:** both fixes below. **Lines changed:** 23 heading lines in `pi-dn-tiika.md` and 24 in `pi-dn-1-abhinavatiika.md`, byte-identical to the dry-run copies.
>
> **Re-check:**
> - text, block IDs and root links unchanged (933 / 1,051 and 325 / 442 links, all matching);
> - no empty heading left;
> - every heading ID agrees with its depth.
>
> **Backups:** `backups/<file>.pre-toc-fix.md.bak`. **Library:** prod still has the old TOCs.

### 1. Pakaraṇanaya section of the Brahmajālasuttavaṇṇanā (ṭīkā and abhinavaṭīkā)

- **What's wrong:** the XML tags every section `subhead`, so the vault has 24 sibling sections. `Soḷasahāravaṇṇanā` ("the sixteen hāras") and `Pañcavidhanayavaṇṇanā` ("the five methods") are left **empty**, while their parts follow as their siblings.
- **The evidence:** `Pakaraṇanayavaṇṇanā` opens *"Ayaṃ pana pakaraṇanayena pāḷiyā atthavaṇṇanā"*, the explanation by the method of the Pakaraṇa (Netti). That method is the 16 hāras, the 5 nayas and the sāsanapaṭṭhāna.

```
#### Pakaraṇanayavaṇṇanā              ^1-1-20-0  (ṭīkā; abhinavaṭīkā ^1-1-19-0)
##### Soḷasahāravaṇṇanā               ^…-1-0     16 hāras under it, Desanā … Samāropana
##### Pañcavidhanayavaṇṇanā           ^…-2-0     Nandiyāvaṭṭa, Tipukkhala, Sīhavikkīḷita, Disālocana-aṅkusa
##### Sāsanapaṭṭhānavaṇṇanā           ^…-3-0
```

- **Changes:** 23 heading lines (ṭīkā) and 23 (abhinavaṭīkā). The deepest heading is `######`, and no ID outside this section changes.

### 2. The abhinavaṭīkā's `Nigamanakathā`

- **What's wrong:** it is the colophon of the whole work, and outside every div in the XML. The vault has it as the 5th section of the **Tevijjasuttavaṇṇanā** (`#### ^1-13-5-0`).
- **Fix:** `### Nigamanakathā ^1-14-0`, the book's last section after the 13 suttas.

## Nigamana in all Sutta commentaries: one rule

**The Nigamana goes where the XML puts it:**
- **inside a div:** as the last child of that div;
- **outside every div:** as the last child of the file's last book.

| File | Now | By the rule |
|---|---|---|
| DN aṭṭhakathā, ṭīkā | `### ^3-12-0` | ✅ already (outside every div → last book) |
| DN 1 abhinavaṭīkā | `#### ^1-13-5-0`, inside the Tevijjasutta | `### ^1-14-0` (fix 2 above) |
| MN aṭṭhakathā | `##### ^3-5-10-1-0`, inside a sutta | the last child of the vagga (XML: `book/vagga`) |
| SN aṭṭhakathā | `### ^5-13-0` | ✅ already (XML: in book 5) |
| SN ṭīkā | `##### ^5-12-10-5-0`, inside a sutta | the last child of the saṃyutta (XML: `book/samyutta`) |
| AN aṭṭhakathā, ṭīkā | `#### ^11-2-…`, inside the last vagga | the last child of book 11 (XML: `book`) |
| KN 1, KN 2 aṭṭhakathā | `####`, inside the last section or story | the last child of the book (XML: outside every div) |

These are handled with each nikāya's commentaries.

## Faithful as they are

- **Ṭīkā Mahāsatipaṭṭhāna:** the *pabba* sections are nested under their sutta, one level below the XML's `subhead`, as in the root texts.
- **Abhinavaṭīkā levels:** its `.nrf` XML has no divs, only rend ranks, and the 155 level differences come from that. The tree matches tipitaka.app's (`tika2-dn-1`).
- **Ṭīkā lines 2350 and 7397, `279. ** Tividhaṃ sīla**nti`:** the XML's bold starts with a space (`279.** Tividhaṃ`). This is cosmetic, and the text is the same.
- **The second abhinavaṭīkā volume's title `(Dutiyo bhāgo)`:** a text block since the two files were joined.
