#!/usr/bin/env python3
"""Pull fresh market data for semiconductor and broad market tickers."""

import yfinance as yf
import json
from datetime import datetime, timedelta

TICKERS = [
    # Semi
    "SMH", "SOXX", "NVDA", "AMD", "AVGO", "TSM", "ASML", "INTC", "MU",
    "AMAT", "LRCX", "KLAC", "TXN", "QCOM", "ARM", "MRVL", "ON",
    # Broad
    "SPY", "QQQ", "IWM", "^TNX", "TLT", "^VIX",
    # His ETF
    "SMGB.L"
]

START = "2026-01-01"
END = "2026-07-07"

# Calculate date range boundaries
jan2 = datetime(2026, 1, 2)
one_month_ago = datetime(2026, 6, 7)
one_week_ago = datetime(2026, 6, 30)

print(f"Downloading data for {len(TICKERS)} tickers from {START} to {END}...")
data = yf.download(TICKERS, start=START, end=END, group_by="ticker", auto_adjust=True)
print(f"Download complete. Shape: {data.shape}")
print(f"Columns (first 10): {list(data.columns[:10])}")

results = {}

for ticker in TICKERS:
    try:
        # Handle MultiIndex columns
        close_col = (ticker, "Close")
        if close_col in data.columns:
            close_series = data[close_col]
        else:
            # Try flat column access
            if ticker in data.columns:
                close_series = data["Close"] if "Close" in data.columns else data
            else:
                print(f"  WARNING: {ticker} not found in data columns")
                results[ticker] = {"error": "not found"}
                continue

        close_series = close_series.dropna()
        if len(close_series) == 0:
            print(f"  WARNING: {ticker} has no data")
            results[ticker] = {"error": "no data"}
            continue

        latest = close_series.iloc[-1]
        latest_date = close_series.index[-1].strftime("%Y-%m-%d")
        
        # Get close on Jan 2 (or nearest available)
        jan2_close = None
        if jan2 in close_series.index:
            jan2_close = close_series.loc[jan2]
        else:
            # Find closest date on or after jan2
            mask = close_series.index >= jan2
            if mask.any():
                jan2_close = close_series[mask].iloc[0]
        
        # Get close 1 month ago (or nearest)
        mask_1m = close_series.index >= one_month_ago
        if mask_1m.any():
            one_mo_close = close_series[mask_1m].iloc[0]
            one_mo_date = close_series[mask_1m].index[0].strftime("%Y-%m-%d")
        else:
            one_mo_close = None
            one_mo_date = None
        
        # Get close 1 week ago (or nearest)
        mask_1w = close_series.index >= one_week_ago
        if mask_1w.any():
            one_wk_close = close_series[mask_1w].iloc[0]
            one_wk_date = close_series[mask_1w].index[0].strftime("%Y-%m-%d")
        else:
            one_wk_close = None
            one_wk_date = None

        entry = {
            "latest_close": round(float(latest), 2),
            "latest_date": latest_date,
            "ytd_start_price": round(float(jan2_close), 2) if jan2_close is not None else None,
            "ytd_pct": round((float(latest) / float(jan2_close) - 1) * 100, 2) if jan2_close is not None and jan2_close != 0 else None,
            "one_mo_price": round(float(one_mo_close), 2) if one_mo_close is not None else None,
            "one_mo_date": one_mo_date,
            "one_mo_pct": round((float(latest) / float(one_mo_close) - 1) * 100, 2) if one_mo_close is not None and one_mo_close != 0 else None,
            "one_wk_price": round(float(one_wk_close), 2) if one_wk_close is not None else None,
            "one_wk_date": one_wk_date,
            "one_wk_pct": round((float(latest) / float(one_wk_close) - 1) * 100, 2) if one_wk_close is not None and one_wk_close != 0 else None,
            "n_obs": len(close_series),
        }
        results[ticker] = entry
        print(f"  {ticker:8s}: ${latest:<10.2f} | YTD: {entry['ytd_pct']}% | 1M: {entry['one_mo_pct']}% | 1W: {entry['one_wk_pct']}%")
        
    except Exception as e:
        print(f"  ERROR {ticker}: {e}")
        results[ticker] = {"error": str(e)}

# Also get VIX term structure / additional info
print("\n--- VIX current data ---")
vix = yf.Ticker("^VIX")
try:
    vix_info = vix.history(period="5d")
    print(vix_info.tail(3))
except Exception as e:
    print(f"VIX error: {e}")

# Output as JSON for the next step
output = {
    "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
    "date_range": f"{START} to {END}",
    "tickers": results
}

with open("/root/workspace/investment-research/reports/2026-07-07-semi-volatility/prices.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nDone. {len(results)} tickers processed. Output saved to prices.json")