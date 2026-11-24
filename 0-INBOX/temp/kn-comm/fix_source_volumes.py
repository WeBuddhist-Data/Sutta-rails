"""Rebuild source_volumes of the KN aṭṭhakathā from its source_filename list
(one URL per volume file, same order). Only the source_volumes block changes;
CRLF kept; the body after the frontmatter is checked byte-identical."""
import re, sys, shutil
from pathlib import Path

p = Path(sys.argv[1])
raw = p.read_bytes()
t = raw.decode("utf-8")
assert "\r\n" in t and t.count("\n") == t.count("\r\n"), "not pure CRLF"
head, sep, body = t.partition("\r\n---\r\n")
assert head.startswith("---\r\n") and sep
files = re.search(r"^source_filename: \[(.*)\]\r$", head, re.M).group(1).split(", ")
base = "https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn/"
m = re.search(r"^source_volumes:\r\n(?:  - .*\r\n)+", head, re.M)
old = re.findall(r'"(https?://[^"]+)"', m.group(0))
new = [base + f for f in files]
assert all(u in new for u in old), "an existing URL is not in source_filename"
added = [u for u in new if u not in old]
block = "source_volumes:\r\n" + "".join(f'  - "{u}"\r\n' for u in new)
head2 = head[:m.start()] + block + head[m.end():]
out = head2 + sep + body
assert out.partition("\r\n---\r\n")[2] == body
assert out.count("\n") == out.count("\r\n")
bk = Path(sys.argv[2]); bk.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, bk)
p.write_bytes(out.encode("utf-8"))
print(f"source_volumes: {len(old)} -> {len(new)} URLs; added {len(added)}:")
for u in added: print("  ", u.rsplit("/", 1)[1])
print("body unchanged; CRLF only; backup:", bk)
