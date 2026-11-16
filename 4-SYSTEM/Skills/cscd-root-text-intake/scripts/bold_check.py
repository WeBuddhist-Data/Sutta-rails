"""bold_check.py — shared by the cscd-root-text-intake and cscd-commentary-intake
verifiers. The converter writes CSCD's <hi rend="bold"> as **…** exactly where
the XML's tags are (spaces and punctuation inside a tag stay inside). These
helpers let a verifier

  * strip the markers before comparing word streams (strip_bold);
  * compare the bold spans with the XML exactly, in order (xml_spans/md_spans
    with exact=True: only runs of whitespace are collapsed, as the converter
    does);
  * compare them with tipitaka.app's text (site_spans) by their core — edge
    spaces and punctuation trimmed — because the site drops whitespace-only
    bold and joins some neighbouring spans (see compare()).

Not run on its own.
"""
import re
import unicodedata

# ".*?", not ".+?": an empty XML tag <hi rend="bold"></hi> is copied as "****"
# (CSCD SN s0301a) and must be counted as a span like any other.
BOLD_RE = re.compile(r"\*\*(.*?)\*\*")


def strip_bold(s):
    # A space inside a bold tag next to one outside it ("passatā. ** Sabba")
    # leaves two spaces once the markers go; collapse them for text compares.
    return re.sub(r"(?<=\S)  +(?=\S)", " ", s.replace("**", ""))


def norm(s):
    s = s.replace("‘‘", '"').replace("’’", '"')
    s = re.sub(r"\s+", " ", s)
    return re.sub(r"\s+\]", "]", re.sub(r"\[\s+", "[", s))


def core(s):
    s = norm(s)
    k, m = 0, len(s)
    edge = lambda c: c.isspace() or unicodedata.category(c)[0] in "PS"
    while k < m and edge(s[k]):
        k += 1
    while m > k and edge(s[m - 1]):
        m -= 1
    return s[k:m]


def md_spans(lines, exact=False):
    """Bold spans in md lines, in order (exact text, or cores with empty ones
    left out), plus lines whose ** do not pair up."""
    spans, unpaired = [], []
    for ln in lines:
        if ln.count("**") % 2:
            unpaired.append(ln[:70])
        spans += [m.group(1) if exact else core(m.group(1)) for m in BOLD_RE.finditer(ln)]
    return (spans if exact else [s for s in spans if s]), unpaired


def _render(el, out):
    if el.tag == "pb":
        pass
    elif el.tag == "note":
        out.append(" [" + "".join(el.itertext()).strip() + "]")
    else:
        if el.text:
            out.append(el.text)
        for c in el:
            _render(c, out)
            if c.tail:
                out.append(c.tail)


def xml_spans(bodies, exact=False):
    """Every <hi rend="bold"> in the given ElementTree <body>s, in document
    order: its exact text (notes as " [x]", page markers dropped, quotes and
    whitespace normalised as the converter does), or its core with empty ones
    left out."""
    spans = []
    for body in bodies:
        for h in body.iter("hi"):
            if h.get("rend") == "bold":
                buf = []
                _render(h, buf)
                spans.append(norm("".join(buf)))
    return spans if exact else [c for c in (core(x) for x in spans) if c]


def site_spans(paras):
    """Bold cores in tipitaka.app /api/text paragraphs (site writes **…**)."""
    spans = []
    for p in paras:
        t = re.sub(r"\s*\|[A-Z]\d+\.\d+\|\s*", " ", p.get("t", ""))
        t = re.sub(r"\s+([,.;:?!])", r"\1", t)     # page marker before punctuation
        t = t.replace("{", "[").replace("}", "]")
        spans += [core(m.group(1)) for m in BOLD_RE.finditer(t)]
    return [s for s in spans if s]


def _squash(spans):
    return re.sub(r"[\s\W]", "", "".join(spans))


def compare(ref, md, ref_name, site_merges=None):
    """Problems (list of str) when the md bold cores differ from the reference.

    site_merges: pass a list when ref is tipitaka.app. The site joins bold spans
    that the XML separates by a space or punctuation, often dropping the space
    (XML '<hi>Āyasmato</hi> <hi>mahākassapassa</hi>' -> site
    '**Āyasmatomahākassapassa**'). Such a difference, where the site's spans
    hold exactly the md's spans' letters, is appended to the list instead of
    being reported as a problem."""
    if ref == md:
        return []
    import difflib
    sm = difflib.SequenceMatcher(a=ref, b=md, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    if site_merges is not None:
        rest = []
        for o in ops:
            tag, a0, a1, b0, b1 = o
            if tag == "replace" and a1 - a0 < b1 - b0 and _squash(ref[a0:a1]) == _squash(md[b0:b1]):
                site_merges.append((ref[a0:a1], md[b0:b1]))
            else:
                rest.append(o)
        ops = rest
        if not ops:
            return []
    out = [f"bold spans differ from {ref_name} in {len(ops)} place(s) ({ref_name} {len(ref)}, md {len(md)})"]
    for tag, a0, a1, b0, b1 in ops[:8]:
        out.append(f"   {tag}: {ref_name} {ref[a0:a1][:3]} | md {md[b0:b1][:3]}")
    return out
