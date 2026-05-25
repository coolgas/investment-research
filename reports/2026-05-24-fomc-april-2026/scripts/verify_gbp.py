import pandas as pd, yfinance as yf

df = yf.download(["GBPUSD=X"], start="2026-05-20", end="2026-05-26", auto_adjust=True, progress=False)
close = df['Close']['GBPUSD=X'].dropna()
print("GBPUSD=X raw values:")
for idx, val in close.items():
    print(f"  {idx.strftime('%Y-%m-%d')}: {val} ({type(val).__name__})")

last = float(close.iloc[-1])
prev = float(close.iloc[-2])
print(f"\nLast: {last}, Prev: {prev}")
print(f"Daily%: {((last/prev)-1)*100:.4f}%")
print(f"Rounded: {round(((last/prev)-1)*100, 2)}%")