#!/usr/bin/env python3
"""Pull fresh market data for data-refresh.md"""
import yfinance as yf
import json
from datetime import date

TICKERS = [
    "SPY", "QQQ", "IWM", "TLT", "XLU", "XLF", "XLRE", "^TNX",
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    "JPM", "GS", "BAC", "PLD", "NEE", "WMT",
    "GC=F", "CL=F", "DX-Y.NYB", "GBPUSD=X",
]

LABELS = {
    "SPY": "SPY (S&P 500)", "QQQ": "QQQ (Nasdaq-100)", "IWM": "IWM (Small Caps)",
    "TLT": "TLT (20Y+ Treasury)", "XLU": "XLU (Utilities)", "XLF": "XLF (Financials)",
    "XLRE": "XLRE (Real Estate)", "^TNX": "10Y Yield",
    "AAPL": "AAPL", "MSFT": "MSFT", "NVDA": "NVDA", "META": "META",
    "GOOGL": "GOOGL", "AMZN": "AMZN", "JPM": "JPM", "GS": "GS",
    "BAC": "BAC", "PLD": "PLD", "NEE": "NEE", "WMT": "WMT",
    "GC=F": "Gold", "CL=F": "Crude Oil", "DX-Y.NYB": "DXY", "GBPUSD=X": "GBP/USD",
}

YTD_START = "2026-01-01"
POST_FOMC = "2026-04-29"

today = date.today()
print(f"Today: {today} ({today.strftime('%A')})")
print()

results = {}

for t in TICKERS:
    label = LABELS[t]
    try:
        ind = yf.download(t, start="2025-12-01", end=today.strftime("%Y-%m-%d"), auto_adjust=True, progress=False)
        if ind.empty or len(ind) < 2:
            print(f"  SKIP {label}: insufficient data")
            continue
        
        # Handle MultiIndex columns (yfinance 1.4+ always returns MultiIndex)
        cols = ind.columns
        close_col = ('Close', t) if isinstance(cols[0], tuple) else 'Close'
        closes = ind[close_col].dropna()
        
        if len(closes) < 2:
            print(f"  SKIP {label}: insufficient close data ({len(closes)})")
            continue
        
        latest_close = float(closes.iloc[-1])
        prev_close = float(closes.iloc[-2])
        daily_pct = round((latest_close - prev_close) / prev_close * 100, 2)
        
        # YTD: from Jan 1, 2026
        mask_ytd = closes.index >= YTD_START
        closes_ytd = closes[mask_ytd]
        if len(closes_ytd) > 0:
            first_ytd = float(closes_ytd.iloc[0])
            ytd_pct = round((latest_close - first_ytd) / first_ytd * 100, 2)
        else:
            ytd_pct = None
        
        # Post-FOMC: from Apr 29, 2026
        mask_pf = closes.index >= POST_FOMC
        closes_pf = closes[mask_pf]
        if len(closes_pf) > 0:
            first_pf = float(closes_pf.iloc[0])
            pf_pct = round((latest_close - first_pf) / first_pf * 100, 2)
        else:
            pf_pct = None
        
        latest_date = closes.index[-1].strftime("%Y-%m-%d")
        
        results[t] = {
            "label": label,
            "latest_price": round(latest_close, 2),
            "latest_date": latest_date,
            "daily_pct": daily_pct,
            "ytd_pct": ytd_pct,
            "post_fomc_pct": pf_pct,
        }
        
        print(f"  {label:25s}  ${latest_close:<10.2f}  daily={daily_pct:+.2f}%  YTD={str(ytd_pct or 'N/A'):>8s}  post-FOMC={str(pf_pct or 'N/A'):>8s}  ({latest_date})")
    except Exception as e:
        print(f"  ERROR {label}: {e}")
        continue

# Save results
outpath = "/home/ty/workspace/investment-research/reports/2026-05-24-fomc-april-2026/scripts/refresh_results.json"
with open(outpath, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\nSaved to {outpath}")
print(f"Tickers resolved: {len(results)}/{len(TICKERS)}")

# Build summary table string
print("\n\n=== SUMMARY TABLE ===")
print(f"{'Ticker':20s} {'Price':>10s} {'Daily':>8s} {'YTD':>8s} {'Post-FOMC':>10s}")
print("-" * 56)
for t in TICKERS:
    if t in results:
        r = results[t]
        pid = "TNX" if t == "^TNX" else t
        ytd_s = f"{r['ytd_pct']:+.2f}%" if r['ytd_pct'] is not None else "N/A"
        pf_s = f"{r['post_fomc_pct']:+.2f}%" if r['post_fomc_pct'] is not None else "N/A"
        print(f"{pid:20s} {r['latest_price']:>8.2f}  {r['daily_pct']:+.2f}%  {ytd_s:>8s}  {pf_s:>10s}")