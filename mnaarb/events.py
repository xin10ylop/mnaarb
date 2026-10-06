"""Build the acquisition-announcement event table from EDGAR.

Pipeline
  1. anchor filings (merger proxies / tender-offer schedules) from quarterly form indexes
  2. cluster per target CIK into deals
  3. walk the target's filings before the anchor, find the first one that announces the
     company itself is being acquired (press release / 8-K text)
  4. extract terms (cash / exchange ratio / CVR / stated premium) and timestamps
"""
from __future__ import annotations

import csv
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

from . import edgar, extract, http

EVENT_FIELDS = [
    "deal_id", "cik", "company", "ticker", "tickers_all", "exchange", "sic", "anchor_form", "anchor_date",
    "ann_form", "ann_adsh", "ann_accepted_et", "pr_date", "first_same_day_accept_et", "consideration",
    "cash", "ratio", "cvr", "cvr_max", "premium_pct", "premium_ref", "tickers_mentioned", "cash_candidates",
    "score", "status",
]
SKIP_DOC_TYPES = ("EX-2", "EX-3", "EX-4", "EX-10", "EX-21", "EX-23", "EX-31", "EX-32", "EX-101", "EX-104", "GRAPHIC")


def load_anchor_rows(start_year: int = 2010) -> list[dict]:
    rows = []
    for p in sorted((http.CACHE_DIR / "formidx").glob("*.csv")):
        if int(p.stem[:4]) < start_year:
            continue
        with open(p) as f:
            rows += [r for r in csv.DictReader(f) if r["form"] in edgar.ANCHOR_FORMS]
    return rows


def cluster_deals(rows: list[dict], gap_days: int = 365) -> list[dict]:
    by_cik: dict[str, list[dict]] = {}
    for r in rows:
        by_cik.setdefault(r["cik"], []).append(r)
    deals = []
    for cik, rs in by_cik.items():
        rs.sort(key=lambda r: r["date"])
        cur = None
        for r in rs:
            d = date.fromisoformat(r["date"])
            if cur is None or (d - cur["last"]).days > gap_days:
                cur = {"cik": cik, "company": r["company"], "anchor_form": r["form"], "anchor_date": d, "last": d}
                deals.append(cur)
            cur["last"] = d
    for i, d in enumerate(deals):
        d["deal_id"] = f"{d['cik']}-{d['anchor_date'].isoformat()}"
    return deals


def _index_docs(f: edgar.Filing) -> list[dict]:
    """Parse the filing index page -> [{type, url}] (cheaper than the full .txt)."""
    url = f"{f.folder}/{f.adsh}-index.htm"
    body = http.get(url)
    if not body:
        return []
    html = body.decode("utf-8", errors="replace")
    docs = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S | re.I):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S | re.I)
        if len(cells) < 4:
            continue
        link = re.search(r'href="([^"]+)"', cells[2])
        typ = re.sub(r"<[^>]+>", "", cells[3]).strip()
        if not link or not typ:
            continue
        href = link.group(1)
        if href.startswith("/ix?doc="):
            href = href[len("/ix?doc="):]
        if not href.lower().endswith((".htm", ".html", ".txt")):
            continue
        docs.append({"type": typ, "url": "https://www.sec.gov" + href if href.startswith("/") else href})
    return docs


def filing_texts(f: edgar.Filing, max_docs: int = 2) -> list[tuple[str, str]]:
    """[(doc type, text)] for the primary doc + press-release exhibits (skips merger agreements etc.)."""
    docs = [d for d in _index_docs(f) if not d["type"].upper().startswith(SKIP_DOC_TYPES)]
    # press releases first: they carry the headline terms and the dateline
    docs.sort(key=lambda d: (0 if d["type"].upper().startswith("EX-99") else 1, d["type"]))
    texts = []
    for d in docs[:max_docs]:
        b = http.get(d["url"], timeout=60)
        if b:
            texts.append((d["type"], extract.html_to_text(b.decode("utf-8", errors="replace"))[:200_000]))
    return texts


def filing_text(f: edgar.Filing, max_docs: int = 2) -> str:
    return "\n\n".join(t for _, t in filing_texts(f, max_docs))


def _candidate_filings(sub: dict, anchor: date, lookback: int = 270) -> list[edgar.Filing]:
    lo, hi = anchor - timedelta(days=lookback), anchor + timedelta(days=1)
    out = []
    for f in edgar.filings(sub):
        if not (lo <= f.filing_date <= hi):
            continue
        if f.form in ("DEFA14A", "SC14D9C", "425", "SC TO-C"):
            out.append(f)
        elif f.form in ("8-K", "6-K") and (f.form == "6-K" or any(i in f.items for i in ("1.01", "7.01", "8.01"))):
            out.append(f)
    out.sort(key=lambda f: f.accepted)
    return out


def build_event(deal: dict) -> dict:
    ev = {k: "" for k in EVENT_FIELDS}
    ev.update(deal_id=deal["deal_id"], cik=deal["cik"], company=deal["company"],
              anchor_form=deal["anchor_form"], anchor_date=deal["anchor_date"].isoformat())
    sub = edgar.submissions(deal["cik"])
    if sub is None:
        ev["status"] = "no_submissions"
        return ev
    ev["tickers_all"] = "|".join(sub.get("tickers") or [])
    ev["ticker"] = (sub.get("tickers") or [""])[0]
    ev["exchange"] = (sub.get("exchanges") or [""])[0] or ""
    ev["sic"] = sub.get("sic", "")
    if str(ev["sic"]) == "6770" or re.search(r"acquisition\s+(corp|co\b|company|ltd)", deal["company"], re.I):
        ev["status"] = "spac"
        return ev
    recent = sub["filings"]["recent"]
    oldest = min(recent["filingDate"]) if recent["filingDate"] else "9999"
    if oldest > (deal["anchor_date"] - timedelta(days=270)).isoformat():
        sub = edgar.submissions(deal["cik"], full=True)
    cands = _candidate_filings(sub, deal["anchor_date"])
    all_f = edgar.filings(sub)
    # Check first the filings around the earliest M&A-specific form (DEFA14A/SC14D9C/425/SC TO-C):
    # the press release is usually filed under one of them on announcement day.
    mna_days = sorted({f.filing_date for f in cands if f.form in ("DEFA14A", "SC14D9C", "425", "SC TO-C")})
    if mna_days:
        d0 = mna_days[0]
        near = [f for f in cands if timedelta(days=-4) <= f.filing_date - d0 <= timedelta(days=1)]
        cands = near + [f for f in cands if f not in near]
    for f in cands[:10]:
        parts = filing_texts(f)
        text = "\n\n".join(t for _, t in parts)
        ok, score = extract.is_target_announcement(text, deal["company"])
        if not ok:
            continue
        terms = extract.extract_terms(text)
        if "cash" not in terms and "ratio" not in terms:
            # 8-K body filed a few days later usually states the per-share consideration
            for g in cands:
                if f.accepted < g.accepted and (g.filing_date - f.filing_date).days <= 7:
                    t2 = extract.extract_terms(filing_text(g))
                    if "cash" in t2 or "ratio" in t2:
                        for k, v in t2.items():
                            terms.setdefault(k, v)
                        break
        pr = None
        for typ, t in parts:  # dateline of the press release, never the 8-K cover page
            if typ.upper().startswith("EX-99") or f.form != "8-K":
                pr = extract.parse_dateline(t)
                if pr:
                    break
        pr = pr or f.accepted.date()
        if pr > f.accepted.date() or (f.accepted.date() - pr).days > 10:
            pr = f.accepted.date()
        same_day = [g.accepted for g in all_f if g.accepted.date() == pr]
        ev.update(
            ann_form=f.form, ann_adsh=f.adsh, ann_accepted_et=f.accepted.isoformat(), pr_date=pr.isoformat(),
            first_same_day_accept_et=min(same_day).isoformat() if same_day else "",
            consideration=terms.get("consideration", ""), cash=terms.get("cash", ""), ratio=terms.get("ratio", ""),
            cvr=terms.get("cvr", ""), cvr_max=terms.get("cvr_max", ""), premium_pct=terms.get("premium_pct", ""),
            premium_ref=terms.get("premium_ref", ""),
            tickers_mentioned="|".join(terms.get("tickers_mentioned", [])),
            cash_candidates="|".join(map(str, terms.get("cash_candidates", []))), score=score,
            status="ok" if terms.get("consideration") else "no_terms",
        )
        return ev
    ev["status"] = "no_announcement_found"
    return ev


def build_events(deals: list[dict], out_csv: Path, workers: int = 4, done: set | None = None) -> None:
    done = done or set()
    todo = [d for d in deals if d["deal_id"] not in done]
    new_file = not out_csv.exists()
    with open(out_csv, "a", newline="") as fh, ThreadPoolExecutor(workers) as pool:
        w = csv.DictWriter(fh, fieldnames=EVENT_FIELDS)
        if new_file:
            w.writeheader()
        for i, ev in enumerate(pool.map(_safe_build, todo)):
            w.writerow(ev)
            fh.flush()
            if i % 25 == 0:
                print(f"[{i}/{len(todo)}] {ev['company'][:40]:40s} {ev['ticker']:6s} {ev['status']} "
                      f"{ev['consideration']} {ev['cash']} {ev['ratio']}", flush=True)


def _safe_build(deal: dict) -> dict:
    try:
        return build_event(deal)
    except Exception as e:  # keep the batch going; record the failure
        ev = {k: "" for k in EVENT_FIELDS}
        ev.update(deal_id=deal["deal_id"], cik=deal["cik"], company=deal["company"],
                  anchor_form=deal["anchor_form"], anchor_date=deal["anchor_date"].isoformat(),
                  status=f"error:{type(e).__name__}:{str(e)[:80]}")
        return ev
