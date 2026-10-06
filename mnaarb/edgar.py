"""SEC EDGAR access: quarterly form indexes, company submissions, filing documents, full-text search."""
from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

from . import http

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

# Form types that only exist because a public company is being acquired.
#   PREM14A/DEFM14A  merger proxy filed by the target (shareholder vote)
#   SC 14D9          target's recommendation statement in a tender offer
#   SC14D9C          target's pre-commencement tender-offer communication (often filed on announcement day)
ANCHOR_FORMS = ("PREM14A", "DEFM14A", "SC 14D9", "SC14D9C")

# Filings that can carry the announcement press release on day 0.
ANNOUNCE_FORMS = ("8-K", "DEFA14A", "SC14D9C", "425", "SC TO-C", "6-K")


def _formidx_cache(year: int, qtr: int) -> Path:
    return http.CACHE_DIR / "formidx" / f"{year}Q{qtr}.csv"


def form_index(year: int, qtr: int, forms=ANCHOR_FORMS) -> list[dict]:
    """Rows of the EDGAR quarterly form.idx restricted to `forms` (cached as a small CSV)."""
    path = _formidx_cache(year, qtr)
    today = date.today()
    current = (year, qtr) == (today.year, (today.month - 1) // 3 + 1)
    if path.exists() and not current:
        with open(path) as f:
            rows = list(csv.DictReader(f))
        return [r for r in rows if r["form"] in forms]
    url = f"https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{qtr}/form.idx"
    body = http.get(url, cache=False, timeout=180)
    if body is None:
        return []
    rows = []
    for line in body.decode("latin-1").splitlines():
        # fixed-width-ish: form type, company, cik, date, filename separated by 2+ spaces
        m = re.match(r"^(\S.*?)\s{2,}(.+?)\s{2,}(\d+)\s+(\d{4}-\d{2}-\d{2})\s+(edgar/\S+)", line)
        if not m:
            continue
        form = m.group(1).strip()
        if form not in ANCHOR_FORMS + ANNOUNCE_FORMS + ("SC TO-T",):
            continue
        rows.append({"form": form, "company": m.group(2).strip(), "cik": m.group(3),
                     "date": m.group(4), "file": m.group(5)})
    path.parent.mkdir(parents=True, exist_ok=True)
    keep = [r for r in rows if r["form"] in ANCHOR_FORMS + ("SC TO-T",)]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["form", "company", "cik", "date", "file"])
        w.writeheader()
        w.writerows(keep)
    return [r for r in keep if r["form"] in forms]


def announce_index(year: int, qtr: int, forms=("DEFA14A", "SC14D9C", "SC TO-C", "425")) -> list[dict]:
    """Rows of form.idx for announcement-day form types (cached separately from the anchor index)."""
    path = http.CACHE_DIR / "formidx" / f"{year}Q{qtr}_announce.csv"
    today = date.today()
    current = (year, qtr) == (today.year, (today.month - 1) // 3 + 1)
    if not (path.exists() and not current):
        body = http.get(f"https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{qtr}/form.idx", cache=False, timeout=180)
        rows = []
        for line in (body or b"").decode("latin-1").splitlines():
            m = re.match(r"^(\S.*?)\s{2,}(.+?)\s{2,}(\d+)\s+(\d{4}-\d{2}-\d{2})\s+(edgar/\S+)", line)
            if m and m.group(1).strip() in ANNOUNCE_FORMS:
                rows.append({"form": m.group(1).strip(), "company": m.group(2).strip(), "cik": m.group(3),
                             "date": m.group(4), "file": m.group(5)})
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["form", "company", "cik", "date", "file"])
            w.writeheader()
            w.writerows([r for r in rows if r["form"] != "8-K"])
    with open(path) as f:
        return [r for r in csv.DictReader(f) if r["form"] in forms]


def submissions(cik: int | str, full: bool = False) -> dict | None:
    """data.sec.gov submissions JSON. With full=True, older filing pages are merged in."""
    cik = int(cik)
    body = http.get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    if body is None:
        return None
    d = json.loads(body)
    if full:
        recent = d["filings"]["recent"]
        for page in d["filings"].get("files", []):
            b = http.get(f"https://data.sec.gov/submissions/{page['name']}")
            if not b:
                continue
            older = json.loads(b)
            for k in recent:
                recent[k] = recent[k] + older.get(k, [])
    return d


def listed_ciks() -> dict[int, str]:
    """CIK -> ticker for every company SEC currently maps to an exchange ticker (one request)."""
    body = http.get("https://www.sec.gov/files/company_tickers.json", ttl=86400)
    d = json.loads(body)
    out: dict[int, str] = {}
    for v in d.values():
        out.setdefault(int(v["cik_str"]), v["ticker"])
    return out


@dataclass
class Filing:
    cik: int
    form: str
    filing_date: date
    accepted: datetime  # timezone-aware, America/New_York
    adsh: str
    items: str
    primary_doc: str

    @property
    def folder(self) -> str:
        return f"https://www.sec.gov/Archives/edgar/data/{self.cik}/{self.adsh.replace('-', '')}"

    @property
    def txt_url(self) -> str:
        return f"https://www.sec.gov/Archives/edgar/data/{self.cik}/{self.adsh}.txt"


def filings(sub: dict) -> list[Filing]:
    r = sub["filings"]["recent"]
    out = []
    cik = int(sub["cik"])
    for i in range(len(r["form"])):
        acc = r["acceptanceDateTime"][i]
        try:
            accepted = datetime.fromisoformat(acc.replace("Z", "+00:00")).astimezone(ET)
        except ValueError:
            continue
        out.append(Filing(cik, r["form"][i], date.fromisoformat(r["filingDate"][i]), accepted,
                          r["accessionNumber"][i], r["items"][i] or "", r["primaryDocument"][i]))
    return out


_DOC_RE = re.compile(r"<DOCUMENT>(.*?)</DOCUMENT>", re.S | re.I)


def filing_documents(f: Filing) -> list[dict]:
    """Split the full submission text file into its documents: [{type, filename, text_html}]."""
    body = http.get(f.txt_url, timeout=120)
    if body is None:
        return []
    raw = body.decode("utf-8", errors="replace")
    docs = []
    for m in _DOC_RE.finditer(raw):
        chunk = m.group(1)
        typ = re.search(r"<TYPE>([^\n<]+)", chunk)
        fn = re.search(r"<FILENAME>([^\n<]+)", chunk)
        t = typ.group(1).strip() if typ else ""
        if t.upper().startswith(("GRAPHIC", "ZIP", "EXCEL", "XML", "JSON", "EX-101")) or t.upper() == "PDF":
            continue
        docs.append({"type": t, "filename": fn.group(1).strip() if fn else "", "html": chunk})
    return docs


def efts_search(q: str, forms: str | None = None, start: str | None = None, end: str | None = None,
                ciks: str | None = None, page_from: int = 0) -> dict | None:
    """EDGAR full-text search (2001+). Returns the raw JSON response."""
    params = {"q": q}
    if forms:
        params["forms"] = forms
    if start or end:
        params.update({"dateRange": "custom", "startdt": start or "2001-01-01", "enddt": end or date.today().isoformat()})
    if ciks:
        params["ciks"] = ciks
    if page_from:
        params["from"] = page_from
    body = http.get("https://efts.sec.gov/LATEST/search-index?" + urlencode(params))
    return json.loads(body) if body else None


def current_feed_url(form: str = "8-K", count: int = 100) -> str:
    """Atom feed of the latest filings (what the live monitor polls)."""
    return ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent"
            f"&type={form}&company=&dateb=&owner=include&count={count}&output=atom")
