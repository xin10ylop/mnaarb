"""Build data/events.csv from EDGAR anchor filings.

usage: python scripts/02_build_events.py [--start 2010] [--all]
  default: only targets that still have an exchange ticker in EDGAR (=> free price data exists)
  --all:   every deal (needs a paid price source for delisted targets)
"""
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, ".")
from mnaarb import edgar, events

ap = argparse.ArgumentParser()
ap.add_argument("--start", type=int, default=2010)
ap.add_argument("--all", action="store_true")
ap.add_argument("--out", default="data/events.csv")
args = ap.parse_args()

deals = events.cluster_deals(events.load_anchor_rows(args.start))
print(len(deals), "deals", flush=True)
if not args.all:
    listed = edgar.listed_ciks()
    deals = [d for d in deals if int(d["cik"]) in listed]
    print(len(deals), "deals whose target still has a ticker", flush=True)

deals.sort(key=lambda d: d["anchor_date"], reverse=True)  # recent deals first (intraday data exists for them)
out = Path(args.out)
done = set()
if out.exists():
    with open(out) as f:
        done = {r["deal_id"] for r in csv.DictReader(f)}
events.build_events(deals, out, workers=4, done=done)
