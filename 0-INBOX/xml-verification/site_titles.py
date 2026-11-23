"""Compare the sequence of heading titles (numbers stripped) of one vault book with a
tipitaka.app contents tree, ignoring the site's keys (which follow printed sutta numbers).

usage: python site_titles.py <file.md> <site.toc.json> <book-number>
"""
import re, sys, json, difflib
sys.stdout.reconfigure(encoding="utf-8")
md, js, book = sys.argv[1], sys.argv[2], sys.argv[3]
strip = lambda t: re.sub(r"^\s*[\d\-–]+\.\s*", "", re.sub(r"^\s*\(\d+\)\s*(?=\d+\.)", "", t)).replace("‘‘", '"').replace("’’", '"').strip()
txt = open(md, encoding="utf-8").read().replace("\r\n", "\n")
vault = [strip(re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2)))
         for m in re.finditer(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$", txt, flags=re.M)
         if m.group(3).startswith(book + "-") and m.group(3) != book + "-0"]
site = [strip(n["title"]) for n in json.load(open(js, encoding="utf-8"))]
sm = difflib.SequenceMatcher(None, site, vault, autojunk=False)
diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]
print(f"site {len(site)} titles, vault {len(vault)} headings in book {book}; differences: {len(diffs)}")
for t, i1, i2, j1, j2 in diffs[:25]:
    print(f"  {t}: site {site[i1:i2][:4]} | vault {vault[j1:j2][:4]}")
