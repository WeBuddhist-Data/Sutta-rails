"""In each file's frontmatter source_description, replace the stripped-numbers phrase
with what is now true. Only that phrase in the frontmatter changes."""
import re, sys
OLD = "chapter numbers stripped from headings"
NEW = "printed heading numbers kept in the headings, as in the XML"
for f in sys.argv[1:]:
    t = open(f, encoding="utf-8", newline="").read()
    end = t.index("\n---\n", 4)
    fm, body = t[:end], t[end:]
    n = fm.count(OLD)
    line = next(l for l in fm.split("\n") if l.startswith("source_description:"))
    if n != 1 or OLD not in line:
        print(f"{f}: SKIPPED, phrase found {n} times"); continue
    open(f, "w", encoding="utf-8", newline="").write(fm.replace(OLD, NEW) + body)
    print(f"{f}: updated")
