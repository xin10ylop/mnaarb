"""Live acquisition-announcement detector (research / paper-trading grade).

Polls several PUBLIC sources concurrently, timestamps when each item is first seen,
classifies M&A headlines, extracts deal terms, and computes the capture-ratio signal.

    python -m mnaarb.live --log data/live_log.jsonl            # monitor + log
    python -m mnaarb.live --log data/live_log.jsonl --once     # single sweep (testing)

Nothing here obtains information before its public release. The point is to be first
among the public: poll the primary publication points (newswire feeds, EDGAR, exchange
halt feed) directly instead of waiting for aggregators.
"""
from __future__ import annotations

import argparse
import json
import re
import threading
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path

import lxml.etree as ET_XML

from . import edgar, extract, http, prices

M_AND_A_HEADLINE = re.compile(
    r"\bto\s+acquire\b|\bto\s+be\s+acquired\b|\bacquisition\s+of\b|\bdefinitive\s+(?:merger\s+)?agreement\b|"
    r"\bmerger\b|\btender\s+offer\b|\btake[- ]private\b|\bgo[- ]private\b|\bper\s+share\s+in\s+cash\b|"
    r"\ball[- ]cash\b|\bto\s+combine\b|\bbuyout\b|\bunsolicited\s+proposal\b|\bnon-binding\s+proposal\b", re.I)

SOURCES = {
    # name: (url, poll seconds, kind)
    "edgar_8k": (edgar.current_feed_url("8-K", 100), 5.0, "atom"),
    "edgar_defa14a": (edgar.current_feed_url("DEFA14A", 40), 5.0, "atom"),
    "edgar_sc14d9c": (edgar.current_feed_url("SC14D9C", 40), 5.0, "atom"),
    "edgar_sctoc": (edgar.current_feed_url("SC TO-C", 40), 5.0, "atom"),
    "edgar_425": (edgar.current_feed_url("425", 40), 5.0, "atom"),
    "prn_ma": ("https://www.prnewswire.com/rss/financial-services-latest-news/acquisitions-mergers-and-takeovers-list.rss", 2.0, "rss"),
    "prn_all": ("https://www.prnewswire.com/rss/news-releases-list.rss", 2.0, "rss"),
    "gnw_ma": ("https://www.globenewswire.com/RssFeed/subjectcode/27-Mergers%20And%20Acquisitions/feedTitle/"
               "GlobeNewswire%20-%20Mergers%20And%20Acquisitions", 2.0, "rss"),
    "gnw_public": ("https://www.globenewswire.com/RssFeed/orgclass/1/feedTitle/GlobeNewswire%20-%20News%20about%20Public%20Companies", 2.0, "rss"),
    "bw_all": ("https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeGVtRWA==", 2.0, "rss"),
    "nasdaq_halts": ("https://www.nasdaqtrader.com/rss.aspx?feed=tradehalts", 2.0, "halts"),
}


@dataclass
class Item:
    source: str
    uid: str
    title: str
    link: str
    published: str          # what the source claims (ISO, may be minute precision)
    seen: str               # when we first saw it (ISO, ms precision)
    is_ma: bool = False
    extra: dict = field(default_factory=dict)


def _now() -> datetime:
    return datetime.now(prices.ET)


def parse_feed(kind: str, body: bytes) -> list[dict]:
    try:
        root = ET_XML.fromstring(body)
    except ET_XML.XMLSyntaxError:
        return []
    out = []
    if kind == "atom":
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for e in root.findall("a:entry", ns):
            link = e.find("a:link", ns)
            summ = re.sub(r"<[^>]+>", " ", e.findtext("a:summary", "", ns) or "")
            cat = e.find("a:category", ns)
            out.append({"uid": (e.findtext("a:id", "", ns) or "").strip(),
                        "title": (e.findtext("a:title", "", ns) or "").strip(),
                        "link": link.get("href") if link is not None else "",
                        "published": e.findtext("a:updated", "", ns),
                        "summary": re.sub(r"\s+", " ", summ)[:500],
                        "form": cat.get("term") if cat is not None else ""})
    elif kind == "rss":
        for it in root.iter("item"):
            pub = it.findtext("pubDate") or ""
            try:
                pub = parsedate_to_datetime(pub).astimezone(prices.ET).isoformat()
            except (TypeError, ValueError):
                pass
            out.append({"uid": (it.findtext("guid") or it.findtext("link") or "").strip(),
                        "title": (it.findtext("title") or "").strip(), "link": (it.findtext("link") or "").strip(),
                        "published": pub, "summary": (it.findtext("description") or "")[:2000]})
    elif kind == "halts":
        ns = {"n": "http://www.nasdaqtrader.com/"}
        for it in root.iter("item"):
            sym = it.findtext("n:IssueSymbol", "", ns)
            code = it.findtext("n:ReasonCode", "", ns)
            d, t = it.findtext("n:HaltDate", "", ns), it.findtext("n:HaltTime", "", ns)
            out.append({"uid": f"{sym}|{code}|{d}|{t}", "title": f"{sym} {code} {it.findtext('n:IssueName', '', ns)}",
                        "link": "", "published": f"{d} {t}", "symbol": sym, "code": code})
    return out


class Monitor:
    def __init__(self, log_path: Path, sources: dict = SOURCES, on_ma=None):
        self.log_path = log_path
        self.sources = sources
        self.seen: set[str] = set()
        self.lock = threading.Lock()
        self.on_ma = on_ma
        self.primed: set[str] = set()

    def _emit(self, item: Item) -> None:
        with self.lock, open(self.log_path, "a") as f:
            f.write(json.dumps(asdict(item)) + "\n")

    def poll(self, name: str) -> None:
        url, _, kind = self.sources[name]
        body = http.get(url, cache=False, timeout=10, retries=1)
        if not body:
            return
        seen_at = _now().isoformat(timespec="milliseconds")
        for e in parse_feed(kind, body):
            key = f"{name}|{e['uid']}"
            if key in self.seen:
                continue
            self.seen.add(key)
            if name not in self.primed:  # first sweep = backlog; mark but don't treat as new
                continue
            text = e["title"] + " " + e.get("summary", "")
            is_ma = (bool(M_AND_A_HEADLINE.search(text))
                     or (kind == "halts" and e.get("code") in ("T1", "T2", "T12"))
                     or (kind == "atom" and (e.get("form") in ("DEFA14A", "SC14D9C", "SC TO-C", "425")
                                             or "1.01" in e.get("summary", ""))))
            item = Item(name, e["uid"], e["title"], e["link"], e["published"], seen_at, is_ma,
                        {k: e[k] for k in ("symbol", "code", "form", "summary") if k in e})
            self._emit(item)
            if is_ma and self.on_ma:
                threading.Thread(target=self.on_ma, args=(item,), daemon=True).start()
        self.primed.add(name)

    def run(self, once: bool = False, duration: float | None = None) -> None:
        stop = time.time() + duration if duration else None

        def loop(name):
            every = self.sources[name][1]
            while True:
                t = time.time()
                try:
                    self.poll(name)
                except Exception as ex:  # noqa: BLE001
                    print(f"{name}: {type(ex).__name__} {ex}", flush=True)
                if once or (stop and time.time() > stop):
                    return
                time.sleep(max(0.0, every - (time.time() - t)))

        threads = [threading.Thread(target=loop, args=(n,), daemon=True) for n in self.sources]
        for t in threads:
            t.start()
        for t in threads:
            t.join()


# ---------------------------------------------------------------- signal

def fetch_release_text(url: str) -> str:
    body = http.get(url, cache=False, timeout=10, retries=1)
    return extract.html_to_text(body.decode("utf-8", errors="replace")) if body else ""


def last_price(symbol: str) -> tuple[float | None, float | None]:
    """(last trade incl. extended hours, previous regular close) from Yahoo 1m bars."""
    now = _now()
    df = prices.yahoo_chart(symbol, now - timedelta(days=4), now + timedelta(minutes=1), "1m", prepost=True, ttl=0)
    if df.empty:
        return None, None
    meta = df.attrs.get("meta", {})
    return float(df["close"].iloc[-1]), meta.get("chartPreviousClose") or meta.get("previousClose")


def evaluate(text: str, target: str, max_capture: float = 0.5, min_remaining: float = 0.03) -> dict:
    """Capture-ratio signal for a detected announcement."""
    terms = extract.extract_terms(text)
    out = {"target": target, **{k: terms.get(k) for k in ("consideration", "cash", "ratio", "cvr", "premium_pct")}}
    if terms.get("consideration") != "cash":
        out["decision"] = "skip:not_all_cash"  # stock legs need a live acquirer quote + hedge; see README
        return out
    last, prev = last_price(target)
    if not last or not prev:
        out["decision"] = "skip:no_quote"
        return out
    offer = terms["cash"]
    cap = (last - prev) / (offer - prev) if offer != prev else float("nan")
    remaining = offer / last - 1
    out.update(last=last, prev_close=prev, capture=cap, remaining=remaining)
    out["decision"] = "BUY" if (cap < max_capture and remaining > min_remaining) else "skip:repriced"
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default="data/live_log.jsonl")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--minutes", type=float, default=None)
    a = ap.parse_args()
    Path(a.log).parent.mkdir(parents=True, exist_ok=True)

    def on_ma(item: Item):
        print(f"{item.seen} [{item.source}] {item.title[:120]}", flush=True)

    m = Monitor(Path(a.log), on_ma=on_ma)
    m.run(once=False, duration=a.minutes * 60 if a.minutes else None) if not a.once else (m.run(once=True), m.run(once=True))


if __name__ == "__main__":
    main()
