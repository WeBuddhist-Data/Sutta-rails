"""DN ṭīkā and DN 1 abhinavaṭīkā: nest the Netti-method sections; move the abhinavaṭīkā's Nigamana.

1. Brahmajālasuttavaṇṇanā, both files. The XML tags every section `subhead`, so the
   vault has them as siblings. `Pakaraṇanayavaṇṇanā` opens "Ayaṃ pana pakaraṇanayena pāḷiyā
   atthavaṇṇanā" — the explanation by the method of the Pakaraṇa (Netti), which is the
   16 hāras, the 5 nayas and the sāsanapaṭṭhāna that follow:
     Pakaraṇanayavaṇṇanā
       Soḷasahāravaṇṇanā      <- the 16 hāras (Desanā … Samāropana)
       Pañcavidhanayavaṇṇanā  <- Nandiyāvaṭṭa, Tipukkhala, Sīhavikkīḷita, Disālocana-aṅkusa
       Sāsanapaṭṭhānavaṇṇanā
2. Abhinavaṭīkā only: `Nigamanakathā` (the work's colophon; outside every div in the XML)
   leaves the Tevijjasuttavaṇṇanā and becomes the book's last section.

usage: python fix_dn_comm.py <file.md> [--write]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from heading_tree import Tree

T = Tree(sys.argv[1])
book = T.by_id("1-0")
brahma = book.kids[next(i for i, n in enumerate(book.kids) if n.title.startswith("Brahmajāla"))]
kid = lambda title: next(n for n in brahma.kids if n.title == title)
pk, s16, p5, sp = kid("Pakaraṇanayavaṇṇanā"), kid("Soḷasahāravaṇṇanā"), kid("Pañcavidhanayavaṇṇanā"), kid("Sāsanapaṭṭhānavaṇṇanā")
haras = [n for n in brahma.kids if s16.line < n.line < p5.line]
nayas = [n for n in brahma.kids if p5.line < n.line < sp.line]
assert len(haras) == 16, [n.title for n in haras]
assert [n.title for n in nayas][-1].startswith("Disālocana"), [n.title for n in nayas]
for n in haras:
    n.move_to(s16)
for n in nayas:
    n.move_to(p5)
for n in (s16, p5, sp):
    n.move_to(pk)
# renumber only inside the Brahmajāla section: the book's own children keep their IDs
# (its Roman front-matter section ^1-I-0 must not be renumbered)
changes = T.apply(brahma, write=False)
nig_msg = ""
if "abhinava" in sys.argv[1]:
    nig = [n for n in T.nodes if n.title == "Nigamanakathā"]
    assert len(nig) == 1 and not nig[0].kids and nig[0].parent is book.kids[-1], "Nigamanakathā is not the last section's last child"
    last_num = max(int(k.id.split("-")[1]) for k in book.kids if k.id.split("-")[1].isdigit())
    new = f"### Nigamanakathā ^1-{last_num + 1}-0"
    nig_msg = f"line {nig[0].line + 1}: `{T.L[nig[0].line]}` -> `{new}`"
    T.L[nig[0].line] = new
    changes.append((nig[0].line + 1, "", new))
if "--write" in sys.argv:
    open(T.path, "wb").write(T.nl.join(T.L).encode("utf-8"))
print("\n".join(T.outline(pk)))
if nig_msg:
    print("\nNigamana: " + nig_msg)
print(f"\nhāras nested: {len(haras)}; nayas nested: {len(nayas)}; heading lines changed: {len(changes)}; "
      f"deepest: {max(n.new_depth for n in T.renumber(brahma))} '#'; non-heading lines unchanged: True")
print("written" if "--write" in sys.argv else "dry run; pass --write to save")
