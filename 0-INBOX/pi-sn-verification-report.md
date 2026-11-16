# Saṃyuttanikāya — independent verification of structure, hierarchy and alignment

**Checked:** 2026-11-16, on the files as they sit in `1-SOURCES/`. This is a second check of the intake recorded in `pi-sn-structure-report.md` (2026-11-14).
**Against:**
- VipassanaTech/tipitaka-xml `romn/`;
- tipitaka.app `sn-1..5`, `atta-sn-1..5`, `tika-sn-1..5`: text, contents tree, and paragraph links.

**Scope:**
- 5 root texts (`pi-sn-1..5.md`);
- 5 aṭṭhakathās and 5 ṭīkās (`pi-sn-1..5-atthakatha.md`, `pi-sn-1..5-tiika.md`).

**Edits:** one, after approval: the Daṇḍasutta link in `pi-sn-5-tiika.md` (§4.1). All check scripts are scratch files and are not in the vault.

---

## 0. Verdict

The hierarchy and alignment are correct, with one source misprint and two numbering choices for a human.

- Every heading matches the XML and the site, with no gaps:
  - every saṃyutta, vagga and sutta heading of every file;
  - its title, its nesting depth and its order.
- Every root paragraph sits under the same sutta as on the site.
- Every commentary citation:
  - links to a root block that exists;
  - sits under the right saṃyutta;
  - agrees with the site's paragraph link.
- **One wrong link**, inherited from the source; now fixed (§4.1).
- **Two numbering points** for a human to decide (§4.2, §4.3).

## 1. Inputs are current

| Check | Result |
|---|---|
| 15 XML files in `0-INBOX/raw-data/sn/` vs upstream `romn/` (git blob SHA) | 15 / 15 identical |
| tipitaka.app re-fetched today vs the copies in `0-INBOX/tipitaka-app/` | 45 / 45 identical |

## 2. The skill's own checkers, rerun in place

| File | `verify.py` / `verify_commentary.py` |
|---|---|
| pi-sn-1..5 (root) | PASS ×5: same words as the XML, same IDs, same headings |
| 10 commentaries | PASS ×10: 2,162 citations linked right, 0 wrong |

**Note on running the checker in place.**
- `verify_commentary.py` looks for its `.unresolved.json` log next to the file it checks.
- The logs stayed in `0-INBOX/temp/sn-comm/` when the files were moved.
- So run in place, `pi-sn-1-tiika` shows 18 false errors. These are the ṭīkā's own front-matter numbers 1.–19., which are left unlinked on purpose.
- With `--unresolved 0-INBOX/temp/sn-comm/<file>.unresolved.json` it passes.
- Worth a one-line note in the skill.

## 3. Independent checks (no code shared with the skills)

### 3.1 Root texts

| | Headings vs site tree (title + depth) | Headings vs XML, parsed afresh | Paragraph numbers vs site | Paragraph → sutta node vs site |
|---|---|---|---|---|
| pi-sn-1 | 307/307, 0 diff | 307/307, 0 diff | 271/271 | 0 diff |
| pi-sn-2 | 281/281, 0 diff | 281/281, 0 diff | 246/246 | 2 diff (a) |
| pi-sn-3 | 369/369, 1 diff (b) | 369/369, 0 diff | 362/362 | 48 diff (a, b) |
| pi-sn-4 | 381/381, 0 diff | 381/381, 0 diff | 361/361 | 28 diff (a) |
| pi-sn-5 | 713/713, 1 diff (b) | 713/713, 0 diff | 621/621 | 37 diff (a, b) |

- **(a) Sutta keys.** The paragraph is under the same sutta as on the site, but the sutta's key differs. The site keys a sutta by its **printed** number; the vault ID uses its **position**. See §4.2.
- **(b) Site nesting.** These are the site artefacts already recorded:
  - `Khayadhammasuttaṃ`, and the five unnumbered Bojjhaṅga suttas, which the site nests one level down;
  - the XML gives them sutta class, and the files follow the XML.

### 3.2 Commentaries

| | Headings vs site (title + depth) | Headings vs XML | Citations: target exists / right saṃyutta | Citations vs site paragraph links |
|---|---|---|---|---|
| sn-1 aṭṭhakathā | 291/291, 0 | 0 (c) | 271 / 271 | 270 = 270 |
| sn-1 ṭīkā | 306/306, 1 (b) | 0 (c) | 270 / 270 | 269 vs 287 (d) |
| sn-2 aṭṭhakathā | 221/221, 0 | 0 | 246 / 246 | 188 = 188 |
| sn-2 ṭīkā | 224/224, 1 (b) | 0 | 241 / 241 | 188 vs 182 (e) |
| sn-3 aṭṭhakathā | 138/138, 0 | 0 | 362 / 362 | 112 = 112 |
| sn-3 ṭīkā | 135/135, 1 (b) | 0 | 361 / 361 | 109 = 109 |
| sn-4 aṭṭhakathā | 188/188, 0 | 0 | 361 / 361 | 156 = 156 |
| sn-4 ṭīkā | 181/181, 0 | 0 | 350 / 350 | 149 = 149 |
| sn-5 aṭṭhakathā | 289/289, 0 | 0 | 458 / 458 | 233 = 233 |
| sn-5 ṭīkā | 267/267, 2 (b) | 0 | 426 / 426 | 210 vs 208 (e) |

**How the citations were compared.** For each commentary paragraph that cites the root, I paired its printed number with the root blocks transcluded before it. I did the same with the site's paragraph links.
- **Same sequence:** the printed numbers run in the same order as the site's, in every file.
- **Nothing missing:** every root paragraph the site links is also linked in the vault file.
- **Nothing out of range:** no vault link falls outside the commentary's printed number or range.
- **Printed ranges:** the vault links every root block in a printed range (`5-10.` → `^2-5`…`^2-10`). The site links only the first. This applies to 1–58 groups per file.
- **Placement:** every transclusion directly precedes its numbered paragraph.
- **Order:** no citation runs backwards in any file.

**Sutta check.** The first citation under each commentary sutta heading lands in the root sutta of the same name in 1,814 of 1,825 sections.
- Nine of the other 11 are spelling variants:
  - in the heading: Magha/Māgha, Kiṃnu/Kinnu, Saṃbhejja/Sambhejja, Suci/Sūci, Vana-/Navakammika, Dabba/Daṭṭhabba;
  - or a vagga-level heading.
- One is the misprint in §4.1.
- `…ādivaṇṇanā` sections ("on X and those that follow") cover several root suttas, as the source groups them.

**Notes to the tables.**
- **(c) Front matter.** The `Ganthārambhakathā` heading has a different XML element; it is present in the file and on the site.
- **(d) SN 1 ṭīkā front matter.** The site pairs the ṭīkā's own front-matter numbers 1.–19. with the aṭṭhakathā. The vault leaves them unlinked, by design.
- **(e) Ṭīkā links the site does not have.** The vault links more here, and correctly:
  - the site links the ṭīkā to the aṭṭhakathā only by exact number;
  - where the aṭṭhakathā prints `25-26.` and the ṭīkā prints `26.` (SN 2: 26, 28, 30, 94, 132, 171), the site has no link;
  - likewise where the aṭṭhakathā has no such paragraph (SN 5: 371, 397-407);
  - the vault's ṭīkā links straight to the root paragraph, which exists.

## 4. For a human

### 4.1 Source misprint: wrong link in `pi-sn-5-tiika.md` (Daṇḍasutta) — fixed

- **Where:** `s0305t.tik.xml` line 3181. `3. Daṇḍasuttavaṇṇanā` prints its paragraph as `1101.`.
- **Expected:** the root and the aṭṭhakathā put the Daṇḍasutta at `1103`. Root `^5-1101` is the Sīsapāvanasutta.
- **The gloss:** *punappunaṃ vaṭṭasmiṃyeva nibbattanti* ("they are reborn again and again in the round"). It fits the Daṇḍasutta, not the Sīsapāvanasutta.
- **Effect:** the file and tipitaka.app both follow the XML. The ṭīkā's Daṇḍasutta comment therefore transcludes `pi-sn-5.md#^5-1101`, the wrong sutta.
- **Fixed 2026-11-16, with the user's approval:**
  - the transclusion now points to `^5-1103`;
  - an `[Ed: …]` note at the end of the paragraph, before `^5-546`, records the misprint;
  - the printed `1101.` and all wording are unchanged.
  - The correction is logged under `corrections` in `0-INBOX/temp/sn-comm/pi-sn-5-tiika.unresolved.json`.
- **Expected checker output from now on.** `verify_commentary.py` on `pi-sn-5-tiika.md` reports exactly two problems, and nothing else changed:
  - the note's words, as an insertion;
  - citation 1101, as linked to `5-1103` instead of `5-1101`.
  - My independent checks show only this one departure from the XML and the site.
- **Regeneration undoes it.** Rebuilding this file from the XML would drop the fix, so reapply it after any rebuild. The checker could be taught to read the `corrections` list; that is a skill change.

### 4.2 Root sutta IDs are positions, not printed sutta numbers (133 headings)

- **The cause:** where one heading covers a run of abbreviated suttas, the vault's position ID and the printed number drift apart.
  - Example: `Rūpādisuttanavakaṃ` covers 2–10.
  - So `11. Anusayasuttaṃ` gets `^2-7-2-3-0`, while the site key is `sn-2-7-2-11`.
- **Counts:** SN 1: 0, SN 2: 3, SN 3: 41, SN 4: 28, SN 5: 61.
- **The printed number is lost.** The intake strips it from the heading, so `11` now appears nowhere in `pi-sn-2.md`.
- **Printed numbers are not unique either.** Peyyāla series restart at 1 inside a vagga. For example, `1. Kalyāṇamittasuttaṃ` is at `^5-1-6-4-0`. So the position scheme is the only one that never collides.
- **Options:**
  - keep it as is, per annex §2;
  - or keep the position IDs and also keep the printed number in the heading text (`11. Anusayasuttaṃ`) or in a field, so a reader can find SN 2.7.2.11. This is a change to the intake rule.

### 4.3 Commentary heading IDs often differ from the root sutta's ID

- **The cause:** the commentary IDs are positions among the commentary's own headings, and the commentaries skip suttas they do not comment on. This is the known decision §5.2 of the intake report.
- **How often:** across 1,822 sections, the commentary heading ID equals the root sutta's ID in 70%. By volume: SN 1 90–95%, SN 2 80–85%, SN 3 65–69%, SN 4 58–59%, SN 5 36–37%.
- **Example:** `Daṭṭhabbasuttavaṇṇanā ^5-4-1-3-0` comments on the root's `Daṭṭhabbasuttaṃ ^5-4-1-8-0`.
- **Effect:** alignment through the transclusions is unaffected. But a tool that matched a commentary to the root by heading ID would be wrong in most of SN 5.
- **Option:** number commentary vagga and sutta headings by the root sutta they cite. This would be an annex change.

---

## 5. Outline and upload-readiness checks (2026-11-16)

These are the checks the Abhidhamma `pi-3`…`pi-7` reports and the DN/MN upload ran, applied to the SN.

### 5.1 Outline (as in the Abhidhamma reports)

All 15 files pass:
- the heading level equals the ID path length + 1;
- every child is one level below its parent and extends the parent's ID;
- siblings are numbered 1…n with no gaps;
- every heading and content ID is unique;
- the only block before the first heading is the homage `^T-1`.

Two expected results:
- **Front matter:** the only non-numeric heading segment is the front-matter `I` (SN 1 aṭṭhakathā and ṭīkā).
- **The book heading:** the checker reports each file's `##` book heading `^<book>-0` as a sibling "gap" for books 2–5. This is by design (annex §2: book = volume number).

**Headings with no text of their own** (a title directly followed by its first child) are normal, as in the Abhidhamma:

| File | root | aṭṭhakathā | ṭīkā |
|---|---|---|---|
| SN 1 | 37 | 37 | 37 |
| SN 2 | 35 | 35 | 35 |
| SN 3 | 38 | 28 | 28 |
| SN 4 | 39 | 34 | 34 |
| SN 5 | 100 | 57 | 57 |

### 5.2 Lint and parse: root texts (upload dry run, offline)

`upload_root_text.py --no-live`. All five lint and parse OK. The only warning is that author/translator are missing, which is ignored, as for the DN and MN.

| | Characters | Segments | = content + `U` + `T-1` | TOC nodes = headings | Max depth |
|---|---|---|---|---|---|
| pi-sn-1 | 324,986 | 273 | 271 + 1 + 1 | 309 | 4 |
| pi-sn-2 | 385,810 | 249 | 246 + 2 + 1 | 283 | 4 |
| pi-sn-3 | 389,839 | 363 | 362 + 0 + 1 | 371 | 4 |
| pi-sn-4 | 580,962 | 362 | 361 + 0 + 1 | 383 | 4 |
| pi-sn-5 | 667,600 | 634 | 621 + 12 + 1 | 715 | 4 |

- **Payloads:** the parser payloads are in `4-SYSTEM/Skills/translation-upload/scripts/parser-root-text/output/pi-sn-*`.
- **Logs:** the dry-run logs are in `0-INBOX/temp/sn-upload/`.
- **Files untouched:** the 15 SN files are byte-identical before and after (checked by hash).
- **Side effect undone:** the linter rewrote the timestamp in the tracked `linter-root-text/languages.py`; it was restored with `git checkout`, as the Abhidhamma report advises.

### 5.3 Not done

- **Live checks (no stale text or duplicate in library-prod).** Blocked: loading the API key from `4-SYSTEM/scripts/.env` was refused by the session's permission check. They run as part of the upload dry run once you allow it, or when you run the upload yourself.
- **Commentary lint, parse and dry run.** `upload_commentary.py` needs the root's `text_id`/`edition_id`, and the SN roots are not uploaded yet. A scratch run with placeholder root IDs was also refused. Run it after the roots are uploaded, as for the MN.
  - The alignment content is already checked: every transclusion target exists in its root (§3.2). These targets become the alignment pairs.
- **Upload:** `--execute` and `--verify` for 5 roots then 10 commentaries, like `0-INBOX/temp/mn/upload-mn.sh` (host `library-prod.webuddhist.com`). Not run; needs your explicit go-ahead.
- **The WeBuddhist reader** was not looked at, as in the Abhidhamma reports.
