"""Secondary event class: public NON-BINDING acquisition proposals (13D Item 4 letters, 8-K/press releases).

These are announced acquisitions too, but with real uncertainty, so the market prices them at a
deep discount to the proposal price. Question: does the price keep drifting after the first print?
"""
from __future__ import annotations

import re
from datetime import date, datetime

import pandas as pd

from . import edgar, extract, http

QUERIES = ['"non-binding proposal" "per share in cash"', '"unsolicited proposal" "per share in cash"',
           '"non-binding indication of interest" "per share"', '"preliminary non-binding proposal" "per share"']
FORMS = "SC 13D,SC 13D/A,SCHEDULE 13D,SCHEDULE 13D/A,8-K,6-K,DFAN14A,SC 14D9"


def search(start: str = "2016-01-01", end: str | None = None) -> pd.DataFrame:
    end = end or date.today().isoformat()
    rows = []
    for q in QUERIES:
        frm = 0
        while True:
            d = edgar.efts_search(q, forms=FORMS, start=start, end=end, page_from=frm)
            if not d:
                break
            hits = d["hits"]["hits"]
            for h in hits:
                s = h["_source"]
                # pick the entity that has a ticker in its display name (the subject company)
                for name, cik in zip(s["display_names"], s["ciks"]):
                    m = re.search(r"\(([A-Z][A-Z0-9\.\-]{0,6})(?:,|\))", name)
                    if m:
                        rows.append({"cik": int(cik), "company": name.split("  (")[0], "ticker": m.group(1),
                                     "file_date": s["file_date"], "form": s["form"], "adsh": h["_id"].split(":")[0],
                                     "doc": h["_id"].split(":")[1], "query": q})
                        break
            frm += len(hits)
            if not hits or frm >= d["hits"]["total"]["value"] or frm >= 1000:
                break
    df = pd.DataFrame(rows).drop_duplicates(["adsh", "doc"])
    return df


def acceptance_time(cik: int, adsh: str) -> datetime | None:
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{adsh.replace('-', '')}/{adsh}-index-headers.html"
    b = http.get(url)
    if not b:
        return None
    m = re.search(rb"ACCEPTANCE-DATETIME>\s*(\d{14})", b)
    if not m:
        return None
    return datetime.strptime(m.group(1).decode(), "%Y%m%d%H%M%S").replace(tzinfo=edgar.ET)


def first_proposals(hits: pd.DataFrame, gap_days: int = 365) -> pd.DataFrame:
    """Earliest proposal filing per subject company (new episode after `gap_days` of silence)."""
    hits = hits.sort_values("file_date")
    out, last = [], {}
    for _, r in hits.iterrows():
        d = date.fromisoformat(r.file_date)
        if r.cik in last and (d - last[r.cik]).days <= gap_days:
            last[r.cik] = d
            continue
        last[r.cik] = d
        out.append(r)
    return pd.DataFrame(out)


def enrich(row) -> dict:
    """Proposal price + acceptance timestamp for one filing."""
    cik_folder = None
    for c in [row.cik]:
        cik_folder = c
    url = f"https://www.sec.gov/Archives/edgar/data/{cik_folder}/{row.adsh.replace('-', '')}/{row.doc}"
    b = http.get(url)
    text = extract.html_to_text(b.decode("utf-8", errors="replace")) if b else ""
    terms = extract.extract_terms(text)
    if "cash" not in terms:  # proposals often read "$X.XX per share" without "in cash"
        m = re.search(r"(?:proposal|offer|price|acquire)[^.$]{0,200}?" + extract.DOLLAR + extract.NUM + r"\s+per\s+(?:share|ordinary|ADS)",
                      text, re.I)
        if m:
            terms["cash"] = float(m.group(1).replace(",", ""))
    acc = acceptance_time(row.cik, row.adsh)
    return {"cash": terms.get("cash"), "accepted": acc.isoformat() if acc else "", "cvr": terms.get("cvr", False)}
