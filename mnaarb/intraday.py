"""Intraday capture curves around announcements (incl. pre/post-market).

Resolution is limited by what Yahoo serves for free:
    1m  for events in the last ~30 days, 5m for the last 60, 60m for the last 730.
With Polygon/Databento (see prices.polygon_bars) the same code runs on any history.
"""
from __future__ import annotations

from datetime import date, datetime, time, timedelta

import numpy as np
import pandas as pd

from . import prices
from .backtest import acquirer_ticker

ET = prices.ET
OFFSETS_MIN = [0, 1, 2, 5, 10, 15, 30, 60, 120, 240]


def best_interval(d: date, today: date | None = None) -> str | None:
    today = today or date.today()
    age = (today - d).days
    if age <= 28:
        return "1m"
    if age <= 58:
        return "5m"
    if age <= 725:
        return "60m"
    return None


def _regular(df: pd.DataFrame) -> pd.DataFrame:
    t = df.index.time
    return df[(t >= time(9, 30)) & (t < time(16, 0))]


def intraday_event(row, interval: str | None = None) -> dict | None:
    pr: date = row["pr_date"]
    interval = interval or best_interval(pr)
    if interval is None:
        return None
    start = datetime.combine(pr - timedelta(days=5), time(0), ET)
    end = datetime.combine(pr + timedelta(days=4), time(23, 59), ET)
    limit = {"1m": 29, "5m": 59, "60m": 729}.get(interval)
    now = datetime.now(ET)
    if limit:  # Yahoo rejects requests that start before its lookback window
        start = max(start, now - timedelta(days=limit))
    end = min(end, now)
    px = prices.yahoo_intraday(row["ticker"], start, end, interval)
    if px.empty:
        return {"deal_id": row["deal_id"], "dq": "no_intraday"}
    if row["consideration"] != "cash":
        return {"deal_id": row["deal_id"], "dq": "non_cash"}  # keep the intraday study to clean cash deals
    offer = float(row["cash"])
    reg = _regular(px)
    # reference: last regular-session close strictly before the press-release date
    before = reg[reg.index.date < pr]
    if before.empty:  # window clipped by Yahoo's lookback: take the prior close from daily bars
        d = prices.yahoo_daily(row["ticker"], pr - timedelta(days=10), pr)
        d = d[d.index.date < pr]
        if d.empty:
            return {"deal_id": row["deal_id"], "dq": "no_pre"}
        p_ref = float(d["close"].iloc[-1])
        last_close_ts = pd.Timestamp(datetime.combine(d.index[-1].date(), time(15, 59), ET))
    else:
        p_ref = float(before["close"].iloc[-1])
        last_close_ts = before.index[-1]
    gap = offer - p_ref
    if abs(gap) / p_ref < 0.02:
        return {"deal_id": row["deal_id"], "dq": "tiny_gap"}
    # scan from the last regular close before pr_date (catches after-hours releases the evening before)
    scan = px[px.index > last_close_ts]
    moved = (scan["close"] - p_ref) / gap
    # reaction = first bar >= 35% of the way to the offer AND the move persists over the next
    # 30 minutes of prints (filters isolated bad ticks / odd lots)
    t_react = None
    for k in np.flatnonzero(moved.values >= 0.35):
        t = scan.index[k]
        nxt = moved[(moved.index > t) & (moved.index <= t + pd.Timedelta(minutes=30))]
        if len(nxt) == 0 or nxt.median() >= 0.35:
            t_react = t
            break
    if t_react is None:
        return {"deal_id": row["deal_id"], "dq": "no_reaction", "ticker": row["ticker"]}
    i = px.index.get_loc(t_react)
    step = pd.Timedelta(interval.replace("m", "min"))

    def cap(p):
        return (p - p_ref) / gap

    out = {"deal_id": row["deal_id"], "ticker": row["ticker"], "company": row["company"], "interval": interval,
           "p_ref": p_ref, "offer": offer, "premium": offer / p_ref - 1, "t_react": t_react.isoformat(),
           "react_session": prices.session_of(t_react), "accepted_et": row["ann_accepted_et"],
           "edgar_lag_min": (row["accepted"] - t_react).total_seconds() / 60, "dq": "ok"}
    out["cap_react_open"] = cap(px["open"].iloc[i])      # first print inside the reaction bar
    out["cap_react_close"] = cap(px["close"].iloc[i])
    # previous bar (last pre-news print) to see if the jump happened inside one bar
    out["cap_prev_bar"] = cap(px["close"].iloc[i - 1]) if i > 0 else np.nan
    for m in OFFSETS_MIN:
        if m and m < step.total_seconds() / 60:  # finer than the bar size: not observable
            continue
        tgt = t_react + step + pd.Timedelta(minutes=m)   # bar-close of reaction bar + m minutes
        j = px.index.searchsorted(tgt - step, side="right") - 1
        if 0 <= j < len(px) and px.index[j] <= t_react + pd.Timedelta(minutes=m) + step:
            out[f"cap_+{m}m"] = cap(px["close"].iloc[j])
    day_reg = reg[reg.index >= t_react]  # first regular session that starts at/after the reaction
    if not day_reg.empty:
        first_day = day_reg.index[0].date()
        d0 = day_reg[day_reg.index.date == first_day]
        out["cap_reg_open"] = cap(d0["open"].iloc[0])
        out["cap_reg_close"] = cap(d0["close"].iloc[-1])
        out["cap_reg_high"] = cap(d0["high"].max())
        out["cap_reg_low"] = cap(d0["low"].min())
        nxt = reg[reg.index.date > first_day]
        if not nxt.empty:
            d1 = nxt[nxt.index.date == nxt.index[0].date()]
            out["cap_d1_close"] = cap(d1["close"].iloc[-1])
        # trade simulations: enter at a capture level (price = p_ref + c * gap), exit later
        def ret(c_in, c_out):
            if c_in is None or c_out is None or not (np.isfinite(c_in) and np.isfinite(c_out)):
                return np.nan
            return (c_out - c_in) * gap / (p_ref + c_in * gap)
        for ent in ("cap_react_close", "cap_+5m", "cap_+15m", "cap_+30m"):
            for ex in ("cap_reg_open", "cap_reg_close", "cap_d1_close"):
                out[f"ret_{ent[4:]}_to_{ex[4:]}"] = ret(out.get(ent), out.get(ex))
        # minutes between the reaction and the first regular-session print
        out["min_to_reg_open"] = (d0.index[0] - t_react).total_seconds() / 60
        out["d0_dollar_vol"] = float((d0["close"] * d0["volume"]).sum())  # Yahoo reports 0 volume pre/post
    return out


def run(ev: pd.DataFrame, interval: str | None = None) -> pd.DataFrame:
    rows = []
    for _, r in ev.iterrows():
        try:
            o = intraday_event(r, interval)
        except Exception as e:  # noqa: BLE001
            o = {"deal_id": r["deal_id"], "dq": f"error:{type(e).__name__}:{e}"[:120]}
        if o:
            rows.append(o)
    return pd.DataFrame(rows)
