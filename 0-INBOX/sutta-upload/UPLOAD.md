# Sutta re-upload to the library, 2026-11-25

Why: the review restored the printed heading numbers (`1. Brahmajālasuttaṃ`,
`(1) 1. Puggalavaggo`). Headings are not edition content on the library, only
table-of-contents titles, so every text already live needed its TOC replaced.

Tool: `library-upload` (installed from rails-template today; it replaces
`root-text-upload`, `commentary-upload`, `translation-upload`, `yigchung-upload`,
which were removed). Environment: **prod** (`library-prod.webuddhist.com`).

## Sent to prod — 15 of 16, each `ok` in `status` afterwards

| Text | What | New id |
|---|---|---|
| pi-dighanikaya | TOC replaced | toc `veWEbJjyVRHqoIU4ED4f0` |
| pi-majjhimanikaya | TOC replaced | toc `16zvk3mKzkPv3hD3UkhmM` |
| pi-samyuttanikaya | TOC replaced | toc `5DpaKibrLj4YvOzeFvI4t` |
| pi-anguttaranikaya | 1 in-place content patch (the space in `[[ ] etthantare`, as in the XML; fixed in a822251 after the upload), then TOC replaced | toc `3QDGynHYhWMMbhLRsVovA` |
| pi-khuddakanikaya | **first upload**: text, edition (5,861,595 chars, 23,140 segments), TOC | text `N6BiQbDleFKqVnDyH9KZW`, edition `PmMOLyVnfRWvMcjZK9bA1`, toc `oPwxjiXRTCnXZ1GtSTdxW` |
| pi-dighanikaya-atthakatha | TOC replaced | toc `1ehAGkTF09isQRToXN2Nh` |
| pi-dighanikaya-tiika | TOC replaced | toc `G3XZuGkM0BADsfNuCI2u6` |
| pi-dighanikaya-1-abhinavatiika | TOC replaced | toc `15RT79WbFB8dxq2fDPaxN` |
| pi-majjhimanikaya-atthakatha | TOC replaced | toc `YCxgMFlLCLAPLLq7n9SDc` |
| pi-majjhimanikaya-tiika | TOC replaced | toc `hyUG5TF4wmSJ6DB5mu7fF` |
| pi-samyuttanikaya-atthakatha | TOC replaced | toc `T4dQDUFPigDAII93UbyPG` |
| pi-anguttaranikaya-atthakatha | TOC replaced | toc `Z3xR8n6wUKBHKrNNQ4w26` |
| pi-anguttaranikaya-tiika | TOC replaced | toc `7QnIRd2dBRIhxR5ILB6Xd` |
| pi-samyuttanikaya-tiika | **re-segmented** (later the same day; `replace --dev`, the person confirmed they are a developer): segmentation deleted, content replaced (1,398,052 → 1,398,099 chars), 3,652 segments posted and read back, TOC re-synced; then its alignment to the SN root re-sent (5,609 pairs read back). Same ids for text and edition | toc `PIOYylxFp1dZpbjnpzmI9` |
| pi-khuddakanikaya-tiika | **first upload** (later the same day): text, edition (262,214 chars, 718 segments), TOC, alignment to the KN root (589 pairs) | text `NFPMtNVBndTKqpcUR1A3z`, edition `FGydrYE3tDdaJU27t3H4l`, toc `GywCVGQiLmtvwu95mUI5H` |

The TOC changes are the restored heading numbers, plus the TOC-structure fixes
committed on 2026-11-23 after the 2026-11-20 upload (1258207 DN/MN/SN, a822251 AN).
`toc_check.py` confirmed nothing else differed.

## Not sent

### pi-khuddakanikaya-atthakatha — held

Ready (dry run clean: 51,596 segments, 40,933 alignment pairs), but **not
uploaded**, by decision. (The KN ṭīkā, first skipped with it, was sent to
prod later the same day — see the table above; it is small.)

- They were to go to **dev first**. That needs the KN root on dev, and pushing
  it there failed half-way: the text was created (`BCugzNrcUr4zYeus4QO8j`), but
  the edition upload (13.9 MB payload) got **HTTP 504 Gateway Time-out** and
  never landed. The dev text has no edition, and it **cannot be deleted** —
  the delete times out too, while reads of it work and `/__/health` is fine
  (dev-70242a7). Likely a stuck write on the server; needs a backend developer.
- The KN aṭṭhakathā edition is 30.5 MB (17 M chars), more than twice the root
  that timed out on dev. A timeout on prod would leave a half-made text there
  that `library-upload` cannot remove (it never deletes texts).

- **testing** was tried next and failed the same way: the KN root's text was
  created (`XrgJ1v7nwrJhETWsQ8MUn`, testing `main-b4c3651`), the edition POST got
  a 504 after about 60 s, and no edition appeared afterwards. Harmless there:
  testing is replaced by its next refresh from prod. So dev and testing both
  cut an edition POST off at about 60 s, while prod accepted the same 13.9 MB
  edition; the aṭṭhakathā's is 30.5 MB.

To resume: a backend developer raises the edition-POST timeout on dev and
testing (nginx `proxy_read_timeout` or the backend's own limit), confirms what
prod allows, and clears `BCugzNrcUr4zYeus4QO8j` on dev (its id is in the dev
ledger). Then push the KN root and the aṭṭhakathā to testing, and the
aṭṭhakathā to prod.

### pi-samyuttanikaya-tiika — needed re-segmentation (done later the same day; see the table)

Commit 1258207 turned the subhead "Sāratthappakāsiniyā saṃyuttanikāya-aṭṭhakathāya"
into the first line of block `^5-574`. That inserts text on a segment boundary,
which cannot be patched in place: it needs `replace`, which `library-upload` runs
only with `--dev` (a person who says they are a developer), because it breaks the
ṭīkā's alignment with the SN root until `push --only alignment` is run. Until
then its TOC cannot be updated either (annotations are compared only when the
content matches). Prod is one fix behind the vault, otherwise correct.

## Changes needed so the vault's parsers build what prod holds

The live texts were uploaded with a parser bundled in the old `commentary-upload`
skill, which carried Sutta-specific rules the shared `4-SYSTEM/scripts/` parsers
lack. Without them, `status` reported re-segmentation for 9 texts. Restored:

- **Bold**: `**` is dropped from edition content in both parsers, as it already
  was from TOC titles (decided 2026-11-25: the library has no bold annotation
  yet; a bold annotation may come later).
- **Volume openings** (`^N-T1`, `^N-T2` in the merged commentaries) are never
  aligned and end the alignment scope (decided 2026-11-20).
- **Segment type**: the block ID decides; commentary blocks are paragraphs,
  gāthās included, as in vinaya-rails (decided 2026-11-20). The shared parser's
  "a multi-line block is a verse" rule is not used.
- The DN aṭṭhakathā's `[^ed-504]` note is now `[^f1]` (a footnote; definition
  at the end of the file). Prod has no footnote endpoint yet, so it is reported,
  not sent; dev and testing support footnotes.

The linters were brought in step with rails-template (new check: a heading must
be a block of its own).

## Incident

The first prod run passed `--report` before the note paths; `--report` takes an
optional file name, so the report was written over `1-SOURCES/Text/pi-dighanikaya.md`
and DN was not sent. The file had no uncommitted changes; it was restored from
git (same blob hash, LF), and DN's TOC was sent on its own. Use `--report` last,
or not at all.

## Scripts here

- `diff_probe.py`, `comm_probe.py` — read-only: segment and alignment differences, live vs built
- `toc_check.py` — read-only: TOC differences are only restored heading numbers?
- `bold_count.py` — read-only: `**` in live vs built content
- `run_lint_parse.py` — the vault's linter + parser on all 16 files (notes restored afterwards)
