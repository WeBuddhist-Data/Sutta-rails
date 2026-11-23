"""KN aṭṭhakathās: TOC fixes (heading lines only).

pi-kn-1-atthakatha: `Nigamanakathā` (the work's colophon) leaves the Mettasuttavaṇṇanā
  (`#### ^1-9-13-0`) and becomes the book's last section.
pi-kn-2-atthakatha:
  - the front matter `Ganthārambhakathā` takes the Roman front-matter ID (`^2-I-0`, as in
    the Khuddakapāṭha aṭṭhakathā and the other commentaries), so the 26 vaggas take the
    root's numbers again (`^2-1-0` Yamakavaggo … `^2-26-0`), not one more;
  - `Nigamanakathā` leaves the Brāhmaṇavagga (`#### ^2-27-41-0`, after the last story)
    and becomes the book's last section.
Both XML files have no divs; the Nigamana closes the whole work, as in the other files.

usage: python fix_kn_comm.py <file.md> [--write]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from heading_tree import Tree

T = Tree(sys.argv[1])
book_id = "1-0" if "kn-1" in sys.argv[1] else "2-0"
book = T.by_id(book_id)
if book_id == "2-0":
    front = book.kids[0]
    assert front.title == "Ganthārambhakathā" and front.id == "2-1-0", (front.title, front.id)
    front.id = "2-I-0"            # renumber() keeps a non-numeric slot
    for n in T.nodes:             # its sub-headings, if any, follow the new slot
        if n is not front and n.id.startswith("2-1-") and n.line < book.kids[1].line:
            n.id = "2-I-" + n.id[len("2-1-"):]
nig = [n for n in T.nodes if n.title == "Nigamanakathā"]
assert len(nig) == 1 and not nig[0].kids and nig[0].parent is not book
nig[0].move_to(book)
changes = T.apply(book)
if "--write" in sys.argv:
    open(T.path, "wb").write(T.nl.join(T.L).encode("utf-8"))
print(f"heading lines changed: {len(changes)}; non-heading lines unchanged: True")
for ln, old, new in changes[:6] + ([("…", "", "")] if len(changes) > 8 else []) + changes[-2:]:
    print(f"  line {ln}: {old.strip()}  ->  {new}")
print("written" if "--write" in sys.argv else "dry run; pass --write to save")
