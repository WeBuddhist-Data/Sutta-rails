# Dhammapada (`pi-kn-2`) — verification of structure, hierarchy and alignment

**Checked:** 2026-11-16, on the files in `1-SOURCES/` as built by the KN intake (`pi-kn-structure-report.md`).
**Against:**
- VipassanaTech/tipitaka-xml `romn/`;
- tipitaka.app `kn-dhp` and `atta-kn-dhp`: text, contents tree, and paragraph links.

**Scope:**
- `1-SOURCES/Text/pi-kn-2.md`;
- `1-SOURCES/Commentaries/pi-kn-2-atthakatha.md`.

**Standard:** the files must follow the repo (XML) and the website. Where the two differ, the XML decides. **Edits:** none.

---

## 0. Verdict

**Both files follow the repo and the website.** Nothing was changed.
- **Root:** text, verse numbers, vaggas and contents tree all match.
- **Aṭṭhakathā:**
  - The text matches.
  - Every one of its 436 links is the same as the site's.
  - Every verse it quotes is the verse it links to.
- **Differences from the site:** two, both where the site departs from the XML (§3).
- **For your information:** one point that follows neither the site's numbering nor the root's (§4). It was not changed.

## 1. Inputs are current

| Check | Result |
|---|---|
| `s0502m.mul.xml`, `s0502a.att.xml` vs upstream `romn/` (git blob SHA) | 2 / 2 identical |
| tipitaka.app `kn-dhp`, `atta-kn-dhp` fetched again today vs `0-INBOX/tipitaka-app/` | 6 / 6 identical |
| A fresh build of the aṭṭhakathā from the XML (`build_kn_comm.sh` into a scratch folder) | identical to the file, apart from the three library-field lines added after the build |

## 2. Results

### 2.1 Root (`pi-kn-2.md`)

| Check | Result |
|---|---|
| `verify.py --tree` (vs XML) | PASS: 423 IDs `^2-1` … `^2-423`, 6,084 words identical |
| `check_headings.py` (vs XML) | 26 / 26 vagga headings, ALL MATCH |
| `compare_site.py` (vs site) | PASS: 971 / 971 lines, 423 / 423 numbers in their block, contents tree 26 / 26 |
| Independent: headings vs site and XML | 26 / 26 in title and depth; IDs `^2-1-0` … `^2-26-0` = site keys `kn-dhp-1` … `-26` |
| Independent: blocks vs site | 423 / 423 blocks have the same verse number, vagga and text. The closing line "Dhammapadapāḷi niṭṭhitā." stays in `^2-423`. |
| Independent: numbering | 1 … 423 contiguous, no duplicate IDs |

### 2.2 Aṭṭhakathā (`pi-kn-2-atthakatha.md`)

| Check | Result |
|---|---|
| `verify_commentary.py` (vs XML) | PASS: 175,056 words identical, 436 citations linked, 0 wrong |
| `compare_site_commentary.py` | 4,797 / 4,797 lines; 436 / 436 site paragraph links agree |
| Independent: link sequence vs the site's paragraph links | identical, 436 = 436 |
| Independent: link targets | all exist; none falls outside its vagga; each printed number equals the linked verse |
| Independent: quoted verse = linked verse | 426 / 426 citations outside the front matter quote exactly the verse they link to. 425 quote it in full, some with spelling variants (*succhannaṃ*, *passatī*, *sagandhakaṃ* where the root reads *suchannaṃ*, *passati*, *sugandhakaṃ*). `2.` cites it by its opening words. |
| Independent: text vs site | 174,621 words. Differences: the file's `(aṭṭhakathā)` title label, and "Ko dhammapadaṃ", where the XML has the space and the site drops it |
| Headings vs XML | 333 / 333 |

## 3. Differences from the website (the XML decides)

**Part 2's reprinted title:**
- The aṭṭhakathā is printed in two parts. At the start of part 2 the site adds a contents node for the reprinted book title, "Dhammapada-aṭṭhakathā" (`atta-kn-dhp-8a`), and nests vaggas 9–26 under it, one level deeper.
- The file keeps the reprinted title as text, as the XML has it, and keeps vaggas 9–26 at the same level as 1–8.
- So 229 headings are one level shallower than on the site; the 103 headings up to vagga 8 have the same depth.

**`Nigamanakathā` (the closing section):** the site nests it under the last story of vagga 26. The file keeps it at story level, where the XML puts it.

## 4. For your information (not changed)

**Front-matter verses are linked to Dhammapada verses:**
- The `Ganthārambhakathā` is the commentator's own introduction. Its verses are numbered 1.–10. in the XML, and they are linked to Dhp 1–10.
- tipitaka.app links them exactly the same way, so they are kept as the website and repo have them.
- They are not citations of the Dhammapada.

**Vagga heading IDs are one off from the root and the site:**
- The front matter takes `^2-1-0`, so Yamakavagga is `^2-2-0` in the aṭṭhakathā, against `^2-1-0` in the root and `atta-kn-dhp-1` on the site. All 26 vaggas are offset.
- In the Khuddakapāṭha aṭṭhakathā, the front matter was built as `^1-I-0`, so its sections keep the root's numbers. That build option was not used for the Dhammapada.
- The links are unaffected, because they point at the verses. Only the commentary's own heading IDs are offset.

## 5. Library fields

`license: cc0`, `tag_ids: [296WZOr8MXWteSqBBI7pl]` (Theravāda), `category_id: XfCwZpoJMtfO7s0laQkdK` (Discourses), on both files. Not uploaded.
