"""Event study for public NON-BINDING take-private proposals (secondary event class).

Entry = first regular-session price after the proposal became public on EDGAR
(the d0 open if accepted before 9:30 ET, otherwise the d0 close).
outputs: results/proposals.csv and a section appended to results/tables.md
"""
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, ".")
import numpy as np
import pandas as pd

from mnaarb import prices, proposals

hits_path = Path("data/proposal_hits.csv")
if not hits_path.exists():
    proposals.first_proposals(proposals.search("2016-01-01")).to_csv(hits_path, index=False)
eps = pd.read_csv(hits_path)
rows = []
for _, r in eps.iterrows():
    info = proposals.enrich(r)
    if not info["cash"] or not info["accepted"]:
        rows.append({"ticker": r.ticker, "file_date": r.file_date, "dq": "no_terms"})
        continue
    acc = pd.Timestamp(info["accepted"])
    d = acc.date()
    px = prices.yahoo_daily(r.ticker, d - timedelta(days=60), min(date.today(), d + timedelta(days=45)))
    if len(px) < 25:
        rows.append({"ticker": r.ticker, "file_date": r.file_date, "dq": "no_prices"})
        continue
    idx = px.index.date
    # first session whose open is after the acceptance time (pre-market filing -> same day open)
    if acc.hour * 60 + acc.minute < 9 * 60 + 30:
        i0 = int(np.searchsorted(idx, d))
        entry_kind = "open"
    else:
        i0 = int(np.searchsorted(idx, d))
        entry_kind = "close" if acc.hour < 16 else "next_open"
        if entry_kind == "next_open":
            i0 += 1
            entry_kind = "open"
    if i0 < 1 or i0 >= len(px):
        rows.append({"ticker": r.ticker, "file_date": r.file_date, "dq": "no_window"})
        continue
    p_pre = px.close.iloc[i0 - 1]
    offer = info["cash"]
    entry = px.open.iloc[i0] if entry_kind == "open" else px.close.iloc[i0]
    out = {"ticker": r.ticker, "company": r.company, "file_date": r.file_date, "form": r.form,
           "accepted": info["accepted"], "entry_kind": entry_kind, "offer": offer, "p_pre": p_pre,
           "premium": offer / p_pre - 1, "runup_20d": p_pre / px.close.iloc[max(0, i0 - 21)] - 1,
           "cap_entry": (entry - p_pre) / (offer - p_pre) if offer != p_pre else np.nan}
    for h in (0, 1, 5, 20):
        j = i0 + h
        if j < len(px):
            out[f"ret_entry_d{h}_close"] = px.close.iloc[j] / entry - 1
            out[f"cap_d{h}_close"] = (px.close.iloc[j] - p_pre) / (offer - p_pre) if offer != p_pre else np.nan
    ok = 0.5 < px.close.iloc[min(i0 + 1, len(px) - 1)] / offer < 1.3 and 0.03 < out["premium"] < 2
    out["dq"] = "ok" if ok else "suspect"
    rows.append(out)

res = pd.DataFrame(rows)
res.to_csv("results/proposals.csv", index=False)
ok = res[res.dq == "ok"]
lines = ["\n## Non-binding proposals (secondary event class)\n",
         f"episodes found: {len(eps)}; priced & validated: {len(ok)}; dq: {res.dq.value_counts().to_dict()}  \n"]
if len(ok):
    desc = ok[["premium", "runup_20d", "cap_entry", "cap_d0_close", "cap_d1_close", "cap_d5_close", "cap_d20_close",
               "ret_entry_d0_close", "ret_entry_d1_close", "ret_entry_d5_close", "ret_entry_d20_close"]].describe(
        percentiles=[0.25, 0.5, 0.75]).T[["count", "mean", "25%", "50%", "75%"]]
    lines.append(desc.round(3).to_markdown())
    lines.append("\n\n" + ok[["ticker", "file_date", "entry_kind", "premium", "cap_entry", "cap_d0_close", "cap_d5_close",
                              "ret_entry_d0_close", "ret_entry_d5_close", "ret_entry_d20_close"]]
                 .sort_values("file_date").round(3).to_markdown(index=False))
Path("results/proposals.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
