#!/usr/bin/env python3
"""yfinance data refresh: pull latest prices, compute returns."""
import json, sys
import yfinance as yf
from datetime import datetime, date

TICKERS = [
    # Broad market
    "SPY", "QQQ", "IWM", "TLT",
    # Sectors
    "XLU", "XLF", "XLRE",
    # Rates
    "^TNX",
    # Mega-cap tech
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    # Banks
    "JPM", "GS", "BAC",
    # REIT / utilities / consumer
    "PLD", "NEE", "WMT",
    # Commodities
    "GC=F", "CL=F",
    # FX
    "DX-Y.NYB", "GBPUSD=X",
]

TODAY = date(2026, 5, 24)
YTD_START = "2025-12-31"
FOMC_START = "2026-04-29"

results = []

for ticker in TICKERS:
    try:
        t = yf.Ticker(ticker)
        hist = t.history(start="2025-12-01", end="2026-05-25")
        
        if hist.empty:
            results.append({"ticker": ticker, "error": "no data"})
            continue
        
        # Latest close
        latest = hist.iloc[-1]
        latest_date = hist.index[-1].strftime("%Y-%m-%d")
        price = round(float(latest["Close"]), 2)
        
        # Daily change (vs previous close)
        prev_close = float(hist.iloc[-2]["Close"]) if len(hist) >= 2 else price
        daily_chg = round(price - prev_close, 2)
        daily_chg_pct = round((price / prev_close - 1) * 100, 2)
        
        # YTD return from 2025-12-31 close
        ytd_slice = hist.loc[YTD_START:]
        if not ytd_slice.empty and len(ytd_slice) >= 2:
            ytd_start_price = float(ytd_slice.iloc[0]["Close"])  # Dec 31 close
            ytd_return = round((price / ytd_start_price - 1) * 100, 2)
        else:
            ytd_return = None
        
        # Post-FOMC return from 2026-04-29 close
        fomc_slice = hist.loc[FOMC_START:]
        if not fomc_slice.empty and len(fomc_slice) > 1:
            # The Apr 29 close is the first data point - that's the FOMC day close
            fomc_start_price = float(fomc_slice.iloc[0]["Close"])
            fomc_return = round((price / fomc_start_price - 1) * 100, 2)
        else:
            fomc_return = None
        
        results.append({
            "ticker": ticker,
            "latest_date": latest_date,
            "price": price,
            "daily_chg": daily_chg,
            "daily_chg_pct": daily_chg_pct,
            "ytd_return": ytd_return,
            "fomc_return": fomc_return,
            "error": None,
        })
        
        print(f"OK  {ticker:>10s}  {price:>8.2f}  d{daily_chg_pct:>+7.2f}%  YTD:{ytd_return if ytd_return is not None else 'N/A':>+8}  FOMC:{fomc_return if fomc_return is not None else 'N/A':>+8}", flush=True)
        
    except Exception as e:
        results.append({"ticker": ticker, "error": str(e)})
        print(f"ERR {ticker:>10s}  {e}", flush=True)

# Save JSON
out = {
    "fetched_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "as_of_date": results[0]["latest_date"] if results and not results[0].get("error") else "unknown",
    "tickers": results,
}
with open(sys.argv[1], "w") as f:
    json.dump(out, f, indent=2)
print(f"\nSaved to {sys.argv[1]}")