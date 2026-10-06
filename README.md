# mnaarb — acquisition-announcement momentum research

Research code for one question:

> When a takeover is announced, can a fast but non-HFT trader buy the target **after** the news is
> public but **before** the price has repriced toward the offer, and exit within minutes–hours?

The findings are in **[REPORT.md](REPORT.md)**. This file covers how to run the pipeline.

## Pipeline

| step | script | what it does |
|---|---|---|
| 1 | `scripts/01_form_indexes.py [start_year]` | Downloads EDGAR quarterly `form.idx` files and keeps the M&A *anchor* filings (merger proxies `PREM14A`/`DEFM14A`, tender-offer schedules `SC 14D9`/`SC14D9C`/`SC TO-T`). |
| 2 | `scripts/02_build_events.py [--all]` | Clusters anchors into deals, walks each target's filings back to the **first public announcement**, and extracts the terms (cash per share, exchange ratio, CVR, stated premium, tickers) plus the EDGAR acceptance timestamp → `data/events.csv`. Without `--all` it keeps only targets that still have a ticker, because free price data does not cover delisted targets. |
| 2b | `scripts/02b_recent_events.py [days]` | Adds deals announced in the last N days that have no merger proxy yet (anchor = the target's announcement-day `DEFA14A`/`SC14D9C`/`SC TO-C`/`425`, prefiltered by EDGAR full-text search). These are the only deals with free 1-minute and 5-minute bars. |
| 3 | `scripts/03_backtest.py` | Daily event study + trade simulation (`results/daily_events.csv`), and an intraday capture study including pre/post-market (`results/intraday_events.csv`). |
| 4 | `scripts/04_report.py` | Tables (`results/tables.md`) and figures (`results/fig_*.png`). |
| live | `python -m mnaarb.live --minutes 120` | Polls EDGAR, PR Newswire, GlobeNewswire, Business Wire and the Nasdaq halt feed concurrently. Logs when each item is first seen (`data/live_log.jsonl`) and flags M&A headlines. `live.evaluate()` computes the capture-ratio signal for a detected release. |
| latency | `scripts/05_latency.py` | Summarizes the live log: how far each source lags the time it claims for publication. |
| 6 | `scripts/06_proposals.py` | Secondary event study: public non-binding take-private proposals (13D Item 4 / 8-K). |
| 7 | `scripts/07_case_charts.py TICKER…` | Per-deal intraday chart: price vs offer, with the EDGAR acceptance time marked. |

```
pip install -r requirements.txt
python scripts/01_form_indexes.py 2010
python scripts/02_build_events.py
python scripts/02b_recent_events.py 75
python scripts/03_backtest.py
python scripts/04_report.py
```

Set `MNAARB_SEC_UA="Your Name your@email"`. SEC requires a declared User-Agent, and the client
stays under SEC's 10 requests/second fair-access limit.

## Modules

- `mnaarb/edgar.py` — form indexes, submissions JSON (acceptance timestamps are UTC → converted to ET),
  filing documents, full-text search (EFTS), and the "current filings" Atom feed used live.
- `mnaarb/extract.py` — regex extraction of deal terms. It is transparent on purpose so every number can be audited.
- `mnaarb/prices.py` — Yahoo chart API (daily; 1m/5m/60m incl. extended hours within Yahoo's lookback windows)
  and a Polygon adapter (`POLYGON_API_KEY`) for full history including delisted tickers.
- `mnaarb/backtest.py` — the capture ratio, reaction-day detection, and daily strategy returns.
- `mnaarb/intraday.py` — minute-level capture curves around the first price reaction.
- `mnaarb/proposals.py` — secondary event class: public non-binding take-private proposals.
- `mnaarb/live.py` — the live detector and signal.

## Data limitations (read before trusting any number)

1. **Survivorship by construction.** Free price sources drop delisted tickers, and a completed deal
   delists the target. The free sample therefore contains **pending** deals (recent) and **failed**
   deals (old). For day-0 dynamics this matters less than it sounds, because nobody knows the outcome
   on day 0. Still, rerun on the full universe with `--all` + `prices.polygon_bars` before deploying capital.
2. **Bars are trades, not quotes.** A stale last-trade print in pre-market is not proof you could have
   bought at that price. The ask has usually moved already. To validate fills you need NBBO quotes
   (Polygon/Databento/TAQ).
3. **Resolution.** Yahoo serves 1-minute bars for ~30 days, 5-minute for ~60 days and 60-minute
   for ~2 years. Questions at the 1-second level need tick data.
