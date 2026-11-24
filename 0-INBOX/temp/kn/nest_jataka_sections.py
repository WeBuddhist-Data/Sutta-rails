"""Jātaka, Mahānipāta (KN book 14, nipāta 22): nest the sections of the Vidhura- and
Vessantarajātaka under their jātaka (human decision 2026-11-23).

The CSCD XML prints the 8 kaṇḍas of Vidhurajātakaṃ (9) and the 12 sections of
Vessantarajātakaṃ (10) as siblings of the jātaka headings, which are then empty;
tipitaka.app nests them. Only 21 heading lines change (the 20 sections, and Vessantara's ID) ('#' count and ID):

  #### Vidhurajātakaṃ (9) ^14-22-9-0        (unchanged)
  #### Dohaḷakaṇḍaṃ ^14-22-10-0       ->    ##### Dohaḷakaṇḍaṃ ^14-22-9-1-0  … 8 kaṇḍas
  #### Vessantarajātakaṃ (10) ^14-22-18-0 -> #### Vessantarajātakaṃ (10) ^14-22-10-0
  #### Dasavarakathā ^14-22-19-0      ->    ##### Dasavarakathā ^14-22-10-1-0 … 12 sections

usage: python nest_jataka_sections.py <file.md>     (pi-kn-14.md draft or pi-kn.md; in place)
"""
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
p = Path(sys.argv[1])
raw = p.read_bytes().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
lines = raw.split(nl)
H = re.compile(r"^(#+) (.*) \^14-22-(\d+)-0$")

old = {i: H.match(l) for i, l in enumerate(lines) if H.match(l)}
seq = [(i, m.group(2), int(m.group(3))) for i, m in sorted(old.items())]
assert [s for _, _, s in seq] == list(range(1, 31)), "nipāta 22 is not the expected 30 flat headings (already nested?)"
assert seq[8][1] == "Vidhurajātakaṃ (9)" and seq[17][1] == "Vessantarajātakaṃ (10)" and seq[29][1] == "Chakhattiyakammaṃ"
assert all(len(old[i].group(1)) == 4 for i, _, _ in seq)

new = {}
for k, (i, title, _) in enumerate(seq[9:17], 1):
    new[i] = f"##### {title} ^14-22-9-{k}-0"
i, title, _ = seq[17]
new[i] = f"#### {title} ^14-22-10-0"
for k, (i, title, _) in enumerate(seq[18:30], 1):
    new[i] = f"##### {title} ^14-22-10-{k}-0"

for i, l in new.items():
    print(f"  {lines[i]}  ->  {l}")
    lines[i] = l

# each jātaka heading now has its sections right under it (it was empty)
for i, t, _ in (seq[8], seq[17]):
    nxt = next(l for l in lines[i + 1:] if l.strip())
    assert nxt.startswith("##### "), (t, nxt)
out = nl.join(lines)
assert out.count(nl) == raw.count(nl)
ids = re.findall(r"\^([\w-]+)\s*(?:\r?\n|$)", out)
assert len(ids) == len(set(ids)), "duplicate block IDs"
p.write_bytes(out.encode("utf-8"))
print(f"{p}: {len(new)} heading lines changed; all {len(ids)} block IDs unique; no other line touched")
