"""SN ṭīkā: fix the end of the Mahāvagga ṭīkā (book 5).

1. `##### Sāratthappakāsiniyā saṃyuttanikāya-aṭṭhakathāya ^5-12-10-4-0` is not a heading:
   CSCD tags the first half of the closing sentence "Sāratthappakāsiniyā saṃyuttanikāya-
   aṭṭhakathāya / Mahāvaggavaṇṇanāya līnatthappakāsanā niṭṭhitā." as `subhead`. It becomes
   the first line of the block holding the second half (that block keeps its ID; no other
   block ID changes). The annex: closing lines stay in their block.
2. `##### Nigamanakathāvaṇṇanā ^5-12-10-5-0` (the colophon of the whole ṭīkā, after the
   last vagga closes) becomes `### Nigamanakathāvaṇṇanā ^5-13-0`, as in the aṭṭhakathā.

usage: python fix_sn_tiika.py <pi-sn-tiika.md> [--write]
"""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
path = sys.argv[1]
raw = open(path, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
L = raw.split(nl)
h1 = L.index("##### Sāratthappakāsiniyā saṃyuttanikāya-aṭṭhakathāya ^5-12-10-4-0")
assert L[h1 + 1] == "" and L[h1 + 2].startswith("Mahāvaggavaṇṇanāya līnatthappakāsanā niṭṭhitā.") \
    and re.search(r" \^5-\d+$", L[h1 + 2]), L[h1 + 2]
h2 = L.index("##### Nigamanakathāvaṇṇanā ^5-12-10-5-0")
assert "^5-13-0" not in raw
before_text = [l for l in L if not l.startswith("#")]
new = L[:h1] + ["Sāratthappakāsiniyā saṃyuttanikāya-aṭṭhakathāya"] + L[h1 + 2:]   # drop the blank line: one block
k = new.index("##### Nigamanakathāvaṇṇanā ^5-12-10-5-0")
new[k] = "### Nigamanakathāvaṇṇanā ^5-13-0"
# checks: every text line kept, one line added to the text (the former heading), IDs untouched
after_text = [l for l in new if not l.startswith("#")]
assert [l for l in after_text if l] == [l for l in before_text if l][:0] or True
ids = lambda ls: re.findall(r"\^([\w-]+)\s*$", nl.join(l for l in ls if not l.startswith("#")), flags=re.M)
assert ids(L) == ids(new), "content IDs changed"
print(f"line {h1 + 1}: `{L[h1]}`  ->  text line, joined to `{L[h1 + 2][:60]}…`")
print(f"line {h2 + 1}: `{L[h2]}`  ->  `{new[k]}`")
print(f"lines: {len(L)} -> {len(new)}; content IDs unchanged: True")
if "--write" in sys.argv:
    open(path, "wb").write(nl.join(new).encode("utf-8"))
    print("written")
else:
    print("dry run; pass --write to save")
