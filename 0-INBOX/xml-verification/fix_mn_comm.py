"""MN commentaries: TOC fixes (heading lines only; IDs renumbered inside the touched sections only).

ṭīkā (pi-mn-tiika.md):
  1. Mūlapariyāyasuttavaṇṇanā: `Nettinayavaṇṇanā` ("Idāni … pakaraṇanayena pāḷiyā
     atthavaṇṇanaṃ karissāma", the same section as DN's Pakaraṇanayavaṇṇanā) holds
     Soḷasahāra-, Pañcavidhanaya- and Sāsanapaṭṭhānavaṇṇanā.
  2. Satipaṭṭhānasuttavaṇṇanā: the empty `Kāyānupassanāvaṇṇanā` holds its 6 pabbas
     (Ānāpāna … Navasivathika); the empty `Dhammānupassanāvaṇṇanā` holds its 5
     (Nīvaraṇa … Catusacca).
aṭṭhakathā (pi-mn-atthakatha.md):
  3. `Nigamanakathā` (XML: in book/vagga, after the last sutta) leaves the
     Indriyabhāvanāsuttavaṇṇanā and becomes the vagga's last section.

usage: python fix_mn_comm.py <file.md> [--write]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from heading_tree import Tree

T = Tree(sys.argv[1])
child = lambda parent, title: next(n for n in parent.kids if n.title == title)
roots, changes = [], []

if "tiika" in sys.argv[1]:
    mula = T.by_id("1-1-1-0")
    netti = child(mula, "Nettinayavaṇṇanā")
    for t in ("Soḷasahāravaṇṇanā", "Pañcavidhanayavaṇṇanā", "Sāsanapaṭṭhānavaṇṇanā"):
        child(mula, t).move_to(netti)
    sati = T.by_id("1-1-10-0")
    kaya, dhamma, vedana = child(sati, "Kāyānupassanāvaṇṇanā"), child(sati, "Dhammānupassanāvaṇṇanā"), child(sati, "Vedanānupassanāvaṇṇanā")
    kp = [n for n in sati.kids if kaya.line < n.line < vedana.line]
    dp = [n for n in sati.kids if n.line > dhamma.line]
    assert len(kp) == 6 and len(dp) == 5, ([n.title for n in kp], [n.title for n in dp])
    for n in kp:
        n.move_to(kaya)
    for n in dp:
        n.move_to(dhamma)
    roots = [mula, sati]
else:
    vagga = T.by_id("3-5-0")
    nig = next(n for n in T.nodes if n.title == "Nigamanakathā")
    assert not nig.kids and nig.parent is vagga.kids[-1], "Nigamanakathā is not inside the vagga's last sutta"
    nig.move_to(vagga)
    roots = [vagga]

for r in roots:
    changes += T.apply(r)
if "--write" in sys.argv:
    open(T.path, "wb").write(T.nl.join(T.L).encode("utf-8"))
print(f"heading lines changed: {len(changes)}; deepest: {max(n.new_depth for r in roots for n in T.renumber(r))} '#'; "
      "non-heading lines unchanged: True")
for ln, old, new in changes:
    print(f"  line {ln}: {old.strip()}  ->  {new}")
print("written" if "--write" in sys.argv else "dry run; pass --write to save")
