"""Shared HTTP layer: per-host rate limiting, retries and an on-disk cache."""
from __future__ import annotations

import gzip
import hashlib
import os
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = Path(os.environ.get("MNAARB_CACHE", ROOT / "data" / "cache"))

# SEC asks automated clients to declare who they are and to stay under 10 req/s.
SEC_UA = os.environ.get("MNAARB_SEC_UA", "mnaarb-research research@example.com")
DEFAULT_UA = os.environ.get("MNAARB_UA", "mnaarb-research research@example.com")
# Some hosts reject non-browser agents (Yahoo answers 429); others reset browser agents (GlobeNewswire).
BROWSER_UA = "Mozilla/5.0"
_BROWSER_HOSTS = ("finance.yahoo.com",)

_RATE = {  # max requests per second per host
    "www.sec.gov": 8,
    "data.sec.gov": 8,
    "efts.sec.gov": 2,
    "query1.finance.yahoo.com": 4,
    "query2.finance.yahoo.com": 4,
}
_last: dict[str, float] = {}
_lock = threading.Lock()
_session = requests.Session()


def _throttle(host: str) -> None:
    rate = _RATE.get(host, 5)
    with _lock:
        wait = _last.get(host, 0) + 1.0 / rate - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last[host] = time.monotonic()


def _headers(host: str) -> dict:
    if host.endswith("sec.gov"):
        return {"User-Agent": SEC_UA, "Accept-Encoding": "gzip, deflate"}
    if host.endswith(_BROWSER_HOSTS):
        return {"User-Agent": BROWSER_UA}
    return {"User-Agent": DEFAULT_UA}


def _cache_path(url: str) -> Path:
    h = hashlib.sha1(url.encode()).hexdigest()
    return CACHE_DIR / h[:2] / f"{h}.gz"


def get(url: str, *, cache: bool = True, ttl: float | None = None, retries: int = 4,
        timeout: float = 30) -> bytes | None:
    """GET a URL, returning the body or None on a 404. Cached on disk unless cache=False.

    ttl: seconds after which a cached copy is considered stale (None = never).
    """
    path = _cache_path(url)
    if cache and path.exists() and (ttl is None or time.time() - path.stat().st_mtime < ttl):
        with gzip.open(path, "rb") as f:
            body = f.read()
        return None if body == b"__404__" else body
    host = urlparse(url).netloc
    for attempt in range(retries):
        _throttle(host)
        try:
            r = _session.get(url, headers=_headers(host), timeout=timeout)
        except requests.RequestException:
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 200:
            if cache:
                path.parent.mkdir(parents=True, exist_ok=True)
                with gzip.open(path, "wb") as f:
                    f.write(r.content)
            return r.content
        if r.status_code == 404:
            if cache:
                path.parent.mkdir(parents=True, exist_ok=True)
                with gzip.open(path, "wb") as f:
                    f.write(b"__404__")
            return None
        # 429 / 403 (SEC throttling) / 5xx: back off and retry
        time.sleep(2 ** (attempt + 1))
    return None
