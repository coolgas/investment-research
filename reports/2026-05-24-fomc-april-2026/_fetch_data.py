#!/usr/bin/env python3
"""Pull yfinance data for FOMC market brief data refresh.

Tickers:
  Indices: SPY, QQQ, IWM, ^TNX, DXY
  Sectors: TLT, XLU, XLF, XLRE
  Stocks: AAPL, MSFT, NVDA, META, GOOGL, AMZN, JPM, GS, BAC, PLD, NEE, WMT
  Commodities: GC=F, CL=F
  FX: GBPUSD=X
"""
import yfinance as yf
import pandas as pd
import json
import datetime

TICKER_MAP = {
    "SPY": "S&P 500",
    "QQQ": "Nasdaq 100",
    "IWM": "Russell 2000",
    "^TNX": "10Y Yield",
    "DXY": "US Dollar Index",
    "TLT": "20Y+ Treasury",
    "XLU": "Utilities",
    "XLF": "Financials",
    "XLRE": "Real Estate",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "META": "Meta",
    "GOOGL": "Alphabet",
    "AMZN": "Amazon",
    "JPM": "JPMorgan",
    "GS": "Goldman Sachs",
    "BAC": "Bank of America",
    "PLD": "Prologis",
    "NEE": "NextEra Energy",
    "WMT": "Walmart",
    "GC=F": "Gold",
    "CL=F": "Crude Oil",
    "GBPUSD=X": "GBP/USD",
}

TICKERS = list(TICKER_MAP.keys())

today = datetime.date.today()
print(f"Today: {today}")
print(f"Fetching data for {len(TICKERS)} tickers...")

start_date = "2026-01-02"
end_date = today.strftime("%Y-%m-%d")

data = yf.download(TICKERS, start=start_date, end=end_date, auto_adjust=True, group_by="ticker")
print(f"Downloaded data. Columns: {data.columns.nlevels if hasattr(data.columns, 'nlevels') else 1}")

results = {}

for t in TICKERS:
    try:
        if hasattr(data.columns, 'nlevels') and data.columns.nlevels == 2:
            # MultiIndex case: columns are (ticker, OHLCV)
            closes = data.xs('Close', axis=1, level=1)[t].dropna()
        else:
            # Single level - might be scalar or DataFrame
            closes = data['Close'][t].dropna() if isinstance(data, pd.DataFrame) and 'Close' in data.columns else data[t].dropna()

        if len(closes) < 2:
            results[t] = {"error": f"Insufficient data ({len(closes)} rows)"}
            print(f"  {t}: INSUFFICIENT DATA ({len(closes)} rows)")
            continue

        latest_close = closes.iloc[-1]
        prev_close = closes.iloc[-2]

        daily_pct = (latest_close / prev_close - 1) * 100
        ytd_start = closes.iloc[0]
        ytd_pct = (latest_close / ytd_start - 1) * 100

        # Post-FOMC: closest date to Apr 29, 2026
        target_date = pd.Timestamp("2026-04-29")
        idx = closes.index.searchsorted(target_date)
        if idx >= len(closes):
            idx = len(closes) - 1
        post_fomc_close = closes.iloc[idx]
        post_fomc_pct = (latest_close / post_fomc_close - 1) * 100

        # Format price
        if t in ("^TNX",):
            price = round(float(latest_close), 3)
        elif t in ("GC=F",):
            price = round(float(latest_close), 1)
        else:
            price = round(float(latest_close), 2)

        results[t] = {
            "price": price,
            "daily_pct": round(float(daily_pct), 2),
            "ytd_pct": round(float(ytd_pct), 2),
            "post_fomc_pct": round(float(post_fomc_pct), 2),
        }
        print(f"  {TICKER_MAP[t]:20s} ${price:<8}  Daily: {daily_pct:+7.2f}%  YTD: {ytd_pct:+7.2f}%  Post-FOMC: {post_fomc_pct:+7.2f}%")

    except Exception as e:
        results[t] = {"error": str(e)}
        print(f"  {t}: ERROR - {e}")

with open("/tmp/fomc_data.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nDone. {sum(1 for v in results.values() if 'error' not in v)}/{len(TICKERS)} tickers OK.")
print("Data saved to /tmp/fomc_data.json")