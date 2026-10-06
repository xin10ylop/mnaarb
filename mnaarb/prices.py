"""Price bars. Yahoo (free; no delisted tickers; intraday only for recent windows) and Polygon (paid; full history).

All functions return a DataFrame indexed by tz-aware America/New_York timestamps with
columns open, high, low, close, volume (unadjusted for dividends, split-adjusted as served).

Yahoo intraday availability (as served by the chart API):
    1m        last ~30 days, max 8 days per request
    2m..30m   last 60 days
    60m       last 730 days
    1d        full history
"""
from __future__ import annotations

import json
import os
import time
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd

from . import http

ET = ZoneInfo("America/New_York")
COLS = ["open", "high", "low", "close", "volume"]


def _epoch(d: date | datetime) -> int:
    if isinstance(d, datetime):
        return int(d.timestamp())
    return int(datetime(d.year, d.month, d.day, tzinfo=ET).timestamp())


def yahoo_chart(symbol: str, start: date | datetime, end: date | datetime, interval: str = "1d",
                prepost: bool = True, ttl: float | None = None) -> pd.DataFrame:
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={_epoch(start)}"
           f"&period2={_epoch(end)}&interval={interval}&includePrePost={'true' if prepost else 'false'}"
           "&events=div%2Csplits")
    body = http.get(url, ttl=ttl)
    if not body:
        return pd.DataFrame(columns=COLS)
    try:
        res = json.loads(body)["chart"]["result"][0]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
        return pd.DataFrame(columns=COLS)
    ts = res.get("timestamp")
    if not ts:
        return pd.DataFrame(columns=COLS)
    q = res["indicators"]["quote"][0]
    df = pd.DataFrame({c: q.get(c) for c in COLS}, index=pd.to_datetime(ts, unit="s", utc=True).tz_convert(ET))
    df = df.dropna(subset=["open", "close"])
    df.attrs["splits"] = res.get("events", {}).get("splits", {})
    df.attrs["meta"] = res.get("meta", {})
    if interval == "1d":
        df.index = df.index.normalize()
    return df[~df.index.duplicated()]


def yahoo_daily(symbol: str, start: date, end: date) -> pd.DataFrame:
    # daily bars for past windows never change -> cache forever unless the window touches today
    ttl = None if end < date.today() - timedelta(days=3) else 6 * 3600
    return yahoo_chart(symbol, start, end, "1d", prepost=False, ttl=ttl)


def yahoo_intraday(symbol: str, start: datetime, end: datetime, interval: str = "5m") -> pd.DataFrame:
    """Intraday bars incl. pre/post market. Splits 1m requests into 7-day chunks."""
    chunk = timedelta(days=7) if interval == "1m" else timedelta(days=59)
    out, s = [], start
    while s < end:
        e = min(end, s + chunk)
        out.append(yahoo_chart(symbol, s, e, interval, prepost=True, ttl=None if e < datetime.now(ET) - timedelta(days=1) else 3600))
        s = e
    out = [d for d in out if len(d)]
    if not out:
        return pd.DataFrame(columns=COLS)
    df = pd.concat(out).sort_index()
    return df[~df.index.duplicated()]


def polygon_bars(symbol: str, start: date, end: date, multiplier: int = 1, timespan: str = "minute",
                 api_key: str | None = None) -> pd.DataFrame:
    """Polygon.io aggregates (includes delisted tickers & extended hours). Needs POLYGON_API_KEY."""
    key = api_key or os.environ.get("POLYGON_API_KEY")
    if not key:
        raise RuntimeError("set POLYGON_API_KEY to use polygon_bars")
    base = os.environ.get("POLYGON_BASE", "https://api.polygon.io")
    url = (f"{base}/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{start.isoformat()}/{end.isoformat()}"
           f"?adjusted=false&sort=asc&limit=50000&apiKey={key}")
    rows = []
    while url:
        body = http.get(url)
        if not body:
            break
        d = json.loads(body)
        rows += d.get("results", [])
        nxt = d.get("next_url")
        url = f"{nxt}&apiKey={key}" if nxt else None
        time.sleep(0.2)
    if not rows:
        return pd.DataFrame(columns=COLS)
    df = pd.DataFrame(rows)
    df.index = pd.to_datetime(df["t"], unit="ms", utc=True).dt.tz_convert(ET)
    df = df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})[COLS]
    if timespan == "day":
        df.index = df.index.normalize()
    return df


def session_of(ts: pd.Timestamp) -> str:
    """US equity session for an ET timestamp."""
    m = ts.hour * 60 + ts.minute
    if m < 4 * 60:
        return "overnight"
    if m < 9 * 60 + 30:
        return "pre"
    if m < 16 * 60:
        return "regular"
    if m < 20 * 60:
        return "post"
    return "overnight"
