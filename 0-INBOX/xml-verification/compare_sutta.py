"""Compare a Sutta-rails root-text .md against its CST tipitaka-xml source(s).

usage: python compare_sutta.py <vault.md> <out_report.md> <xml1> [xml2 ...]

Written for this vault's conversion (cscd-root-text-intake):
- every XML <p>/<trailer>/<head> is one vault line; blocks group the lines
  of one printed paragraph number, whose number moves into the block ID;
- variant readings <note> are kept inline as [ ... ];
- bold <hi rend="bold"> is kept as **...**;
- page markers are dropped; CST's ‘‘ ’’ become ";
- heading numbers ("1. Brahmajālasuttaṃ") are stripped.

Checks, independent of the intake skill's own verify.py:
1. content line by line (words, punctuation, spacing, bold, variants);
2. every content line carries the block ID of the printed paragraph it belongs to;
3. block-ID hygiene (duplicates, missing IDs, heading IDs = depth);
4. heading text and level against the XML structure.
"""
import re, sys, difflib
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")

md_path, out_path, xml_paths = sys.argv[1], sys.argv[2], sys.argv[3:]

# ---------------------------------------------------------------- XML side
def inner(el, top=True, head=False):
    s = el.text or ""
    for ch in el:
        if ch.tag == "note":
            s += "[" + inner(ch, False) + "]"
        elif ch.tag == "hi" and ch.get("rend") == "dot" and top and head:
            s += ch.text or ""        # a heading's "152<hi rend=dot>.</hi>": the number's dot, for strip_num
        elif ch.tag == "hi" and ch.get("rend") in ("paranum", "dot") and top:
            # the printed number moves into the block ID; an untagged dot right after it
            # ("<hi rend=paranum>1</hi>. Sotāvadhāne", Paṭisambhidāmagga) goes with it
            if ch.get("rend") == "paranum" and (ch.tail or "").startswith("."):
                s += ch.tail[1:]
                continue
        elif ch.tag == "hi" and ch.get("rend") == "bold":
            s += "**" + inner(ch, False) + "**"
        elif ch.tag != "pb":
            s += inner(ch, False)
        s += ch.tail or ""
    return s

xml_heads = []   # (level, rend, text)
xml_lines = []   # (kind, text, rend, paranum, raw)
cur_para = [None]

def strip_num(t):
    t = re.sub(r"^\s*\(\d+\)\s*(?=\d+\.)", "", t)  # AN's running vagga number: "(6) 1. Puggalavaggo"
    return re.sub(r"^\s*[\d\-–]+\.\s*", "", t)

def walk(el, depth):
    for ch in el:
        if ch.tag == "div":
            walk(ch, depth + 1)
        elif ch.tag == "head":
            t = strip_num(inner(ch).strip())
            xml_heads.append((depth, ch.get("rend"), t, inner(ch).strip()))
            xml_lines.append(("H", t, ch.get("rend"), None, inner(ch).strip()))
            cur_para[0] = None
        elif ch.tag in ("p", "trailer"):
            rend = ch.get("rend")
            t = inner(ch).strip()
            if ch.tag == "p" and rend in ("nikaya", "title", "subhead", "subsubhead", "chapter", "book"):
                lvl = {"nikaya": 0, "book": depth + 1, "chapter": depth + 1, "title": depth + 1,
                       "subhead": depth + 1, "subsubhead": depth + 2}[rend]
                t = strip_num(inner(ch, head=True).strip())
                xml_heads.append((lvl, rend, t, inner(ch).strip()))
                xml_lines.append(("H", t, rend, None, inner(ch).strip()))
                cur_para[0] = None
            else:
                pn = ch.find("hi[@rend='paranum']")
                if pn is not None:
                    cur_para[0] = pn.text
                if not t:
                    continue      # e.g. a hangnum holding only its number, which moves into the block ID
                xml_lines.append(("P", t, rend, cur_para[0], t))
        else:
            walk(ch, depth)

for xp in xml_paths:
    root = ET.parse(xp).getroot()
    cur_para[0] = None    # each CSCD volume restarts its paragraph numbers
    walk(root.find(".//body"), 0)

# ---------------------------------------------------------------- vault side
md_all = open(md_path, encoding="utf-8").read().replace("\r\n", "\n")
fm = re.match(r"\A---\n.*?\n---\n", md_all, flags=re.S)
offset = md_all[:fm.end()].count("\n") if fm else 0
md = md_all[fm.end():] if fm else md_all

vault_heads = []   # (level, text, id, lineno)
vault_lines = []   # (kind, text, lineno, blockid)
id_problems = []
blocks = []        # (bid, first_line, text)
lineno = offset + 1
for raw in re.split(r"(\n\s*\n)", md):
    if not raw.strip():
        lineno += raw.count("\n"); continue
    b = raw.strip("\n")
    lead = len(raw) - len(raw.lstrip("\n"))
    start = lineno + lead
    m = re.match(r"^(#+)\s+(.*?)\s*(\^[\w-]+)?\s*$", b)
    if m and "\n" not in b:
        htext = re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2))
        vault_heads.append((len(m.group(1)) - 1, htext, m.group(3) or "", start))
        vault_lines.append(("H", htext, start, m.group(3) or ""))
    else:
        mid = re.search(r"\s*\^([\w-]+)\s*$", b)
        bid = mid.group(1) if mid else None
        text = b[:mid.start()] if mid else b
        if bid is None:
            id_problems.append(f"line {start}: block without block ID: {b[:80]!r}")
        blocks.append((bid, start, text))
        for i, ln in enumerate(text.split("\n")):
            vault_lines.append(("P", ln, start + i, bid))
    lineno += raw.count("\n")

seen = {}
for bid, ln, _ in blocks:
    if bid in seen:
        id_problems.append(f"line {ln}: duplicate block ID ^{bid} (first at line {seen[bid]})")
    seen[bid] = ln
for k, t, ln, b in vault_lines:
    if "  " in t or t != t.strip() or "\t" in t:
        id_problems.append(f"line {ln}: stray whitespace (double, leading/trailing or tab): {t.strip()[:80]!r}")
for lvl, t, hid, ln in vault_heads:
    if hid and hid[1:] in seen:
        id_problems.append(f"line {ln}: heading ID {hid} also used by a block")

# ---------------------------------------------------------------- normalise
def strict(s, xml):
    if xml:
        s = s.replace("‘‘", '"').replace("’’", '"')
    return re.sub(r"\s+", " ", s).strip()

def loose(s, xml):        # ignore bold markers and spacing before punctuation
    s = strict(s, xml).replace("**", "")
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"\s+([.,;:!?…])", r"\1", s)

xa = [loose(l[1], True) for l in xml_lines]
va = [loose(l[1], False) for l in vault_lines]

out = []
P = out.append
P(f"# Comparison report: `{md_path.replace(chr(92), '/').split('/')[-1]}`\n")
P("Sources: " + ", ".join(p.replace(chr(92), '/').split('/')[-1] for p in xml_paths) + "\n")
paranums = [l[3] for l in xml_lines if l[0] == "P" and l[3]]
P("## 1. Counts\n")
P(f"- XML: {len(xml_lines)} lines ({len(xml_heads)} headings, {len(set(paranums))} printed paragraph numbers)")
P(f"- Vault: {len(vault_lines)} lines ({len(vault_heads)} headings, {len(blocks)} blocks)\n")

P("## 2. Block ID problems\n")
P("\n".join("- " + p for p in id_problems) if id_problems else "- none")
P("")

sm = difflib.SequenceMatcher(None, xa, va, autojunk=False)
ops = sm.get_opcodes()
diffs = [op for op in ops if op[0] != "equal"]
eq_pairs = [(i1 + d, j1 + d) for t, i1, i2, j1, j2 in ops if t == "equal" for d in range(i2 - i1)]
strict_diff = [(i, j) for i, j in eq_pairs
               if strict(xml_lines[i][1], True) != strict(vault_lines[j][1], False)]

P("## 3. Content (line by line)\n")
P(f"- Identical lines (ignoring bold markers and space before punctuation): {len(eq_pairs)} of {len(xa)} XML / {len(va)} vault")
P(f"- Of those, lines that differ in bold markers or spacing only: {len(strict_diff)}")
for i, j in strict_diff[:60]:
    P(f"  - line {vault_lines[j][2]}: XML `{strict(xml_lines[i][1], True)[:200]}` | vault `{strict(vault_lines[j][1], False)[:200]}`")
P(f"- Difference hunks: {len(diffs)}\n")
for t, i1, i2, j1, j2 in diffs:
    vl = vault_lines[j1][2] if j1 < len(vault_lines) else vault_lines[-1][2]
    P(f"### {t} — vault line {vl}")
    if t == "replace" and (i2 - i1) == (j2 - j1):
        for d in range(i2 - i1):
            aw, bw = xa[i1 + d].split(" "), va[j1 + d].split(" ")
            s2 = difflib.SequenceMatcher(None, aw, bw, autojunk=False)
            for tt, a1, a2, b1, b2 in s2.get_opcodes():
                if tt != "equal":
                    P(f"- line {vault_lines[j1+d][2]}: {tt}: XML `{' '.join(aw[max(0,a1-2):a2+2])}` → vault `{' '.join(bw[max(0,b1-2):b2+2])}`")
    else:
        for i in range(i1, i2):
            P(f"- XML  [{xml_lines[i][0]}/{xml_lines[i][2]}]: `{xa[i][:220]}`")
        for j in range(j1, j2):
            P(f"- vault line {vault_lines[j][2]} [{vault_lines[j][0]}]: `{va[j][:220]}`")
    P("")

# ---------------------------------------------------------------- block IDs vs printed numbers
P("## 4. Block IDs vs printed paragraph numbers\n")
bad_ids, u_ids = [], []
for i, j in eq_pairs:
    k, _, rend, pn, _ = xml_lines[i]
    if k != "P":
        continue
    bid = vault_lines[j][3] or ""
    num = re.sub(r"x\d+$", "", bid.split("-")[-1])   # ^…-274x1: 2nd print of the same number
    if bid.startswith("T-") or re.match(r"^T\d+$", num):
        continue          # homage / volume-opening blocks (^T-1, ^<book>-T<k>) sit outside the numbering
    if pn is None:
        if not re.match(r"^(U\d+|\d+)$", num) and not bid.startswith("T-"):
            bad_ids.append(f"line {vault_lines[j][2]}: unnumbered XML line but ^{bid}")
        if num.startswith("U"):
            u_ids.append(bid)
    else:
        lo = pn.split("-")[0]
        if num.startswith("U") and rend == "centre" and re.match(r"^\d+\.\s", xml_lines[i][1]):
            u_ids.append(bid)
            continue      # a centred "N. …" title with no paranum of its own (Vimānavatthu, Guttilavimāna)
        if bid.endswith("-" + pn):
            continue      # a range ID such as ^3-225-240 for the printed range 225-240
        if num != pn and num != lo and not num.startswith(lo + "-"):
            # a U-block after a numbered paragraph is fine if XML had no new number
            bad_ids.append(f"line {vault_lines[j][2]}: printed ¶{pn} but ^{bid}")
P(f"- lines checked: {sum(1 for i, j in eq_pairs if xml_lines[i][0] == 'P')}")
P(f"- `U` blocks (unnumbered in the source): {len(set(u_ids))}")
P(f"- mismatches: {len(bad_ids)}")
for b in bad_ids[:80]:
    P(f"  - {b}")
P("")

# ---------------------------------------------------------------- headings
P("## 5. Headings (XML structural level vs vault level)\n")
P("XML level: nikaya = 0; a div `head` = div depth; `p` heading rends = depth + 1 (subsubhead + 2). Vault level = number of `#` − 1.\n")
xh = [loose(t, True) for l, r, t, raw in xml_heads]
vh = [loose(t, False) for l, t, i, ln in vault_heads]
hm = difflib.SequenceMatcher(None, xh, vh, autojunk=False)
lvl_mis, txt_mis = [], []
raw_of = {}        # vault heading line -> the XML heading as printed (with its numbers)
for t, i1, i2, j1, j2 in hm.get_opcodes():
    if t == "equal":
        for d in range(i2 - i1):
            raw_of[vault_heads[j1 + d][3]] = xml_heads[i1 + d][3]
            if xml_heads[i1 + d][0] != vault_heads[j1 + d][0]:
                lvl_mis.append((xml_heads[i1 + d], vault_heads[j1 + d]))
    else:
        txt_mis.append((t, xml_heads[i1:i2], vault_heads[j1:j2]))
P(f"- XML headings: {len(xh)}; vault headings: {len(vh)}")
P(f"- Text mismatches: {len(txt_mis)}")
for t, a, b in txt_mis:
    P(f"  - {t}: XML {[(h[0], h[1], h[2]) for h in a]} → vault {[(h[0], h[1], h[2], 'line '+str(h[3])) for h in b]}")
P(f"- Level mismatches: {len(lvl_mis)}")
for xhd, vhd in lvl_mis[:150]:
    P(f"  - line {vhd[3]}: `{vhd[1]}` {vhd[2]}: XML level {xhd[0]} ({xhd[1]}), vault level {vhd[0]}")
P("")

P("## 6. Heading block-ID consistency\n")
bad = []
for lvl, t, hid, ln in vault_heads:
    if not hid:
        bad.append(f"line {ln}: `{t}` has no block ID"); continue
    if hid == "^0":
        continue
    segs = hid[1:].split("-")
    if segs[-1] != "0":
        bad.append(f"line {ln}: `{t}` {hid} does not end in -0")
    if len(segs) - 1 != lvl:
        bad.append(f"line {ln}: `{t}` {hid} path length {len(segs)-1} ≠ heading level {lvl}")
# sibling numbering: each heading's last path segment = its position among siblings
stack, counters = [], {}
for lvl, t, hid, ln in vault_heads:
    if not hid or hid == "^0":
        continue
    segs = hid[1:].split("-")[:-1]
    parent = "-".join(segs[:-1])
    counters.setdefault(parent, [])
    counters[parent].append((segs[-1], ln, t))
for parent, kids in counters.items():
    nums = [k[0] for k in kids]
    if all(n.isdigit() for n in nums) and nums != [str(i) for i in range(int(nums[0]), int(nums[0]) + len(nums))]:
        bad.append(f"children of `{parent or '(top)'}` not sequential: {nums[:20]}")
P("\n".join("- " + b for b in bad) if bad else "- all heading IDs agree with heading depth, siblings numbered in sequence")
P("")

P("## 6b. Hierarchy hints\n")
P("Numbers are the XML's printed ones (the vault strips them). A restart among siblings often means a level was flattened; an empty heading has neither text nor sub-headings.\n")
hints = []
by_parent = {}
for lvl, t, hid, ln in vault_heads:
    if not hid or hid == "^0":
        continue
    parent = "-".join(hid[1:].split("-")[:-2])
    m = re.match(r"^\s*(?:\(\d+\)\s*)?(\d+)[\.\-–]", raw_of.get(ln, ""))
    by_parent.setdefault(parent, []).append((int(m.group(1)) if m else None, ln, t, hid, raw_of.get(ln, "")))
for parent, kids in by_parent.items():
    prev = None
    for n, ln, t, hid, raw in kids:
        if n is not None and prev is not None and n <= prev[0]:
            hints.append(f"line {ln}: `{raw}` {hid} restarts numbering after sibling `{prev[1]}`")
        if n is not None:
            prev = (n, raw)
lvl_at = {ln: lvl for lvl, t, hid, ln in vault_heads}
for k, (kind, text, ln, b) in enumerate(vault_lines):
    if kind != "H" or b == "^0":
        continue
    nxt = vault_lines[k + 1] if k + 1 < len(vault_lines) else None
    if nxt is None or (nxt[0] == "H" and lvl_at.get(nxt[2], 99) <= lvl_at[ln]):
        hints.append(f"line {ln}: `{text}` {b} is empty (no text, no sub-headings)")
P(f"- hints: {len(hints)}")
P("\n".join("  - " + h for h in hints[:300]) if hints else "- none")
P("")

P("## 7. Vault outline\n")
P("```")
for lvl, t, hid, ln in vault_heads:
    P("  " * lvl + f"{t}  {hid}   (line {ln})")
P("```")

open(out_path, "w", encoding="utf-8").write("\n".join(out))
print(f"xmlLines={len(xa)} vaultLines={len(va)} equal={len(eq_pairs)} boldOrSpaceOnly={len(strict_diff)} hunks={len(diffs)} "
      f"idMismatch={len(bad_ids)} uBlocks={len(set(u_ids))} headsX={len(xh)} headsV={len(vh)} "
      f"headTxtMis={len(txt_mis)} headLvlMis={len(lvl_mis)} idProblems={len(id_problems)} headIdBad={len(bad)} hints={len(hints)}")
