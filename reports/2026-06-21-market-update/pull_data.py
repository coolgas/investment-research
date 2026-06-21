#!/usr/bin/env python3
"""Pull market data for 24 tickers, compute % changes, SPY-10Y correlation, and write data-refresh.md"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

TICKERS = [
    # Indices
    "SPY", "QQQ", "IWM", "^TNX", "DXY",
    # Sectors
    "TLT", "XLU", "XLF", "XLRE",
    # Stocks - Mega-cap Tech
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    # Financials
    "JPM", "GS", "BAC",
    # Other stocks
    "PLD", "NEE", "WMT",
    # Commodities
    "GC=F", "CL=F",
    # FX
    "GBPUSD=X"
]

# Friendly names for display
FRIENDLY = {
    "SPY": "SPY (S&P 500)",
    "QQQ": "QQQ (Nasdaq-100)",
    "IWM": "IWM (Russell 2000)",
    "^TNX": "10Y UST Yield",
    "DXY": "DXY (US Dollar Index)",
    "TLT": "TLT (20+ Yr Treasuries)",
    "XLU": "XLU (Utilities)",
    "XLF": "XLF (Financials)",
    "XLRE": "XLRE (Real Estate)",
    "AAPL": "AAPL (Apple)",
    "MSFT": "MSFT (Microsoft)",
    "NVDA": "NVDA (NVIDIA)",
    "META": "META (Meta Platforms)",
    "GOOGL": "GOOGL (Alphabet)",
    "AMZN": "AMZN (Amazon)",
    "JPM": "JPM (JPMorgan Chase)",
    "GS": "GS (Goldman Sachs)",
    "BAC": "BAC (Bank of America)",
    "PLD": "PLD (Prologis)",
    "NEE": "NEE (NextEra Energy)",
    "WMT": "WMT (Walmart)",
    "GC=F": "Gold (GC=F)",
    "CL=F": "Crude Oil (CL=F)",
    "GBPUSD=X": "GBP/USD"
}

ASSET_CLASS = {
    "SPY": "indices", "QQQ": "indices", "IWM": "indices", "^TNX": "indices", "DXY": "indices",
    "TLT": "sectors", "XLU": "sectors", "XLF": "sectors", "XLRE": "sectors",
    "AAPL": "megacap", "MSFT": "megacap", "NVDA": "megacap", "META": "megacap", "GOOGL": "megacap", "AMZN": "megacap",
    "JPM": "financials", "GS": "financials", "BAC": "financials",
    "PLD": "other", "NEE": "other", "WMT": "other",
    "GC=F": "commodities", "CL=F": "commodities",
    "GBPUSD=X": "fx"
}

SECTION_ORDER = {
    "indices": "Indices",
    "sectors": "Sectors",
    "megacap": "Mega-Cap Tech",
    "financials": "Financials",
    "commodities": "Commodities",
    "fx": "FX",
    "other": "Other Notable Stocks"
}

print("Downloading data for 24 tickers from 2026-01-01 to 2026-06-21...")
data = yf.download(TICKERS, start="2026-01-01", end="2026-06-21", group_by="ticker", threads=True, progress=False)

print(f"Downloaded. Data shape: {data.shape if hasattr(data, 'shape') else 'see ticker keys'}")
print(f"Ticker keys in data: {list(data.keys())[:5]}...")

# The download with group_by='ticker' returns a MultiIndex DataFrame
# Columns: (Ticker, PriceField), Index: Date
# We need to extract Close prices for each ticker

results = {}

for ticker in TICKERS:
    try:
        close_col = (ticker, 'Close')
        if close_col in data.columns:
            close_series = data[close_col]
        else:
            # try lower ticker
            close_col = (ticker.upper(), 'Close')
            if close_col in data.columns:
                close_series = data[close_col]
            else:
                print(f"  WARNING: No Close data for {ticker}, columns: {[c for c in data.columns if ticker in c or ticker.upper() in c]}")
                continue
        
        # Drop NaNs
        close_series = close_series.dropna()
        
        if len(close_series) < 5:
            print(f"  WARNING: Insufficient data for {ticker}, only {len(close_series)} points")
            continue
        
        latest_date = close_series.index[-1]
        latest_close = close_series.iloc[-1]
        
        # YTD % (Jan 2 or first trading day of 2026)
        ytd_start = close_series.iloc[0]
        ytd_pct = ((latest_close / ytd_start) - 1) * 100
        
        # 2-week: Jun 7 -> Jun 20 (use nearest trading days)
        # June 7 2026 is a Sunday, so closest trading day around it
        # June 20 2026 is a Saturday, so closest trading day around it
        
        # Find the data for ~Jun 7 (near start of 2-week period)
        # We'll look at entries around Jun 7 and Jun 20
        # Since weekends, use the closest available dates
        
        target_start = pd.Timestamp("2026-06-07")
        target_end = pd.Timestamp("2026-06-20")
        
        # Find closest date on or after target_start (the first trading day after Jun 7)
        start_mask = close_series.index >= target_start
        if start_mask.any():
            start_idx = start_mask.idxmax()
            two_week_start_val = close_series.loc[start_idx]
            two_week_start_date = start_idx
        else:
            two_week_start_val = None
            two_week_start_date = None
        
        # Find closest date on or before target_end (the last trading day before/on Jun 20)
        end_mask = close_series.index <= target_end
        if end_mask.any():
            # Get the last matching index
            end_idx = close_series.index[end_mask][-1]
            two_week_end_val = close_series.loc[end_idx]
            two_week_end_date = end_idx
        else:
            two_week_end_val = latest_close
            two_week_end_date = latest_date
        
        if two_week_start_val is not None and two_week_end_val is not None and two_week_start_val > 0:
            two_week_pct = ((two_week_end_val / two_week_start_val) - 1) * 100
        else:
            two_week_pct = None
        
        # 1-week: Jun 14 -> Jun 20 (approximate)
        target_1w_start = pd.Timestamp("2026-06-14")
        w1_mask = close_series.index >= target_1w_start
        if w1_mask.any():
            w1_start_idx = w1_mask.idxmax()
            w1_start_val = close_series.loc[w1_start_idx]
            w1_start_date = w1_start_idx
            if w1_start_val > 0 and two_week_end_val is not None:
                one_week_pct = ((two_week_end_val / w1_start_val) - 1) * 100
            else:
                one_week_pct = None
        else:
            one_week_pct = None
        
        results[ticker] = {
            "latest_close": float(latest_close),
            "latest_date": latest_date,
            "ytd_pct": float(ytd_pct),
            "two_week_pct": float(two_week_pct) if two_week_pct is not None else None,
            "two_week_start_date": two_week_start_date,
            "two_week_end_date": two_week_end_date,
            "one_week_pct": float(one_week_pct) if one_week_pct is not None else None,
            "ytd_start_price": float(ytd_start),
            "ytd_start_date": close_series.index[0]
        }
        
        # Print for debugging
        print(f"  {ticker:15s} Close={latest_close:>10.2f}  YTD={ytd_pct:>+7.2f}%  2W={two_week_pct if two_week_pct is not None else 'N/A':>7}")
        
    except Exception as e:
        print(f"  ERROR processing {ticker}: {e}")

print(f"\nProcessed {len(results)} tickers successfully")

# --- SPY-10Y Correlation ---
print("\nComputing SPY-10Y correlation...")
try:
    spy_close = data[('SPY', 'Close')].dropna()
    tnx_close = data[('^TNX', 'Close')].dropna()
    
    # Daily returns
    spy_returns = spy_close.pct_change().dropna()
    tnx_returns = tnx_close.pct_change().dropna()
    
    # YTD (all data)
    common_ytd = pd.concat([spy_returns, tnx_returns], axis=1, join='inner')
    common_ytd.columns = ['SPY', 'TNX']
    
    if len(common_ytd) > 2:
        corr_ytd = common_ytd['SPY'].corr(common_ytd['TNX'])
    else:
        corr_ytd = None
    
    # 2-week window (Jun 7 - Jun 20)
    target_start = pd.Timestamp("2026-06-07")
    target_end = pd.Timestamp("2026-06-20")
    common_2w = common_ytd[(common_ytd.index >= target_start) & (common_ytd.index <= target_end)]
    
    if len(common_2w) > 2:
        corr_2w = common_2w['SPY'].corr(common_2w['TNX'])
    else:
        corr_2w = None
    
    print(f"  SPY-10Y correlation (YTD): {corr_ytd:.4f} (n={len(common_ytd)})")
    print(f"  SPY-10Y correlation (2-week): {corr_2w:.4f} (n={len(common_2w)})")
    
    # Latest TNX level
    latest_tnx = float(tnx_close.iloc[-1])
    tnx_date = tnx_close.index[-1]
    tnx_ytd_start = float(tnx_close.iloc[0])
    tnx_ytd_chg = latest_tnx - tnx_ytd_start
    
    print(f"  Latest ^TNX: {latest_tnx:.4f} on {tnx_date.date()}")
    print(f"  ^TNX YTD change: {tnx_ytd_chg:+.4f} bps")
    
    threshold_4_75 = latest_tnx >= 4.75
    
except Exception as e:
    print(f"  ERROR computing correlation: {e}")
    corr_ytd = None
    corr_2w = None
    latest_tnx = None
    tnx_date = None
    tnx_ytd_chg = None
    threshold_4_75 = False

# --- Write Markdown Report ---
print("\nWriting report...")

def fmt_pct(val):
    """Format percentage with span tags"""
    if val is None or np.isnan(val):
        return "N/A"
    if val >= 0:
        return f'<span class="up">+{val:.2f}%</span>'
    else:
        return f'<span class="down">{val:.2f}%</span>'

def fmt_num(val):
    """Format plain number with span tags"""
    if val is None or np.isnan(val):
        return "N/A"
    return f'<span class="num">{val:.2f}</span>'

def fmt_num4(val):
    """Format 4-decimal number"""
    if val is None or np.isnan(val):
        return "N/A"
    return f'<span class="num">{val:.4f}</span>'

lines = []
lines.append("# Market Data Refresh: June 21, 2026")
lines.append("")
lines.append(f"**Data pulled**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
lines.append(f"**Period**: YTD (Jan 1, 2026) through latest available ({results.get('SPY', {}).get('latest_date', 'N/A').date() if isinstance(results.get('SPY', {}).get('latest_date', 'N/A'), pd.Timestamp) else 'N/A'})")
lines.append(f"**2-week window**: Jun 7 - Jun 20, 2026 (nearest trading days used)")
lines.append("")
lines.append("---")
lines.append("")

# Build tables per asset class
asset_sections = {
    "indices": ["SPY", "QQQ", "IWM", "^TNX", "DXY"],
    "sectors": ["TLT", "XLU", "XLF", "XLRE"],
    "megacap": ["AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN"],
    "financials": ["JPM", "GS", "BAC"],
    "commodities": ["GC=F", "CL=F"],
    "fx": ["GBPUSD=X"],
    "other": ["PLD", "NEE", "WMT"]
}

for section_key, ticker_list in asset_sections.items():
    section_name = SECTION_ORDER[section_key]
    
    # Filter to tickers we actually have data for
    valid_tickers = [t for t in ticker_list if t in results]
    if not valid_tickers:
        continue
    
    lines.append(f"## {section_name}")
    lines.append("")
    
    # Table header
    lines.append("| Ticker | Latest Close | 2-Week % (Jun 7->Jun 20) | YTD % | 1-Week % (Jun 14->Jun 20) |")
    lines.append("|--------|-------------|--------------------------|-------|--------------------------|")
    
    for ticker in valid_tickers:
        r = results[ticker]
        name = FRIENDLY.get(ticker, ticker)
        
        lc = fmt_num(r['latest_close'])
        tw = fmt_pct(r['two_week_pct'])
        ytd = fmt_pct(r['ytd_pct'])
        ow = fmt_pct(r['one_week_pct'])
        
        lines.append(f"| {name} | {lc} | {tw} | {ytd} | {ow} |")
    
    lines.append("")
    
    # Additional notes for indices section
    if section_key == "indices" and latest_tnx is not None:
        lines.append(f"**^TNX Level**: {fmt_num4(latest_tnx)} (last observation: {tnx_date.date() if tnx_date else 'N/A'})")
        lines.append(f"**^TNX YTD Change**: {fmt_num(tnx_ytd_chg) if tnx_ytd_chg is not None else 'N/A'} bps")
        if threshold_4_75:
            lines.append(f"**Key Level Alert**: 10Y yield is ABOVE the 4.75% trigger threshold.")
        else:
            lines.append(f"**Note**: 10Y yield remains below the 4.75% trigger threshold.")
        lines.append("")

    # Check for major moves >5%
    major_moves = []
    for ticker in valid_tickers:
        r = results[ticker]
        for label, pct in [("YTD", r['ytd_pct']), ("2-week", r['two_week_pct'])]:
            if pct is not None and abs(pct) > 5:
                major_moves.append(f"  - {FRIENDLY.get(ticker, ticker)}: {fmt_pct(pct)} ({label})")
    
    if major_moves:
        lines.append("**Major moves (>5%):**")
        lines.extend(major_moves)
        lines.append("")

# Rates / Yield section
lines.append("## Rates / Yield Summary")
lines.append("")
lines.append("| Metric | Value |")
lines.append("|--------|-------|")

if latest_tnx is not None:
    lines.append(f"| 10Y UST Yield (^TNX) Latest | {fmt_num4(latest_tnx)} |")
    lines.append(f"| ^TNX YTD Change (bps) | {fmt_num(tnx_ytd_chg) if tnx_ytd_chg is not None else 'N/A'} |")
    lines.append(f"| Threshold 4.75% Breached | {'YES' if threshold_4_75 else 'No'} |")

lines.append("")

# Correlation table
lines.append("### SPY-10Y Correlation Analysis")
lines.append("")
lines.append("| Period | Correlation | Observations |")
lines.append("|--------|------------|--------------|")

if corr_ytd is not None:
    lines.append(f"| YTD (Jan 1 - Jun 20) | {fmt_num(corr_ytd)} | {fmt_num(len(common_ytd))} |")
else:
    lines.append(f"| YTD (Jan 1 - Jun 20) | N/A | N/A |")

if corr_2w is not None:
    lines.append(f"| 2-Week (Jun 7 - Jun 20) | {fmt_num(corr_2w)} | {fmt_num(len(common_2w))} |")
else:
    lines.append(f"| 2-Week (Jun 7 - Jun 20) | N/A | N/A |")

lines.append("")
lines.append("*Note: A negative correlation suggests stocks and bonds are moving inversely (risk-on/risk-off dynamic). Positive correlation suggests common macro factor driving both.*")
lines.append("")

# Data quality notes
lines.append("## Data Quality Notes")
lines.append("")
lines.append(f"- Tickers requested: {len(TICKERS)}")
lines.append(f"- Tickers with valid data: {len(results)}")
lines.append(f"- Date range: {results.get('SPY', {}).get('ytd_start_date', 'N/A').date() if isinstance(results.get('SPY', {}).get('ytd_start_date', 'N/A'), pd.Timestamp) else 'N/A'} through {results.get('SPY', {}).get('latest_date', 'N/A').date() if isinstance(results.get('SPY', {}).get('latest_date', 'N/A'), pd.Timestamp) else 'N/A'}")
lines.append(f"- Missing tickers: {', '.join([t for t in TICKERS if t not in results])}")
lines.append("")
lines.append("---")
lines.append("")
lines.append(f"*Generated automatically by Hermes Agent data refresh script on {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*")
lines.append("")

report_content = "\n".join(lines)

output_path = "/root/workspace/investment-research/reports/2026-06-21-market-update/data-refresh.md"
with open(output_path, "w") as f:
    f.write(report_content)

byte_count = len(report_content.encode('utf-8'))
print(f"\nReport written to {output_path}")
print(f"File size: {byte_count} bytes")
print(f"Lines: {len(lines)}")

# Also print the full report for verification
print("\n" + "="*60)
print("REPORT PREVIEW:")
print("="*60)
print(report_content[:3000])
print("..." if len(report_content) > 3000 else "")
