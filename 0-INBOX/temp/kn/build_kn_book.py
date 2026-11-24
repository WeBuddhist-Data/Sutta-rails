"""Run cscd-root-text-intake steps 3-9 for one Khuddakanikāya book (tree mode), and stop where
the skill says a human must decide. Draft: 0-INBOX/temp/kn/pi-kn-<book>.md.

usage: python build_kn_book.py <book> <stem> <site-key> "<label>"      (from the vault root)
  e.g. python build_kn_book.py 4 s0504m kn-iti "Itivuttaka"
Stops (exit 1) on: a css class outside the allowed set, more than one numbering run or an
anomaly in `apply.py audit`, or any check that does not PASS / ALL MATCH.
"""
import json, re, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
book, stem, key, label = sys.argv[1:5]
# --zones: a book with more than one numbering run, each its own zone (human decision,
# skill Rule 3): run k gets ^<book>-k-<N>; verify/compare_site run with --zoned
ZONES = "--zones" in sys.argv or "--zone-labels" in sys.argv
# --zone-labels M,1,2,3: run k's zone label is the k-th label instead of k (human decision;
# Paṭisambhidāmagga: the Mātikā is ^17-M-N, the three vaggas ^17-1-N … ^17-3-N)
LABELS = sys.argv[sys.argv.index("--zone-labels") + 1].split(",") if "--zone-labels" in sys.argv else None
ZFLAG = ["--zone-labels", ",".join(LABELS)] if LABELS else ["--zoned"]
S = "4-SYSTEM/Skills/cscd-root-text-intake/scripts"
D = Path("0-INBOX/temp/kn"); D.mkdir(parents=True, exist_ok=True)
# --per-section: each '###' section numbers from 1 (human decision): ^<book>-<section>-<N>
PER_SECTION = "--per-section" in sys.argv
# a book cut from the CSCD volumes by make_kn_book_xml.py lives in 0-INBOX/temp/kn/xml/
xml = next(iter(sorted(Path("0-INBOX/raw-data/kn").glob(f"{stem}.*.xml"))), None) or Path(f"0-INBOX/temp/kn/xml/{stem}.xml")
draft = D / f"pi-kn-{book}.md"
ALLOWED = {"centered", "nikaya", "book", "chapter", "subhead", "bodytext", "gatha1", "gatha2", "gatha3",
           "gathalast", "unindented", "indent", "heading", "sutta"}

def run(*args, show=True):
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", *args], capture_output=True, text=True, encoding="utf-8")
    out = (r.stdout + r.stderr).strip()
    if show and out:
        print("\n".join("   " + l for l in out.splitlines()[-12:]))
    if r.returncode:
        sys.exit(f"STOP: {args[0]} exited {r.returncode}")
    return out

print(f"== book {book} {stem} ({label})")
print("-- 3 xml -> json"); run(f"{S}/cscd_xml_to_json.py", str(xml), str(D / f"{stem}.json"), "--tree")
css = json.loads(run("4-SYSTEM/Skills/json-to-source-text/json_inspector.py", str(D / f"{stem}.json"), show=False)) \
    if False else None
segs = json.loads((D / f"{stem}.json").read_text(encoding="utf-8"))
items = segs if isinstance(segs, list) else segs.get("segments") or segs.get("data") or []
classes = {}
for s in items:
    c = s.get("css_class") if isinstance(s, dict) else None
    if c: classes[c] = classes.get(c, 0) + 1
print(f"   css classes: {classes}")
bad = set(classes) - ALLOWED
if bad:
    sys.exit(f"STOP: css classes outside the allowed set: {sorted(bad)} — decide their role first")
print("-- 4 json -> md"); run(f"{S}/tree_to_md.py", str(D / f"{stem}.json"), str(D / f"{stem}.md"))
draft.write_bytes((D / f"{stem}.md").read_bytes())
run(f"{S}/prepare_ids.py", book, str(draft))
print("-- 5a audit")
audit = run(f"{S}/apply.py", "audit", str(draft), show=False)
runs = re.findall(r"Run \d+: lines (\d+)-(\d+) \((\d+) items, ([^)]*)\)", audit)
print(f"   {re.search(r'Detected book number: .*', audit).group(0) if 'Detected book' in audit else 'book number not detected'}; runs: {runs}")
# A skip is fine only where the XML prints the same skip (elided "…pe…" verses still counted).
xt = xml.read_text(encoding="utf-16")
sys.path.insert(0, S)
import zones  # noqa: E402  (the run rules apply.py uses)
seq, hs = [], False
for m in re.finditer(r'<head |<p rend="(?:subhead|subsubhead|title|chapter|book)"|<hi rend="paranum">([\d\-–]+)</hi>', xt):
    if m.group(1) is None:
        hs = True
    else:
        seq.append((m.group(1).replace("–", "-"), hs)); hs = False
last, xml_gaps = {}, set()
for (p, _h), z in zip(seq, zones.assign(seq)):
    a, b = zones.span(p)
    pn = last.get(z)
    if pn is not None and a not in (pn, pn + 1):
        # (a number printed twice, a == pn, is a repeat: ^…Nx1, not a gap)
        xml_gaps.add((pn + 1, p))
    last[z] = b
anom = set((int(e), g) for e, g in re.findall(r"ANOMALY at L\d+: expected (\d+), got ([\d-]+)", audit))
if anom:
    print(f"   {len(anom)} skip(s); all printed the same in the XML: {anom == xml_gaps}")
if (anom and anom != xml_gaps) or (len(runs) != 1 and not ZONES and not PER_SECTION) or f"Detected book number: {book}" not in audit:
    print(audit[-2500:])
    sys.exit("STOP: numbering is not a single clean run — show it to the human (skill Rule 3)")
dl = draft.read_text(encoding="utf-8").split("\n")
h2 = next(i for i, l in enumerate(dl, 1) if l.startswith("## "))
spec = f"1=@{h2}"
if ZONES:
    # zone k opens at the '##' line (run 1) or at the last heading before the run (else
    # the run's first line itself, which keeps its content ID: '@' only marks a heading)
    parts = []
    for k, (s, *_r) in enumerate(runs, 1):
        hd = [i for i, l in enumerate(dl[:int(s) - 1], 1) if l.startswith("#")]
        at = h2 if k == 1 else (hd[-1] if hd and hd[-1] > int(runs[k - 2][1]) else None)
        lab = LABELS[k - 1] if LABELS else k
        parts.append(f"{k}={lab}" + (f"@{at}" if at else ""))
    assert not LABELS or len(LABELS) == len(runs), f"{len(runs)} runs but labels {LABELS}"
    spec = ",".join(parts)
    print(f"   zones: {spec}")
print("-- 5b apply"); run(f"{S}/apply.py", "apply", str(draft), *(["--zone-per-section"] if PER_SECTION else ["--zones", spec]), show=False)
print("-- 6 heading ids"); run(f"{S}/heading_ids.py", book, str(draft))
print("-- 7 frontmatter"); run(f"{S}/set_frontmatter.py", str(draft), stem, "Khuddakanikāya", label)
print("-- 8 verify")
v = run(f"{S}/verify.py", book, str(draft), str(xml), "--tree", *(ZFLAG if ZONES else ["--per-section"] if PER_SECTION else []))
h = run(f"{S}/check_headings.py", str(draft), str(xml))
print("-- 9 tipitaka.app")
if not Path(f"0-INBOX/tipitaka-app/{key}.toc.json").exists():
    run(f"{S}/fetch_site.py", "0-INBOX/tipitaka-app", key)
c = run(f"{S}/compare_site.py", book, str(draft), f"0-INBOX/tipitaka-app/{key}.text.json", f"0-INBOX/tipitaka-app/{key}.toc.json",
            *(ZFLAG if ZONES else ["--per-section"] if PER_SECTION else []))
ok = v.rstrip().endswith("PASS") and "ALL MATCH" in h and c.rstrip().endswith("PASS")
print(f"== RESULT book {book}: verify {'PASS' if v.rstrip().endswith('PASS') else 'FAIL'}, headings "
      f"{'ALL MATCH' if 'ALL MATCH' in h else 'MISMATCH'}, site {'PASS' if c.rstrip().endswith('PASS') else 'FAIL'}")
sys.exit(0 if ok else 1)
