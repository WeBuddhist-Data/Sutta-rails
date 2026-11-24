"""Test the heading-number change in the intake: rebuild sample volumes with the
skill's own steps, run its checks, and compare every heading's text, in order,
with the corrected vault file.

usage (vault root): python -I -X utf8 0-INBOX/sutta-review/test_build.py
"""
import re, subprocess, sys
from pathlib import Path

PY = [sys.executable, "-I", "-X", "utf8"]
R = "4-SYSTEM/Skills/cscd-root-text-intake/scripts"
C = "4-SYSTEM/Skills/cscd-commentary-intake/scripts"
J = "4-SYSTEM/Skills/json-to-source-text/converters/tipitaka_org_book.py"
T = Path("0-INBOX/sutta-review/test"); T.mkdir(exist_ok=True)
ok = True


def run(*a, check=True):
    p = subprocess.run([*PY, *a], capture_output=True, text=True, encoding="utf-8")
    out = (p.stdout + p.stderr).strip()
    if check and p.returncode:
        print("   FAILED:", " ".join(a[:2])); print("   " + out.replace("\n", "\n   ")[-3000:])
        raise SystemExit(1)
    return p.returncode, out


def heads(path, book_prefix=None):
    """Heading texts in order (### and deeper), number included; optionally only one book's."""
    out = []
    for l in Path(path).read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^(#{3,})\s+(.*?)\s+\^([\w-]+)\s*$", l)
        if m and (book_prefix is None or m.group(3).startswith(book_prefix)):
            out.append(re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2)))
    return out


def compare(name, built, vault):
    global ok
    import difflib
    ops = [o for o in difflib.SequenceMatcher(None, built, vault, autojunk=False).get_opcodes() if o[0] != "equal"]
    numbered = sum(1 for h in built if re.match(r"^\(?\d", h))
    print(f"   headings: built {len(built)}, vault {len(vault)}, with a printed number {numbered}; "
          + ("ALL IDENTICAL" if not ops else f"{len(ops)} DIFFERENCES"))
    for op, a, b, c, d in ops[:8]:
        print("     ", op, built[a:b][:3], "|", vault[c:d][:3])
    ok = ok and not ops


def root(stem, book, nk, tree, vault, nikaya, label):
    global ok
    print(f"== root {stem} ({'tree' if tree else 'tipitaka_org_book'})")
    xml = f"0-INBOX/raw-data/{nk}/{stem}.mul.xml"
    js, md, draft = T / f"{stem}.json", T / f"{stem}.md", T / f"pi-{nk}-{book}.md"
    run(f"{R}/cscd_xml_to_json.py", xml, str(js), *(["--tree"] if tree else []))
    run(f"{R}/tree_to_md.py" if tree else J, str(js), str(md))
    draft.write_text(md.read_text(encoding="utf-8"), encoding="utf-8")
    run(f"{R}/prepare_ids.py", str(book), str(draft))
    lines = draft.read_text(encoding="utf-8").split("\n")
    h2 = next(i for i, l in enumerate(lines, 1) if l.startswith("## "))
    run(f"{R}/apply.py", "apply", str(draft), "--zones", f"1=@{h2}")
    run(f"{R}/heading_ids.py", str(book), str(draft))
    run(f"{R}/set_frontmatter.py", str(draft), stem, nikaya, label)
    rc, out = run(f"{R}/verify.py", str(book), str(draft), xml, *(["--tree"] if tree else []), check=False)
    print("   verify.py:", out.splitlines()[-1] if out else rc); ok = ok and rc == 0
    rc, out = run(f"{R}/check_headings.py", str(draft), xml, check=False)
    print("   check_headings.py:", out.splitlines()[0]); ok = ok and rc == 0
    compare(stem, heads(draft), heads(vault, f"{book}-"))
    return draft


dn1 = root("s0101m", 1, "dn", False, "1-SOURCES/Text/pi-dighanikaya.md", "Dīghanikāya", "Sīlakkhandhavaggapāḷi")
root("s0401m", 1, "an", True, "1-SOURCES/Text/pi-anguttaranikaya.md", "Aṅguttaranikāya", "Ekakanipātapāḷi")

print("== commentary s0101a (DN aṭṭhakathā vol 1, against the test root above)")
xml = "0-INBOX/raw-data/dn/s0101a.att.xml"
js, out_md = T / "s0101a.json", T / "pi-dn-1-atthakatha.md"
run(f"{R}/cscd_xml_to_json.py", xml, str(js))
run(f"{C}/build_commentary.py", str(js), dn1.as_posix(), out_md.as_posix(), "--registered-id", "test", "--layer", "atthakatha",
    "--layer-label", "aṭṭhakathā", "--nikaya", "Dīghanikāya")
rc, out = run(f"{C}/verify_commentary.py", out_md.as_posix(), dn1.as_posix(), xml, check=False)
print("   verify_commentary.py (exit", rc, "):\n     " + out.replace("\n", "\n     ")[:1500]); ok = ok and rc == 0
rc, out = run(f"{R}/check_headings.py", out_md.as_posix(), xml, check=False)
print("   check_headings.py:", out.splitlines()[0]); ok = ok and rc == 0
compare("s0101a", heads(out_md), heads("1-SOURCES/Commentaries/pi-dighanikaya-atthakatha.md", "1-"))
print("\nRESULT:", "ALL PASS" if ok else "PROBLEMS")
