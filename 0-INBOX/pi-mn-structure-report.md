# Majjhimanikāya — structure, hierarchy and alignment check (pre-intake)

Checked 2026-11-13 against `github.com/VipassanaTech/tipitaka-xml` (`romn/`, 9 files) and tipitaka.app (`mn-1..3`, `atta-mn-1..3`, `tika-mn-1..3`: text, contents tree, links).
Nothing was written to `1-SOURCES/` or the annex. Dry runs of `cscd-root-text-intake` and `cscd-commentary-intake` ran in a scratch folder only.

Downloads: `0-INBOX/raw-data/mn/` (sizes equal the GitHub listing). Site data: `0-INBOX/tipitaka-app/`.

---

## 1. Source files

| Work | CSCD file | XML paras | Site paras | Printed ¶ run | Vaggas | Suttas | Bold spans |
|---|---|---|---|---|---|---|---|
| Mūlapaṇṇāsapāḷi | `s0201m.mul.xml` | 1797 | 1796 | 1–513, one run | 5 | 50 | 0 |
| Majjhimapaṇṇāsapāḷi | `s0202m.mul.xml` | 1690 | 1684 | 1–486, one run | 5 | 50 | 1 |
| Uparipaṇṇāsapāḷi | `s0203m.mul.xml` | 1463 | 1460 | 1–463, one run | 5 | 52 (Vibhaṅgavagga 12) | 1 |
| Mūlapaṇṇāsa-aṭṭhakathā | `s0201a.att.xml` | 2911 | 2911 | — | 5 + front matter | 50 | 5,999 |
| Majjhimapaṇṇāsa-aṭṭhakathā | `s0202a.att.xml` | 1339 | 1339 | — | 5 | 50 | 3,070 |
| Uparipaṇṇāsa-aṭṭhakathā | `s0203a.att.xml` | 1107 | 1107 | — | 5 | 52 | 2,152 |
| Mūlapaṇṇāsa-ṭīkā | `s0201t.tik.xml` | 2387 | 2387 | — | 5 + front matter | 50 | 12,361 |
| Majjhimapaṇṇāsaṭīkā | `s0202t.tik.xml` | 906 | 906 | — | 5 | 50 | 4,103 |
| Uparipaṇṇāsa-ṭīkā | `s0203t.tik.xml` | 858 | 858 | — | 5 | 52 | 4,107 |

- **Root numbering:** clean in all three volumes. There is one run per volume, starting at 1, with no gaps, repeats or resets. The `^<book>-<N>` scheme works unchanged (books 1–3 = the three paṇṇāsas).
- **Root vs site paragraph counts:** they differ by 1, 6 and 3. That is exactly the number of `hangnum` paragraphs (§3.2).
- **Commentary paragraph counts:** equal to the site's in all six files.
- **Contents tree:** the site has 80 / 56 / 57 nodes. That equals the XML's vaggas + suttas + in-sutta sub-heads (5+50+25, 5+50+1, 5+52+0), with every title the same.
- **No abhinavaṭīkā** exists for the MN in CSCD. There are two commentary layers only.

## 2. Hierarchy: the MN is one level deeper than the DN

| Level | DN (ingested) | MN (XML) | tipitaka.app depth (MN) |
|---|---|---|---|
| Nikāya | `<p rend="nikaya">` | same | 1–2 (piṭaka, nikāya) |
| Book | `<div type="book">` | `<div type="book">` = paṇṇāsa | 3 |
| Vagga | — | `<div type="vagga">` + `<head rend="chapter">` | 4 |
| Sutta | `<div type="sutta">` | **`<p rend="subhead">` with a printed number** (`1. Mūlapariyāyasuttaṃ`; restarts at 1 in each vagga) | 5 |
| Sub-heading | `<p rend="subhead">` | `<p rend="subhead">` **without** a number | 6 |

The sutta and its sub-headings use **the same XML class**. They can only be told apart by the printed number.

Root ↔ commentary sutta match:

- In all six commentaries, each vagga has exactly one numbered sutta heading for each root sutta, in the same order and with the same number.
- Some titles differ only in spelling or in the commentary's own name for the sutta. These are not errors:
  - `Satipaṭṭhānasuttavaṇṇanā` vs root `Mahāsatipaṭṭhānasuttaṃ`
  - `Vanapatthapariyāya-` vs `Vanapattha-`
  - `Bahuvedaniya-` vs `Bahuvedanīya-`
  - `Samaṇamuṇḍikāputta-` vs `Samaṇamuṇḍika-`
  - `Sappurisadhamma-` vs `Sappurisa-`
  - `Rāhulovāda-` vs `Cūḷarāhulovāda-`
  - root titles carrying a variant (`Pañcattayasuttaṃ pañcāyatanasutta (ka.)`)

## 3. Problems the current skills would hit

### 3.1 Sutta level silently flattened (root and commentary). Blocking.
- `cscd_xml_to_json.py` accepts `book > vagga` as "one chapter-level div type" and does **not** STOP. Skill Rule 4 and annex §1 both say it stops on vagga/paṇṇāsa nesting. For the MN that is untrue.
- Result of the dry run:
  - `### Mūlapariyāyavaggo ^1-1-0`
  - then suttas **and** their sub-heads as `####` siblings: `#### Sabbāsavasuttaṃ ^1-1-2-0`, `#### Dassanā pahātabbāsavā ^1-1-3-0`, …
- The vault's own checkers catch it:
  - `compare_site.py`: `tree nesting differs (depth offsets [1, 2])`
  - `verify.py`: 50 "text differs" items, because sutta numbers are stripped from `####` headings and it allows that only on `###`
  - `compare_site_commentary.py`: nesting differs on 56 headings
- **Needs:**
  - converter/heading logic: vagga = `###`, numbered subhead = sutta `####`, unnumbered subhead = `#####`
  - the annex heading table extended for the MN (human decision, see §5)

### 3.2 `hangnum`: number-only paragraphs. Blocking.
- Ten paragraphs hold only their number. The verse text follows in the next `gatha1` lines:
  - MN 1: ¶513
  - MN 2: ¶76, 456–460
  - MN 3: ¶135, 237, 382
- The class is not in the skill's allowed `css_class` list.
- The converter keeps them as bare `456.` lines. `apply.py` recognises only `N. text`, so:
  - the paragraph gets **no block ID** (dry run: MN 1 has 512/513 IDs, and ¶513 is folded into `^1-512`)
  - `apply.py audit` reports `ANOMALY: expected 456, got 461` (MN 2) and `expected 382, got 383` (MN 3)
  - commentary citations of those paragraphs end up unresolved (both MN 1 commentaries log `513.`)
- tipitaka.app joins the number to the following gāthā line (`n: "456"` on that line).
- **Needs:** a decision on whether the number starts the gāthā block, as on the site. Then `apply.py` and `compare_site.py` should treat a number-only line as the block's opening.

### 3.3 Two-part volumes inside one file (MN 1 aṭṭhakathā and ṭīkā)
- Both files restart partway through with homage + `Majjhimanikāye` + `<p rend="book">` + `(Dutiyo bhāgo)`:
  - XML para 1843 in `s0201a`
  - XML para 1281 in `s0201t`
- Both also open with `(Paṭhamo bhāgo)`.
- Dry run:
  - `(Paṭhamo bhāgo)` and `(Dutiyo bhāgo)` become `###` headings alongside the vaggas. That shifts every vagga position: `Mūlapariyāyavaggo` becomes `^1-2-0` (aṭṭhakathā) and `^1-3-0` (ṭīkā), not `^1-1-0` as in the root. This breaks the rule "commentary sutta k = `^<book>-k-0`, as in the root".
  - The repeated `Majjhimanikāye` / `Mūlapaṇṇāsa-aṭṭhakathā` lines are **dropped** (site has them, md doesn't), against Rule 4 ("every line is kept").
- **Needs:** treat the `bhāgo` markers and the second-part opening as plain text blocks, as `merge_parts.py` does for DN's abhinavaṭīkā.

### 3.4 Front matter (MN 1 aṭṭhakathā and ṭīkā)
- `<div type="vagga" id="mn1_0">` holds Ganthārambhakathā + Nidānakathā. In the aṭṭhakathā it has no `<head>`; in the ṭīkā its head is `Ganthārambhakathāvaṇṇanā`.
- So the `--frontmatter` heading text differs per layer (human confirmation, Rule 5).
- **The ṭīkā numbers its own front-matter paragraphs `1.`–`16.`** These are not root citations. The converter links every leading number, so the dry run put **16 wrong transclusions** (`^1-1`…`^1-16`) into the Ganthārambhakathāvaṇṇanā. `--frontmatter` only changes heading IDs, not linking.
- **Needs:** no root links inside the front-matter subtree.

### 3.5 Numbered sub-heads that are not suttas (MN 1 ṭīkā)
- Inside `Mūlapariyāyasuttavaṇṇanā` → `Nettinayavaṇṇanā`, the ṭīkā has two `<p rend="title">` groups:
  - `Soḷasahāravaṇṇanā`, with 16 numbered hāra sub-heads (`1. Desanāhāravaṇṇanā` … `16. Samāropanahāravaṇṇanā`)
  - `Pañcavidhanayavaṇṇanā`, with 4 numbered sub-heads, one of them `4-5. Disālocana-aṅkusanayadvayavaṇṇanā`
- Any "numbered subhead = sutta" rule from §3.1 must exclude these. Match on the root's sutta list or on the `…suttavaṇṇanā` ending instead.
- tipitaka.app puts `Soḷasahāravaṇṇanā` at **sutta** depth (5). That looks like a site artefact; inside the text it belongs under Mūlapariyāyasutta.
- `title` is also a new class for the skill.

### 3.6 Source anomalies to record (not to fix)
- `s0201a` and `s0201t` each have one `<hi rend="paranum">01</hi>`. In `s0201a` it is the paragraph `Bahinagareti …`, just before the block citing ¶147. `verify_commentary.py` flags `XML citation 01 has no matching cited block`. The site shows it without the number. It should be logged as unresolved, never linked.
- `s0201t`: the hāra list prints `14.` twice (`14. Adhiṭṭhāna-`, `14. Parikkhāra-`; the second should be 15). Keep as printed.
- Abbreviated ranges, all expanded correctly in the dry run:
  - aṭṭhakathā: `380-1.`, `410-4.`
  - ṭīkā: `192-3.`, `195-7.`, …

## 4. Alignment (commentary → root)

Each printed citation was checked against the root's paragraph numbers and against tipitaka.app's `paranum` links. Headings were excluded.

| Commentary | Body citations | Resolve to a root ¶ | Out of order | Agree with site |
|---|---|---|---|---|
| atta-mn-1 | 438 | 438 | 0 | 438 / 438 |
| atta-mn-2 | 354 | 354 | 0 | 354 / 354 |
| atta-mn-3 | 306 | 306 | 0 | 306 / 306 |
| tika-mn-1 | 443 | 443 (incl. 16 front-matter self-numbers, §3.4) | 13 (front matter → body restart) | see note |
| tika-mn-2 | 333 | 333 | 0 | see note |
| tika-mn-3 | 307 | 307 | 0 | see note |

- **Aṭṭhakathā:** clean. All 1,098 citations resolve, run in order and match the site. The MN 1 dry run with the real converter gave `linked right 437, wrong 0`. The one remaining citation is ¶513, which fails only because of §3.2.
- **Ṭīkā:** every body citation names an existing root paragraph.
  - The site links ṭīkā → aṭṭhakathā, not → root.
  - 16 ṭīkā citations name a root paragraph that the aṭṭhakathā never cites, so the site has nothing to link (tika-mn-1 ¶138, 255, 257, 318; tika-mn-2 ¶130, 441; tika-mn-3 ¶86, 96, 192, 347, 382, 388, 403, 404, …). This is the same "explained difference" class as in the DN.
  - Because the site's ṭīkā links point at the aṭṭhakathā, my "agree" count for the ṭīkā is only a rough check. `compare_site_commentary.py` with the aṭṭhakathā file is the proper check once the root is fixed.

## 5. Decisions needed before intake (human)

1. **Annex §1/§2:**
   - register the MN volumes: books 1–3, `pi-mn-1..3.md`, stems `s0201m`–`s0203m`, site keys `mn-1..3`
   - extend the heading table for the MN: `##` paṇṇāsa, `###` vagga, `####` sutta, `#####` sub-heading
   - correct the claim that the skill stops on deeper nesting
2. **Annex §3:** register the IDs: `mn-1..3-atthakatha`, `mn-1..3-tiika`.
3. **`hangnum` handling (§3.2):** recommended — the number opens the following gāthā block, as tipitaka.app shows it.
4. **Front-matter headings** per layer (§3.4): `Ganthārambhakathā` (aṭṭhakathā) and `Ganthārambhakathāvaṇṇanā` (ṭīkā).

## 6. Skill changes needed (tooling, `4-SYSTEM/Skills/`)

- `cscd_xml_to_json.py`:
  - mark numbered subheads inside a vagga div as sutta-level
  - accept `hangnum`, `title`, `subsubhead`
  - stop instead of passing `book > vagga` silently when suttas are not divs
- `tipitaka_org_book.py` / `heading_ids.py` / `verify.py` / `compare_site.py`: one more heading level; allow the sutta-number strip on `####`.
- `apply.py`: number-only paragraph lines.
- `commentary_converter.py` / `apply_commentary_ids.py`:
  - no links in front matter
  - `bhāgo` markers and second-part openings kept as text, not headings
  - title-group sub-heads not treated as suttas

Each change should be re-run on the DN to confirm all ten DN files still PASS.

---

## 7. Status after the skill fixes (2026-11-13)

The problems in §3 are fixed in `cscd-root-text-intake` and `cscd-commentary-intake`, plus one mapping line in `json-to-source-text/converters/tipitaka_org_book.py`. A new shared helper, `cscd_shape.py`, holds the sutta rule.

**Dry run of all nine MN files** (scratch folder; nothing in `1-SOURCES/`):

| File | XML check | Site check |
|---|---|---|
| pi-mn-1 / 2 / 3 | PASS (513 / 486 / 463 IDs; 50 / 50 / 52 suttas) | PASS (every line, every ¶ number, tree) |
| mn-1 aṭṭhakathā | PASS (438 linked, `01` logged) | explained only: synthetic `Ganthārambhakathā` node; `01` not shown on the site |
| mn-1 ṭīkā | PASS (427 linked; 16 front-matter numbers unlinked; `01` logged) | explained only: `01`; site nests the vagga too deep after the `title` groups |
| mn-2 aṭṭhakathā / ṭīkā | PASS / PASS | PASS / PASS |
| mn-3 aṭṭhakathā / ṭīkā | PASS / PASS | explained only: site lacks `Saḷāyatanavaggo` node / PASS |

- Every commentary's vagga and sutta heading IDs equal the root's.
- **DN regression:** all ten DN files regenerate byte-identical from the XML; their unresolved logs are unchanged. `verify.py` and `verify_commentary.py` PASS on them. `compare_site_commentary.py` prints the same output as the original scripts.

**Still open — human decisions (§5):**
- Annex §1/§2 (MN volumes, heading table) and §3 (`registered_id`s).
- Correct the annex §1 sentence that says the skill "stops rather than flattening" for deeper nesting. It is now true for SN/AN, and the MN shape is supported.
- Confirm the `--frontmatter` / `--unlinked` headings for the MN 1 commentaries.

Then run the two skills for real.

- **Shared skill library:** these are vault copies. Per CLAUDE.md §14 the fix should go to the shared library and be re-synced.

## 8. Ingested (2026-11-13)

The MN is now in the vault:
- annex §1–§3 registered;
- `1-SOURCES/Text/pi-mn-1..3.md` and the six files `1-SOURCES/Commentaries/pi-mn-*`;
- every file verified in place.

Results and every judgment call are in `pi-mn-commentary-report.md`.
