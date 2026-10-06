"""Turn results/*.csv into the tables and figures used in REPORT.md.

Writes results/tables.md and results/fig_*.png
"""
import sys
from pathlib import Path

sys.path.insert(0, ".")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mnaarb import backtest as bt

OUT = Path("results")
# reference palette (dataviz skill): categorical slots 1-3, recessive ink
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False, "font.size": 10, "axes.titlesize": 11,
    "axes.titleweight": "bold", "axes.titlecolor": INK, "legend.frameon": False, "lines.linewidth": 2,
})

md: list[str] = []


def table(df: pd.DataFrame, title: str, fmt: dict | None = None) -> None:
    d = df.copy()
    for c, f in (fmt or {}).items():
        if c in d:
            d[c] = d[c].map(lambda v: f.format(v) if pd.notna(v) else "")
    md.append(f"\n### {title}\n")
    md.append(d.to_markdown())


daily = pd.read_csv(OUT / "daily_events.csv")
ev = bt.load_events()
md.append("# Generated tables\n")
md.append(f"events with extracted terms and a live ticker: {len(ev)}  \n")
md.append(f"daily rows: {len(daily)}; dq counts: {daily.dq.value_counts().to_dict()}  \n")

# ---------------------------------------------------------------- sample definition
d = daily[(daily.dq == "ok") & (daily.flag == "ok")].copy()
d = d[d.premium.between(0.05, 2.0)]                    # meaningful gap to capture
d["leaked"] = np.where(d.stated_premium.notna(),
                       d.premium < 0.6 * d.stated_premium,   # market had already moved before t0
                       d.runup_20d > 0.15)
d["cash_only"] = (d.consideration == "cash") & (~d.cvr.astype(bool))
d["liq"] = pd.qcut(d.adv_usd_60.rank(method="first"), 3, labels=["low ADV", "mid ADV", "high ADV"])
d["prem_b"] = pd.cut(d.premium, [0.05, 0.2, 0.4, 0.7, 2.0], labels=["5-20%", "20-40%", "40-70%", "70%+"])
d["cap_b"] = d.cap_open.map(bt.capture_bucket)
d.to_csv(OUT / "daily_sample.csv", index=False)
md.append(f"\nclean sample (dq ok, reaction found, 5%-200% premium): **{len(d)}** deals; "
          f"cash-only {int(d.cash_only.sum())}, leaked {int(d.leaked.sum())}  \n")

# the d0 open is a valid post-news price only when the news was provably out before 9:30 ET
d.loc[~d.news_before_open.astype(bool), "cap_open"] = np.nan

# ---------------------------------------------------------------- capture path
cols = ["cap_open", "cap_d0_close", "cap_d1_close", "cap_d2_close", "cap_d5_close", "cap_d10_close", "cap_d20_close"]
labels = ["open d0", "close d0", "close d1", "close d2", "close d5", "close d10", "close d20"]
cp = d.groupby("leaked")[cols].median().T
cp.index = labels
cp.columns = ["surprise" if not c else "leaked/rumoured" for c in cp.columns]
table(cp, "Median capture ratio by horizon (0 = pre-announcement close, 1 = offer)", {c: "{:.3f}" for c in cp})

fig, ax = plt.subplots(figsize=(7.2, 3.8))
for (lk, g), col in zip(d.groupby("leaked"), (BLUE, ORANGE)):
    q = g[cols].quantile([0.25, 0.5, 0.75])
    x = np.arange(len(cols)) + 1
    ax.plot(np.r_[0, x], np.r_[0, q.loc[0.5].values], color=col, marker="o", ms=4,
            label=("leaked / rumoured before t0" if lk else "surprise announcement") + f" (n={len(g)})")
    ax.fill_between(x, q.loc[0.25].values, q.loc[0.75].values, color=col, alpha=0.12, lw=0)
ax.set_xticks(range(len(cols) + 1), ["close d-1"] + labels, rotation=0, fontsize=8)
ax.axhline(1, color=INK2, lw=0.8, ls="--")
ax.set_ylabel("capture ratio")
ax.set_ylim(-0.1, 1.25)
ax.set_title("Most of the move is already in the first regular-session price")
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "fig_daily_capture.png", dpi=160)
plt.close(fig)

# ---------------------------------------------------------------- strategy returns
def strat(df, col, by, title):
    rows = []
    for k, g in df.groupby(by, observed=True):
        r = g[col].dropna()
        if len(r) == 0:
            continue
        rows.append({by: k, "n": len(r), "mean": r.mean(), "median": r.median(), "hit": (r > 0).mean(),
                     "t": r.mean() / (r.std(ddof=1) / np.sqrt(len(r))) if len(r) > 2 else np.nan,
                     "mean net 25bp": r.mean() - 0.0025, "mean net 100bp": r.mean() - 0.01})
    t = pd.DataFrame(rows).set_index(by)
    table(t, title, {"mean": "{:.2%}", "median": "{:.2%}", "hit": "{:.0%}", "t": "{:.2f}",
                     "mean net 25bp": "{:.2%}", "mean net 100bp": "{:.2%}"})
    return t


order = ["<25%", "25-50%", "50-80%", "80-95%", "95-102%", ">102%"]
d["cap_b"] = pd.Categorical(d.cap_b, order)
md.append(f"\nnews provably public before the d0 open (EDGAR accepted < 9:30 ET on d0): "
          f"{int(d.news_before_open.sum())} of {len(d)} deals. Open-entry tests use only these; for the rest "
          "the d0 open may predate the news (that would be look-ahead).  \n")
d_all = d
d = d[d.news_before_open].copy()
strat(d, "ret_open_d0_close", "cap_b", "Buy at d0 open, sell at d0 close - by capture at the open")
strat(d, "ret_open_d1_close", "cap_b", "Buy at d0 open, sell at d1 close - by capture at the open")
strat(d, "ret_open_d5_close", "cap_b", "Buy at d0 open, sell at d5 close - by capture at the open")
strat(d[d.cash_only], "ret_open_d0_close", "cap_b", "Cash-only deals: buy d0 open, sell d0 close")
strat(d, "ret_open_d0_close", "liq", "Buy d0 open, sell d0 close - by liquidity tercile")
strat(d, "ret_open_d0_close", "prem_b", "Buy d0 open, sell d0 close - by premium")
strat(d, "ret_open_d0_close", "accept_session", "Buy d0 open, sell d0 close - by EDGAR acceptance session")
d_all["cap_close_b"] = pd.Categorical(d_all.cap_d0_close.map(bt.capture_bucket), order)
strat(d_all, "ret_close_d1_close", "cap_close_b", "Buy d0 close, sell d1 close (day-after drift) - by capture at d0 close (all deals)")
strat(d_all, "ret_close_d5_close", "cap_close_b", "Buy d0 close, sell d5 close - by capture at d0 close (all deals)")
strat(d_all, "ret_close_d20_close", "consideration", "Buy d0 close, hold 20 days (classic arb start) - by consideration")

# the user's proposed rule
rule = d[d.cap_open < 0.5]
md.append(f"\n**User rule 'enter only if <50% repriced' at the d0 open**: triggers on {len(rule)} of {len(d)} deals "
          f"({len(rule) / max(1, len(d)):.0%}).  \n")
if len(rule):
    show = rule[["ticker", "t0", "consideration", "premium", "stated_premium", "runup_20d", "cap_open",
                 "cap_d0_close", "cap_d5_close", "ret_open_d0_close", "ret_open_d5_close"]].sort_values("t0")
    table(show.set_index("ticker"), "Deals where the open was <50% repriced (what you would have bought)",
          {c: "{:.2f}" for c in ["premium", "stated_premium", "runup_20d", "cap_open", "cap_d0_close", "cap_d5_close"]}
          | {"ret_open_d0_close": "{:.2%}", "ret_open_d5_close": "{:.2%}"})

fig, ax = plt.subplots(figsize=(7.2, 3.4))
g = d.dropna(subset=["cap_open"])
ax.hist(g.cap_open.clip(-0.2, 1.4), bins=np.arange(-0.2, 1.45, 0.05), color=BLUE, edgecolor=SURF, lw=1.5)
ax.axvline(0.5, color=ORANGE, lw=2)
ax.text(0.48, ax.get_ylim()[1] * 0.92, "proposed entry rule:\ncapture < 50%", ha="right", va="top", fontsize=8, color=INK2)
ax.set_xlabel("capture ratio at the first regular-session print (d0 open)")
ax.set_ylabel("deals")
ax.set_title(f"Where the stock opens after an announcement (n={len(g)})")
fig.tight_layout()
fig.savefig(OUT / "fig_open_capture_hist.png", dpi=160)
plt.close(fig)

# ---------------------------------------------------------------- timing of announcements
acc = pd.to_datetime(ev.ann_accepted_et, utc=True).dt.tz_convert("America/New_York")
hrs = acc.dt.hour + acc.dt.minute / 60
sess = pd.cut(hrs, [0, 9.5, 16, 24], right=False, labels=["before 9:30", "9:30-16:00", "after 16:00"])
table(sess.value_counts().to_frame("filings").assign(share=lambda x: x.filings / x.filings.sum()),
      "EDGAR acceptance time of the announcement filing (ET)", {"share": "{:.0%}"})
fig, ax = plt.subplots(figsize=(7.2, 3.0))
ax.hist(hrs, bins=np.arange(5, 23, 0.5), color=BLUE, edgecolor=SURF, lw=1.5)
ax.axvspan(9.5, 16, color=GRID, alpha=0.5, lw=0)
ax.text(12.75, ax.get_ylim()[1] * 0.9, "regular session", ha="center", fontsize=8, color=INK2)
ax.set_xlabel("hour of EDGAR acceptance (ET)")
ax.set_ylabel("announcements")
ax.set_title("Announcement filings cluster before the open and after the close")
fig.tight_layout()
fig.savefig(OUT / "fig_accept_hour.png", dpi=160)
plt.close(fig)

# ---------------------------------------------------------------- intraday
ip = OUT / "intraday_events.csv"
if ip.exists():
    it = pd.read_csv(ip)
    it = it[it.dq == "ok"].copy()
    it = it[it.premium.between(0.05, 2.0)]
    it.to_csv(OUT / "intraday_sample.csv", index=False)
    md.append(f"\nintraday sample: {len(it)} cash deals; by bar size {it.interval.value_counts().to_dict()}  \n")
    cc = ["cap_prev_bar", "cap_react_open", "cap_react_close", "cap_+5m", "cap_+15m", "cap_+30m", "cap_+60m",
          "cap_reg_open", "cap_reg_close", "cap_d1_close"]
    t = it.groupby("interval")[[c for c in cc if c in it]].median().T
    t["all"] = it[[c for c in cc if c in it]].median()
    t["n"] = it[[c for c in cc if c in it]].count()
    table(t, "Median intraday capture around the first reaction (by bar size)", {c: "{:.3f}" for c in t if c != "n"})
    lag = it.edgar_lag_min
    md.append(f"\nEDGAR acceptance minus first price reaction (minutes): median {lag.median():.1f}, "
              f"share where price reacted before the EDGAR filing {(lag > 0).mean():.0%} (n={lag.notna().sum()})  \n")
    show = it[["ticker", "interval", "t_react", "react_session", "edgar_lag_min", "premium", "cap_prev_bar",
               "cap_react_open", "cap_react_close", "cap_reg_open", "cap_reg_close", "cap_d1_close"]].sort_values("t_react")
    table(show.set_index("ticker"), "Per-deal intraday detail",
          {c: "{:.2f}" for c in ["edgar_lag_min", "premium", "cap_prev_bar", "cap_react_open", "cap_react_close",
                                 "cap_reg_open", "cap_reg_close", "cap_d1_close"]})
    fine = it[it.interval.isin(["1m", "5m"])]
    if len(fine):
        fig, ax = plt.subplots(figsize=(7.2, 3.6))
        steps = ["cap_prev_bar", "cap_react_open", "cap_react_close", "cap_+5m", "cap_+15m", "cap_+30m", "cap_+60m"]
        xl = ["last print\nbefore", "first print\nafter news", "end of\n1st bar", "+5m", "+15m", "+30m", "+60m"]
        for _, r in fine.iterrows():
            ax.plot(range(len(steps)), r[steps].astype(float).values, color=BLUE if r.interval == "1m" else AQUA,
                    lw=1, alpha=0.45)
        ax.plot(range(len(steps)), fine[steps].median().values, color=INK, lw=2.5, label="median")
        ax.axhline(1, color=INK2, lw=0.8, ls="--")
        ax.set_xticks(range(len(steps)), xl, fontsize=8)
        ax.set_ylim(-0.3, 1.3)
        ax.set_ylabel("capture ratio")
        ax.set_title(f"Intraday: the jump happens inside the first bar (1m/5m bars, n={len(fine)})")
        ax.plot([], [], color=BLUE, lw=1, label="1-minute bars")
        ax.plot([], [], color=AQUA, lw=1, label="5-minute bars")
        ax.legend(fontsize=8, loc="lower right")
        fig.tight_layout()
        fig.savefig(OUT / "fig_intraday_capture.png", dpi=160)
        plt.close(fig)

(OUT / "tables.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
