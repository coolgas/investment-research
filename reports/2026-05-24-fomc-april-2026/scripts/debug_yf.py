#!/usr/bin/env python3
"""Debug yfinance structure"""
import yfinance as yf

# Test one ticker
ind = yf.download("SPY", start="2026-01-01", end="2026-05-25", auto_adjust=True, progress=False)
print("Type:", type(ind))
print("Shape:", ind.shape if hasattr(ind, 'shape') else 'N/A')
print("Columns:", ind.columns.tolist())
print("Index:", ind.index[:5])
print()
print("First 3 rows:")
print(ind.head(3))
print()

# Try accessing Close
close_col = None
for c in ind.columns:
    if 'close' in c.lower():
        close_col = c
        break
print(f"Close column: {close_col}")

if close_col:
    series = ind[close_col]
    print(f"Series type: {type(series)}")
    print(f"Last val type: {type(series.iloc[-1])}")
    print(f"Last val: {series.iloc[-1]}")

# Test one more that might be different
print("\n--- Testing ^TNX ---")
ind2 = yf.download("^TNX", start="2026-01-01", end="2026-05-25", auto_adjust=True, progress=False)
print("Type:", type(ind2))
print("Shape:", ind2.shape if hasattr(ind2, 'shape') else 'N/A')
print("Columns:", ind2.columns.tolist())
print(ind2.head(3))

for c in ind2.columns:
    if 'close' in c.lower():
        series = ind2[c]
        print(f"Last val: {series.iloc[-1]}, type: {type(series.iloc[-1])}")

# Test gold
print("\n--- Testing GC=F ---")
ind3 = yf.download("GC=F", start="2026-01-01", end="2026-05-25", auto_adjust=True, progress=False)
print("Columns:", ind3.columns.tolist())
for c in ind3.columns:
    if 'close' in c.lower():
        series = ind3[c]
        print(f"Last val: {series.iloc[-1]}, type: {type(series.iloc[-1])}")