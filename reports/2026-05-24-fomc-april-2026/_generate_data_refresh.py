#!/usr/bin/env python3
"""Generate data-refresh.md from fetched data."""
import json

# Load data
with open("/tmp/fomc_data.json") as f:
    data = json.load(f)

def fmt_pct(val):
    """Format a percentage value with span class."""
    if val == 0:
        return f'<span class="num">0.00%</span>'
    elif val > 0:
        return f'<span class="up">+{val:.2f}%</span>'
    else:
        return f'<span class="down">{val:.2f}%</span>'

def fmt_price(val, ticker):
    if val is None:
        return '<span class="num">N/A</span>'
    if ticker == "^TNX":
        return f'<span class="num">{val:.3f}%</span>'
    elif ticker == "GC=F":
        return f'<span class="num">${val:,.1f}</span>'
    elif ticker in ("CL=F",):
        return f'<span class="num">${val:.1f}</span>'
    else:
        return f'<span class="num">${val:.2f}</span>'

def row(ticker, name):
    d = data.get(ticker, {})
    if "error" in d:
        price = '<span class="num">N/A</span>'
        daily = '<span class="num">N/A</span>'
        ytd = '<span class="num">N/A</span>'
        pf = '<span class="num">N/A</span>'
    else:
        price = fmt_price(d.get("price"), ticker)
        daily = fmt_pct(d.get("daily_pct", 0))
        ytd = fmt_pct(d.get("ytd_pct", 0))
        pf = fmt_pct(d.get("post_fomc_pct", 0))
    return f"| {ticker} | {name} | {price} | {daily} | {ytd} | {pf} |"

# Categories
indices = [
    ("SPY", "S&P 500"),
    ("QQQ", "Nasdaq 100"),
    ("IWM", "Russell 2000"),
    ("^TNX", "10Y Yield"),
    ("DXY", "US Dollar Index"),
]

sectors = [
    ("TLT", "20Y+ Treasury"),
    ("XLU", "Utilities"),
    ("XLF", "Financials"),
    ("XLRE", "Real Estate"),
]

megacap = [
    ("AAPL", "Apple"),
    ("MSFT", "Microsoft"),
    ("NVDA", "NVIDIA"),
    ("META", "Meta"),
    ("GOOGL", "Alphabet"),
    ("AMZN", "Amazon"),
]

banks = [
    ("JPM", "JPMorgan"),
    ("GS", "Goldman Sachs"),
    ("BAC", "Bank of America"),
]

holdings = [
    ("PLD", "Prologis"),
    ("NEE", "NextEra Energy"),
    ("WMT", "Walmart"),
]

commodities = [
    ("GC=F", "Gold"),
    ("CL=F", "Crude Oil"),
    ("GBPUSD=X", "GBP/USD"),
]

lines = []
lines.append("---")
lines.append("date: 2026-05-24")
lines.append("event: fomc-april-2026")
lines.append("type: data-refresh")
lines.append("source: yfinance")
lines.append("data_as_of: 2026-05-24")
lines.append("tags:")
lines.append("  - data-refresh")
lines.append("  - yfinance")
lines.append("---")
lines.append("")
lines.append("# Data Refresh: May 24, 2026")
lines.append("")
lines.append("**Data as of close:** 2026-05-24")
lines.append("**Periods:** Daily change (prev close) | YTD (Jan 1, 2026) | Post-FOMC (Apr 29, 2026)")
lines.append("")
lines.append("## Broad Market & Indices")
lines.append("")
lines.append("| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |")
lines.append("|--------|------|-------|-------|-----|-----------|")
for t, n in indices:
    lines.append(row(t, n))
lines.append("")
lines.append("## Sector ETFs")
lines.append("")
lines.append("| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |")
lines.append("|--------|------|-------|-------|-----|-----------|")
for t, n in sectors:
    lines.append(row(t, n))
lines.append("")
lines.append("## Mega-Cap Tech")
lines.append("")
lines.append("| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |")
lines.append("|--------|------|-------|-------|-----|-----------|")
for t, n in megacap:
    lines.append(row(t, n))
lines.append("")
lines.append("## Banks")
lines.append("")
lines.append("| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |")
lines.append("|--------|------|-------|-------|-----|-----------|")
for t, n in banks:
    lines.append(row(t, n))
lines.append("")
lines.append("## Other Holdings")
lines.append("")
lines.append("| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |")
lines.append("|--------|------|-------|-------|-----|-----------|")
for t, n in holdings:
    lines.append(row(t, n))
lines.append("")
lines.append("## Commodities & FX")
lines.append("")
lines.append("| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |")
lines.append("|--------|------|-------|-------|-----|-----------|")
for t, n in commodities:
    lines.append(row(t, n))
lines.append("")
lines.append("## Notes")
lines.append("")
lines.append("- Data via yfinance. Close of 2026-05-24 (last trading day before report date).")
lines.append("- DXY (DX-Y.NYB) returned no data from yfinance for the date range.")
lines.append("- YTD base: Jan 2, 2026 (Jan 1 is a holiday). Post-FOMC base: Apr 29, 2026 (FOMC decision date).")
lines.append("- Gold via GC=F (COMEX futures). Crude oil via CL=F (WTI futures).")
lines.append("- GBP/USD via GBPUSD=X.")
lines.append("- Span classes: up (green), down (red), num (neutral). No emojis.")
lines.append("- YTD changes use auto_adjust=True in yfinance, so dividend adjustments are applied.")

output = "\n".join(lines) + "\n"

with open("/home/ty/workspace/investment-research/reports/2026-05-24-fomc-april-2026/data-refresh.md", "w") as f:
    f.write(output)

print("data-refresh.md written successfully")
print(f"Size: {len(output)} bytes")
print(f"Lines: {len(lines)}")