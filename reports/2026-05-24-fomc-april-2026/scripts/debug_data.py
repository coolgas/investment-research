import yfinance as yf
import pandas as pd

# Try without auto_adjust first to see structure
TICKERS = ["SPY", "QQQ", "IWM", "TLT", "XLU", "XLF", "XLRE",
    "^TNX", "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    "JPM", "GS", "BAC", "PLD", "NEE", "WMT",
    "GC=F", "CL=F", "DX-Y.NYB", "GBPUSD=X"]

print("=== Without auto_adjust ===")
df = yf.download(TICKERS, start="2026-05-22", end="2026-05-26", auto_adjust=False, progress=False)
print(type(df))
print(df.shape)
print(df.columns)
print(df.index)
print(df.iloc[-1].head(20))

# Try auto_adjust=True separately
print("\n=== With auto_adjust=True ===")
df2 = yf.download(TICKERS, start="2026-05-22", end="2026-05-26", auto_adjust=True, progress=False)
print(type(df2))
print(df2.shape)
if isinstance(df2.columns, pd.MultiIndex):
    print("MultiIndex columns:", df2.columns.tolist())
else:
    print("Columns:", df2.columns.tolist())
print(type(df2))
print(df2)