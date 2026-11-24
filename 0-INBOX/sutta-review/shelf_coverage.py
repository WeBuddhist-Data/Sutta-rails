"""Which CSCD Sutta-shelf XML files (romn/s01*–s05*) are in the vault, and which are not.
A file is "in" when some 1-SOURCES file names it in source_filename."""
import glob, re
from pathlib import Path

used = set()
for f in glob.glob("1-SOURCES/*/*.md"):
    fm = Path(f).read_text(encoding="utf-8").split("\n---\n", 1)[0]
    m = re.search(r"^source_filename:\s*\[?(.*?)\]?\s*$", fm, re.M)
    if m:
        used |= {s.strip() for s in m.group(1).split(",") if s.strip()}
shelf = sorted(Path(p).name for p in glob.glob(r"D:\Work\OpenPecha\tipitaka-xml\romn\s0[1-5]*.xml"))
print(f"Sutta shelf in romn/: {len(shelf)} files; in the vault: {sum(s in used for s in shelf)}")
for s in shelf:
    if s not in used:
        t = open(rf"D:\Work\OpenPecha\tipitaka-xml\romn\{s}", "rb").read().decode("utf-16")
        title = re.search(r'<p rend="book">(.*?)</p>|<head rend="book">(.*?)</head>', t)
        print("  NOT IN VAULT:", s, "-", re.sub("<[^>]+>", "", (title.group(1) or title.group(2)) if title else "?"))
print("named in the vault but not in romn/:", sorted(used - set(shelf)) or "none")
