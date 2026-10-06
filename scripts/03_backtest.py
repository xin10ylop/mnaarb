"""Run the daily event study and the intraday capture study.

outputs: results/daily_events.csv, results/intraday_events.csv
"""
import sys
from pathlib import Path

sys.path.insert(0, ".")
import pandas as pd

from mnaarb import backtest as bt, intraday

Path("results").mkdir(exist_ok=True)
ev = bt.load_events()
print(len(ev), "events with terms and a live ticker", flush=True)

daily = bt.run_daily(ev)
daily.to_csv("results/daily_events.csv", index=False)
print(daily.dq.value_counts().to_string(), flush=True)

recent = ev[ev.pr_date.map(intraday.best_interval).notna()]
print(len(recent), "events inside Yahoo's intraday windows", flush=True)
intra = intraday.run(recent)
intra.to_csv("results/intraday_events.csv", index=False)
print(intra.dq.value_counts().to_string() if len(intra) else "none", flush=True)
