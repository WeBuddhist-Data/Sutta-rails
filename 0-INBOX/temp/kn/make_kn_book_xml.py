"""Cut / join CSCD volumes into one XML per tipitaka.app book, where the two differ.

  apadana  s0510m1 = Therāpadāna part 1 (vaggas 1-42); s0510m2 = Therāpadāna part 2 (vaggas
           43-56), then the Therīapadāna in a second <div type="book">. Writes
           s0510thera.xml (m1 + m2's Thera part) and s0510theri.xml (the rest of m2).
  jataka   s0513m = Jātaka part 1 (nipātas 1-16), s0514m = part 2 (nipātas 17-22).
           Writes s0513jat.xml (both parts as one book).

A second volume's part is appended inside the first volume's book <div>. Its printed opening
(homage, "Khuddakanikāye", the book title, "(Dutiyo bhāgo)") is kept, in place, as plain
<p rend="centre"> text — tipitaka.app shows it the same way, inside the one book; only those
elements' rend/tag change. Every word and every other element is unchanged (asserted).

  milinda  s0518m.nrf restructured to the shape decided for the Milindapañha (see that branch).
           Writes s0518mil.xml.

usage: python make_kn_book_xml.py apadana|jataka|milinda   (from the vault root; writes 0-INBOX/temp/kn/xml/)
"""
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
R = Path("0-INBOX/raw-data/kn"); O = Path("0-INBOX/temp/kn/xml"); O.mkdir(parents=True, exist_ok=True)
BODY = '<body xml:space="preserve">'
words = lambda s: re.sub(r"<[^>]+>", " ", s).split()


def join_parts(m1, m2, part2_end, first_div):
    """m1's book with m2[body:part2_end] appended inside it. first_div: m2's first section <div."""
    m1_end = m1.rindex("</body>")
    m1_body = m1[:m1_end].rstrip()
    assert m1_body.endswith("</div>"), m1_body[-200:]
    m1_body = m1_body[: -len("</div>")]                      # reopen m1's book div
    body_open = m2.index(BODY) + len(BODY)
    part2 = m2[body_open:part2_end]
    k = part2.index(first_div)
    opening, rest = part2[:k], part2[k:]
    changed = []

    def as_text(m):
        changed.append(m.group(2).strip())
        return f'<p rend="centre">{m.group(2)}</p>'

    opening = re.sub(r'<(p|head) rend="(?:centre|nikaya|book|title)">([^<]*)</\1>', as_text, opening)
    opening = re.sub(r'<div id="[^"]+" n="[^"]+" type="book">', "", opening)
    rest = rest.rstrip()
    if rest.endswith("</div>") and part2_end == m2.index("</body>"):
        rest = rest[: -len("</div>")]                        # m2's own book div closes at the end
    else:
        # the book's </div> comes before some closing text outside it: keep that text inside
        close = rest.rindex("</div>", 0, rest.index("Ettāvatā"))
        rest = rest[:close] + rest[close + len("</div>"):]
    out = m1_body + "\n" + opening + rest.rstrip() + "\n</div>\n" + m2[m2.index("</body>"):]
    assert words(out) == words(m1[:m1_end]) + words(part2) + words(m2[m2.index("</body>"):]), "words changed"
    return out, changed


def read(stem):
    return (R / f"{stem}.mul.xml").read_text(encoding="utf-16")


which = sys.argv[1] if len(sys.argv) > 1 else ""
if which == "apadana":
    m1, m2 = read("s0510m1"), read("s0510m2")
    cut = m2.index('<div id="kn11"')
    theri = m2[: m2.index(BODY) + len(BODY)] + "\n" + m2[cut:]
    assert words(theri) == words(m2[: m2.index(BODY) + len(BODY)]) + words(m2[cut:])
    (O / "s0510theri.xml").write_text(theri, encoding="utf-16")
    thera, changed = join_parts(m1, m2, cut, '<div id="kn10_43"')
    (O / "s0510thera.xml").write_text(thera, encoding="utf-16")
    print("part-2 opening kept as text:", changed, "-> s0510thera.xml, s0510theri.xml")
elif which == "jataka":
    m1, m2 = read("s0513m"), read("s0514m")
    jat, changed = join_parts(m1, m2, m2.index("</body>"), '<div id="kn14_17"')
    (O / "s0513jat.xml").write_text(jat, encoding="utf-16")
    print("part-2 opening kept as text:", changed, "-> s0513jat.xml")
elif which == "milinda":
    # s0518m.nrf has no book heading: the work's title is chapter 1's head, and "1. Bāhirakathā"
    # (kaṇḍa 1 of the six the text itself lists: "chadhā vibhajitvā … pubbayogo milindapañhaṃ …")
    # is a subsubhead inside it. Human decisions 2026-11-24:
    #  - the title is the book head; the preface (¶1-2 and the six-part announcement) stays under it;
    #  - "1. Bāhirakathā" opens chapter 1 (sibling of "2-3. Milindapañho" … "6. Opammakathāpañho");
    #  - <p rend="nikaya">Mātikā</p> is a vagga-level title (as the Paṭisambhidāmagga's Mātikā);
    #  - <p rend="nikaya">Nigamanaṃ</p>, after the last kaṇḍa, opens its own chapter <div>.
    m = (R / "s0518m.nrf.xml").read_text(encoding="utf-16")
    old_open = re.search(r'<div id="kn18" n="kn18" type="book">\s*<div id="kn18_1" n="kn18_1" type="chapter">\s*'
                         r'<head rend="chapter">Milindapañhapāḷi</head>', m)
    bah = '<p rend="subsubhead">1. Bāhirakathā</p>'
    assert old_open and m.count(bah) == 1
    s = m[: old_open.start()] + '<div id="kn18" n="kn18" type="book">\n<head rend="book">Milindapañhapāḷi</head>' \
        + m[old_open.end(): m.index(bah)] \
        + '<div id="kn18_1" n="kn18_1" type="chapter">\n<head rend="chapter">1. Bāhirakathā</head>' \
        + m[m.index(bah) + len(bah):]
    assert s.count('<p rend="nikaya">Mātikā</p>') == 1
    s = s.replace('<p rend="nikaya">Mātikā</p>', '<p rend="title">Mātikā</p>')
    nig = re.search(r'</div>\s*<p rend="nikaya">Nigamanaṃ</p>', s)
    assert nig
    s = s[: nig.start()] + '</div>\n<div id="kn18_6" n="kn18_6" type="chapter">\n<head rend="chapter">Nigamanaṃ</head>' \
        + s[nig.end():]
    end = '<trailer rend="centre">Milindapañho niṭṭhito.</trailer>'
    assert s.count(end) == 1
    s = s.replace(end, "</div>\n" + end)
    assert words(s) == words(m), "words changed"
    assert s.count("<div") == s.count("</div>"), "unbalanced divs"
    (O / "s0518mil.xml").write_text(s, encoding="utf-16")
    print("-> s0518mil.xml (title as book head, Bāhirakathā chapter 1, Mātikā title, Nigamanaṃ chapter)")
else:
    sys.exit(__doc__)
print("word streams identical to the sources")
