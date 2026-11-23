# MN and SN commentaries vs tipitaka-xml, tipitaka.app and their roots — verification

- **Date:** 2026-11-23
- **Files:** `pi-mn-atthakatha`, `pi-mn-tiika`, `pi-sn-atthakatha`, `pi-sn-tiika`.
- **Tools:** [`compare_comm.py`](compare_comm.py), [`site_titles.py`](site_titles.py) and [`toc_view.py`](toc_view.py). Output: `<file>-detail.md`.

## Result

| | MN aṭṭhakathā | MN ṭīkā | SN aṭṭhakathā | SN ṭīkā |
|---|---|---|---|---|
| Text vs XML (character for character) | ✅ | ✅ | ✅ | ✅ (+ the documented `[Ed:]` note on `1101.`) |
| Block IDs (running counters, no duplicates) | ✅ | ✅ | ✅ | ✅ |
| Root links: all resolve and match the printed number | 1,110 ✅ | 1,088 ✅ | 1,698 ✅ | 1,648 ✅ (`1101.` → `^5-1103`, documented) |
| Heading titles vs tipitaka.app, in order | — | — | 1,127/1,127 ✅ | 1,113/1,113 ✅ |
| **TOC structure** | ⚠️ Nigamana | ⚠️ 2 flattened sections | ✅ | ⚠️ the closing section |

- **Printed ranges:** a printed range (`531-650.`) links every root block inside it, including the SN root's range blocks (`^5-541-552`) and its gaps where suttas are abbreviated. The check now accepts exactly that set.
- **Level differences:** sutta sub-sections nested under their sutta, as in the root texts.

## TOC fixes ✅ APPLIED 2026-11-23 on the user's approval (heading lines only, except SN ṭīkā item 4)

> **What changed:** 37 heading lines in `pi-mn-tiika.md` and 1 in `pi-mn-atthakatha.md`. In `pi-sn-tiika.md`, 1 heading became a text line and 1 heading moved. All three files are byte-identical to their dry-run copies.
>
> **Re-check:**
> - text, block IDs and root links unchanged;
> - no empty heading left;
> - heading IDs agree with depth.
>
> The remaining hints are the CSCD numbering slips below. **Backups:** `backups/<file>.pre-toc-fix.md.bak`. **Library:** prod still has the old TOCs, and for the SN ṭīkā the old segmentation.

**MN** ([`fix_mn_comm.py`](fix_mn_comm.py)):
1. **ṭīkā, Mūlapariyāyasutta.**
   - `Nettinayavaṇṇanā` opens *"Idāni … pakaraṇanayena pāḷiyā atthavaṇṇanaṃ karissāma"*, the same section as DN's Pakaraṇanaya. It cross-references `dī. ni. ṭī. 1.149`.
   - **Fix:** it holds `Soḷasahāravaṇṇanā` (16 hāras), `Pañcavidhanayavaṇṇanā` (4) and `Sāsanapaṭṭhānavaṇṇanā`. The hāras go 7 levels deep, so their titles are in **bold**.
2. **ṭīkā, Satipaṭṭhānasutta.**
   - The empty `Kāyānupassanāvaṇṇanā` holds its 6 pabbas (Ānāpāna … Navasivathika).
   - The empty `Dhammānupassanāvaṇṇanā` holds its 5 (Nīvaraṇa … Catusacca).
3. **aṭṭhakathā, `Nigamanakathā`.**
   - Now: `##### ^3-5-10-1-0`, inside the Indriyabhāvanāsutta.
   - Fix: `#### ^3-5-11-0`, the vagga's last section, which is where the XML puts it (`book/vagga`).

The size: 37 heading lines in the ṭīkā and 1 in the aṭṭhakathā.

**SN** ([`fix_sn_tiika.py`](fix_sn_tiika.py)):

4. **ṭīkā, the end of book 5.**
   - **The mis-tagged heading:** CSCD tags the first half of the closing sentence, *"Sāratthappakāsiniyā saṃyuttanikāya-aṭṭhakathāya / Mahāvaggavaṇṇanāya līnatthappakāsanā niṭṭhitā"*, as `subhead`. So the vault has a heading `##### … ^5-12-10-4-0` inside the last peyyāla vagga.
     - **Fix:** it becomes the first line of the block holding the second half (`^5-574`). No block ID changes.
   - **The Nigamana:** `##### Nigamanakathāvaṇṇanā ^5-12-10-5-0` becomes `### Nigamanakathāvaṇṇanā ^5-13-0`, as in the aṭṭhakathā.

## Faithful as they are

- **MN ṭīkā `14. Adhiṭṭhāna…` / `14. Parikkhāra…`, and SN ṭīkā `3. Dubbaṇṇiya…` / `3. Sambarimāyā…`:** CSCD numbering slips, invisible in the vault.
- **SN ṭīkā's `Nettinayavaṇṇanā`:** it has no sub-headings, so there is nothing to nest.
