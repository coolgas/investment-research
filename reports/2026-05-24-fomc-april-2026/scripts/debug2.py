import pandas as pd
import yfinance as yf

TICKERS = ["SPY", "QQQ", "IWM", "TLT", "XLU", "XLF", "XLRE",
    "^TNX", "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    "JPM", "GS", "BAC", "PLD", "NEE", "WMT",
    "GC=F", "CL=F", "DX-Y.NYB", "GBPUSD=X"]

df = yf.download(TICKERS, start="2025-12-30", end="2026-05-26", auto_adjust=True, progress=False)
close = df['Close']

# Print last 5 rows for SPY and a few others
print("Last 5 rows for key tickers:")
for t in ["SPY", "QQQ", "^TNX", "AAPL", "GS", "GC=F", "CL=F", "DX-Y.NYB", "GBPUSD=X"]:
    vals = close[t].tail(5).values
    idxs = close[t].tail(5).index
    print(f"{t}: {list(zip([d.strftime('%Y-%m-%d') for d in idxs], [round(v,2) if pd.notna(v) else 'NaN' for v in vals]))}")

# Figure out last actual non-NaN price for each ticker
print("\nLast actual price for each ticker:")
for t in TICKERS:
    last_valid = close[t].dropna()
    if len(last_valid) > 0:
        last_dt = last_valid.index[-1]
        last_val = last_valid.iloc[-1]
        print(f"  {t}: {round(last_val,2)} on {last_dt.strftime('%Y-%m-%d')}")
    else:
        print(f"  {t}: NO DATA")