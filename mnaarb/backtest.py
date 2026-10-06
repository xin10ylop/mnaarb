"""Event study + trading simulation for acquisition-announcement momentum.

Core quantity (the user's "critical variable"):

    capture(t) = (P_t - P_pre) / (V_t - P_pre)

    P_pre  last regular-session close before the announcement reached the market
    V_t    offer value per target share at time t (cash, or ratio x acquirer price (+cash))

capture = 0  -> nothing priced in, 1 -> trading at the offer. In steady state after a
definitive deal, capture < 1 by the merger-arbitrage spread (deal risk + time value).
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from . import prices

HORIZONS = {"d0_close": 0, "d1_close": 1, "d2_close": 2, "d5_close": 5, "d10_close": 10, "d20_close": 20}


def load_events(path: str = "data/events.csv") -> pd.DataFrame:
    ev = pd.read_csv(path, dtype=str).fillna("")
    ev = ev[(ev.status == "ok") & (ev.ticker != "")].copy()
    for c in ("cash", "ratio", "premium_pct", "cvr_max"):
        ev[c] = pd.to_numeric(ev[c], errors="coerce")
    ev["cvr"] = ev["cvr"].astype(str).str.lower().eq("true")
    ev["accepted"] = pd.to_datetime(ev["ann_accepted_et"], utc=True).dt.tz_convert(prices.ET)
    ev["pr_date"] = pd.to_datetime(ev["pr_date"]).dt.date
    # the same announcement can be reached from two anchors (e.g. DEFA14A and the later PREM14A)
    ev = ev.sort_values("anchor_date").drop_duplicates(["cik", "pr_date"])
    return ev.drop_duplicates("deal_id").reset_index(drop=True)


def acquirer_ticker(row) -> str | None:
    others = [t for t in str(row.get("tickers_mentioned", "")).split("|") if t and t != row["ticker"]
              and t not in str(row.get("tickers_all", "")).split("|")]
    return others[0] if others else None


def _offer_series(row, idx: pd.DatetimeIndex, acq: pd.DataFrame | None, field: str) -> pd.Series:
    cash = row["cash"] if pd.notna(row["cash"]) else 0.0
    if row["consideration"] == "cash":
        return pd.Series(cash, index=idx)
    if acq is None or acq.empty or pd.isna(row["ratio"]):
        return pd.Series(np.nan, index=idx)
    a = acq[field].reindex(idx).ffill()
    return cash + row["ratio"] * a


def reaction_day(px: pd.DataFrame, offer: pd.Series, first: date, last: date) -> tuple[int | None, str]:
    """Index (into px) of the first session that reacted to the announcement.

    Candidate sessions: trading days from the press-release dateline to one day after the
    EDGAR acceptance. Choose the first whose close moved >= 35% of the way to the offer.
    """
    days = px.index.date
    cand = [i for i, d in enumerate(days) if first <= d <= last + timedelta(days=4) and i > 0][:4]
    for i in cand:
        prev = px["close"].iloc[i - 1]
        gap = offer.iloc[i] - prev
        if not np.isfinite(gap) or prev <= 0:
            continue
        if abs(gap) / prev < 0.01:
            return i, "no_gap"
        mv = px["close"].iloc[i] - prev
        if mv / gap >= 0.35:
            return i, "ok"
    return (cand[0], "no_reaction") if cand else (None, "no_data")


def daily_event(row) -> dict | None:
    t0 = row["pr_date"]
    start, end = t0 - timedelta(days=120), min(date.today(), t0 + timedelta(days=45))
    px = prices.yahoo_daily(row["ticker"], start, end)
    if len(px) < 30:
        return {"deal_id": row["deal_id"], "dq": "no_prices"}
    acq_t = acquirer_ticker(row) if row["consideration"] in ("stock", "mixed") else None
    acq = prices.yahoo_daily(acq_t, start, end) if acq_t else None
    v_close = _offer_series(row, px.index, acq, "close")
    v_open = _offer_series(row, px.index, acq, "open")
    accepted_day = row["accepted"].date()
    i0, flag = reaction_day(px, v_close, t0, accepted_day)
    if i0 is None or i0 < 25:
        return {"deal_id": row["deal_id"], "dq": "no_window"}
    p_pre = px["close"].iloc[i0 - 1]
    p_m20 = px["close"].iloc[i0 - 21]
    v_pre = v_close.iloc[i0 - 1]
    if not np.isfinite(v_pre) or p_pre <= 0:
        return {"deal_id": row["deal_id"], "dq": "no_offer_value"}
    premium = v_pre / p_pre - 1
    out = {
        "deal_id": row["deal_id"], "ticker": row["ticker"], "company": row["company"],
        "t0": px.index[i0].date().isoformat(), "flag": flag, "acq_ticker": acq_t or "",
        "consideration": row["consideration"], "cvr": row["cvr"], "offer_pre": v_pre, "p_pre": p_pre,
        "premium": premium, "stated_premium": row["premium_pct"] / 100 if pd.notna(row["premium_pct"]) else np.nan,
        "runup_20d": p_pre / p_m20 - 1,
        "accepted_et": row["ann_accepted_et"], "accept_session": prices.session_of(row["accepted"]),
        "accepted_on_t0": accepted_day == px.index[i0].date(),
        # the d0 open is only a legitimate *post-news* entry if the news was provably out before 9:30 ET
        "news_before_open": bool(row["accepted"] < pd.Timestamp(px.index[i0].date().isoformat() + " 09:30",
                                                                 tz=prices.ET)),
        "adv_usd_60": float((px["close"] * px["volume"]).iloc[max(0, i0 - 65): i0 - 5].median()),
        "year": px.index[i0].year, "exchange": row.get("exchange", ""),
    }
    # quality: does the series look like this company? (catches ticker reuse / bad parses)
    ok_rng = 0.6 <= px["close"].iloc[i0] / v_close.iloc[i0] <= 1.35 if np.isfinite(v_close.iloc[i0]) else False
    out["dq"] = "ok" if ok_rng and -0.5 < premium < 5 else "suspect"

    def cap(p, v):
        g = v - p_pre
        return (p - p_pre) / g if g != 0 and np.isfinite(g) else np.nan

    o0 = px["open"].iloc[i0]
    out["cap_open"] = cap(o0, v_open.iloc[i0])
    out["gap_open"] = o0 / p_pre - 1
    out["cap_high0"] = cap(px["high"].iloc[i0], v_close.iloc[i0])
    out["cap_low0"] = cap(px["low"].iloc[i0], v_close.iloc[i0])
    out["vol_ratio0"] = float(px["volume"].iloc[i0] / max(1.0, px["volume"].iloc[max(0, i0 - 65): i0 - 5].median()))
    # Corwin-Schultz-free proxy for the spread cost on day 0: (high-low)/close (upper bound on round-trip cost)
    out["hl_range0"] = (px["high"].iloc[i0] - px["low"].iloc[i0]) / px["close"].iloc[i0]
    for name, h in HORIZONS.items():
        j = i0 + h
        if j < len(px):
            out[f"cap_{name}"] = cap(px["close"].iloc[j], v_close.iloc[j])
            # long-only returns, with stock-deal hedge variant (short ratio x acquirer)
            out[f"ret_open_{name}"] = px["close"].iloc[j] / o0 - 1
            if h > 0:
                out[f"ret_close_{name}"] = px["close"].iloc[j] / px["close"].iloc[i0] - 1
            if acq is not None and not acq.empty and pd.notna(row["ratio"]):
                a = acq["close"].reindex(px.index).ffill()
                ao = acq["open"].reindex(px.index).ffill()
                hedge = row["ratio"] * (a.iloc[j] - ao.iloc[i0]) / o0
                out[f"ret_open_hedged_{name}"] = out[f"ret_open_{name}"] - hedge
    return out


def run_daily(ev: pd.DataFrame, workers: int = 4) -> pd.DataFrame:
    from concurrent.futures import ThreadPoolExecutor

    def safe(r):
        try:
            return daily_event(r)
        except Exception as e:  # noqa: BLE001 - keep going, record why
            return {"deal_id": r["deal_id"], "dq": f"error:{type(e).__name__}:{e}"[:120]}

    with ThreadPoolExecutor(workers) as pool:
        rows = list(pool.map(safe, [r for _, r in ev.iterrows()]))
    return pd.DataFrame([r for r in rows if r])


def capture_bucket(c: float) -> str:
    if not np.isfinite(c):
        return "na"
    for lo, hi, lab in ((-np.inf, 0.25, "<25%"), (0.25, 0.5, "25-50%"), (0.5, 0.8, "50-80%"),
                        (0.8, 0.95, "80-95%"), (0.95, 1.02, "95-102%"), (1.02, np.inf, ">102%")):
        if lo <= c < hi:
            return lab
    return "na"


def summarize(df: pd.DataFrame, col: str, by: str | None = None, cost_bps: float = 0) -> pd.DataFrame:
    d = df[np.isfinite(df[col])].copy()
    d["_r"] = d[col] - cost_bps / 1e4
    g = d.groupby(by) if by else d.assign(_all="all").groupby("_all")
    res = g["_r"].agg(n="count", mean="mean", median="median", std="std",
                      hit=lambda s: (s > 0).mean())
    res["t"] = res["mean"] / (res["std"] / np.sqrt(res["n"]))
    return res
