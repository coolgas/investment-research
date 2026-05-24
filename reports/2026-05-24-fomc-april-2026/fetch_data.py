#!/usr/bin/env python3
"""Fetch fresh market data via yfinance for FOMC market brief."""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date

TICKERS = {
    # Indices — DXY replaced with DX-Y.NYB (US Dollar Index futures)
    "SPY": "S&P 500",
    "QQQ": "Nasdaq-100",
    "IWM": "Small Caps (Russell)",
    "^TNX": "10Y Treasury Yield",
    "DX-Y.NYB": "US Dollar Index",  # DXY equivalent
    # Sectors
    "TLT": "20+ Year Treasury",
    "XLU": "Utilities",
    "XLF": "Financials",
    "XLRE": "Real Estate",
    # Mega-Cap Tech
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "META": "Meta",
    "GOOGL": "Alphabet",
    "AMZN": "Amazon",
    # Banks
    "JPM": "JPMorgan Chase",
    "GS": "Goldman Sachs",
    "BAC": "Bank of America",
    # Other Holdings
    "PLD": "Prologis",
    "NEE": "NextEra Energy",
    "WMT": "Walmart",
    # Commodities & FX
    "GC=F": "Gold (Futures)",
    "CL=F": "Crude Oil (WTI)",
    "GBPUSD=X": "GBP/USD",
}

# Mapping from yfinance ticker to display ticker
DISPLAY_TICKER = {
    "DX-Y.NYB": "DXY",
}

TODAY = date(2026, 5, 24)
YTD_START = "2026-01-02"
FOMC_DATE = "2026-04-29"

# Which tickers have percentage prices (like yields)
PCT_TICKERS = {"^TNX"}
# Which tickers are forex with 4 decimal places
FX_TICKERS = {"GBPUSD=X"}

def fmt_pct(val):
    if val is None or pd.isna(val) or not np.isfinite(val):
        return "N/A"
    sign = "+" if val >= 0 else ""
    return f"{sign}{val:.2f}%"

def make_span(cls, text):
    return f'<span class="{cls}">{text}</span>'

def pct_span(val_str):
    if val_str == "N/A" or val_str == "0.00%" or val_str == "+0.00%":
        return make_span("num", val_str)
    if val_str.startswith("+"):
        return make_span("up", val_str)
    return make_span("down", val_str)

def format_price(ticker, lc):
    if pd.isna(lc):
        return "N/A"
    if ticker in PCT_TICKERS:
        return f"{lc:.2f}%"
    elif ticker in FX_TICKERS:
        return f"{lc:.4f}"
    elif lc >= 1000:
        return f"{lc:.2f}"
    elif lc >= 100:
        return f"{lc:.2f}"
    elif lc >= 10:
        return f"{lc:.2f}"
    else:
        return f"{lc:.2f}"

def get_close(df, ticker, idx=-1):
    """Get close price for a ticker at position idx from the MultiIndex columns.
    
    yf.download returns columns as MultiIndex: (('Close', 'AAPL'), ('Close', 'SPY'), ...)
    or ('Adj Close', 'AAPL'), ... when auto_adjust=True.
    """
    try:
        return df.iloc[idx][('Close', ticker)]
    except (KeyError, IndexError):
        pass
    try:
        return df.iloc[idx][('Adj Close', ticker)]
    except (KeyError, IndexError):
        pass
    # Try flat columns
    try:
        return df.iloc[idx][ticker]
    except (KeyError, IndexError):
        pass
    return np.nan

def main():
    print("Downloading data from yfinance...")
    
    all_tickers = list(TICKERS.keys())
    
    # Download one ticker at a time for reliability — yfinance MultiIndex
    # can be finicky with delisted tickers
    data = yf.download(
        all_tickers,
        start="2026-01-02",
        end="2026-05-25",
        auto_adjust=True,
        progress=False,
        actions=False,
    )
    
    print(f"Downloaded. Shape: {data.shape}")
    print(f"Columns: {data.columns.tolist()}")
    print(f"Date range: {data.index[0]} to {data.index[-1]}")
    
    # Dictionary of {ticker: Series of closes}
    series_map = {}
    for ticker in all_tickers:
        try:
            s = data['Close'][ticker].dropna()
            if len(s) > 0:
                series_map[ticker] = s
                print(f"  {ticker}: {len(s)} days, last={s.iloc[-1]:.4f} on {s.index[-1].date()}")
            else:
                print(f"  {ticker}: NO DATA")
        except (KeyError, TypeError):
            # Try flat access
            try:
                s = data[ticker].dropna()
                if len(s) > 0:
                    series_map[ticker] = s
                    print(f"  {ticker} (flat): {len(s)} days, last={s.iloc[-1]:.4f}")
                else:
                    print(f"  {ticker}: NO DATA")
            except (KeyError, TypeError) as e:
                print(f"  {ticker}: ERROR - {e}")
    
    if not series_map:
        print("ERROR: No data retrieved at all!")
        return
    
    # Get data_as_of date
    all_dates = []
    for ticker, s in series_map.items():
        all_dates.append(s.index[-1])
    last_overall = max(all_dates)
    
    gbpusd_series = series_map.get("GBPUSD=X", None)
    if gbpusd_series is not None:
        gbpusd_last = gbpusd_series.index[-1]
    else:
        gbpusd_last = None
    
    # Build sections
    sections = {
        "## Broad Market & Indices": ["SPY", "QQQ", "IWM", "^TNX", "DX-Y.NYB"],
        "## Sector ETFs": ["TLT", "XLU", "XLF", "XLRE"],
        "## Mega-Cap Tech": ["AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN"],
        "## Banks": ["JPM", "GS", "BAC"],
        "## Other Holdings": ["PLD", "NEE", "WMT"],
        "## Commodities & FX": ["GC=F", "CL=F", "GBPUSD=X"],
    }
    
    def calc_pct(ticker, s, idx_current, idx_ref):
        """Calculate percentage change for a ticker from idx_ref to idx_current."""
        try:
            cur = s.iloc[idx_current]
            ref = s.iloc[idx_ref]
            if pd.isna(cur) or pd.isna(ref) or ref == 0:
                return 0.0
            return (cur / ref - 1) * 100
        except (IndexError, TypeError):
            return 0.0
    
    def find_closest_idx(s, target_date):
        """Find index position closest to target_date."""
        for i in range(len(s)):
            if s.index[i] >= pd.Timestamp(target_date):
                return i
        return 0
    
    def find_prev_close_idx(s, last_idx):
        """Find the previous trading day's index."""
        if last_idx > 0:
            return last_idx - 1
        return last_idx
    
    lines = []
    lines.append("---")
    lines.append(f"date: {TODAY}")
    lines.append("event: fomc-april-2026")
    lines.append("type: data-refresh")
    lines.append("source: yfinance")
    
    # Determine data_as_of: use Friday May 22 for most, GBPUSD might be Sunday
    data_as_of_str = str(last_overall.date())
    lines.append(f"data_as_of: {data_as_of_str}")
    lines.append("tags:")
    lines.append("  - data-refresh")
    lines.append("  - yfinance")
    lines.append("---")
    lines.append("")
    lines.append(f"# Data Refresh: {TODAY.strftime('%B %d, %Y')}")
    lines.append("")
    
    # Build the data as of line
    # Use May 22 as the main date (last trading day), note GBPUSD separately if newer
    data_as_of_str = "2026-05-22"
    if gbpusd_last is not None and gbpusd_last > pd.Timestamp("2026-05-22"):
        lines.append(f"**Data as of close:** {data_as_of_str} (most tickers); GBPUSD {gbpusd_last.date()}")
    elif last_overall.date().isoformat() != "2026-05-22":
        lines.append(f"**Data as of close:** {last_overall.date()}")
    else:
        lines.append(f"**Data as of close:** {data_as_of_str}")
    
    lines.append("**Periods:** Daily change (prev close) | YTD (Jan 1, 2026) | Post-FOMC (Apr 29, 2026)")
    lines.append("")
    
    header = "| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |"
    sep = "|--------|------|-------|-------|-----|-----------|"
    
    for section_name, ticker_list in sections.items():
        lines.append(section_name)
        lines.append("")
        lines.append(header)
        lines.append(sep)
        
        for yticker in ticker_list:
            if yticker not in series_map:
                continue
            
            s = series_map[yticker]
            last_idx = len(s) - 1
            prev_idx = find_prev_close_idx(s, last_idx)
            ytd_idx = find_closest_idx(s, "2026-01-02")
            fomc_idx = find_closest_idx(s, "2026-04-29")
            
            name = TICKERS[yticker]
            display_ticker = DISPLAY_TICKER.get(yticker, yticker)
            
            lc = s.iloc[last_idx]
            price = format_price(yticker, lc)
            
            daily_pct = calc_pct(yticker, s, last_idx, prev_idx)
            ytd_pct = calc_pct(yticker, s, last_idx, ytd_idx)
            fomc_pct = calc_pct(yticker, s, last_idx, fomc_idx)
            
            cols = [
                display_ticker,
                name,
                make_span("num", price),
                pct_span(fmt_pct(daily_pct)),
                pct_span(fmt_pct(ytd_pct)),
                pct_span(fmt_pct(fomc_pct)),
            ]
            lines.append("| " + " | ".join(cols) + " |")
        
        lines.append("")
    
    lines.append("## Notes")
    lines.append("")
    
    # Determine which date to cite for main close
    lines.append(f"- Data via yfinance. Close of 2026-05-22 (last trading day before report date).")
    if gbpusd_last is not None and gbpusd_last > pd.Timestamp("2026-05-22"):
        lines.append(f"- GBPUSD=X reflects weekend session data through {gbpusd_last.date()}.")
    lines.append("- YTD base: Jan 2, 2026 (Jan 1 is a holiday). Post-FOMC base: Apr 29, 2026 (FOMC decision date).")
    lines.append("- Gold via GC=F (COMEX futures). Crude oil via CL=F (WTI futures).")
    lines.append("- DXY via DX-Y.NYB (US Dollar Index futures). GBP/USD via GBPUSD=X.")
    lines.append("- Span classes: up (green), down (red), num (neutral). No emojis.")
    lines.append("- YTD changes use auto_adjust=True in yfinance, so dividend adjustments are applied to historical prices.")
    
    output = "\n".join(lines) + "\n"
    
    outpath = "/home/ty/workspace/investment-research/reports/2026-05-24-fomc-april-2026/data-refresh.md"
    with open(outpath, "w") as f:
        f.write(output)
    
    print(f"\nWritten to {outpath}")
    print(f"\n=== VERIFICATION ===")
    print(output)

if __name__ == "__main__":
    main()