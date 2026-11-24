"""Paṭisambhidāmagga-aṭṭhakathā (KN book 17): the shape decided by a human, 2026-11-24. Headings only.

  prep <segments.json>   nothing to do before the build (all headings are already headings).
  post <draft.md> <segments.json>   after the build: every heading below the front matter takes
     its level and ID from the root.
     - The three vaggas ("(1) Mahāvaggo" …), which the XML puts at the kathās' level, are '###' on
       the root's IDs, the kathās '####' under them, as in the root   [decision: nest as the root]
     - A heading whose name is a root heading's (less "-vaṇṇanā"/"-niddeso", printed numbers and
       "Ka./Kha./…" letters; a grouped title "41-42. Khanti…pariyogāhaṇa…" by its first section)
       takes that root heading's ID and level, even where the XML nests it differently
       (Saṅkhārupekkhā under Ādīnava, Indriyaparopariyatta under Suddhikapaṭisambhidā, the three
       chakkas, the Indriyakathā's Ka./Kha./Ga.)            [decision: follow the root's nesting]
       It is looked for in root order, among the not yet matched root headings under the heading
       the commentary has it under, then under that heading's parents up to the vagga.
     - A heading the root lacks (the commentary's own "Yuganaddhakathāvaṇṇanā", the Sutamaya's
       thirteen sub-sections …) keeps the commentary's nesting, numbered after the root's last
       heading under the same parent, so its ID claims no root section. Mātikāvaṇṇanā, printed
       inside the Ñāṇakathā, is one of these (^17-1-2-49-0), not the root's Mātikā ^17-1-1-0
                                                             [decision: under Ñāṇakathā, own ID]
     - Nigamanakathā: '###' after the root's last section (standing decision).
"""
import difflib
import re
import sys
import unicodedata
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
mode, path = sys.argv[1], Path(sys.argv[2])
BOOK = "17"
OWN = {"Mātikāvaṇṇanā"}
# names the rule cannot pair, read from the texts: the commentary's title -> the root's
ALIAS = {"Vimokkhuddesavaṇṇanā": "Uddeso", "Vimokkhaniddesavaṇṇanā": "Niddeso",
         "Balādivārattayavaṇṇanā": "Balavāro", "Vivaṭṭañāṇachakkaniddesavaṇṇanā": "Chavivaṭṭañāṇaniddeso"}

if mode == "prep":
    print("   ps prep: nothing to do")
    sys.exit(0)

H = re.compile(r"^(#+) (.*) \^([\w-]+)$")
LEAD = re.compile(r"^\s*(?:\(\d+\)\s*)?(?:[\d-]+\.\s*)?(?:(?:ka|kha|ga|gha|ṅa|ca)(?:-(?:ka|kha|ga|gha|ṅa|ca))?\.\s*)?", re.I)


def norm(s):
    s = LEAD.sub("", s.strip()).lower().replace("-", "").replace(" ", "")
    s = re.sub(r"vaṇṇanā$", "", s)
    s = re.sub(r"niddes(?:o|a)$", "", s)
    s = re.sub(r"(?:aṃ|ṃ|o|a|ā)$", "", s)
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))


def same(c, r):
    a, b = norm(ALIAS.get(LEAD.sub("", c).strip(), c)), norm(r)
    # a spelling variant (Sabbaññutaññāṇa / Sabbaññutañāṇa) counts as the same name
    return a == b or (min(len(a), len(b)) >= 6 and (a.startswith(b) or b.startswith(a))) \
        or (min(len(a), len(b)) >= 8 and difflib.SequenceMatcher(None, a, b).ratio() >= 0.9)


root = [(len(m.group(1)), m.group(3), m.group(2)) for m in map(H.match, Path(f"0-INBOX/temp/kn/pi-kn-{BOOK}.md").read_text(encoding="utf-8").split("\n")) if m]
root = [r for r in root if r[0] >= 3]
rpos = {rid: i for i, (_, rid, _) in enumerate(root)}
rlev = {rid: lv for lv, rid, _ in root}
under = lambda anc, rid: rid != anc and rid.startswith(anc[:-1])          # "17-1-2-0" covers "17-1-2-…"
kids = lambda pid: [rid for _, rid, _ in root if rid.rsplit("-", 2)[0] + "-0" == pid]
tops = [rid for lv, rid, _ in root if lv == 3]

lines = path.read_text(encoding="utf-8").split("\n")
used, last = set(), -1
stack = []            # (commentary level, final id, matched root id or None)
own_n = {}            # parent id -> own headings numbered so far
out = {}
for i, l in enumerate(lines):
    m = H.match(l)
    if not m or len(m.group(1)) < 3 or "-I" in m.group(3):
        continue
    lev, title = len(m.group(1)), m.group(2)
    if re.match(r"\(\d+\)\s*\S+vaggo$", title):
        lev -= 1             # a vagga the XML puts at its kathās' level: it holds them
    if title.startswith("Nigamana"):
        out[i] = (3, f"{BOOK}-{max(int(t.split('-')[1]) for t in tops) + 1}-0"); continue
    while stack and stack[-1][0] >= lev:
        stack.pop()
    hit = None
    if title not in OWN:
        scopes = [s[2] for s in reversed(stack) if s[2]] + [None]          # nearest parent first, then up
        for sc in scopes:
            cand = [rid for _, rid, rt in root if rid not in used and rpos[rid] > last
                    and (sc is None and rlev[rid] == 3 or sc is not None and under(sc, rid)) and same(title, rt)]
            if cand:
                hit = min(cand, key=rpos.get); break
    if hit:
        used.add(hit); last = rpos[hit]
        out[i] = (rlev[hit], hit)
        stack.append((lev, hit, hit))
    else:
        pid = stack[-1][1] if stack else None
        assert pid, f"no parent for {title}"
        rk = [int(r.split("-")[-2]) for r in kids(pid)]
        own_n[pid] = own_n.get(pid, 0) + 1
        nid = f"{pid[:-2]}-{(max(rk) if rk else 0) + own_n[pid]}-0"
        out[i] = (len(nid.split("-")), nid)
        stack.append((lev, nid, None))
        print(f"   ps post: own heading {title}  ^{nid}")
moved = 0
for i, (lv, nid) in out.items():
    m = H.match(lines[i])
    assert len(nid.split("-")) == lv, (nid, lv)
    new = f"{'#' * lv} {m.group(2)} ^{nid}"
    if new != lines[i]:
        moved += 1
        if len(m.group(1)) != lv:
            print(f"   ps post: level {len(m.group(1))} -> {lv}  {m.group(2)}  ^{nid}")
    lines[i] = new
ids = [H.match(l).group(3) for l in lines if H.match(l)]
dup = sorted({x for x in ids if ids.count(x) > 1})
assert not dup, f"duplicate heading IDs: {dup}"
print(f"   ps post: {len(out)} headings placed, {moved} changed; root headings with no commentary heading: "
      f"{[rt for _, rid, rt in root if rid not in used]}")
path.write_text("\n".join(lines), encoding="utf-8")
