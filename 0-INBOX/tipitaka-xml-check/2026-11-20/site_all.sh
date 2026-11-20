#!/usr/bin/env bash
# Compare every 1-SOURCES file with tipitaka.app data in $1 (fetch_site.py --links output). Read-only.
A=$1; cd /Users/lobsangtseten/Desktop/Suttapitaka/Sutta-rails
R=4-SYSTEM/Skills/cscd-root-text-intake/scripts; S=4-SYSTEM/Skills/cscd-commentary-intake/scripts; C1=1-SOURCES/Commentaries
last() { tail -1 | tr -s ' ' | cut -c1-170; }
root() { echo "pi-$1 | $(python3 -I $R/compare_site.py $2 1-SOURCES/Text/pi-$1.md $A/$3.text.json $A/$3.toc.json $4 | last)"; }
atta() { echo "pi-$1-atthakatha | $(python3 -I $S/compare_site_commentary.py $C1/pi-$1-atthakatha.md $A atta-$2 $2 $3 | last)"; }
tika() { echo "pi-$1-tiika | $(python3 -I $S/compare_site_commentary.py $C1/pi-$1-tiika.md $A tika-$2 $2 $C1/pi-$1-atthakatha.md atta-$2 | last)"; }
for C in dn mn sn; do case $C in sn) V="1 2 3 4 5";; *) V="1 2 3";; esac
 for b in $V; do root $C-$b $b $C-$b; atta $C-$b $C-$b; tika $C-$b $C-$b; done; done
echo "pi-dn-1-abhinavatiika | $(python3 -I $S/compare_site_commentary.py $C1/pi-dn-1-abhinavatiika.md $A tika2-dn-1 dn-1 $C1/pi-dn-1-atthakatha.md atta-dn-1 | last)"
for b in $(seq 1 11); do root an-$b $b an-$b; atta an-$b an-$b; tika an-$b an-$b; done
root kn-1 1 kn-khp --per-section; atta kn-1 kn-khp --per-section
root kn-2 2 kn-dhp; atta kn-2 kn-dhp
