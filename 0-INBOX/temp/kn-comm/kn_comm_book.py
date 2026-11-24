"""Build, check and (if everything passes) join one Khuddakanikāya aṭṭhakathā book
(cscd-commentary-intake, steps 2-10), with the human decisions taken so far:
  - an opening "Ganthārambhakathā" section is front matter (^<book>-I-0)      [book 3, 2026-11-24]
  - a closing "Nigamanakathā" heading becomes its own '###' after the last
    top-level section                                                        [book 3, 2026-11-24]
  - each book that passes every check is joined into 1-SOURCES (standing approval 2026-11-24)

usage: python kn_comm_book.py <book> <stem[,stem2…]> <site-key> <root-key> "<label>" [--per-section] [--dry]
  e.g. python kn_comm_book.py 4 s0504a.att kn-it… (run from the vault root)
Stops (exit 1) on: a failed check, an unresolved citation, a site difference that is not a note,
or anything that needs a new human decision. --dry builds and checks but does not join.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
book, stems, key, rkey, label = args[0], args[1].split(","), args[2], args[3], args[4]
PER_SECTION, DRY = "--per-section" in sys.argv, "--dry" in sys.argv
# --zones=<labels>: the root's zone labels in order ("1,2" Suttanipāta; ",1" Nettippakaraṇa)
ZONES = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--zones=")), None)
R, S = "4-SYSTEM/Skills/cscd-root-text-intake/scripts", "4-SYSTEM/Skills/cscd-commentary-intake/scripts"
T = Path("0-INBOX/temp/kn-comm"); RAW = Path("0-INBOX/raw-data/kn"); CLONE = Path("D:/Work/OpenPecha/tipitaka-xml/romn")
root_draft = f"0-INBOX/temp/kn/pi-kn-{book}.md"
draft = T / f"pi-kn-{book}-atthakatha.md"
comm = Path("1-SOURCES/Commentaries/pi-khuddakanikaya-atthakatha.md")
ROOT = "1-SOURCES/Text/pi-khuddakanikaya.md"


def run(*a, ok=True, show=8):
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", *a], capture_output=True, text=True, encoding="utf-8")
    out = (r.stdout + r.stderr).strip()
    if show:
        print("\n".join("   " + l for l in out.splitlines()[-show:]))
    if ok and r.returncode:
        sys.exit(f"STOP: {Path(a[0]).name} exited {r.returncode}")
    return out, r.returncode


print(f"== book {book}: {label} ({', '.join(stems)})")
assert f"^{book}-0" not in comm.read_text(encoding="utf-8"), f"book {book} is already in {comm}"
xmls = []
for st in stems:
    x = RAW / f"{st}.xml"
    if not x.exists():
        shutil.copyfile(CLONE / f"{st}.xml", x)
        print(f"   copied {x.name} ({x.stat().st_size / 1e6:.2f} MB) from the local tipitaka-xml clone")
    xmls.append(str(x))
jsons, reprinted = [], []
for x in xmls:
    j = T / (Path(x).name.split(".")[0] + ".json")
    o, _ = run(f"{R}/cscd_xml_to_json.py", x, str(j), "--tree", show=1)
    jsons.append(str(j))
    mr = re.search(r"reprinted title lines as text \(\d+\): (.*)", o)
    if mr:
        reprinted += [re.sub(r"^\s*\d+\.\s*", "", t).strip() for t in mr.group(1).split(", ")]
if len(jsons) > 1:
    j = T / ("-".join(Path(p).stem for p in jsons) + ".json")
    run(f"{S}/merge_parts.py", str(j), *jsons, show=2)
    jsons = [str(j)]
segs = json.loads(Path(jsons[0]).read_text(encoding="utf-8"))["segments"]
if not Path(f"0-INBOX/tipitaka-app/{key}.toc.json").exists():
    run(f"{R}/fetch_site.py", "0-INBOX/tipitaka-app", key, "--links", show=1)
# the site also counts empty XML paragraphs (an empty <p rend="gatha1"/>), which the converter drops
_sp = json.loads(Path(f"0-INBOX/tipitaka-app/{key}.text.json").read_text(encoding="utf-8"))["paras"]
site_n = sum(1 for p in _sp if p["t"].strip())
# … or shows a number-only paragraph ("314" alone, the text in the next one) as empty: then all count
site_all = len(_sp)
print(f"   segments {len(segs)} vs site paragraphs {site_n}")
if len(segs) not in (site_n, site_all):
    sys.exit("STOP: segment count differs from tipitaka.app")

# --shape=<script>: a book-specific shape decided by a human (headings only), run as
# "<script> prep <json>" before the build and "<script> post <draft> <json>" after it
SHAPE = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--shape=")), None)
if SHAPE:
    run(SHAPE, "prep", jsons[0], show=2)
    segs = json.loads(Path(jsons[0]).read_text(encoding="utf-8"))["segments"]

# standing decisions
heads = [s for s in segs if s["css_class"] == "heading"]
fm = ["--frontmatter", "Ganthārambhakathā"] if heads and heads[0]["content"].strip() == "Ganthārambhakathā" else []
if fm:
    print("   decision (standing): Ganthārambhakathā -> front matter ^%s-I-0" % book)
# --fm=<heading>: a further front-matter section decided for this book (Itivuttaka: Nidānavaṇṇanā, ^4-II-0)
for extra in [a.split("=", 1)[1] for a in sys.argv if a.startswith("--fm=")]:
    fm += ["--frontmatter", extra]
    print(f"   decision (this book): {extra} -> front matter")
run(f"{S}/build_commentary.py", jsons[0], root_draft, str(draft), "--registered-id", f"kn-{book}-atthakatha",
    "--layer", "atthakatha", "--layer-label", "aṭṭhakathā", "--nikaya", "Khuddakanikāya", *fm,
    *(["--per-section"] if PER_SECTION else []), *(["--zones", ZONES] if ZONES is not None else []), show=1)
t = draft.read_text(encoding="utf-8")
nig = re.search(r"^(#{4,}) (Nigamana(?:kathā|gāthā)) \^([\w-]+)$", t, re.M)   # gāthā: Therīgāthā-aṭṭhakathā
if nig and not re.search(r"^#+ ", t[nig.end():], re.M):
    tops = [int(m.group(1)) for m in re.finditer(rf"^### .* \^{book}-(\d+)-0$", t, re.M)]
    new = f"### {nig.group(2)} ^{book}-{max(tops) + 1}-0"
    shutil.copyfile(draft, T / f"pi-kn-{book}-atthakatha.xmllevels.md")
    draft.write_text(t.replace(nig.group(0), new), encoding="utf-8")
    print(f"   decision (standing): {nig.group(0)}  ->  {new}")
elif nig:
    sys.exit("STOP: a Nigamanakathā that is not the last heading — needs a human decision")
if SHAPE:
    run(SHAPE, "post", str(draft), jsons[0], show=2)

# the commentary's tree must line up with the root's: same heading IDs for the same sections
H = re.compile(r"^(#+) (.*) \^([\w-]+)$")
rh = {m.group(3): m.group(2) for m in map(H.match, Path(root_draft).read_text(encoding="utf-8").split("\n")) if m}
stem = lambda s: re.sub(r"[^a-z]", "", s.lower().replace("ṃ", "m").replace("ā", "a").replace("ī", "i").replace("ū", "u"))[:4]
ch = [(len(m.group(1)), m.group(3), m.group(2)) for m in map(H.match, draft.read_text(encoding="utf-8").split("\n")) if m]
body = [(l, i, t) for l, i, t in ch if l >= 3 and "-I" not in i and not t.startswith("Nigamana")]
match = [(l, i, t) for l, i, t in body if i in rh and stem(rh[i]) == stem(t)]
top_bad = [(i, t, rh.get(i)) for l, i, t in body if l == 3 and (l, i, t) not in match]
print(f"   tree vs root: {len(match)}/{len(body)} headings have the root's ID and title; '###' not matching: {top_bad[:4]}")
# --accept-tree: below 90% only where the misses are reviewed as the commentary grouping sections
# (reported in 0-INBOX/pi-kn-commentary-report.md); every '###' must still match
if top_bad or (len(match) < 0.9 * len(body) and "--accept-tree" not in sys.argv):
    sys.exit("STOP: the commentary's contents tree does not line up with the root's — review before joining")

ps = (["--per-section"] if PER_SECTION else []) + (["--zones", ZONES] if ZONES is not None else [])
v, _ = run(f"{S}/verify_commentary.py", str(draft), root_draft, *xmls, *ps, show=3)
h, _ = run(f"{R}/check_headings.py", str(draft), *xmls, show=1, ok=False)
c, _ = run(f"{S}/compare_site_commentary.py", str(draft), "0-INBOX/tipitaka-app", key, rkey, "--all", *(["--per-section"] if PER_SECTION else []), *(["--zones", ZONES] if ZONES is not None else []), show=6, ok=False)
unres = json.loads((T / f"pi-kn-{book}-atthakatha.unresolved.json").read_text(encoding="utf-8"))
# reviewed exceptions (reported in 0-INBOX/pi-kn-commentary-report.md):
#  --accept-unresolved=<printed>[,…]: a citation reviewed as a source slip, left unlinked (Rule 2)
#  a site "tree delete" of exactly the reprinted part-opening lines the converter kept as text (Rule 4)
acc = [x for a in sys.argv if a.startswith("--accept-unresolved=") for x in a.split("=", 1)[1].split(",")]
left = [u for u in unres.get("unresolved", []) if u[0] not in acc]
n_unres = len(left)
probs = [l.strip()[2:] for l in c.splitlines() if l.strip().startswith("- ")]
# an empty site paragraph that carries a printed number (an empty <p rend="gatha1"/> after its
# hangnum, as in the roots): the vault gives the number and its link to the verse that follows
site_paras = json.loads(Path(f"0-INBOX/tipitaka-app/{key}.text.json").read_text(encoding="utf-8"))["paras"]
dtext = draft.read_text(encoding="utf-8")
def empty_para_ok(p):
    if p == "text delete: site [''] | md []":
        return True
    m = re.match(r"site link commentary para (\d+) -> root (\S+): md scope None$", p)
    if not m or site_paras[int(m.group(1))]["t"].strip():
        return False
    # "N." on the next verse, or the number alone as its own block ("314 ^10-1171")
    return re.search(rf"#\^{book}-(?:[\w]+-)?{re.escape(m.group(2))}\]\]\n\n{re.escape(m.group(2))}(?:\.|\s+\^)", dtext) is not None
emp = [p for p in probs if empty_para_ok(p)]
if emp:
    print(f"   site: {len(emp)} difference(s) from empty numbered paragraphs, linked on the next verse instead")
probs = [p for p in probs if p not in emp]
# a number-only paragraph ("314", its dot opening the next one): the site shows it empty
num_only = [p for p in probs if re.fullmatch(r"text replace: site \[''\] \| md \['\d+'\]", p)]
# a per-section root (each vagga numbered from 1): tipitaka.app looks a printed number up across
# the whole root book, so its number link can land in another vagga. Accepted when the site's own
# gloss links for that commentary paragraph name the vault's vagga; when it has none and the vault
# links the same number in the commentary's current vagga; or for a reviewed unlinked citation.
sec_art = []
if PER_SECTION:
    import ast
    gl = {}
    for l in json.loads(Path(f"0-INBOX/tipitaka-app/{key}.links.json").read_text(encoding="utf-8")):
        if l["src"] == "gloss" and l["k"].count("-") >= 2:
            gl.setdefault(l["i"], set()).add(l["k"].split("-")[2])

    def sec_ok(p):
        m = re.match(r"site link commentary para (\d+) -> root (\S+): md scope (.*)$", p)
        if not m:
            return False
        i, n = int(m.group(1)), m.group(2)
        scope = ast.literal_eval(m.group(3)) if m.group(3) != "None" else None
        if not scope:
            return f"{site_paras[i].get('n')}." in acc
        secs = {s.split("-")[1] for s in scope}
        if i in gl:
            return secs <= gl[i]
        return all(s.split("-")[-1] == n for s in scope[:1])
    sec_art = [p for p in probs if sec_ok(p)]
    if sec_art:
        print(f"   site: {len(sec_art)} number link(s) the site resolved in another vagga "
              f"(the vault's vagga is the one the site's own gloss links name)")
probs = [p for p in probs if p not in num_only and p not in sec_art]
site_ok = c.rstrip().endswith("PASS") or not probs or (probs and all(
    p.startswith("tree delete: site [") and p.endswith("| md []")
    and all(t in reprinted for t in re.findall(r"'([^']+)'", p.split("|")[0])) for p in probs))
if site_ok and not c.rstrip().endswith("PASS"):
    print(f"   site: accepted, only the reprinted part-opening lines differ ({probs})")
# --text-heading=<title>: an XML heading turned into text by a human decision (Apadāna-aṭṭhakathā:
# "Therāpadānaṃ"); check_headings.py may then differ only by deleting exactly that title
th = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--text-heading=")]
hd = [l.strip() for l in h.splitlines()[1:] if l.strip()]
heads_ok = "ALL MATCH" in h or (th and hd and all(
    re.fullmatch(r"delete \[(.*)\] \| \[\]", l) and all(x in th for x in re.findall(r"'([^']+)'", l)) for l in hd))
if heads_ok and "ALL MATCH" not in h:
    print(f"   headings: accepted, only {th} differ (decided as text)")
ok = v.rstrip().endswith("PASS") and heads_ok and site_ok and n_unres == 0
print(f"== checks: verify {'PASS' if v.rstrip().endswith('PASS') else 'FAIL'}, headings "
      f"{'ALL MATCH' if 'ALL MATCH' in h else ('accepted' if heads_ok else 'MISMATCH')}, site {'PASS' if c.rstrip().endswith('PASS') else ('accepted' if site_ok else 'FAIL')}, unresolved {n_unres}")
if not ok:
    sys.exit("STOP: not joining — review the output above")
if DRY:
    sys.exit(0)

# join (step 10): merge, split proof, links
out = T / "kn-atthakatha.join.md"
rl = f"{root_draft}={ROOT}"
run(f"{R}/merge_volumes.py", str(out), str(comm), str(draft), "--title", "Khuddakanikāya-aṭṭhakathā",
    "--registered-id", "kn-atthakatha", "--root-text", ROOT, "--relink", rl, "--label", label, show=3)
sp, _ = run(f"{R}/merge_volumes.py", "--split", str(out), str(comm), str(draft), "--relink", rl, show=1)
if "SPLIT OK" not in sp:
    sys.exit("STOP: split proof failed")
j = out.read_text(encoding="utf-8")
rid = set(re.findall(r"\s\^([\w-]+)\s*$", Path(ROOT).read_text(encoding="utf-8"), re.M))
links = re.findall(r"!\[\[([^\]#]+)#\^([\w-]+)\]\]", j)
bad = [l for l in links if l[0] != ROOT or l[1] not in rid]
ids = re.findall(r"\s\^([\w-]+)\s*$", j.split("\n---\n", 1)[1], re.M)
print(f"   joined: {len(links)} links, broken {len(bad)}; {len(ids)} block IDs, unique {len(ids) == len(set(ids))}")
if bad or len(ids) != len(set(ids)):
    sys.exit("STOP: joined file has broken links or duplicate IDs")
(T / "backups").mkdir(exist_ok=True)
shutil.copyfile(comm, T / "backups" / f"pi-khuddakanikaya-atthakatha.before-{book}.md")
shutil.copyfile(out, comm)
print(f"== book {book} joined into {comm}")
