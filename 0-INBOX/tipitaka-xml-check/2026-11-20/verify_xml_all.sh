#!/usr/bin/env bash
# Run the intake skills' verifiers (verify.py, verify_commentary.py, check_headings.py)
# on every 1-SOURCES file against the XML in $1. Read-only.
X=$1; cd /Users/lobsangtseten/Desktop/Suttapitaka/Sutta-rails
R=4-SYSTEM/Skills/cscd-root-text-intake/scripts; S=4-SYSTEM/Skills/cscd-commentary-intake/scripts; T=0-INBOX/temp; C1=1-SOURCES/Commentaries
last() { tail -1 | tr -s ' ' | cut -c1-160; }
hd() { python3 -I $R/check_headings.py "$@" 2>&1 | grep -o 'ALL MATCH\|[0-9]* diff.*' | head -1; }
for C in dn mn sn; do case $C in dn) n=01; V="1 2 3";; mn) n=02; V="1 2 3";; sn) n=03; V="1 2 3 4 5";; esac
 for b in $V; do x=$X/s${n}0${b}m.mul.xml
  echo "pi-$C-$b | $(python3 -I $R/verify.py $b 1-SOURCES/Text/pi-$C-$b.md $x | last) | headings $(hd 1-SOURCES/Text/pi-$C-$b.md $x)"
  for t in a t; do ext=$([ $t = a ] && echo att || echo tik); l=$([ $t = a ] && echo atthakatha || echo tiika); x=$X/s${n}0$b$t.$ext.xml
   echo "pi-$C-$b-$l | $(python3 -I $S/verify_commentary.py $C1/pi-$C-$b-$l.md 1-SOURCES/Text/pi-$C-$b.md $x --unresolved $T/$C-comm/pi-$C-$b-$l.unresolved.json | last) | headings $(hd $C1/pi-$C-$b-$l.md $x)"; done; done; done
echo "pi-dn-1-abhinavatiika | $(python3 -I $S/verify_commentary.py $C1/pi-dn-1-abhinavatiika.md 1-SOURCES/Text/pi-dn-1.md $X/s0104t.nrf.xml $X/s0105t.nrf.xml --unresolved $T/dn-comm/pi-dn-1-abhinavatiika.unresolved.json | last)"
STEMS=(x s0401m s0402m1 s0402m2 s0402m3 s0403m1 s0403m2 s0403m3 s0404m1 s0404m2 s0404m3 s0404m4); VOL=(x 1 2 2 2 3 3 3 4 4 4 4); BK=(x 1 1 2 3 1 2 3 1 2 3 4)
for b in $(seq 1 11); do x=$X/${STEMS[$b]}.mul.xml
 echo "pi-an-$b | $(python3 -I $R/verify.py $b 1-SOURCES/Text/pi-an-$b.md $x --tree | last) | headings $(hd 1-SOURCES/Text/pi-an-$b.md $x)"
 for t in a t; do ext=$([ $t = a ] && echo att || echo tik); l=$([ $t = a ] && echo atthakatha || echo tiika); x=$X/s040${VOL[$b]}$t.$ext.xml
  echo "pi-an-$b-$l | $(python3 -I $S/verify_commentary.py $C1/pi-an-$b-$l.md 1-SOURCES/Text/pi-an-$b.md $x --book ${BK[$b]} --unresolved $T/an-comm/pi-an-$b-$l.unresolved.json | last) | headings $(hd $C1/pi-an-$b-$l.md $x --book ${BK[$b]})"; done; done
for b in 1 2; do s=$([ $b = 1 ] && echo s0501 || echo s0502); ps=(); [ $b = 1 ] && ps=(--per-section)
 echo "pi-kn-$b | $(python3 -I $R/verify.py $b 1-SOURCES/Text/pi-kn-$b.md $X/${s}m.mul.xml --tree "${ps[@]}" | last) | headings $(hd 1-SOURCES/Text/pi-kn-$b.md $X/${s}m.mul.xml)"
 echo "pi-kn-$b-atthakatha | $(python3 -I $S/verify_commentary.py $C1/pi-kn-$b-atthakatha.md 1-SOURCES/Text/pi-kn-$b.md $X/${s}a.att.xml --unresolved $T/kn-comm/pi-kn-$b-atthakatha.unresolved.json "${ps[@]}" | last) | headings $(hd $C1/pi-kn-$b-atthakatha.md $X/${s}a.att.xml)"; done
