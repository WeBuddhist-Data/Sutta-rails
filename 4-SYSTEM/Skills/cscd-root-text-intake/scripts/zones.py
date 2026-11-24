"""zones.py — the numbering-run rules shared by apply.py, verify.py and compare_site.py.

A book's printed paragraph numbers fall into runs (zones). Given the numbers in reading order,
each with a flag "a heading came between this number and the previous one", assign() returns
the run (1-based) each number belongs to:

- New run: the number is 1 and either the previous number was not 1, or a heading lies between
  them (a 1 right after a 1 with no heading between is the same number printed twice: Nx1).
- Resume: a number that breaks the current run (not prev, not prev+1) but is exactly the next
  number of the run just before it goes back to that run. CSCD Nettippakaraṇa: the main count
  1-4, then the Hārasaṅkhepa/Dvādasapada verses 1-26, then the main count again from 5.
Anything else that breaks a run (a skip, a misprint) stays in the run; callers report it.
"""


def span(printed):
    a, _, b = str(printed).partition("-")
    return int(a), int(b or a)


def assign(seq):
    """seq: iterable of (printed_number, heading_since). Returns [run index, …]."""
    last = []          # last number of each run so far
    cur, prev, out = 0, None, []
    for printed, heading_since in seq:
        a, b = span(printed)
        if cur == 0 or (a == 1 and (prev != 1 or heading_since)):
            last.append(0)
            cur = len(last)
        elif a not in (prev, prev + 1) and cur >= 2 and a == last[cur - 2] + 1:
            cur -= 1                                   # resume the run before this one
        out.append(cur)
        last[cur - 1] = b
        prev = b
    return out
