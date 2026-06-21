#!/usr/bin/env python3
"""Pull market data for 24 tickers, compute % changes, SPY-10Y correlation, and write data-refresh.md"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

TICKERS = [
    "SPY", "QQQ", "IWM", "^TNX", "DXY",
    "TLT", "XLU", "XLF", "XLRE",
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    "JPM", "GS", "BAC",
    "PLD", "NEE", "WMT",
    "GC=F", "CL=F",
    "GBPUSD=X"
]

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

SECTION_ORDER = {
    "indices": "Indices",
    "sectors": "Sectors",
    "megacap": "Mega-Cap Tech",
    "financials": "Financials",
    "commodities": "Commodities",
    "fx": "FX",
}

asset_sections_map = {
    "indices": ["SPY", "QQQ", "IWM", "^TNX", "DXY"],
    "sectors": ["TLT", "XLU", "XLF", "XLRE"],
    "megacap": ["AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN"],
    "financials": ["JPM", "GS", "BAC"],
    "commodities": ["GC=F", "CL=F"],
    "fx": ["GBPUSD=X"],
}

# Also include WMT, PLD, NEE in relevant sections
# PLD is Real Estate (XLRE covers that), NEE is Utilities (XLU covers that), WMT is Consumer Staples
# Let's add an "Other" section
SECTION_ORDER["other"] = "Other Notable Stocks"
asset_sections_map["other"] = ["WMT", "PLD", "NEE"]

print("Downloading data for 24 tickers from 2026-01-01 to 2026-06-21...")

# Use Ticker objects individually for better control
results = {}

# First get SPY, ^TNX separately for correlation + main timeline
main_tickers = ["SPY", "QQQ", "IWM", "^TNX", "TLT", "XLU", "XLF", "XLRE",
                "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
                "JPM", "GS", "BAC", "WMT", "PLD", "NEE"]

# Batch download the main tickers
print("Batch downloading main tickers...")
main_data = yf.download(main_tickers, start="2026-01-01", end="2026-06-21", group_by="ticker", threads=True, progress=False)

# Download special tickers
print("Downloading DXY...")
dxy_ticker = yf.Ticker("DX-Y.NYB")
dxy_hist = dxy_ticker.history(start="2026-01-01", end="2026-06-21")

print("Downloading commodities and FX...")
spec_data = yf.download(["GC=F", "CL=F", "GBPUSD=X"], start="2026-01-01", end="2026-06-21", group_by="ticker", threads=True, progress=False)

print("Data download complete.")

# Process main tickers
for ticker in main_tickers:
    try:
        if ticker not in main_data.columns.get_level_values(0):
            print(f"  {ticker}: not found in batch download columns")
            continue
        close_series = main_data[(ticker, 'Close')].dropna()
        if len(close_series) < 5:
            print(f"  {ticker}: insufficient data ({len(close_series)} points)")
            continue
        
        results[ticker] = close_series
        print(f"  {ticker}: {len(close_series)} data points, last={close_series.iloc[-1]:.2f}")
    except Exception as e:
        print(f"  {ticker}: error - {e}")

# Process DXY
if len(dxy_hist) > 5:
    dxy_close = dxy_hist['Close'].dropna()
    results["DXY"] = dxy_close
    print(f"  DXY: {len(dxy_close)} data points, last={dxy_close.iloc[-1]:.2f}")
else:
    print(f"  DXY: insufficient data ({len(dxy_hist)} points)")

# Process special tickers
for ticker in ["GC=F", "CL=F", "GBPUSD=X"]:
    try:
        if ticker in spec_data.columns.get_level_values(0):
            close_series = spec_data[(ticker, 'Close')].dropna()
        else:
            print(f"  {ticker}: not found in special download")
            continue
        if len(close_series) < 5:
            print(f"  {ticker}: insufficient data ({len(close_series)} points)")
            continue
        results[ticker] = close_series
        print(f"  {ticker}: {len(close_series)} data points, last={close_series.iloc[-1]:.2f}")
    except Exception as e:
        print(f"  {ticker}: error - {e}")

print(f"\nTotal tickers with data: {len(results)}")

# --- Compute metrics ---
def compute_metrics(series):
    """Compute latest close, YTD%, 2-week%, 1-week%"""
    if series is None or len(series) < 5:
        return None
    
    # Normalize timezone to naive for consistent date comparison
    if hasattr(series.index, 'tz') and series.index.tz is not None:
        series = series.copy()
        series.index = series.index.tz_localize(None)
    
    latest_close = float(series.iloc[-1])
    latest_date = series.index[-1]
    
    # YTD % (first available close vs latest)
    ytd_start = float(series.iloc[0])
    ytd_pct = ((latest_close / ytd_start) - 1) * 100
    
    # 2-week: Jun 7 (Sun) -> Jun 20 (Sat)
    # Find first trading day on or after Jun 7
    target_start = pd.Timestamp("2026-06-07")
    target_end = pd.Timestamp("2026-06-20")
    
    mask_start = series.index >= target_start
    mask_end = series.index <= target_end
    
    if mask_start.any():
        two_week_start = series[mask_start].iloc[0]
        two_week_start_date = series[mask_start].index[0]
    else:
        two_week_start = None
        two_week_start_date = None
    
    if mask_end.any():
        two_week_end = series[mask_end].iloc[-1]
        two_week_end_date = series[mask_end].index[-1]
    else:
        two_week_end = latest_close
        two_week_end_date = latest_date
    
    if two_week_start is not None and two_week_start > 0:
        two_week_pct = ((two_week_end / two_week_start) - 1) * 100
    else:
        two_week_pct = None
    
    # 1-week: Jun 14 (Sun) -> Jun 20 (Sat)
    target_1w = pd.Timestamp("2026-06-14")
    mask_1w = series.index >= target_1w
    if mask_1w.any():
        one_week_start = series[mask_1w].iloc[0]
        if one_week_start > 0:
            one_week_pct = ((two_week_end / one_week_start) - 1) * 100
        else:
            one_week_pct = None
    else:
        one_week_pct = None
    
    return {
        "latest_close": latest_close,
        "latest_date": latest_date,
        "ytd_pct": ytd_pct,
        "ytd_start": ytd_start,
        "ytd_start_date": series.index[0],
        "two_week_pct": two_week_pct,
        "two_week_start_date": two_week_start_date,
        "two_week_end_date": two_week_end_date,
        "one_week_pct": one_week_pct,
    }

metrics = {}
for ticker, series in results.items():
    m = compute_metrics(series)
    if m:
        metrics[ticker] = m
        tw_str = "N/A" if m['two_week_pct'] is None else f"{m['two_week_pct']:>+7.2f}%"
        ow_str = "N/A" if m['one_week_pct'] is None else f"{m['one_week_pct']:>+7.2f}%"
        print(f"  {ticker:15s} Close={m['latest_close']:>10.2f}  YTD={m['ytd_pct']:>+7.2f}%  2W={tw_str}  1W={ow_str}")

# --- SPY-10Y Correlation ---
print("\n--- SPY-10Y Correlation ---")
spy_series = results.get("SPY")
tnx_series = results.get("^TNX")

corr_ytd = None
corr_2w = None
latest_tnx = None
tnx_date = None
tnx_ytd_chg = None

if spy_series is not None and tnx_series is not None:
    spy_ret = spy_series.pct_change().dropna()
    tnx_ret = tnx_series.pct_change().dropna()
    
    common = pd.concat([spy_ret, tnx_ret], axis=1, join='inner')
    common.columns = ['SPY', 'TNX']
    
    if len(common) > 5:
        corr_ytd = float(common['SPY'].corr(common['TNX']))
        print(f"  YTD correlation: {corr_ytd:.4f} (n={len(common)})")
    
    # 2-week window
    target_start = pd.Timestamp("2026-06-07")
    target_end = pd.Timestamp("2026-06-20")
    common_2w = common[(common.index >= target_start) & (common.index <= target_end)]
    
    if len(common_2w) > 3:
        corr_2w = float(common_2w['SPY'].corr(common_2w['TNX']))
        print(f"  2-week correlation: {corr_2w:.4f} (n={len(common_2w)})")
    
    latest_tnx = float(tnx_series.iloc[-1])
    tnx_date = tnx_series.index[-1]
    tnx_ytd_chg = float(tnx_series.iloc[-1] - tnx_series.iloc[0])
    
    print(f"  ^TNX: {latest_tnx:.4f} on {tnx_date.date()}, YTD change: {tnx_ytd_chg:+.4f}")

threshold_4_75 = latest_tnx is not None and latest_tnx >= 4.75

# --- WRITE REPORT ---
print("\n=== WRITING REPORT ===")

def fmt_pct(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    if val >= 0:
        return f'<span class="up">+{val:.2f}%</span>'
    else:
        return f'<span class="down">{val:.2f}%</span>'

def fmt_num(val, decimals=2):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return f'<span class="num">{val:.{decimals}f}</span>'

lines = []
lines.append("# Market Data Refresh: June 21, 2026")
lines.append("")
lines.append(f"**Data pulled**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
lines.append(f"**Period**: YTD (Jan 1, 2026) through Jun 20, 2026")
lines.append(f"**2-week window**: Jun 7 - Jun 20, 2026 (nearest trading days used)")
lines.append(f"**1-week window**: Jun 14 - Jun 20, 2026")
lines.append("")
lines.append("---")
lines.append("")

# Get SPY latest date for reference
spy_metrics = metrics.get("SPY", {})
spy_latest_date = spy_metrics.get("latest_date", "N/A")
if hasattr(spy_latest_date, 'date'):
    spy_latest_date = spy_latest_date.date()

# Build tables per section
for section_key, ticker_list in asset_sections_map.items():
    section_name = SECTION_ORDER[section_key]
    valid = [t for t in ticker_list if t in metrics]
    if not valid:
        continue
    
    lines.append(f"## {section_name}")
    lines.append("")
    
    # Check for >5% moves in this section
    has_major = False
    major_notes = []
    for t in valid:
        m = metrics[t]
        for label, pct in [("YTD", m['ytd_pct']), ("2-week", m['two_week_pct']), ("1-week", m['one_week_pct'])]:
            if pct is not None and abs(pct) > 5:
                has_major = True
                major_notes.append(f"- {FRIENDLY.get(t, t)}: {fmt_pct(pct)} ({label})")
    
    if has_major:
        lines.append("**Major moves (>5%):**")
        for note in major_notes:
            lines.append(note)
        lines.append("")
    
    lines.append("| Ticker | Latest Close | 2-Week % (Jun 7 -> Jun 20) | YTD % (Jan 1 -> Jun 20) | 1-Week % (Jun 14 -> Jun 20) |")
    lines.append("|--------|-------------|---------------------------|-------------------------|-----------------------------|")
    
    for t in valid:
        m = metrics[t]
        name = FRIENDLY.get(t, t)
        lc = fmt_num(m['latest_close'])
        tw = fmt_pct(m['two_week_pct'])
        ytd = fmt_pct(m['ytd_pct'])
        ow = fmt_pct(m['one_week_pct'])
        lines.append(f"| {name} | {lc} | {tw} | {ytd} | {ow} |")
    
    lines.append("")

# Rates/Yield section
lines.append("## Rates / Yield Summary")
lines.append("")
lines.append("| Metric | Value |")
lines.append("|--------|-------|")
if latest_tnx is not None:
    lines.append(f"| 10Y UST Yield (^TNX) Latest | {fmt_num(latest_tnx, 4)} |")
    lines.append(f"| ^TNX Level at YTD Start (Jan 2) | {fmt_num(float(tnx_series.iloc[0]) if tnx_series is not None else 0, 4)} |")
    lines.append(f"| ^TNX YTD Change (bps) | {fmt_num(tnx_ytd_chg * 100, 1) if tnx_ytd_chg is not None else 'N/A'} |")
    lines.append(f"| 4.75% Trigger Threshold Breached? | {'YES' if threshold_4_75 else 'No'} |")
    if latest_tnx < 4.75:
        lines.append(f"| Distance to 4.75% Trigger | {fmt_num((4.75 - latest_tnx) * 100, 1)} bps below |")
lines.append("")

# Correlation
lines.append("### SPY-10Y Correlation Analysis")
lines.append("")
lines.append("| Period | Correlation | Daily Observations |")
lines.append("|--------|------------|-------------------|")
if corr_ytd is not None:
    lines.append(f"| YTD (Jan 2 - Jun 20) | {fmt_num(corr_ytd, 4)} | {fmt_num(len(common))} |")
else:
    lines.append(f"| YTD (Jan 2 - Jun 20) | N/A | N/A |")
if corr_2w is not None:
    lines.append(f"| 2-Week (Jun 7 - Jun 20) | {fmt_num(corr_2w, 4)} | {fmt_num(len(common_2w))} |")
else:
    lines.append(f"| 2-Week (Jun 7 - Jun 20) | N/A | N/A |")

lines.append("")
lines.append("*Interpretation: Negative SPY-10Y correlation = risk-on/risk-off (stocks and bonds move inversely). Positive correlation = common macro factor (e.g., inflation, growth expectations) driving both.*")
lines.append("")

# Data quality
lines.append("## Data Quality Notes")
lines.append("")
lines.append(f"- Tickers requested: 24")
lines.append(f"- Tickers with valid data: {len(metrics)}")
spy_m = metrics.get("SPY", {})
ytd_start_date = spy_m.get("ytd_start_date", "N/A")
if hasattr(ytd_start_date, 'date'):
    ytd_start_date = ytd_start_date.date()
lines.append(f"- Date range: {ytd_start_date} through {spy_latest_date}")
missing = [t for t in TICKERS if t not in metrics]
if missing:
    lines.append(f"- Missing/no data: {', '.join(missing)}")
else:
    lines.append("- All tickers accounted for.")
lines.append("")
lines.append("---")
lines.append("")
lines.append(f"*Generated automatically by Hermes Agent data refresh script on {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*")
lines.append("")

content = "\n".join(lines)

output_path = "/root/workspace/investment-research/reports/2026-06-21-market-update/data-refresh.md"
with open(output_path, "w") as f:
    f.write(content)

byte_count = len(content.encode('utf-8'))
print(f"\nReport written: {output_path}")
print(f"File size: {byte_count} bytes (need >2000)")
print(f"Total lines: {len(lines)}")

# Print full report
print("\n" + "="*70)
print("FULL REPORT")
print("="*70)
print(content)