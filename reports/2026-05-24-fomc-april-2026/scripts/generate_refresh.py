#!/usr/bin/env python3
"""Generate data-refresh.md from market_data.json with proper formatting."""
import json

with open("scripts/market_data.json") as f:
    data = json.load(f)

r = data["results"]
pull_date = data["pull_date"]  # 2026-05-25

# Format helpers
def fmt_price(ticker, price, decimals):
    """Format price with appropriate decimal places."""
    if ticker == "^TNX":
        return f'{price:.{decimals}f}%'
    else:
        return f'{price:.{decimals}f}'

def span_cls(value):
    """Return span class: up, down, or num (for zero or neutral)."""
    if value > 0:
        return "up"
    elif value < 0:
        return "down"
    else:
        return "num"

def fmt_pct(value):
    """Format percentage with sign."""
    sign = "+" if value > 0 else ""
    return f'{sign}{value:.2f}%'

def span_pct(value):
    """Generate <span class="X">Y%</span> for a percentage value."""
    cls = span_cls(value)
    pct = fmt_pct(value)
    return f'<span class="{cls}">{pct}</span>'

def span_price(ticker, price, decimals):
    """Generate <span class="num">X</span> for price."""
    formatted = fmt_price(ticker, price, decimals)
    return f'<span class="num">{formatted}</span>'

# Determine latest dates for the note
date_map = {}
for ticker, v in r.items():
    d = v["latest_date"]
    if d not in date_map:
        date_map[d] = []
    date_map[d].append(ticker)

# Determine the latest close descriptions
if "2026-05-22" in date_map:
    eq_note = "Equities, bonds, rates as of May 22 (Friday)"
if "2026-05-24" in date_map:
    cm_note = "Commodities, DXY as of May 24 (Sunday)"
if "2026-05-25" in date_map:
    fx_note = "GBP/USD as of May 25 (Monday)"

note = f"**Latest close data by asset class:** {eq_note}. {cm_note}. {fx_note}."

lines = []
lines.append("---")
lines.append("date: 2026-05-25")
lines.append("event: fomc-april-2026")
lines.append("type: data-refresh")
lines.append("source: yfinance")
lines.append(f"data_as_of: 2026-05-25")
lines.append("tags:")
lines.append("  - data-refresh")
lines.append("  - yfinance")
lines.append("---")
lines.append("")
lines.append("# Data Refresh: May 25, 2026")
lines.append("")
lines.append(note)
lines.append("**Periods:** Daily change (prev close) | YTD (Jan 2, 2026) | Post-FOMC (Apr 29, 2026)")
lines.append("")

SECTIONS = {
    "Broad Market & Indices": ["SPY", "QQQ", "IWM", "^TNX", "DX-Y.NYB"],
    "Sector ETFs": ["TLT", "XLU", "XLF", "XLRE"],
    "Mega-Cap Tech": ["AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN"],
    "Banks": ["JPM", "GS", "BAC"],
    "Other Holdings": ["PLD", "NEE", "WMT"],
    "Commodities & FX": ["GC=F", "CL=F", "GBPUSD=X"],
}

NAMES = {
    "SPY": "S&P 500", "QQQ": "Nasdaq-100", "IWM": "Small Caps (Russell)",
    "TLT": "20+ Year Treasury", "XLU": "Utilities", "XLF": "Financials",
    "XLRE": "Real Estate", "^TNX": "10Y Treasury Yield",
    "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "NVIDIA",
    "META": "Meta", "GOOGL": "Alphabet", "AMZN": "Amazon",
    "JPM": "JPMorgan Chase", "GS": "Goldman Sachs", "BAC": "Bank of America",
    "PLD": "Prologis", "NEE": "NextEra Energy", "WMT": "Walmart",
    "GC=F": "Gold (Futures)", "CL=F": "Crude Oil (WTI)",
    "DX-Y.NYB": "US Dollar Index (DXY)", "GBPUSD=X": "GBP/USD",
}

for section_name, tickers in SECTIONS.items():
    lines.append(f"## {section_name}")
    lines.append("")
    lines.append("| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |")
    lines.append("|--------|------|-------|-------|-----|-----------|")
    
    for t in tickers:
        v = r[t]
        price = v["price"]
        daily = v["daily_pct"]
        ytd = v["ytd_pct"]
        fomc = v["fomc_pct"]
        
        price_str = span_price(t, price, v["decimals"])
        daily_str = span_pct(daily)
        ytd_str = span_pct(ytd)
        fomc_str = span_pct(fomc)
        
        name = NAMES[t]
        lines.append(f"| {t} | {name} | {price_str} | {daily_str} | {ytd_str} | {fomc_str} |")
    
    lines.append("")

lines.append("## Notes")
lines.append("")
lines.append("- Data via yfinance (1.4.0). Close dates vary by asset class: equities/bonds/rates close May 22, commodities/DXY close May 24, GBP/USD close May 25.")
lines.append("- YTD base: Jan 2, 2026 (Jan 1 is a holiday). Post-FOMC base: Apr 29, 2026 (FOMC decision date).")
lines.append("- Gold via GC=F (COMEX futures). Crude oil via CL=F (WTI futures).")
lines.append("- DXY via DX-Y.NYB (US Dollar Index futures). GBP/USD via GBPUSD=X.")
lines.append("- Span classes: up (green), down (red), num (neutral). No emojis.")
lines.append("- YTD changes use auto_adjust=True in yfinance, so dividend adjustments are applied to historical prices.")

output = "\n".join(lines) + "\n"
with open("data-refresh.md", "w") as f:
    f.write(output)

print("Written to data-refresh.md")
print(f"File length: {len(output)} chars")