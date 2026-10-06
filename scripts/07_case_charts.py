"""Per-deal intraday charts: price vs offer with the EDGAR acceptance time marked.

usage: python scripts/07_case_charts.py TICKER [TICKER ...]
"""
import sys
from datetime import datetime, time, timedelta

sys.path.insert(0, ".")
import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from mnaarb import backtest as bt, intraday, prices

BLUE, ORANGE, INK, INK2, GRID, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": GRID, "axes.grid": True,
                     "grid.color": GRID, "axes.spines.top": False, "axes.spines.right": False, "font.size": 9,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlesize": 10, "axes.titleweight": "bold"})

ev = bt.load_events()
res = pd.read_csv("results/intraday_events.csv")
for tk in sys.argv[1:]:
    r = ev[ev.ticker == tk].iloc[-1]
    x = res[(res.ticker == tk) & (res.dq == "ok")]
    if x.empty:
        print(tk, "no intraday result")
        continue
    x = x.iloc[0]
    t_react = pd.Timestamp(x.t_react)
    acc = r.accepted
    lo = min(t_react, acc) - timedelta(hours=1)
    hi = max(t_react, acc) + timedelta(hours=2)
    if prices.session_of(t_react) == "pre":
        hi = max(hi, pd.Timestamp(datetime.combine(t_react.date(), time(10, 30)), tz=prices.ET))
    px = prices.yahoo_intraday(tk, lo.to_pydatetime() - timedelta(hours=12), hi.to_pydatetime(), x.interval)
    px = px[(px.index >= lo) & (px.index <= hi)]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.step(px.index, px.close, where="post", color=BLUE, lw=1.6, label=f"{tk} last trade ({x.interval} bars)")
    span = x.offer - x.p_ref
    ax.set_ylim(min(x.p_ref, px.close.min()) - 0.08 * abs(span), max(x.offer, px.close.max()) + 0.12 * abs(span))
    ax.axhline(x.offer, color=INK2, ls="--", lw=1)
    ax.text(hi, x.offer, f"offer ${x.offer:g} ", ha="right", va="bottom", fontsize=8, color=INK2)
    ax.axhline(x.p_ref, color=INK2, lw=0.8, ls=":")
    ax.text(hi, x.p_ref, f"prior close ${x.p_ref:.2f} ", ha="right", va="bottom", fontsize=8, color=INK2)
    ax.axvline(acc, color=ORANGE, lw=1.5)
    ax.text(acc, x.p_ref + 0.45 * span, f" EDGAR accepted {acc:%H:%M}", color=INK, fontsize=8, va="center")
    open_t = pd.Timestamp(datetime.combine(t_react.date(), time(9, 30)), tz=prices.ET)
    if lo < open_t < hi:
        ax.axvspan(lo, open_t, color=GRID, alpha=0.35, lw=0)
        ax.text(open_t, ax.get_ylim()[1], " 9:30 open ", ha="right", va="top", fontsize=8, color=INK2)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=prices.ET))
    ax.set_title(f"{r.company[:40]} ({tk}), {t_react.date()}: first print after news "
                 f"{x.cap_react_open:.0%} repriced, end of that bar {x.cap_react_close:.0%}")
    ax.set_xlim(lo, hi)
    ax.legend(loc="lower right", fontsize=8, frameon=False, bbox_to_anchor=(1, 0.08))
    fig.tight_layout()
    fig.savefig(f"results/case_{tk}.png", dpi=160)
    plt.close(fig)
    print("wrote", f"results/case_{tk}.png")
