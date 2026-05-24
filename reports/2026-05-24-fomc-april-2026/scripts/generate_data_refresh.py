#!/usr/bin/env python3
"""Generate data-refresh.md from data_refresh.json."""
import json
import os
from datetime import datetime

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(WORKSPACE, "scripts/data_refresh.json")) as f:
    data = json.load(f)

def css(val: float, is_pct: bool = False) -> str:
    cls = "num" if abs(val) < 0.005 else ("up" if val > 0 else "down")
    if is_pct:
        return f'<span class="{cls}">{val:+.2f}%</span>'
    return f'<span class="{cls}">{val}</span>'

def css_num(val) -> str:
    return f'<span class="num">{val}</span>'

lines = []
lines.append("---")
lines.append("date: 2026-05-24")
lines.append("event: fomc-april-2026")
lines.append("type: data-refresh")
lines.append("source: yfinance (yfinance 1.4.0)")
lines.append("fetched_at: 2026-05-24T" + datetime.utcnow().strftime("%H:%M:%S"))
lines.append("as_of: 2026-05-22 close")
lines.append("asset_classes:")
lines.append("  - equities")
lines.append("  - rates")
lines.append("  - commodities")
lines.append("  - fx")
lines.append("tickers:")
lines.append("  - SPY | QQQ | IWM | TLT | XLU | XLF | XLRE")
lines.append("  - ^TNX")
lines.append("  - AAPL | MSFT | NVDA | META | GOOGL | AMZN")
lines.append("  - JPM | GS | BAC | PLD | NEE | WMT")
lines.append("  - GLD | CL=F")
lines.append("  - DX-Y.NYB | GBPUSD=X")
lines.append("tags:")
lines.append("  - yfinance")
lines.append("  - market-data")
lines.append("  - snapshot")
lines.append("  - may-22-2026")
lines.append("---")
lines.append("")
lines.append("# Data Refresh: yfinance Market Data Snapshot")
lines.append("")
lines.append(f'**As of:** <span class="num">2026-05-22</span> close  |  '
             f'**Fetched:** <span class="num">2026-05-24</span> UTC')
lines.append("")
lines.append("Returns computed from Dec 31, 2025 close (YTD) and Apr 29, 2026 close (Post-FOMC).")
lines.append("")
lines.append('<span class="up">up</span> / <span class="down">down</span> = day-over-day change. '
             '<span class="num">num</span> = numeric value.')
lines.append("")
lines.append("---")
lines.append("")

# --- 1. Broad Market & Sector ETFs ---
lines.append("## 1. Broad Market & Sector ETFs")
lines.append("")
hdr = "| Ticker | Name | <span class=\"num\">Price</span> | <span class=\"num\">Chg %</span> | <span class=\"num\">YTD %</span> | <span class=\"num\">Post-FOMC %</span> |"
sep = "|--------|------|------:|------:|------:|------:|"
lines.append(hdr)
lines.append(sep)

market = [
    ("SPY", "S&P 500 ETF"),
    ("QQQ", "Nasdaq-100 ETF"),
    ("IWM", "Russell 2000 ETF"),
    ("TLT", "20+ Year Treasury ETF"),
    ("XLU", "Utilities Select Sector"),
    ("XLF", "Financials Select Sector"),
    ("XLRE", "Real Estate Select Sector"),
]

for sym, name in market:
    t = data[sym]
    # Use round for price formatting without trailing zeros
    price = css_num(round(t["latest_price"], 2))
    chg_pct = css(t["daily_pct"], is_pct=True)
    ytd = css(t["ytd_pct"], is_pct=True)
    fomc = css(t["fomc_pct"], is_pct=True)
    lines.append(f"| {sym} | {name} | {price} | {chg_pct} | {ytd} | {fomc} |")

lines.append("")

# --- 2. Rate Benchmarks ---
lines.append("## 2. Rate Benchmarks")
lines.append("")
hdr2 = "| Ticker | Name | <span class=\"num\">Yield</span> | <span class=\"num\">Chg %</span> | <span class=\"num\">YTD %</span> | <span class=\"num\">Post-FOMC %</span> |"
sep2 = "|--------|------|------:|------:|------:|------:|"
lines.append(hdr2)
lines.append(sep2)

t_tnx = data["^TNX"]
lines.append(f"| ^TNX | 10Y Treasury Yield | {css_num(t_tnx['latest_price']):s}% | "
             f"{css(t_tnx['daily_pct'], is_pct=True)} | {css(t_tnx['ytd_pct'], is_pct=True)} | "
             f"{css(t_tnx['fomc_pct'], is_pct=True)} |")

lines.append("")

# --- 3. Individual Stocks ---
lines.append("## 3. Individual Stocks")
lines.append("")
hdr3 = "| Ticker | Name | Sector | <span class=\"num\">Price</span> | <span class=\"num\">Chg %</span> | <span class=\"num\">YTD %</span> | <span class=\"num\">Post-FOMC %</span> |"
sep3 = "|--------|------|--------|------:|------:|------:|------:|"
lines.append(hdr3)
lines.append(sep3)

stocks = [
    ("AAPL", "Apple Inc", "Technology"),
    ("MSFT", "Microsoft Corp", "Technology"),
    ("NVDA", "NVIDIA Corp", "Technology"),
    ("META", "Meta Platforms", "Communication Services"),
    ("GOOGL", "Alphabet Inc", "Communication Services"),
    ("AMZN", "Amazon.com Inc", "Consumer Cyclical"),
    ("JPM", "JPMorgan Chase", "Financial Services"),
    ("GS", "Goldman Sachs", "Financial Services"),
    ("BAC", "Bank of America", "Financial Services"),
    ("PLD", "Prologis Inc", "Real Estate"),
    ("NEE", "NextEra Energy", "Utilities"),
    ("WMT", "Walmart Inc", "Consumer Defensive"),
]

for sym, name, sector in stocks:
    t = data[sym]
    price = css_num(round(t["latest_price"], 2))
    chg_pct = css(t["daily_pct"], is_pct=True)
    ytd = css(t["ytd_pct"], is_pct=True)
    fomc = css(t["fomc_pct"], is_pct=True)
    lines.append(f"| {sym} | {name} | {sector} | {price} | {chg_pct} | {ytd} | {fomc} |")

lines.append("")

# --- 4. Commodities ---
lines.append("## 4. Commodities")
lines.append("")
hdr4 = "| Ticker | Name | <span class=\"num\">Price</span> | <span class=\"num\">Chg %</span> | <span class=\"num\">YTD %</span> | <span class=\"num\">Post-FOMC %</span> |"
sep4 = "|--------|------|------:|------:|------:|------:|"
lines.append(hdr4)
lines.append(sep4)

commodities = [
    ("GLD", "Gold ETF"),
    ("CL=F", "Crude Oil WTI Futures"),
]

for sym, name in commodities:
    t = data[sym]
    price = css_num(round(t["latest_price"], 2))
    chg_pct = css(t["daily_pct"], is_pct=True)
    ytd = css(t["ytd_pct"], is_pct=True)
    fomc = css(t["fomc_pct"], is_pct=True)
    lines.append(f"| {sym} | {name} | {price} | {chg_pct} | {ytd} | {fomc} |")

lines.append("")

# --- 5. Foreign Exchange ---
lines.append("## 5. Foreign Exchange")
lines.append("")
hdr5 = "| Ticker | Name | <span class=\"num\">Price</span> | <span class=\"num\">Chg %</span> | <span class=\"num\">YTD %</span> | <span class=\"num\">Post-FOMC %</span> |"
sep5 = "|--------|------|------:|------:|------:|------:|"
lines.append(hdr5)
lines.append(sep5)

fx = [
    ("DX-Y.NYB", "US Dollar Index"),
    ("GBPUSD=X", "GBP/USD"),
]

for sym, name in fx:
    t = data[sym]
    price = css_num(round(t["latest_price"], 2))
    chg_pct = css(t["daily_pct"], is_pct=True)
    ytd = css(t["ytd_pct"], is_pct=True)
    fomc = css(t["fomc_pct"], is_pct=True)
    lines.append(f"| {sym} | {name} | {price} | {chg_pct} | {ytd} | {fomc} |")

lines.append("")
lines.append("---")
lines.append("")

# --- Day Change Summary ---
up_tickers = []
down_tickers = []
flat_tickers = []

for sym, t in data.items():
    if abs(t["daily_pct"]) < 0.01:
        flat_tickers.append(sym)
    elif t["daily_pct"] > 0:
        up_tickers.append(sym)
    else:
        down_tickers.append(sym)

lines.append("## Day Change Summary")
lines.append("")
lines.append("| Direction | Count | Tickers |")
lines.append("|-----------|------:|---------|")
lines.append(f'| <span class="up">Up</span> | {len(up_tickers)} | {", ".join(sorted(up_tickers))} |')
lines.append(f'| <span class="down">Down</span> | {len(down_tickers)} | {", ".join(sorted(down_tickers))} |')
if flat_tickers:
    lines.append(f'| <span class="num">Flat</span> | {len(flat_tickers)} | {", ".join(sorted(flat_tickers))} |')

lines.append("")

# --- YTD Leaders / Laggards ---
lines.append("## YTD Return Leaders & Laggards")
lines.append("")
lines.append("### Top 5 Performers YTD")
lines.append("")
lines.append("| Rank | Ticker | YTD % | Post-FOMC % |")
lines.append("|------|--------|------:|------:|")

ytd_sorted = [(t["ytd_pct"], t["fomc_pct"], sym) for sym, t in data.items()]
ytd_sorted.sort(key=lambda x: x[0], reverse=True)
for i, (ytd_val, fomc_val, sym) in enumerate(ytd_sorted[:5], 1):
    lines.append(f"| {i} | {sym} | {css(ytd_val, is_pct=True)} | {css(fomc_val, is_pct=True)} |")

lines.append("")
lines.append("### Bottom 5 Performers YTD")
lines.append("")
lines.append("| Rank | Ticker | YTD % | Post-FOMC % |")
lines.append("|------|--------|------:|------:|")
for i, (ytd_val, fomc_val, sym) in enumerate(ytd_sorted[-5:], 1):
    lines.append(f"| {i} | {sym} | {css(ytd_val, is_pct=True)} | {css(fomc_val, is_pct=True)} |")

lines.append("")

# --- Post-FOMC Leaders / Laggards ---
lines.append("## Post-FOMC Return Leaders & Laggards")
lines.append("")
lines.append("### Top 5 Post-FOMC")
lines.append("")
lines.append("| Rank | Ticker | Post-FOMC % | YTD % |")
lines.append("|------|--------|------:|------:|")

fomc_sorted = [(t["fomc_pct"], t["ytd_pct"], sym) for sym, t in data.items()]
fomc_sorted.sort(key=lambda x: x[0], reverse=True)
for i, (fomc_val, ytd_val, sym) in enumerate(fomc_sorted[:5], 1):
    lines.append(f"| {i} | {sym} | {css(fomc_val, is_pct=True)} | {css(ytd_val, is_pct=True)} |")

lines.append("")
lines.append("### Bottom 5 Post-FOMC")
lines.append("")
lines.append("| Rank | Ticker | Post-FOMC % | YTD % |")
lines.append("|------|--------|------:|------:|")
for i, (fomc_val, ytd_val, sym) in enumerate(fomc_sorted[-5:], 1):
    lines.append(f"| {i} | {sym} | {css(fomc_val, is_pct=True)} | {css(ytd_val, is_pct=True)} |")

lines.append("")
lines.append("---")
lines.append("")

# Notes
lines.append("## Notes")
lines.append("")
lines.append('- Data sourced from **yfinance 1.4.0**. All prices reflect most recent available close as of <span class="num">2026-05-22</span>.')
lines.append("- US markets were closed May 23-24 (weekend). Data reflects May 22 close.")
lines.append("- YTD return computed from Dec 31, 2025 close to May 22, 2026 close.")
lines.append("- Post-FOMC return computed from Apr 29, 2026 close (FOMC day) to May 22, 2026 close.")
lines.append("- Gold price via GLD ETF. Crude Oil via CL=F continuous futures contract.")
lines.append("- GBP/USD reflects the latest available forex quote.")

# Notable stats for notes
top_ytd = ytd_sorted[0]
bot_ytd = ytd_sorted[-1]
lines.append(f"- YTD leaders: {top_ytd[2]} +{top_ytd[0]:.2f}% (top), {ytd_sorted[1][2]} +{ytd_sorted[1][0]:.2f}%, {ytd_sorted[2][2]} +{ytd_sorted[2][0]:.2f}%.")
lines.append(f"- YTD laggards: {bot_ytd[2]} {bot_ytd[0]:+.2f}% (bottom), {ytd_sorted[-2][2]} {ytd_sorted[-2][0]:+.2f}%, {ytd_sorted[-3][2]} {ytd_sorted[-3][0]:+.2f}%.")
lines.append(f"- Post-FOMC leader: {fomc_sorted[0][2]} +{fomc_sorted[0][0]:.2f}%.")
lines.append(f"- Post-FOMC laggard: {fomc_sorted[-1][2]} {fomc_sorted[-1][0]:.2f}%.")

output = "\n".join(lines) + "\n"
outpath = os.path.join(WORKSPACE, "data-refresh.md")
with open(outpath, "w") as f:
    f.write(output)
print(f"Wrote {len(lines)} lines to {outpath}")