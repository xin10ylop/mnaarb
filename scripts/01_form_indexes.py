"""Download EDGAR quarterly form indexes and keep only M&A anchor filings."""
import sys
from datetime import date
sys.path.insert(0, ".")
from mnaarb import edgar

start = int(sys.argv[1]) if len(sys.argv) > 1 else 2010
today = date.today()
n = 0
for y in range(start, today.year + 1):
    for q in range(1, 5):
        if (y, q) > (today.year, (today.month - 1) // 3 + 1):
            break
        rows = edgar.form_index(y, q, forms=edgar.ANCHOR_FORMS + ("SC TO-T",))
        n += len(rows)
        print(y, q, len(rows), flush=True)
print("total anchor rows", n)
