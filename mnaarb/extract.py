"""Rule-based extraction of deal terms from announcement press releases / 8-K text.

This is deliberately transparent (regexes, not a black-box model) so every extracted number
can be audited. The same functions are used by the live detector.
"""
from __future__ import annotations

import re
from collections import Counter
from datetime import date, datetime

import lxml.html

NUM = r"(\d{1,4}(?:,\d{3})*(?:\.\d{1,4})?)"
DOLLAR = r"(?:U\.?S\.?\s?)?\$\s?"
SHARE = (r"(?:per|a|for\s+each(?:\s+(?:issued\s+and\s+)?outstanding)?)\s+"
         r"(?:share|common\s+share|ordinary\s+share|ADS|American\s+Depositary\s+Share|unit)s?")

CASH_PATTERNS = [
    # $28.00 per share in cash / $28.00 per share of common stock in cash
    DOLLAR + NUM + r"\s*" + SHARE + r"(?:\s+of\s+[^$.;]{0,80}?(?:stock|shares))?,?\s+(?:payable\s+)?in\s+cash",
    # right to receive $28.00 in cash
    r"right\s+to\s+receive\s+" + DOLLAR + NUM + r"\s+(?:per\s+share\s+)?in\s+cash",
    # $28.00 in cash, without interest, per share / for each share
    DOLLAR + NUM + r"\s+in\s+cash(?:,?\s+without\s+interest)?(?:\s+and\s+less\s+[^,]{0,40})?,?\s+(?:per\s+share|for\s+each)",
    # at a price of $28.00 per share, net to the seller in cash
    r"(?:price|offer\s+price)\s+of\s+" + DOLLAR + NUM + r"\s+per\s+share,?\s+net\s+to\s+the\s+(?:seller|holder)s?\s+in\s+cash",
    # $28.00 per share in an all-cash transaction / all-cash ... $28.00 per share
    DOLLAR + NUM + r"\s+" + SHARE + r"\s+in\s+an?\s+all[- ]cash",
    r"all[- ]cash\s+(?:transaction|deal|offer|tender\s+offer|merger|acquisition)[^.$]{0,160}?" + DOLLAR + NUM + r"\s+" + SHARE,
    r"cash\s+consideration\s+of\s+" + DOLLAR + NUM + r"\s+" + SHARE,
]
GENERIC_PRICE = r"(?:acquire|purchase|buy|acquisition\s+of)[^.$]{0,200}?for\s+" + DOLLAR + NUM + r"\s+" + SHARE

STOCK_PATTERNS = [
    r"(\d+\.\d{2,6})\s+(?:shares?|of\s+a\s+share|common\s+shares?|ordinary\s+shares?)\s+of\s+(?:the\s+)?"
    r"([A-Z][^.;$]{1,80}?)\s+(?:class\s+a\s+)?(?:common\s+stock|common\s+shares|ordinary\s+shares|stock)\s+"
    r"(?:for|per|in\s+exchange\s+for)\s+each",
    r"exchange\s+ratio\s+of\s+(\d+\.\d{2,6})",
    r"receive\s+(\d+\.\d{2,6})\s+(?:shares?|of\s+a\s+share)",
    r"(\d+\.\d{2,6})\s+(?:shares?|of\s+a\s+share)\s+of\s+[^.;$]{1,60}?\s+for\s+each\s+(?:share|outstanding)",
]
CVR_RE = re.compile(r"contingent\s+value\s+rights?", re.I)
CVR_VAL = re.compile(r"(?:up\s+to|aggregate\s+of\s+up\s+to|potential\s+(?:additional\s+)?(?:payment|value)\s+of(?:\s+up\s+to)?)\s+"
                     + DOLLAR + NUM, re.I)
PREMIUM_RE = re.compile(
    r"premium\s+of\s+(?:approximately\s+|about\s+|roughly\s+)?(\d{1,3}(?:\.\d+)?)\s?(?:%|percent)\s+(?:to|over|above)\s+"
    r"([^.;]{0,160})", re.I)
PREMIUM_RE2 = re.compile(
    r"(\d{1,3}(?:\.\d+)?)\s?(?:%|percent)\s+premium\s+(?:to|over|above)\s+([^.;]{0,160})", re.I)
TICKER_RE = re.compile(
    r"\(\s*(?:NYSE(?:\s+American|\s+MKT|\s+Arca)?|NASDAQ|Nasdaq|NasdaqGS|NasdaqGM|NasdaqCM|Nasdaq\s+Global\s+Select|"
    r"TSX|TSXV|LSE|AIM|ASX|OTC|OTCQX|OTCQB)\s*:\s*([A-Z][A-Z0-9\.]{0,6})", re.I)
MERGER_RE = re.compile(
    r"definitive\s+(?:merger\s+)?agreement|agreement\s+and\s+plan\s+of\s+merger|merger\s+agreement|"
    r"tender\s+offer|to\s+be\s+acquired|agreed\s+to\s+(?:be\s+)?acquire|take[- ]private|go[- ]private|"
    r"plan\s+of\s+arrangement|scheme\s+of\s+arrangement", re.I)
SELF_TARGET_RE = re.compile(
    r"merge\s+with\s+and\s+into\s+the\s+Company|to\s+be\s+acquired\s+by|will\s+be\s+acquired\s+by|"
    r"wholly[- ]owned\s+subsidiary\s+of\s+Parent|tender\s+offer\s+(?:to\s+purchase|for)\s+all\s+(?:of\s+)?the\s+"
    r"(?:issued\s+and\s+)?outstanding\s+shares\s+of\s+(?:the\s+)?Company|"
    r"Company\s+will\s+(?:survive|become)\s+[^.]{0,40}wholly[- ]owned\s+subsidiary", re.I)
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATELINE_RE = re.compile(rf"\b({MONTHS}|Jan\.|Feb\.|Mar\.|Apr\.|Aug\.|Sept?\.|Oct\.|Nov\.|Dec\.)\s+(\d{{1,2}}),\s+(20\d\d)")
_MON = {m[:3].lower(): i + 1 for i, m in enumerate(MONTHS.split("|"))}


def html_to_text(html: str) -> str:
    html = re.sub(r"<(TYPE|SEQUENCE|FILENAME|DESCRIPTION)>[^\n]*", " ", html, flags=re.I)
    m = re.search(r"<TEXT>(.*)</TEXT>", html, re.S | re.I)
    if m:
        html = m.group(1)
    try:
        if "<" in html and ">" in html:
            doc = lxml.html.fromstring(html)
            for bad in doc.xpath("//script|//style"):
                bad.drop_tree()
            text = doc.text_content()
        else:
            text = html
    except Exception:
        text = re.sub(r"<[^>]+>", " ", html)
    text = (text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"')
            .replace("–", "-").replace("—", "-").replace("&#160;", " ").replace("&nbsp;", " "))
    return re.sub(r"\s+", " ", text)


def _num(s: str) -> float:
    return float(s.replace(",", ""))


def parse_date(text: str) -> date | None:
    m = DATELINE_RE.search(text[:3000])
    if not m:
        return None
    try:
        return date(int(m.group(3)), _MON[m.group(1)[:3].lower()], int(m.group(2)))
    except (KeyError, ValueError):
        return None


WIRE_RE = re.compile(r"(?:/\s*PRNewswire|BUSINESS\s+WIRE|GLOBE\s+NEWSWIRE|ACCESSWIRE|ACCESS\s+Newswire|/\s*CNW|"
                     r"Marketwired|EQS|/\s*PRNewswire-FirstCall)", re.I)


def parse_dateline(text: str) -> date | None:
    """Date in a press-release dateline ('BOSTON, Jan. 13, 2025 /PRNewswire/ --'); falls back to first date."""
    head = text[:4000]
    w = WIRE_RE.search(head)
    if w:
        m = list(DATELINE_RE.finditer(head[max(0, w.start() - 200): w.end() + 120]))
        if m:
            g = m[-1] if m[-1].end() <= 200 + (w.end() - w.start()) else m[0]
            try:
                return date(int(g.group(3)), _MON[g.group(1)[:3].lower()], int(g.group(2)))
            except (KeyError, ValueError):
                pass
    return parse_date(text[:1500])


def extract_terms(text: str) -> dict:
    """Pull per-share deal terms out of free text. All fields optional."""
    out: dict = {}
    cash = []
    for pat in CASH_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            v = _num(m.group(1))
            if 0.05 <= v <= 5000:
                cash.append(v)
    if not cash:
        for m in re.finditer(GENERIC_PRICE, text, re.I):
            v = _num(m.group(1))
            if 0.05 <= v <= 5000:
                cash.append(v)
        if cash:
            out["cash_generic"] = True
    if cash:
        c = Counter(cash)
        out["cash"] = c.most_common(1)[0][0]
        out["cash_candidates"] = sorted(c)
    ratios = []
    for pat in STOCK_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            v = _num(m.group(1))
            if 0.001 <= v <= 50:
                ratios.append(v)
    if ratios:
        out["ratio"] = Counter(ratios).most_common(1)[0][0]
    if CVR_RE.search(text):
        out["cvr"] = True
        vals = []
        for m in CVR_RE.finditer(text):
            win = text[max(0, m.start() - 300): m.end() + 300]
            vals += [_num(x.group(1)) for x in CVR_VAL.finditer(win)]
        if vals:
            out["cvr_max"] = Counter(vals).most_common(1)[0][0]
    prem = []
    for rx in (PREMIUM_RE, PREMIUM_RE2):
        for m in rx.finditer(text):
            pct, ctx = float(m.group(1)), m.group(2).lower()
            kind = "vwap" if ("vwap" in ctx or "volume" in ctx or "average" in ctx) else (
                "close" if ("clos" in ctx or "unaffected" in ctx or "last" in ctx or "price on" in ctx) else "other")
            prem.append((kind, pct))
    for kind in ("close", "other", "vwap"):
        vals = [p for k, p in prem if k == kind]
        if vals:
            out["premium_pct"] = vals[0]
            out["premium_ref"] = kind
            break
    tick = [t.upper() for t in TICKER_RE.findall(text)]
    if tick:
        out["tickers_mentioned"] = list(dict.fromkeys(tick))
    if "cash" in out and "ratio" in out:
        out["consideration"] = "mixed"
    elif "cash" in out:
        out["consideration"] = "cash"
    elif "ratio" in out:
        out["consideration"] = "stock"
    return out


def short_name(company: str) -> str:
    """'Intra-Cellular Therapies, Inc.' -> 'Intra-Cellular Therapies'."""
    s = re.sub(r"[,\.]?\s+(inc|corp|corporation|co|company|ltd|limited|plc|holdings?|group|n\.v|s\.a|lp|l\.p|llc|trust)\.?$",
               "", company.strip(), flags=re.I)
    s = re.sub(r"\s*/\w+/?$", "", s)  # EDGAR state suffixes like /DE/
    return s.strip(" ,.")


def is_target_announcement(text: str, company: str) -> tuple[bool, int]:
    """Heuristic: does this text announce that `company` itself is being acquired?"""
    score = 0
    if MERGER_RE.search(text):
        score += 1
    if SELF_TARGET_RE.search(text):
        score += 2
    name = short_name(company)
    first = re.escape(name.split()[0]) if name else None
    if first and len(name.split()[0]) >= 3:
        if re.search(r"(?:acquire|acquisition\s+of|to\s+buy|purchase\s+of|take\s+private)\s+(?:all\s+(?:of\s+)?(?:the\s+)?"
                     r"(?:outstanding\s+)?(?:shares\s+of\s+)?)?" + first, text, re.I):
            score += 2
        if re.search(first + r"[^.]{0,120}(?:to\s+be\s+acquired|will\s+be\s+acquired|enters?\s+into\s+(?:a\s+)?definitive"
                             r"\s+agreement\s+to\s+be\s+acquired)", text, re.I):
            score += 2
    return score >= 3, score
