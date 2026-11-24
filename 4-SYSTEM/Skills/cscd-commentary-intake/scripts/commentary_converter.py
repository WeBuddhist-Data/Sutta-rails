#!/usr/bin/env python3
"""
commentary_converter.py — step 4 of cscd-commentary-intake.

Turn the segment JSON of one CSCD commentary work (aṭṭhakathā / ṭīkā / …) into
a Markdown commentary draft:

  Namo tassa …                               <- homage (^T-1 after IDs)
  # <nikāya> (<layer label>) ^…              <- h1, e.g. "Dīghanikāye (aṭṭhakathā)"
  ## <book title> ^<book>-0                  <- h2
  ### <chapter> ^…                           <- h3, one per source chapter
  #### / ##### <sub-section> ^…              <- h4 / h5

  ![[<root_text>#^<book>-<N>]]              <- link to each root paragraph cited
  <N>. <commentary paragraph> ^<book>-<k>    <- one block per source paragraph

Heading and content IDs written here are provisional: apply_commentary_ids.py
strips and reassigns all of them (step 5).

ROOT LINKS
==========
A commentary paragraph that opens with a printed number or range ("149.",
"32-33.") cites those root paragraphs. One transclusion per cited paragraph is
written before it, and the printed number stays in the text (KEEP_REF_NUMBER).
CSCD's truncated-tail ranges ("65-6." = 65–66) are expanded for linking only
and logged in ABBREVIATED. With ROOT_IDS set, only block IDs that exist in the
root file are linked; anything else is logged in UNRESOLVED, as is a paragraph
that opens with a number-like prefix the citation pattern cannot read
(e.g. "292-3-6."). Nothing unresolved is silently dropped.

SUTTAS IN VAGGAS (Majjhimanikāya)
=================================
Where a sutta is a numbered subhead inside a vagga <div>, cscd_xml_to_json.py
types its heading "sutta". Such a chapter is emitted as
  ### <vagga>  >  #### <sutta>  >  ##### <subhead / subsubhead / title>
and a numbered subhead directly after a "title" (a ṭīkā's own list, e.g. the
16 hāras under Soḷasahāravaṇṇanā) is a ###### under that title, until the
next unnumbered heading or sutta. Chapters without "sutta" headings
(Dīghanikāya) are emitted exactly as before.

SECTIONS WITHOUT ROOT LINKS
===========================
UNLINKED_HEADINGS (set by the build script from --unlinked, a human decision):
in the text directly under one of these headings (up to the next heading), a
leading number is the section's own numbering, not a citation — e.g. the
Mūlapaṇṇāsa-ṭīkā numbers its Ganthārambhakathāvaṇṇanā paragraphs 1.–16.
Nothing there is linked; each number is logged in UNLINKED for the report.

GĀTHĀ
=====
gatha1 / gatha2 / gatha3 lines accumulate until gathalast; the stanza is one block.

Configuration is set by the build script (build_commentary.py) on the module:
ROOT_TEXT_PATH, BOOK_ID, ROOT_IDS, LAYER_DISPLAY_MAP.
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIGURATION — set by the build script
# ---------------------------------------------------------------------------

# Vault-relative path of the root text the commentary links to.
ROOT_TEXT_PATH = "1-SOURCES/Text/pi-dn-1.md"

# The <book> segment of every ID (the root volume's book number).
BOOK_ID = 1

# Keep the printed citation number ("12. …") at the start of the paragraph.
KEEP_REF_NUMBER = True

# For a chapter with no chapter-class segment, take the h3 title from the
# first heading in document order.
H3_FIRST_HEADING = True

# Set of root-text block IDs (without "^"). When set, transclusions are
# emitted only for IDs in it; unresolved citations go to UNRESOLVED.
ROOT_IDS: set[str] | None = None
UNRESOLVED: list[tuple[str, list[str], str]] = []
# Headings whose own text carries section numbering, not root citations, and
# the numbers found there: (as printed, heading, paragraph start).
UNLINKED_HEADINGS: set[str] = set()
UNLINKED: list[tuple[str, str, str]] = []
UNLINKED_MATCHED: set[str] = set()
# A root that numbers each section from 1 (CSCD Khuddakapāṭha) has IDs
# ^<book>-<section>-<N>; a citation N links within the commentary's current
# section, the printed number of its last level-3 heading (tree mode only).
PER_SECTION = False
# Per-section: the section for citations that come before the first numbered '###' (in front
# matter), set by build_commentary.py --presection when the text quotes those root verses
# (Cariyāpiṭaka-aṭṭhakathā Nidānakathā: "1. … 'kappe ca satasahasse'…" = root ^13-1-1).
PRESECTION = None
SEEN_SECTION = [False]
# A zoned root (^<book>-<zone>-<N>, CSCD Suttanipāta): a zone_link.ZoneLinker set by
# build_commentary.py --zones; a citation links to the zone zone_link.py picks (tree mode only).
ZONE_LINKER = None
# Truncated-tail ranges expanded for linking: (as printed, start, end).
ABBREVIATED: list[tuple[str, int, int]] = []

# Layer "layer" field -> h1 anchor slug (provisional; IDs are reassigned)
LAYER_SLUG_MAP = {
    "atthakatha": "atthakatha",
    "tika":       "tika",
    "other":      "tika",
}

# Layer display label in the h1 heading. The build script overrides "other"
# per work (e.g. "abhinavaṭīkā").
LAYER_DISPLAY_MAP = {
    "atthakatha": "aṭṭhakathā",
    "tika":       "ṭīkā",
    "other":      "ṭīkā",
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

_leading_num_re   = re.compile(r"^\s*\d+(?:-\d+)*\.\s*")   # heading numbers: "1. ", "1-10. ", "4-5-6. "
_verse_ref_re     = re.compile(r"^\s*(\d+)(?:-(\d+))?\.(?:\s|$)")
_leading_strip_re = re.compile(r"^\s*\d+(?:-\d+)?\.\s*")
_numberlike_re    = re.compile(r"^\s*\d+(?:-\d+)+\.")


def strip_leading_number(text: str) -> str:
    return _leading_num_re.sub("", text).strip()


def clean_text(s: str) -> str:
    return s.strip()


def format_frontmatter(meta: dict) -> str:
    lines = ["---"]
    for k, v in meta.items():
        if v is None:
            continue
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            val = str(v)
            if any(c in val for c in (":", "#", "[", "]", "'")):
                lines.append(f'{k}: "{val}"')
            else:
                lines.append(f"{k}: {val}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def resolve_root_text_ids(book_id: int, context: str,
                          n_start: int, n_end: int) -> list[str]:
    """Return root-text block IDs for printed paragraph numbers n_start..n_end."""
    if context != "main":
        return []
    return [f"{book_id}-{n}" for n in range(n_start, n_end + 1)]


def covering_blocks(root_ids: set[str], book_id: int, n_start: int, n_end: int):
    """Root blocks that hold the printed paragraph numbers n_start..n_end, in
    order, each once, and the numbers no block holds. A root block is ^b-N or a
    printed range ^b-A-B (CSCD Saṃyuttanikāya), which holds A..B."""
    cover = {}
    for rid in root_ids:
        m = re.fullmatch(rf"{book_id}-(\d+)(?:-(\d+))?", rid)
        if m:
            a = int(m.group(1)); b = int(m.group(2) or a)
            for k in range(a, b + 1):
                cover.setdefault(k, rid)
    found, missing = [], []
    for k in range(n_start, n_end + 1):
        rid = cover.get(k)
        if rid is None:
            missing.append(f"{book_id}-{k}")
        elif rid not in found:
            found.append(rid)
    return found, missing


def make_transclusions(root_ids: list[str], root_text_path: str) -> str:
    return "\n".join(f"![[{root_text_path}#^{rid}]]" for rid in root_ids)


# ---------------------------------------------------------------------------
# ROLES
# ---------------------------------------------------------------------------

ROLE_CHAPTER    = "chapter"
ROLE_TITLE      = "title"
ROLE_SUBHEAD    = "subhead"
ROLE_SUBSUBHEAD = "subsubhead"
ROLE_SUTTA      = "sutta"
ROLE_VERSE      = "verse"
ROLE_GATHA      = "gatha"
ROLE_GATHALAST  = "gathalast"
ROLE_SKIP       = "skip"

CATEGORY_TO_ROLE: dict[str, str] = {
    "chapter":    ROLE_CHAPTER,
    "title":      ROLE_TITLE,
    "subhead":    ROLE_SUBHEAD,
    "subsubhead": ROLE_SUBSUBHEAD,
    "sutta":      ROLE_SUTTA,
    "bodytext":   ROLE_VERSE,
    "indent":     ROLE_VERSE,
    "unindented": ROLE_VERSE,
    "gatha1":     ROLE_GATHA,
    "gatha2":     ROLE_GATHA,
    "gatha3":     ROLE_GATHA,
    "gathalast":  ROLE_GATHALAST,
    "centered":   ROLE_VERSE,   # section-closing summaries
    "nikaya":     ROLE_SKIP,    # handled in pre-chapter extraction
    "book":       ROLE_SKIP,    # handled in pre-chapter extraction
}

# ---------------------------------------------------------------------------
# METADATA
# ---------------------------------------------------------------------------


def extract_metadata(data: dict, source_path: Path, book_id: int) -> dict:
    title_pali = data.get("title_pali") or source_path.stem
    breadcrumb = data.get("title_breadcrumb", "")
    pitaka     = data.get("pitaka", "")
    layer      = data.get("layer", "")
    source_id  = data.get("id", "")
    source_fn  = data.get("source_filename", "")
    total_segs = data.get("total_segments", "")

    desc_parts = []
    if breadcrumb:
        desc_parts.append(breadcrumb)
    if total_segs:
        desc_parts.append(f"{total_segs} segments in source")
    description = "CSCD commentary XML."
    if desc_parts:
        description += " " + "; ".join(desc_parts) + "."

    # Derive layer slug for URL
    layer_lower = layer.lower()
    layer_type  = data.get("layer_type", "")
    url_ext = layer_type if layer_type else {"atthakatha": "att", "tika": "tik", "tiika": "tik"}.get(layer_lower, layer_lower[:3])
    source_url = (
        f"https://tipitaka.org/romn/cscd/{source_id}.{url_ext}.html"
        if source_id and url_ext
        else None
    )

    return {
        "title":              title_pali,
        "language":           "Pali",
        "script":             "Roman (PTS diacritics)",
        "file_type":          "commentary",
        "lang_tag":           "pi",
        "verse_id_format":    "book-verse",
        "pitaka":             pitaka,
        "layer":              layer,
        "root_text":          ROOT_TEXT_PATH,
        "source_description": description,
        "source_filename":    source_fn,
        "source_url":         source_url,
        "other_ids": [f"tipitaka.org: {source_id}"] if source_id else None,
    }


# ---------------------------------------------------------------------------
# MAIN CONVERTER
# ---------------------------------------------------------------------------


def convert_json_to_commentary(
    json_path,
    output_path,
    chapter_context: dict[int, str | None] | None = None,
) -> None:
    """Convert one commentary work's segment JSON into a Markdown draft.

    chapter_context maps each source chapter to "main" (link printed
    citations to the root) or None (no links). Default: every chapter "main".
    """
    json_path   = Path(json_path)
    output_path = Path(output_path)

    with json_path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("tree"):
        return convert_tree(data, json_path, output_path)

    segments = data.get("segments", [])
    meta     = extract_metadata(data, json_path, BOOK_ID)

    # Resolve layer slug for h1 anchor
    raw_layer   = str(meta.get("layer", "")).lower()
    layer_slug  = LAYER_SLUG_MAP.get(raw_layer, raw_layer or "commentary")
    layer_label = LAYER_DISPLAY_MAP.get(raw_layer, raw_layer)

    # Chapter-context to use (caller can override)
    ctx = chapter_context if chapter_context is not None else {s.get("chapter", 0): "main" for s in segments}

    # Phase 1: extract pre-chapter structural elements
    # -----------------------------------------------------------------------
    # We consume nikaya, title, book from the very start of the segment list.
    # We stop collecting title/book once we have found the book segment
    # (got_book=True) so that sub-section titles later in ch0 are not
    # mistakenly appended to the h2 heading.
    # -----------------------------------------------------------------------
    homage         = None
    pitaka_heading = None
    title_parts: list[str] = []
    got_book       = False
    saw_chapter    = False

    chapters: dict[int, list[tuple[str, str]]] = {}

    for seg in segments:
        css     = seg.get("css_class", "")
        content = clean_text(seg.get("content", ""))
        if not content:
            continue
        src_ch = seg.get("chapter", 0)

        # Collect structural preamble (nikaya / title / book) ONLY until
        # we have the book segment. After that, remaining title segments
        # belong to the chapter content and go into the chapters dict.
        if not saw_chapter and not got_book:
            if css == "centered" and homage is None:
                homage = content
                continue
            if css == "nikaya":
                pitaka_heading = content
                continue
            if css == "title":
                title_parts.append(content)
                continue
            if css == "book":
                title_parts.append(content)
                got_book = True   # stop collecting; later titles go to chapters
                continue

        role = CATEGORY_TO_ROLE.get(css, ROLE_VERSE)
        if role == ROLE_CHAPTER:
            saw_chapter = True
        # A paragraph the XML numbers (@n) whose printed number the citation
        # pattern cannot read (e.g. MN s0201a "01 Bahinagareti", no dot) is
        # logged as unresolved, never linked and never dropped silently.
        n_attr = str(seg.get("paragraph") or "")
        if n_attr and role in (ROLE_VERSE, ROLE_GATHA, ROLE_GATHALAST) \
                and not _verse_ref_re.match(content) and not _numberlike_re.match(content):
            UNRESOLVED.append((n_attr, [], content[:80]))
        if role == ROLE_SKIP:
            continue
        chapters.setdefault(src_ch, []).append((role, content))

    # Phase 2: assemble headings and emit
    # -----------------------------------------------------------------------
    book_heading = " ".join(title_parts) if title_parts else meta["title"]

    out: list[str] = [format_frontmatter(meta), "\n"]

    if homage:
        out.append(homage + "\n\n")

    if pitaka_heading:
        h1_title = f"{pitaka_heading} ({layer_label})" if layer_label else pitaka_heading
        out.append(f"# {h1_title} ^{layer_slug}-0\n\n")

    out.append(f"## {book_heading} ^{BOOK_ID}-0\n\n")

    # Continuous verse counter across the whole file
    verse_counter = [0]

    def next_verse_id() -> str:
        verse_counter[0] += 1
        return f"^{BOOK_ID}-{verse_counter[0]}"

    # Phase 3: emit each source chapter as a ### section
    # -----------------------------------------------------------------------
    for src_ch in sorted(chapters.keys()):
        items        = chapters[src_ch]
        root_context = ctx.get(src_ch)

        # Determine the h3 title for this chapter
        chapter_title_raw = next(
            (c for r, c in items if r == ROLE_CHAPTER), None
        )
        if chapter_title_raw is not None:
            h3_title = strip_leading_number(chapter_title_raw)
        else:
            # ch0: no chapter-class segment.
            # Prefer the first *subhead* (e.g. "Nidanakatha") over subsubhead
            # (e.g. "Gantharambhakatha") since the subhead names the section.
            if H3_FIRST_HEADING:
                # Use the first heading in document order, so no heading is
                # moved ahead of text that precedes it in the source.
                h3_title = next(
                    (c for r, c in items
                     if r in (ROLE_TITLE, ROLE_SUBHEAD, ROLE_SUBSUBHEAD)),
                    None,
                ) or f"Section {src_ch}"
            else:
                h3_title = (
                    next((c for r, c in items if r == ROLE_SUBHEAD), None)
                    or next((c for r, c in items if r == ROLE_TITLE), None)
                    or next((c for r, c in items if r == ROLE_SUBSUBHEAD), None)
                    or f"Section {src_ch}"
                )
            h3_title = strip_leading_number(h3_title)

        h3_line = f"### {h3_title} ^{BOOK_ID}-{src_ch}-0\n\n"
        unlinked = [False]   # True while the text sits directly under an UNLINKED heading

        def heading(line: str, text: str) -> None:
            out.append(line)
            unlinked[0] = text in UNLINKED_HEADINGS
            if unlinked[0]:
                UNLINKED_MATCHED.add(text)
        # With H3_FIRST_HEADING, text that precedes the chapter's first
        # heading in the source (e.g. a second volume's homage line) is
        # emitted before the ### line instead of after it.
        h3_pending = H3_FIRST_HEADING and not h3_title.startswith("Section ")
        if not h3_pending:
            heading(h3_line, h3_title)

        # Per-chapter sub-section state
        h4_counter  = 0
        h5_counter  = 0
        seen_title  = False
        consumed_h3 = False   # True once chapter-level title is consumed
        in_sutta    = False   # a "sutta" heading has opened (vagga chapters)
        title_group = False   # numbered subheads now belong to a title (h6)
        h6_counter  = 0

        # Gatha (verse stanza) accumulator
        gatha_buffer: list[str] = []

        def flush_gatha() -> None:
            if not gatha_buffer:
                return
            vid  = next_verse_id()
            body = "\n".join(gatha_buffer)
            out.append(f"{body} {vid}\n\n")
            gatha_buffer.clear()

        def emit_verse(content: str, root_ctx: str | None) -> None:
            """Detect inline root-text ref, emit transclusions, then paragraph."""
            m = _verse_ref_re.match(content)
            if unlinked[0]:
                if m or _numberlike_re.match(content):
                    printed = (m.group(0) if m else _numberlike_re.match(content).group(0)).strip()
                    UNLINKED.append((printed, h_text[0], content[:80]))
                if content:
                    out.append(f"{content} {next_verse_id()}\n\n")
                return
            if not m and root_ctx and _numberlike_re.match(content):
                UNRESOLVED.append((_numberlike_re.match(content).group(0).strip(), [], content[:80]))
            if m and root_ctx:
                n_start = int(m.group(1))
                n_end   = int(m.group(2)) if m.group(2) else n_start
                if n_end < n_start:
                    # CST's truncated-tail range: "133-4." = 133-134,
                    # "368-74." = 368-374. Kept as printed in the text,
                    # linked to the full range.
                    tail = m.group(2)
                    n_end = int(m.group(1)[:-len(tail)] + tail) if len(tail) < len(m.group(1)) else n_end
                    if n_end >= n_start:
                        ABBREVIATED.append((m.group(0).strip(), n_start, n_end))
                    else:
                        UNRESOLVED.append((m.group(0).strip(), [], content[:80]))
                rt_ids  = resolve_root_text_ids(BOOK_ID, root_ctx, n_start, n_end)
                if ROOT_IDS is not None and rt_ids:
                    # Link to the root blocks that hold the cited numbers (a
                    # root range block ^b-A-B holds A..B); log the numbers no
                    # block holds, for the citation-irregularities report.
                    rt_ids, missing = covering_blocks(ROOT_IDS, BOOK_ID, n_start, n_end)
                    if missing:
                        UNRESOLVED.append((m.group(0).strip(), missing, content[:80]))
                if rt_ids:
                    out.append(make_transclusions(rt_ids, ROOT_TEXT_PATH) + "\n\n")
                if not KEEP_REF_NUMBER:
                    content = _leading_strip_re.sub("", content).strip()

            if not content:
                return
            vid = next_verse_id()
            out.append(f"{content} {vid}\n\n")

        h_text = [h3_title]   # text of the heading the current text sits under

        for role, content in items:
            if role in (ROLE_TITLE, ROLE_SUBHEAD, ROLE_SUBSUBHEAD, ROLE_SUTTA):
                h_text[0] = strip_leading_number(content)
            if h3_pending and role in (ROLE_CHAPTER, ROLE_TITLE,
                                       ROLE_SUBHEAD, ROLE_SUBSUBHEAD, ROLE_SUTTA):
                flush_gatha()
                heading(h3_line, h3_title)
                h3_pending = False
            if role == ROLE_CHAPTER:
                if not consumed_h3:
                    consumed_h3 = True
                    continue
                # A second chapter-class segment inside the same source
                # chapter is treated as an h4 (rare edge case)
                role = ROLE_TITLE

            if role == ROLE_SUTTA:
                flush_gatha()
                text = strip_leading_number(content)
                in_sutta, title_group, seen_title = True, False, True
                h4_counter += 1
                h5_counter  = 0
                heading(f"#### {text} ^{BOOK_ID}-{src_ch}-{h4_counter}-0\n\n", text)
                continue

            if in_sutta and role in (ROLE_TITLE, ROLE_SUBHEAD, ROLE_SUBSUBHEAD):
                flush_gatha()
                text = strip_leading_number(content)
                if role != ROLE_TITLE and title_group and _leading_num_re.match(content):
                    h6_counter += 1
                    heading(f"###### {text} ^{BOOK_ID}-{src_ch}-{h4_counter}-{h5_counter}-{h6_counter}-0\n\n", text)
                    continue
                title_group = role == ROLE_TITLE
                h5_counter += 1
                h6_counter  = 0
                heading(f"##### {text} ^{BOOK_ID}-{src_ch}-{h4_counter}-{h5_counter}-0\n\n", text)
                continue

            if role == ROLE_TITLE:
                flush_gatha()
                if H3_FIRST_HEADING and not consumed_h3 and \
                        strip_leading_number(content) == h3_title:
                    consumed_h3 = True
                    continue
                seen_title  = True
                h4_counter += 1
                h5_counter  = 0
                heading_id  = f"^{BOOK_ID}-{src_ch}-{h4_counter}-0"
                heading(f"#### {strip_leading_number(content)} {heading_id}\n\n",
                        strip_leading_number(content))
                continue

            if role in (ROLE_SUBHEAD, ROLE_SUBSUBHEAD):
                flush_gatha()
                text = strip_leading_number(content)

                # Skip this subhead if it was used as the synthesised h3 title
                if not consumed_h3 and text == h3_title:
                    consumed_h3 = True
                    continue

                if seen_title:
                    # h5: deeper sub-section under an h4 title
                    h5_counter += 1
                    heading_id  = f"^{BOOK_ID}-{src_ch}-{h4_counter}-{h5_counter}-0"
                    heading(f"##### {text} {heading_id}\n\n", text)
                else:
                    # h4: sub-section before any h4 title in this chapter
                    h4_counter += 1
                    h5_counter  = 0
                    heading_id  = f"^{BOOK_ID}-{src_ch}-{h4_counter}-0"
                    heading(f"#### {text} {heading_id}\n\n", text)
                continue

            if role == ROLE_GATHA:
                gatha_buffer.append(content)
                continue

            if role == ROLE_GATHALAST:
                gatha_buffer.append(content)
                flush_gatha()
                continue

            # ROLE_VERSE (bodytext, indent, unindented, centered)
            flush_gatha()
            emit_verse(content, root_context)

        flush_gatha()  # safety flush at chapter end
        if h3_pending:
            heading(h3_line, h3_title)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(out), encoding="utf-8")
    print(
        f"Wrote {output_path}  ({verse_counter[0]} verses)",
        file=sys.stderr,
    )


# ---------------------------------------------------------------------------
# TREE MODE (cscd_xml_to_json.py --tree: Aṅguttaranikāya)
# ---------------------------------------------------------------------------
# Every heading segment carries its level ('#' count); the commentary is emitted
# in document order with headings at those levels. Paragraphs, root links,
# gāthā grouping, unlinked sections and logging are exactly as in the chapter
# path above (same rules, same logs).

_tree_lead_re = re.compile(r"^\s*(?:\(\d+\)\s*)?\d+(?:-\d+)*\.\s*")   # "1. ", "1-10. ", "(6) 1. "


def convert_tree(data: dict, json_path: Path, output_path: Path) -> None:
    segments = data.get("segments", [])
    meta = extract_metadata(data, json_path, BOOK_ID)
    raw_layer = str(meta.get("layer", "")).lower()
    layer_slug = LAYER_SLUG_MAP.get(raw_layer, raw_layer or "commentary")
    layer_label = LAYER_DISPLAY_MAP.get(raw_layer, raw_layer)
    out: list[str] = [format_frontmatter(meta), "\n"]
    counter = [0]
    section = [None]
    unlinked = [False]
    h_text = [""]
    gatha: list[str] = []

    def next_id() -> str:
        counter[0] += 1
        return f"^{BOOK_ID}-{counter[0]}"

    def flush_gatha() -> None:
        if gatha:
            out.append("\n".join(gatha) + f" {next_id()}\n\n")
            gatha.clear()

    def emit(content: str, n_attr: str) -> None:
        if n_attr and content.strip() == n_attr:
            # the number alone, its dot opening the next paragraph (CSCD Apadāna-aṭṭhakathā:
            # <p n="314">314</p><p>. Uḷurājāva …</p>): a printed citation, read as "314."
            m = _verse_ref_re.match(content.strip() + ". ")
            if m:
                n0 = int(m.group(1))
                ids, missing = (ZONE_LINKER.link([n0]) if ZONE_LINKER is not None else (None, None))
                if PER_SECTION:
                    _s = section[0] or (PRESECTION if not SEEN_SECTION[0] else None)
                    want = [f"{BOOK_ID}-{_s}-{n0}"] if _s else []
                    ids = [r for r in want if ROOT_IDS is None or r in ROOT_IDS]
                    missing = [r for r in want if r not in ids] or ([] if want else [f"(no section) {n0}"])
                elif ids is None:
                    ids, missing = covering_blocks(ROOT_IDS, BOOK_ID, n0, n0) if ROOT_IDS is not None else (resolve_root_text_ids(BOOK_ID, "main", n0, n0), [])
                if missing:
                    UNRESOLVED.append((content.strip(), missing, content[:80]))
                if ids:
                    out.append(make_transclusions(ids, ROOT_TEXT_PATH) + "\n\n")
                out.append(f"{content} {next_id()}\n\n")
                return
        m = _verse_ref_re.match(content)
        if m and not n_attr:
            # a number the XML does not mark as a paragraph number (@n): the
            # text's own numbering (AN Dasaka-ṭīkā "1. ‘‘Munāḷi…" … "12."), not a citation
            UNLINKED.append((m.group(0).strip(), "no @n: own numbering, not a citation", content[:80]))
            out.append(f"{content} {next_id()}\n\n")
            return
        if unlinked[0]:
            if m or _numberlike_re.match(content):
                printed = (m.group(0) if m else _numberlike_re.match(content).group(0)).strip()
                UNLINKED.append((printed, h_text[0], content[:80]))
            out.append(f"{content} {next_id()}\n\n")
            return
        if not m and _numberlike_re.match(content):
            UNRESOLVED.append((_numberlike_re.match(content).group(0).strip(), [], content[:80]))
        if m:
            n_start = int(m.group(1))
            n_end = int(m.group(2)) if m.group(2) else n_start
            if n_end < n_start:
                tail = m.group(2)
                n_end = int(m.group(1)[:-len(tail)] + tail) if len(tail) < len(m.group(1)) else n_end
                if n_end >= n_start:
                    ABBREVIATED.append((m.group(0).strip(), n_start, n_end))
                else:
                    UNRESOLVED.append((m.group(0).strip(), [], content[:80]))
            rt_ids = resolve_root_text_ids(BOOK_ID, "main", n_start, n_end)
            if ZONE_LINKER is not None and n_end >= n_start:
                rt_ids, missing = ZONE_LINKER.link(list(range(n_start, n_end + 1)))
                if missing:
                    UNRESOLVED.append((m.group(0).strip(), missing, content[:80]))
            elif PER_SECTION:
                sec = section[0] or (PRESECTION if not SEEN_SECTION[0] else None)
                want = [f"{BOOK_ID}-{sec}-{k}" for k in range(n_start, n_end + 1)] if sec else []
                rt_ids = [r for r in want if ROOT_IDS is None or r in ROOT_IDS]
                missing = [r for r in want if ROOT_IDS is not None and r not in ROOT_IDS] or ([] if want else [f"(no section) {n_start}"])
                if missing:
                    UNRESOLVED.append((m.group(0).strip(), missing, content[:80]))
            elif ROOT_IDS is not None and rt_ids:
                rt_ids, missing = covering_blocks(ROOT_IDS, BOOK_ID, n_start, n_end)
                if missing:
                    UNRESOLVED.append((m.group(0).strip(), missing, content[:80]))
            if rt_ids:
                out.append(make_transclusions(rt_ids, ROOT_TEXT_PATH) + "\n\n")
        out.append(f"{content} {next_id()}\n\n")

    seen_book = False
    for seg in segments:
        css = seg.get("css_class", "")
        content = clean_text(seg.get("content", ""))
        if not content:
            continue
        if not seen_book:
            if css == "centered":
                out.append(content + "\n\n")
                continue
            if css == "nikaya":
                out.append(f"# {content} ({layer_label}) ^{layer_slug}-0\n\n")
                continue
            if css == "book":
                out.append(f"## {content} ^{BOOK_ID}-0\n\n")
                seen_book = True
                continue
        if css == "heading":
            flush_gatha()
            # keep_number: a title line made a heading by a human decision (Jātaka-aṭṭhakathā
            # "1. Apaṇṇakajātakavaṇṇanā"): its printed number stays, as the XML prints it as text
            text = content.strip() if seg.get("keep_number") else _tree_lead_re.sub("", content).strip()
            h_text[0] = text
            if seg["level"] == 3:
                mnum = re.match(r"^\s*(\d+)\.", content)
                section[0] = mnum.group(1) if mnum else None
                if mnum:
                    SEEN_SECTION[0] = True        # PRESECTION applies only before this
            unlinked[0] = text in UNLINKED_HEADINGS
            if unlinked[0]:
                UNLINKED_MATCHED.add(text)
            out.append(f"{'#' * seg['level']} {text} ^{BOOK_ID}-h-0\n\n")
            continue
        role = CATEGORY_TO_ROLE.get(css, ROLE_VERSE)
        if role == ROLE_SKIP:
            continue
        n_attr = str(seg.get("paragraph") or "")
        if n_attr and role in (ROLE_VERSE, ROLE_GATHA, ROLE_GATHALAST) and content.strip() != n_attr \
                and not _verse_ref_re.match(content) and not _numberlike_re.match(content):
            UNRESOLVED.append((n_attr, [], content[:80]))
        if role in (ROLE_GATHA, ROLE_GATHALAST) and n_attr and _verse_ref_re.match(content) \
                and gatha and not unlinked[0]:
            # a cited verse that opens while an earlier quoted verse is still open (CSCD
            # Vimānavatthu-aṭṭhakathā quotes runs of one-line verses, "256. …", "258. …",
            # each with its own @n and no gathalast): close that one, so each cited verse
            # is its own block with its own links
            flush_gatha()
        if role in (ROLE_GATHA, ROLE_GATHALAST) and n_attr and _verse_ref_re.match(content) \
                and not gatha and not unlinked[0]:
            # a gāthā that opens with a printed citation (a number-only line joined
            # to it, KN Khuddakapāṭha-aṭṭhakathā "10.") links to the root like prose
            before = len(out)
            emit(content, n_attr)
            out[before + 1 if len(out) > before + 1 and out[before].startswith("![[") else before:] = []
            counter[0] -= 1
        elif role in (ROLE_GATHA, ROLE_GATHALAST) and not n_attr and _verse_ref_re.match(content) \
                and not gatha:
            # a verse the text numbers for itself (a number-only line joined to it):
            # never linked, logged so the checker knows it is not a missing citation
            UNLINKED.append((_verse_ref_re.match(content).group(0).strip(), "no @n: own numbering, not a citation", content[:80]))
        if role == ROLE_GATHA:
            gatha.append(content)
            continue
        if role == ROLE_GATHALAST:
            gatha.append(content)
            flush_gatha()
            continue
        flush_gatha()
        emit(content, n_attr)
    flush_gatha()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {output_path}  ({counter[0]} verses, tree mode)", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("json_path",   type=Path)
    ap.add_argument("output_path", type=Path)
    args = ap.parse_args()
    convert_json_to_commentary(args.json_path, args.output_path)


if __name__ == "__main__":
    main()
