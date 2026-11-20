#!/usr/bin/env bash
# Run every check; outputs go to ./out/. Read-only for 1-SOURCES.
# Usage: bash run_all.sh <scratch-dir> [site]   (downloads go to <scratch-dir>/gh and <scratch-dir>/site; "site" = only the tipitaka.app steps)
export SSL_CERT_FILE=${SSL_CERT_FILE:-/etc/ssl/cert.pem}   # some python3 installs ship no CA bundle
H=$(cd "$(dirname "$0")" && pwd); W=$1; O=$H/out; mkdir -p $O $W
V=/Users/lobsangtseten/Desktop/Suttapitaka/Sutta-rails; R=$V/4-SYSTEM/Skills/cscd-root-text-intake/scripts
[ "$2" = site ] || { bash $H/fetch_github.sh $W/gh > $O/1-github.txt 2>&1
bash $H/verify_xml_all.sh $W/gh > $O/2-verify-xml.txt 2>&1
python3 -I $H/indep.py $V $W/gh > $O/3-independent.txt 2>&1; }
cd $V; keys=$(ls 0-INBOX/tipitaka-app | sed -E 's/\.(toc|text|links)\.json$//' | sort -u | grep -v '^tika2-')
python3 -I $R/fetch_site.py $W/site $keys --links > $O/4-site-fetch.txt 2>&1
python3 -I $H/fetch_tika2.py $W/site tika2-dn-1 tika-dn >> $O/4-site-fetch.txt 2>&1
for f in $W/site/*; do c=$V/0-INBOX/tipitaka-app/$(basename $f); if [ ! -f $c ]; then echo "NEW (not in cache) $(basename $f)"; elif ! cmp -s $f $c; then echo "DIFFERS from cache $(basename $f)"; fi; done >> $O/4-site-fetch.txt
echo "site files fetched: $(ls $W/site | wc -l)" >> $O/4-site-fetch.txt
bash $H/site_all.sh $W/site > $O/5-site-compare.txt 2>&1
for f in 1-SOURCES/Commentaries/*-atthakatha.md; do python3 -I $H/content_links.py $f $(grep -m1 '^root_text:' $f | awk '{print $2}'); done > $O/6-meaning-links.txt 2>&1
