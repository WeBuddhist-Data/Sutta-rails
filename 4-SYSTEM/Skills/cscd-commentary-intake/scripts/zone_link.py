"""zone_link.py — which root blocks a citation links to, when the root has zones.

A zoned root (cscd-root-text-intake --zones / --zone-labels) has content IDs ^<book>-<zone>-<N>,
or ^<book>-<N> for a plain zone (label ""): the same printed N can exist in several zones
(CSCD Suttanipāta: verse 12 is ^5-1-12, Suttuddāna 12 is ^5-2-12). A commentary follows its root
in order, so a citation goes to the zone whose blocks hold every cited number and lie nearest
after the last linked block (the nearest before it if none lies after). Used by
commentary_converter.py (to link) and verify_commentary.py (to check), so both apply one rule;
tipitaka.app's own links (compare_site_commentary.py) are the independent check.
"""
import re


class ZoneLinker:
    def __init__(self, root_text, book, labels):
        self.book = str(book)
        self.labels = list(labels)
        self.pos = {}                      # root block id -> its position in the root
        self.cover = {lab: {} for lab in self.labels}   # zone -> printed number -> block id
        ids = re.findall(r"\s\^([\w-]+)\s*$", root_text, re.M)
        # a plain zone's prefix "<book>-" also starts every labelled zone's IDs: "19-1-5" (zone 1,
        # block 5) would read as the plain range 1-5. A plain zone takes no ID of a labelled zone.
        labelled = [f"{self.book}-{lab}-" for lab in self.labels if lab]
        for i, rid in enumerate(ids):
            self.pos[rid] = i
            for lab in self.labels:
                pre = f"{self.book}-{lab}-" if lab else f"{self.book}-"
                if not rid.startswith(pre) or (not lab and any(rid.startswith(o) for o in labelled)):
                    continue
                m = re.fullmatch(r"(\d+)(?:-(\d+))?(?:x\d+)?", rid[len(pre):])
                if m and not rid[len(pre):].endswith("-0"):
                    for k in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
                        self.cover[lab].setdefault(k, rid)
        self.last = -1

    def link(self, nums):
        """nums: the cited numbers in order. Returns (block ids, missing) and advances."""
        cands = []
        for lab in self.labels:
            got = []
            for k in nums:
                rid = self.cover[lab].get(k)
                if rid and rid not in got:
                    got.append(rid)
            if got and all(self.cover[lab].get(k) for k in nums):
                cands.append(got)
        if not cands:
            best = max(self.labels, key=lambda lab: sum(1 for k in nums if k in self.cover[lab]))
            got = []
            for k in nums:
                rid = self.cover[best].get(k)
                if rid and rid not in got:
                    got.append(rid)
            missing = [f"{self.book}-{best + '-' if best else ''}{k}" for k in nums if k not in self.cover[best]]
            if got:
                self.last = self.pos[got[0]]
            return got, missing
        ahead = [c for c in cands if self.pos[c[0]] >= self.last]
        pick = min(ahead, key=lambda c: self.pos[c[0]]) if ahead else max(cands, key=lambda c: self.pos[c[0]])
        self.last = self.pos[pick[0]]
        return pick, []
