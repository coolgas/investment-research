#!/usr/bin/env python3
"""Pull fresh yfinance data for the FOMC market brief."""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date
import json

TICKERS = [
    'SPY', 'QQQ', 'IWM', 'TLT', 'XLU', 'XLF', 'XLRE',
    '^TNX', 'AAPL', 'MSFT', 'NVDA', 'META', 'GOOGL', 'AMZN',
    'JPM', 'GS', 'BAC', 'PLD', 'NEE', 'WMT',
    'GC=F', 'CL=F', 'DX-Y.NYB', 'GBPUSD=X',
]

# Reference dates
YTD_START = '2026-01-02'  # Jan 1 is a holiday
POST_FOMC_START = '2026-04-29'

today = date.today()
print(f"Today: {today} ({today.strftime('%A')})")

# Fetch all tickers without group_by (per memory note about auto_adjust)
df = yf.download(
    TICKERS,
    start='2025-12-31',  # include enough history for YTD
    auto_adjust=True,
)

print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Date range: {df.index[0]} to {df.index[-1]}")

# Extract Close prices - without group_by, the structure is MultiIndex columns
# Access as df['Close'][ticker]
close = df['Close']

print("\nLast 3 trading days of data:")
print(close.tail(3))

# For each ticker, calculate returns
results = {}
for ticker in TICKERS:
    series = close[ticker].dropna()
    if len(series) < 2:
        print(f"WARNING: {ticker} has insufficient data ({len(series)})")
        continue

    latest_price = series.iloc[-1]
    prev_close = series.iloc[-2] if len(series) >= 2 else None

    # Daily change
    daily_pct = ((latest_price / prev_close) - 1) * 100 if prev_close and prev_close != 0 else None

    # YTD from Jan 2
    ytd_data = series[series.index >= YTD_START]
    ytd_start = ytd_data.iloc[0] if len(ytd_data) > 0 else None
    ytd_pct = ((latest_price / ytd_start) - 1) * 100 if ytd_start and ytd_start != 0 else None

    # Post-FOMC from Apr 29
    pf_data = series[series.index >= POST_FOMC_START]
    pf_start = pf_data.iloc[0] if len(pf_data) > 0 else None
    pf_pct = ((latest_price / pf_start) - 1) * 100 if pf_start and pf_start != 0 else None

    results[ticker] = {
        'price': round(float(latest_price), 2),
        'daily_pct': round(float(daily_pct), 2) if daily_pct is not None else None,
        'ytd_pct': round(float(ytd_pct), 2) if ytd_pct is not None else None,
        'pf_pct': round(float(pf_pct), 2) if pf_pct is not None else None,
        'last_date': str(series.index[-1].date()),
    }

    print(f"{ticker:12s} | ${latest_price:>8.2f} | {daily_pct:>+6.2f}% | YTD: {ytd_pct:>+6.2f}% | PF: {pf_pct:>+6.2f}% | {series.index[-1].date()}")

# Save as JSON for reference
with open('/home/ty/workspace/investment-research/reports/2026-05-24-fomc-april-2026/scripts/fresh_data.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\n\nDone. Data saved to scripts/fresh_data.json")