"""Add deals announced in the last ~N days that have no merger proxy / 14D-9 yet.

Merger proxies arrive 3-8 weeks after the announcement, so the anchor-based builder misses the
most recent deals, which are the only ones with free 1-minute / 5-minute bars. Here the anchor is
the target's own announcement-day filing (DEFA14A, SC14D9C, SC TO-C, 425).
usage: python scripts/02b_recent_events.py [days=75]
"""
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, ".")
from mnaarb import edgar, events

days = int(sys.argv[1]) if len(sys.argv) > 1 else 75
since = date.today() - timedelta(days=days)
quarters = sorted({(d.year, (d.month - 1) // 3 + 1) for d in (since, date.today())})
rows = []
for y, q in quarters:
    rows += [r for r in edgar.announce_index(y, q) if r["date"] >= since.isoformat()]
listed = edgar.listed_ciks()
out = Path("data/events.csv")
with open(out) as f:
    existing = list(csv.DictReader(f))
have = {(r["cik"], r["pr_date"]) for r in existing}
recent_ciks = {r["cik"] for r in existing if (r["pr_date"] or "0") >= since.isoformat()}
first: dict[str, dict] = {}
for r in sorted(rows, key=lambda r: r["date"]):
    if int(r["cik"]) in listed and r["cik"] not in recent_ciks:
        first.setdefault(r["cik"], r)
deals = [{"cik": r["cik"], "company": r["company"], "anchor_form": r["form"],
          "anchor_date": date.fromisoformat(r["date"]), "deal_id": f"{r['cik']}-{r['date']}"} for r in first.values()]
print(len(rows), "announcement-form filings;", len(deals), "new listed candidate targets", flush=True)
done = {r["deal_id"] for r in existing}
events.build_events(deals, out, workers=4, done=done)
