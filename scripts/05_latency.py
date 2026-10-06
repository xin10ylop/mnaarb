"""Summarize data/live_log.jsonl: how late does each free source show an item vs the time it claims?

For EDGAR the claimed time is the acceptance timestamp (Atom <updated>); for newswires it is the
RSS pubDate (minute precision). 'lag' = first seen by our poller - claimed publication time.
"""
import json
import sys
from pathlib import Path

import pandas as pd

path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/live_log.jsonl")
rows = [json.loads(line) for line in path.open()]
df = pd.DataFrame(rows)
df = df[df.source != "nasdaq_halts"].copy()
df["seen"] = pd.to_datetime(df.seen, utc=True)
df["published"] = pd.to_datetime(df.published, utc=True, errors="coerce", format="mixed")
df["lag_s"] = (df.seen - df.published).dt.total_seconds()
ok = df[df.lag_s.between(-120, 6 * 3600)]
summary = ok.groupby("source").lag_s.describe(percentiles=[0.1, 0.5, 0.9])[["count", "10%", "50%", "90%", "max"]]
summary = summary.rename(columns={"50%": "median"}).round(0)
print(f"items: {len(df)} ({df.is_ma.sum()} flagged M&A); window {df.seen.min()} - {df.seen.max()}")
print("\nseconds from claimed publication to first seen (polling every 2-5 s):")
print(summary.to_markdown())
ma = df[df.is_ma].sort_values("seen")
print("\nM&A-flagged items:")
print(ma[["seen", "source", "lag_s", "title"]].assign(title=ma.title.str[:90]).to_markdown(index=False))
Path("results").mkdir(exist_ok=True)
Path("results/latency.md").write_text(
    f"items: {len(df)}; window {df.seen.min()} - {df.seen.max()}\n\n" + summary.to_markdown() + "\n\n"
    + ma[["seen", "source", "lag_s", "title"]].assign(title=ma.title.str[:90]).to_markdown(index=False) + "\n")
