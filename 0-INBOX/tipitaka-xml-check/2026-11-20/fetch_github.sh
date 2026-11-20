#!/usr/bin/env bash
# Download every XML named in 1-SOURCES frontmatter from VipassanaTech/tipitaka-xml (romn/)
# into $1 and compare byte for byte with 0-INBOX/raw-data. Read-only for the vault.
G=$1; mkdir -p $G; cd /Users/lobsangtseten/Desktop/Suttapitaka/Sutta-rails
echo "tipitaka-xml HEAD: $(git ls-remote https://github.com/VipassanaTech/tipitaka-xml HEAD | cut -c1-12)"
files=$(grep -h '^source_filename:' 1-SOURCES/Text/*.md 1-SOURCES/Commentaries/*.md | sed 's/source_filename: //; s/[][]//g' | tr ',' '\n' | tr -d ' ' | sort -u)
n=0; d=0
for f in $files; do n=$((n+1))
  curl -sfL -o $G/$f "https://raw.githubusercontent.com/VipassanaTech/tipitaka-xml/main/romn/$f" || { echo "DOWNLOAD FAIL $f"; d=$((d+1)); continue; }
  l=$(ls 0-INBOX/raw-data/*/$f 2>/dev/null | head -1)
  if [ -z "$l" ]; then echo "NO LOCAL COPY $f"; d=$((d+1)); elif ! cmp -s $l $G/$f; then echo "DIFFERS $l"; d=$((d+1)); fi
done
echo "XML files: $n, problems: $d"
