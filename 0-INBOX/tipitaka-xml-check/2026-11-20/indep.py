"""Independent check (uses no vault code). For each 1-SOURCES file:
  - words: the sequence of letter-words in the md body equals the XML's
    (whole file, or the nipāta's <div type="book"> for AN commentaries).
    The AN volume's opening homage / closing colophon sit outside the book
    divs; they are added to the first / last nipāta as the vault files do.
  - spacing: "word ," (space before punctuation) count in md vs XML text.
  - block IDs unique; every transclusion resolves to an existing block.
  - frontmatter: root_text / commentary paths exist; commentary_of and
    aligned_to_edition_id equal the root's text_id / edition_id.
Usage: python3 -I indep.py <vault> <xmldir>"""
import re, sys, glob, os, unicodedata
import xml.etree.ElementTree as ET

vault, xdir = sys.argv[1], sys.argv[2]
WORD = re.compile(r"[^\W\d_]+", re.U)
SPACEPUNCT = re.compile(r"[^\W\d_\s]\s+[,.;:?!]")
EDNOTE = re.compile(r"\[Ed:[^\]]*\]")
AN_VOL = {1: 1, 2: 1, 3: 2, 4: 3, 5: 1, 6: 2, 7: 3, 8: 1, 9: 2, 10: 3, 11: 4}   # book index within volume
AN_LAST = {4, 7, 11}                                                            # last nipāta of its volume


def words(s):
    return WORD.findall(unicodedata.normalize("NFC", s).lower())


def text_of(e, out):
    if e.tag == "pb":
        if e.tail: out.append(e.tail)
        return
    if e.text: out.append(e.text)
    for c in e: text_of(c, out)
    out.append(" ")
    if e.tail: out.append(e.tail)


def xml_text(paths, book=None, first=False, last=False):
    out = []
    for p in paths:
        raw = open(p, "rb").read().decode("utf-16").replace('encoding="UTF-16"', "")
        body = ET.fromstring(raw).find(".//body")
        if book is None:
            text_of(body, out); continue
        kids = list(body)
        divs = [k for k in kids if k.tag == "div" and k.get("type") == "book"]
        d = divs[book - 1]; i = kids.index(d)
        if first:
            if body.text: out.append(body.text)
            for k in kids[:i]: text_of(k, out)
        if d.text: out.append(d.text)
        for c in d: text_of(c, out)
        if last:
            if d.tail: out.append(d.tail)
            for k in kids[i + 1:]: text_of(k, out)
    return " ".join(out)


def split(path):
    fm, body = open(path, encoding="utf-8").read().split("\n---\n", 1)
    return fm, body


def fmval(fm, key):
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return m.group(1).strip().strip('"') if m else None


files = sorted(glob.glob(f"{vault}/1-SOURCES/Text/*.md")) + sorted(glob.glob(f"{vault}/1-SOURCES/Commentaries/*.md"))
ids_by_file = {os.path.relpath(f, vault): re.findall(r"\s\^([\w-]+)\s*$", split(f)[1], re.M) for f in files}
ok = 0
for f in files:
    name = os.path.basename(f)[:-3]
    fm, body = split(f)
    srcs = [s.strip() for s in fmval(fm, "source_filename").strip("[]").split(",")]
    book = first = last = None
    m = re.match(r"pi-an-(\d+)-(atthakatha|tiika)$", name)
    if m:
        n = int(m.group(1)); book = AN_VOL[n]; first = book == 1; last = n in AN_LAST
    xt = xml_text([f"{xdir}/{s}" for s in srcs], book, first, last)
    lines = []
    for ln in body.split("\n"):
        if ln.startswith("![["): continue
        if re.match(r"^\[\^[\w-]+\]:", ln): continue
        ln = EDNOTE.sub("", re.sub(r"\[\^[\w-]+\]", "", ln))
        ln = re.sub(r"\s\^[\w-]+\s*$", "", ln)
        if ln.startswith("# "): ln = re.sub(r"\s*\((aṭṭhakathā|ṭīkā|abhinavaṭīkā)\)\s*$", "", ln)
        lines.append(ln)
    mdtext = "\n".join(lines)
    mw, xw = words(mdtext), words(xt)
    probs = []
    if mw != xw:
        i = next((k for k in range(min(len(mw), len(xw))) if mw[k] != xw[k]), min(len(mw), len(xw)))
        probs.append(f"words differ at #{i} (md {len(mw)} / xml {len(xw)}): md {' '.join(mw[max(0,i-4):i+6])!r} | xml {' '.join(xw[max(0,i-4):i+6])!r}")
    sp_md = len(SPACEPUNCT.findall(mdtext))
    sp_x = len(SPACEPUNCT.findall(re.sub(r"\s+", " ", xt.replace("‘‘", '"').replace("’’", '"'))))
    if sp_md > sp_x: probs.append(f"space-before-punctuation md {sp_md} > xml {sp_x}")
    ids = ids_by_file[os.path.relpath(f, vault)]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup: probs.append(f"duplicate IDs: {dup[:5]}")
    bad = [f"{t}#^{b}" for t, b in re.findall(r"!\[\[([^#\]]+)#\^([\w-]+)\]\]", body)
           if t not in ids_by_file or b not in ids_by_file[t]]
    if bad: probs.append(f"{len(bad)} broken transclusions: {bad[:3]}")
    rt = fmval(fm, "root_text")
    if rt:
        if not os.path.exists(f"{vault}/{rt}"): probs.append(f"root_text missing: {rt}")
        else:
            rfm, _ = split(f"{vault}/{rt}")
            if fmval(fm, "commentary_of") != fmval(rfm, "text_id"): probs.append("commentary_of != root text_id")
            if fmval(fm, "aligned_to_edition_id") != fmval(rfm, "edition_id"): probs.append("aligned_to_edition_id != root edition_id")
    cm = fmval(fm, "commentary")
    if cm and not os.path.exists(f"{vault}/{cm}"): probs.append(f"commentary missing: {cm}")
    nlinks = len(re.findall(r"^!\[\[", body, re.M))
    ok += not probs
    print(f"{name:26s} words {len(mw):7d} ids {len(ids):5d} links {nlinks:5d} space-punct {sp_md:3d}  " + ("OK" if not probs else "PROBLEM: " + " ; ".join(probs)))
print(f"TOTAL {len(files)} files, {ok} OK")
