#!/usr/bin/env python3
"""Refresh yfinance market data for all tickers."""
import yfinance as yf
import pandas as pd
from datetime import datetime, date
import sys

TICKERS = [
    # Broad market
    "SPY", "QQQ", "IWM", "^TNX", "DX-Y.NYB",
    # Sector ETFs
    "TLT", "XLU", "XLF", "XLRE",
    # Mega-cap tech
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    # Banks
    "JPM", "GS", "BAC",
    # Other holdings
    "PLD", "NEE", "WMT",
    # Commodities & FX
    "GC=F", "CL=F", "GBPUSD=X",
]

NAMES = {
    "SPY": "S&P 500",
    "QQQ": "Nasdaq-100",
    "IWM": "Small Caps (Russell)",
    "^TNX": "10Y Treasury Yield",
    "DX-Y.NYB": "US Dollar Index (DXY)",
    "TLT": "20+ Year Treasury",
    "XLU": "Utilities",
    "XLF": "Financials",
    "XLRE": "Real Estate",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "META": "Meta",
    "GOOGL": "Alphabet",
    "AMZN": "Amazon",
    "JPM": "JPMorgan Chase",
    "GS": "Goldman Sachs",
    "BAC": "Bank of America",
    "PLD": "Prologis",
    "NEE": "NextEra Energy",
    "WMT": "Walmart",
    "GC=F": "Gold (Futures)",
    "CL=F": "Crude Oil (WTI)",
    "GBPUSD=X": "GBP/USD",
}

SECTIONS = {
    "Broad Market & Indices": ["SPY", "QQQ", "IWM", "^TNX", "DX-Y.NYB"],
    "Sector ETFs": ["TLT", "XLU", "XLF", "XLRE"],
    "Mega-Cap Tech": ["AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN"],
    "Banks": ["JPM", "GS", "BAC"],
    "Other Holdings": ["PLD", "NEE", "WMT"],
    "Commodities & FX": ["GC=F", "CL=F", "GBPUSD=X"],
}

# Base dates
YTD_START = "2026-01-02"  # Jan 1 is holiday
POST_FOMC_START = "2026-04-29"

def fmt_pct(val, is_yield=False):
    """Format percentage with span class."""
    if pd.isna(val):
        return "<span class=\"num\">N/A</span>"
    
    # For ^TNX (yield), daily/YTD are in bps changes, format as %
    if abs(val) < 0.0001:
        return "<span class=\"num\">0.00%</span>"
    
    if val > 0:
        cls = "up"
        sign = "+"
    elif val < 0:
        cls = "down"
        sign = ""  # negative sign is included in val
    else:
        cls = "num"
        sign = ""
    
    return f"<span class=\"{cls}\">{sign}{val:.2f}%</span>"

def fmt_price(val, ticker):
    """Format price value."""
    if pd.isna(val):
        return "<span class=\"num\">N/A</span>"
    
    if "^TNX" in ticker:
        # Yield - format as percentage
        return f"<span class=\"num\">{val:.2f}%</span>"
    elif "GC=F" in ticker:
        return f"<span class=\"num\">{val:.2f}</span>"
    elif "GBPUSD=X" in ticker:
        return f"<span class=\"num\">{val:.4f}</span>"
    elif val > 100:
        return f"<span class=\"num\">{val:.2f}</span>"
    else:
        return f"<span class=\"num\">{val:.2f}</span>"

def main():
    print("Fetching data for all tickers...", file=sys.stderr)
    
    # Fetch data without group_by='ticker' to avoid auto_adjust bug
    df = yf.download(
        TICKERS,
        start="2026-01-01",
        end="2026-05-25",  # slightly into future to catch latest close
        auto_adjust=True,
        progress=False,
    )
    
    print(f"Data shape: {df.shape}", file=sys.stderr)
    print(f"Columns: {df.columns.names if hasattr(df.columns, 'names') else df.columns}", file=sys.stderr)
    
    # Get close prices
    closes = df['Close']
    print(f"Close data index: {closes.index[-1]} to {closes.index[0]}", file=sys.stderr)
    print(f"Tickers available: {list(closes.columns)}", file=sys.stderr)
    
    # Find the last two trading days for daily change
    dates = closes.index.sort_values()
    last_date = dates[-1]
    # Find prev close (last trading day before last_date)
    if len(dates) >= 2:
        prev_date = dates[-2]
    else:
        prev_date = last_date
    
    print(f"Last date: {last_date.date()}, prev date: {prev_date.date()}", file=sys.stderr)
    
    # YTD base: Jan 2, 2026
    ytd_base = pd.Timestamp(YTD_START)
    # Post-FOMC base: Apr 29, 2026
    fomc_base = pd.Timestamp(POST_FOMC_START)
    
    # Get actual dates in the data
    ytd_date = ytd_base if ytd_base in closes.index else dates[dates >= ytd_base][0]
    fomc_date = fomc_base if fomc_base in closes.index else dates[dates >= fomc_base][0]
    
    print(f"YTD base date used: {ytd_date.date()}", file=sys.stderr)
    print(f"FOMC base date used: {fomc_date.date()}", file=sys.stderr)
    
    # Handle ^TNX specially - it's a yield, so changes are in percentage points
    # For YTD and Post-FOMC on yields, we compute relative change anyway
    
    results = {}
    for ticker in TICKERS:
        if ticker not in closes.columns:
            print(f"WARNING: {ticker} not in close data", file=sys.stderr)
            continue
        
        series = closes[ticker].dropna()
        if len(series) == 0:
            print(f"WARNING: {ticker} has no data", file=sys.stderr)
            continue
        
        last_close = series.iloc[-1]
        prev_close = series.iloc[-2] if len(series) >= 2 else series.iloc[-1]
        
        # Daily change: (last - prev) / prev * 100
        daily_pct = ((last_close - prev_close) / prev_close) * 100
        
        # YTD: from ytd_date to last_date
        ytd_close = series[series.index >= ytd_date].iloc[0]
        ytd_pct = ((last_close - ytd_close) / ytd_close) * 100
        
        # Post-FOMC: from fomc_date to last_date
        fomc_series = series[series.index >= fomc_date]
        fomc_close = fomc_series.iloc[0]
        fomc_pct = ((last_close - fomc_close) / fomc_close) * 100
        
        results[ticker] = {
            "price": last_close,
            "daily_pct": daily_pct,
            "ytd_pct": ytd_pct,
            "fomc_pct": fomc_pct,
            "last_date": series.index[-1],
        }
        
        name = NAMES.get(ticker, ticker)
        print(f"  {ticker:12s} {name:25s} ${last_close:>8.2f}  daily:{daily_pct:>+6.2f}%  ytd:{ytd_pct:>+6.2f}%  fomc:{fomc_pct:>+6.2f}%", file=sys.stderr)
    
    # Generate markdown
    now = datetime.now()
    data_as_of_str = now.strftime("%Y-%m-%d")
    
    # Determine data freshness note
    last_dates = [r["last_date"] for r in results.values() if r["last_date"] is not None]
    if last_dates:
        max_date = max(last_dates)
        min_date = min(last_dates)
        if max_date.date() == min_date.date():
            date_note = f"{max_date.date()}"
        else:
            date_note = f"{min_date.date()} (most tickers); GBPUSD {max_date.date()}"
    else:
        date_note = data_as_of_str
    
    lines = []
    lines.append("---")
    lines.append(f"date: {data_as_of_str}")
    lines.append("event: fomc-april-2026")
    lines.append("type: data-refresh")
    lines.append("source: yfinance")
    lines.append(f"data_as_of: {data_as_of_str}")
    lines.append("tags:")
    lines.append("  - data-refresh")
    lines.append("  - yfinance")
    lines.append("---")
    lines.append("")
    lines.append(f"# Data Refresh: {now.strftime('%B %d, %Y')}")
    lines.append("")
    lines.append(f"**Data as of close:** {date_note}")
    lines.append("**Periods:** Daily change (prev close) | YTD (Jan 1, 2026) | Post-FOMC (Apr 29, 2026)")
    lines.append("")
    
    for section_name, ticker_list in SECTIONS.items():
        lines.append(f"## {section_name}")
        lines.append("")
        lines.append("| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |")
        lines.append("|--------|------|-------|-------|-----|-----------|")
        
        for i, ticker in enumerate(ticker_list):
            if ticker not in results:
                continue
            r = results[ticker]
            name = NAMES.get(ticker, ticker)
            
            price_str = fmt_price(r["price"], ticker)
            daily_str = fmt_pct(r["daily_pct"])
            ytd_str = fmt_pct(r["ytd_pct"])
            fomc_str = fmt_pct(r["fomc_pct"])
            
            lines.append(f"| {ticker} | {name} | {price_str} | {daily_str} | {ytd_str} | {fomc_str} |")
        
        lines.append("")
    
    lines.append("## Notes")
    lines.append("")
    lines.append(f"- Data via yfinance. Close of {max_date.date()} (last trading day before report date).")
    lines.append(f"- GBPUSD=X reflects weekend session data through {max_date.date()}.")
    lines.append("- YTD base: Jan 2, 2026 (Jan 1 is a holiday). Post-FOMC base: Apr 29, 2026 (FOMC decision date).")
    lines.append("- Gold via GC=F (COMEX futures). Crude oil via CL=F (WTI futures).")
    lines.append("- DXY via DX-Y.NYB (US Dollar Index futures). GBP/USD via GBPUSD=X.")
    lines.append("- Span classes: up (green), down (red), num (neutral). No emojis.")
    lines.append("- YTD changes use auto_adjust=True in yfinance, so dividend adjustments are applied to historical prices.")
    lines.append("")
    
    output = "\n".join(lines)
    
    outpath = "/home/ty/workspace/investment-research/reports/2026-05-24-fomc-april-2026/data-refresh.md"
    with open(outpath, "w") as f:
        f.write(output)
    
    print(f"\nWritten to {outpath}", file=sys.stderr)
    print(f"Total lines: {len(lines)}", file=sys.stderr)

if __name__ == "__main__":
    main()