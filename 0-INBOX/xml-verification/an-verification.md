# AN — root text and commentaries — verification

- **Date:** 2026-11-23
- **Files:** `pi-an.md`, `pi-an-atthakatha.md` (`s0401a`–`s0404a.att`) and `pi-an-tiika.md` (`s0401t`–`s0404t.tik`).
- **Tools:**
  - [`compare_sutta.py`](compare_sutta.py) for the root, [`compare_comm.py`](compare_comm.py) for the commentaries;
  - [`rank_depth.py`](rank_depth.py), which flags an XML heading rank that lands at different depths;
  - [`toc_view.py`](toc_view.py) for the trees.

## Result

| | root | aṭṭhakathā | ṭīkā |
|---|---|---|---|
| Text vs XML | ✅ except 2 items below | ✅ | ✅ (13 hangnum verse numbers joined to their verse line, as in Vinaya) |
| Block IDs | ✅ | ✅ | ✅ |
| Root links: all resolve and match the printed number | — | 1,427 ✅ | 1,654 ✅ |
| **TOC structure** | 1 heading | ⚠️ Etadagga, AN 10, AN 11, Saṃkhepakathā | ⚠️ AN 1 vaggas 14–20 tangled; Etadagga, AN 10, AN 11 |

## Fixes ✅ APPLIED 2026-11-23 on the user's approval (all, including E)

> **What changed:**
> - `pi-an.md`: 2 lines.
> - `pi-an-tiika.md`: 98 heading lines.
> - `pi-an-atthakatha.md`: 90 heading lines, plus the `Rūpādivaggavaṇṇanā` heading moved below `^1-20`–`^1-22`.
>
> The two commentaries are byte-identical to their dry-run copies.
>
> **Re-check:**
> - block IDs and root links unchanged (1,427 and 1,654 links, all matching);
> - no empty heading left;
> - heading IDs agree with depth.
>
> The root's only remaining difference from the XML is the deliberate `(11). Rāgapeyyālaṃ` → `Rāgapeyyālaṃ`. **Backups:** `backups/<file>.pre-fix.md.bak`. **Library:** prod still has the old text and TOCs.

### Root `pi-an.md` (2 lines)

1. **Line 11122:** `### (11). Rāgapeyyālaṃ ^8-3-0` becomes `### Rāgapeyyālaṃ ^8-3-0`, like the other 9 Rāgapeyyāla headings.
2. **Line 11090:** the note `[[] etthantare …` becomes `[[ ] etthantare …`, as in the XML (`[ ]`).

### Commentaries ([`fix_an_comm.py`](fix_an_comm.py); heading lines, IDs renumbered in books 1, 10 and 11 only)

**A. ṭīkā, AN 1 vaggas 14–20.** The XML has only ranks there, and the tree came out tangled:

| Now | Fixed |
|---|---|
| the 7 Etadagga sub-vaggas are 7 separate vaggas (`^1-11-0` … `^1-17-0`) | one `Etadaggavaggo` `^1-11-0` holding them, as in the aṭṭhakathā and on tipitaka.app |
| `Aṭṭhānapāḷi` ×2 and the first `Ekadhammapāḷi` are inside the 7th Etadagga sub-vagga | vaggas again: `^1-12-0`, `^1-13-0`, `^1-14-0` (the repeated `Ekadhammapāḷi` titles go under it) |
| vaggas 17–20 (Pasādakaradhamma, Aparaaccharāsaṅghāta, Kāyagatāsati, Amata) are inside the last `Ekadhammapāḷi` | vaggas again: `^1-15-0` … `^1-18-0` |

**B. Both files, Etadaggavagga.**
- **What's wrong:** each sub-vagga heading (`Paṭhama-` … `Sattama-etadaggavagga…`) is **empty**, and its *Etadaggapadavaṇṇanā* and thera/therī *vatthus* follow as its siblings.
- **Fix:** they nest under it.
- **Kept as is:** the CSCD prints the vagga title `14. Etadaggavaggo` again before each sub-vagga, and that repeat stays the sub-vagga's container, as on tipitaka.app.

**C. Both files, AN 10.**
- **What's wrong:** `(21) Karajakāyavaggo` sits inside the 4th paṇṇāsaka, and so does `(22) Sāmaññavagga…` in the aṭṭhakathā.
- **Fix:** both stand beside the paṇṇāsakas (`^10-5-0`, `^10-6-0`), as their numbers and the root say.

**D. Both files, AN 11.** The Nigamana moves from the last vagga to `### ^11-3-0`, which is where the XML puts it (in the book, after the vaggas).

**E. aṭṭhakathā, optional: `Saṃkhepakathā`.**
- **What's wrong:** it is empty, because the CSCD prints `1. Rūpādivaggavaṇṇanā` before the summary paragraphs (`^1-20`–`^1-22`: the 11 nipātas, the 9,557 suttas, the first sutta). tipitaka.app has the same.
- **Fix:** move the `### Rūpādivaggavaṇṇanā` line below those 3 blocks, so `Saṃkhepakathā` holds them. That moves one heading past 3 paragraphs.

**Sizes:**

| File | Heading lines changed |
|---|---|
| ṭīkā | 98 |
| aṭṭhakathā | 89, or 90 with E |

**Re-check on copies:**
- Text, block IDs and root links are unchanged, and the deepest heading is `######`.
- No empty heading is left, except `Saṃkhepakathā` if E is not applied.

## Faithful as they are

- **Numbering restarts that are the source's own:**
  - the repeated `14. Etadaggavaggo` / `16. Ekadhammapāḷi` titles;
  - the peyyāla series (`1. Kodhapeyyālaṃ`, `1. Sammutipeyyālādi…`);
  - CSCD slips such as `2. Phaggunasutta…` / `2. Chaḷabhijātisutta…`.
- **Vaggas outside any paṇṇāsaka** (AN 2–7: the peyyālas, `Upasampadāvaggo`, `Abyākatavaggo` …): that is where the XML and the root have them.
