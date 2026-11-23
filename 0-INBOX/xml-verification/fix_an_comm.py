"""AN commentaries: TOC fixes (heading lines; heading IDs renumbered inside books 1, 10, 11 only).

Both files:
  B. Etadaggavagga (AN 1): each sub-vagga heading (Paṭhama- … Sattama-etadaggavagga…) holds
     its sections (Etadaggapadavaṇṇanā, the thera/therī vatthus); they were its siblings,
     leaving the sub-vagga headings empty. The repeated `14. Etadaggavaggo` (CSCD prints the
     vagga title again before each sub-vagga, rank `title`) stays the container of its
     sub-vagga, as in the aṭṭhakathā and on tipitaka.app.
  C. AN 10: `(21) Karajakāyavaggo` (and in the aṭṭhakathā `(22) Sāmaññavaggavaṇṇanā`) leave the
     4th paṇṇāsaka and stand beside the paṇṇāsakas, as in the XML's numbering and the root.
  D. AN 11: the Nigamana (XML: in book, after the vaggas) leaves the last vagga and becomes
     the book's last section.
ṭīkā only:
  A. AN 1, vaggas 14–20 (the XML has no divs there, only ranks): the 6 repeated
     `Etadaggavaggo` titles go under the first, as in the aṭṭhakathā; `15. Aṭṭhānapāḷi`
     (paṭhama-, dutiyavagga) and `16. Ekadhammapāḷi` leave the 7th Etadagga sub-vagga and
     become vaggas again; the 3 repeated `Ekadhammapāḷi` titles go under the first;
     vaggas 17–20 (Pasādakaradhamma-, Aparaaccharāsaṅghāta-, Kāyagatāsati-, Amatavagga)
     leave the last Ekadhammapāḷi repeat and become vaggas again.
aṭṭhakathā, only with --samkhepa:
  E. `### Rūpādivaggavaṇṇanā ^1-1-0` moves below the three blocks ^1-20–^1-22 (the summary of
     the Aṅguttara: 11 nipātas, 9,557 suttas, its first sutta), so the empty
     `Saṃkhepakathā` holds them. One heading line moves; no text moves.

usage: python fix_an_comm.py <file.md> [--samkhepa] [--write]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from heading_tree import Tree, HEAD

path = sys.argv[1]
tika = "tiika" in path
raw0 = open(path, "rb").read().decode("utf-8")

if "--samkhepa" in sys.argv and not tika:          # E: a line move, done before the tree is read
    nl = "\r\n" if "\r\n" in raw0 else "\n"
    L = raw0.split(nl)
    i = L.index("### Rūpādivaggavaṇṇanā ^1-1-0")
    j = L.index("#### Nidānavaṇṇanā ^1-1-1-0")
    assert L[i + 1] == "" and j > i and all(not HEAD.match(l) for l in L[i + 1:j]), "unexpected layout"
    L = L[:i] + L[i + 2:j] + ["### Rūpādivaggavaṇṇanā ^1-1-0", ""] + L[j:]
    tmp = path + ".samkhepa.tmp"
    open(tmp, "wb").write(nl.join(L).encode("utf-8"))
    T = Tree(tmp); os.remove(tmp); T.path = path   # the final check below compares text lines with the original
else:
    T = Tree(path)

kid = lambda parent, title: next(n for n in parent.kids if n.title == title)
b1, b10, b11 = T.by_id("1-0"), T.by_id("10-0"), T.by_id("11-0")

if tika:
    # A
    reps = [T.by_id(f"1-{k}-0") for k in range(11, 18)]
    assert all(r.title == "Etadaggavaggo" for r in reps), [r.title for r in reps]
    e1, e7 = reps[0], reps[-1]
    a1, a2 = kid(e7, "Aṭṭhānapāḷi (paṭhamavagga)"), kid(e7, "Aṭṭhānapāḷi (dutiyavagga)")
    ek = kid(e7, "Ekadhammapāḷi")
    for n in (a1, a2, ek):
        n.move_to(b1)
    ekreps = [T.by_id(f"1-{k}-0") for k in (18, 19, 20)]
    assert all(r.title == "Ekadhammapāḷi" for r in ekreps)
    late = [n for n in ekreps[-1].kids if n.title.endswith("vaggavaṇṇanā") and not n.title.startswith("Ekadhamma")]
    assert [n.title for n in late] == ["Pasādakaradhammavaggavaṇṇanā", "Aparaaccharāsaṅghātavaggavaṇṇanā",
                                       "Kāyagatāsativaggavaṇṇanā", "Amatavaggavaṇṇanā"], [n.title for n in late]
    for n in late:
        n.move_to(b1)
    for r in reps[1:]:
        r.move_to(e1)
    for r in ekreps:
        r.move_to(ek)
    etadagga = e1
else:
    etadagga = T.by_id("1-14-0")

# B — sub-vaggas hold their sections
first = etadagga.kids[0]
assert first.title.startswith("Paṭhamaetadagga"), first.title
repeats = [n for n in etadagga.kids if n.title == "Etadaggavaggo"]
for n in [n for n in etadagga.kids if first.line < n.line < repeats[0].line]:
    n.move_to(first)
for r in repeats:
    sub = r.kids[0]
    assert "etadaggavagg" in sub.title, sub.title
    for n in r.kids[1:]:
        n.move_to(sub)

# C — AN 10
p4 = kid(b10, "Catutthapaṇṇāsakaṃ")
for t in ("Karajakāyavaggo", "Sāmaññavaggavaṇṇanā"):
    if any(n.title == t for n in p4.kids):
        kid(p4, t).move_to(b10)

# D — AN 11 Nigamana
nig = [n for n in T.nodes if n.title.startswith("Nigamanakathā") and n.id.startswith("11-")]
assert len(nig) == 1 and not nig[0].kids
nig[0].move_to(b11)

changes = []
for r in (b1, b10, b11):
    changes += T.apply(r)
if "--samkhepa" in sys.argv and not tika:
    changes.append((None, "### Rūpādivaggavaṇṇanā ^1-1-0", "moved below ^1-20–^1-22"))
body = lambda s: [l for l in s.split(T.nl) if not HEAD.match(l)]
assert sorted(body(raw0)) == sorted(l for l in T.L if not HEAD.match(l)), "text lines changed"
if "--write" in sys.argv:
    open(path, "wb").write(T.nl.join(T.L).encode("utf-8"))
print(f"heading lines changed: {len(changes)}; deepest: {max(n.new_depth for r in (b1, b10, b11) for n in T.renumber(r))} '#'; "
      "text lines unchanged (same lines; with --samkhepa one heading moved past 3 blocks)")
print("written" if "--write" in sys.argv else "dry run; pass --write to save")
