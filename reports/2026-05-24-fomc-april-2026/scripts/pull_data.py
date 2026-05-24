#!/usr/bin/env python3
"""Pull fresh yfinance data and compute daily%, YTD%, Post-FOMC% for all tickers."""
import json
import yfinance as yf
from datetime import datetime, date

TICKERS = [
    "SPY", "QQQ", "IWM", "TLT", "XLU", "XLF", "XLRE",
    "^TNX",
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    "JPM", "GS", "BAC",
    "PLD", "NEE", "WMT",
    "GC=F", "CL=F",
    "DX-Y.NYB", "GBPUSD=X",
]

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

SECTIONS = {
    "Broad Market & Indices": ["SPY", "QQQ", "IWM", "^TNX", "DX-Y.NYB"],
    "Sector ETFs": ["TLT", "XLU", "XLF", "XLRE"],
    "Mega-Cap Tech": ["AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN"],
    "Banks": ["JPM", "GS", "BAC"],
    "Other Holdings": ["PLD", "NEE", "WMT"],
    "Commodities & FX": ["GC=F", "CL=F", "GBPUSD=X"],
}

YTD_START = "2026-01-02"  # Jan 1 is a holiday
FOMC_DATE = "2026-04-29"

print(f"=== Data Pull: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
print(f"YTD base: {YTD_START} | Post-FOMC base: {FOMC_DATE}")

# Pull all data at once - no group_by='ticker' to avoid auto_adjust issues
print("Downloading data...")
df = yf.download(TICKERS, start="2025-12-15", auto_adjust=True)
print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Date range: {df.index[0]} to {df.index[-1]}")

# Access Close prices
close = df['Close']
print(f"\nLast 5 trading days:")
print(close.tail(10))

# Get the latest available close for each ticker (they may have different last dates)
results = {}
today = date.today()

for t in TICKERS:
    series = close[t].dropna()
    if len(series) == 0:
        print(f"WARNING: No data for {t}")
        continue
    
    latest = series.iloc[-1]
    latest_date = series.index[-1].date()
    
    # Daily change: compare to previous trading day
    if len(series) >= 2:
        prev = series.iloc[-2]
        daily_chg = (latest / prev - 1) * 100
    else:
        daily_chg = 0.0
        prev = latest
    
    # YTD: compare to Jan 2, 2026
    ytd_mask = series.index >= YTD_START
    ytd_series = series[ytd_mask]
    if len(ytd_series) >= 1:
        ytd_start_val = ytd_series.iloc[0]
        ytd_chg = (latest / ytd_start_val - 1) * 100
    else:
        ytd_chg = 0.0
    
    # Post-FOMC: compare to Apr 29, 2026
    fomc_mask = series.index >= FOMC_DATE
    fomc_series = series[fomc_mask]
    if len(fomc_series) >= 1:
        fomc_start_val = fomc_series.iloc[0]
        fomc_chg = (latest / fomc_start_val - 1) * 100
    else:
        fomc_chg = 0.0
    
    # Determine decimal places by ticker type
    if t == "GBPUSD=X":
        decimals = 4
    elif t == "^TNX":
        decimals = 2
    else:
        decimals = 2
    
    results[t] = {
        "name": NAMES.get(t, t),
        "price": round(latest, decimals),
        "decimals": decimals,
        "daily_pct": round(daily_chg, 2),
        "ytd_pct": round(ytd_chg, 2),
        "fomc_pct": round(fomc_chg, 2),
        "latest_date": str(latest_date),
    }
    
    print(f"{t:12s} | ${latest:<8.2f} | Daily: {daily_chg:+.2f}% | YTD: {ytd_chg:+.2f}% | Post-FOMC: {fomc_chg:+.2f}% | as of {latest_date}")

# Also check ^TNX - for yields we use absolute values, not percentages
# Actually yfinance returns yield values for ^TNX directly
print("\n\n=== ^TNX Details ===")
print(close["^TNX"].tail(5))

# Save to JSON for consumption
output = {
    "pull_date": str(today),
    "results": results,
}
with open("scripts/market_data.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nSaved to scripts/market_data.json")