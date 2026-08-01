import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

tickers_dict = {
    "XLU": "Utilities",
    "XLP": "Consumer Staples",
    "XLV": "Health Care",
    "XLI": "Industrials",
    "XLF": "Financials",
    "XLE": "Energy",
    "XLB": "Materials",
    "XLY": "Consumer Discretionary",
    "IWM": "Russell 2000 (Small Caps)",
    "DIA": "Dow Jones (Old Economy)",
    "QQQ": "Nasdaq 100 (Tech)",
    "SMH": "Semiconductors",
    "SOXX": "Semiconductors (iShares)",
    "TLT": "20+ Year Treasury Bonds",
    "GLD": "Gold Trust",
    "SPY": "S&P 500 (Benchmark)",
}

end_date = "2026-07-07"
ytd_start = "2026-01-02"
month_start = "2026-06-01"
week_start = "2026-06-30"

tickers = list(tickers_dict.keys())

data = yf.download(
    tickers, 
    start=ytd_start, 
    end="2026-07-08",
    auto_adjust=True,
    progress=False
)

# data has MultiIndex columns (Price, Ticker)
closes = data['Close'] if 'Close' in data.columns.get_level_values(0) else data.xs('Close', axis=1, level=0)

# If 'Close' not found, try 'Adj Close' or use the first level
if closes.empty:
    print("Trying alternative column access...")
    print(data.columns[:5])
    closes = data

print("Closes shape:", closes.shape)
print("Closes columns:", list(closes.columns))
print("Latest date:", closes.index[-1])
print("Earliest date:", closes.index[0])
print()

def calc_ret(data_slice, label):
    first = data_slice.iloc[0]
    last = data_slice.iloc[-1]
    if first != 0:
        return (last / first - 1) * 100
    return None

# Get latest close for each
latest = closes.iloc[-1]
print("=== LATEST CLOSES (%s) ===" % closes.index[-1].strftime('%Y-%m-%d'))
for t in tickers:
    val = latest[t] if t in latest.index else None
    name = tickers_dict.get(t, t)
    if val is not None:
        print(f"{t:6s} ({name:45s}): {val:.2f}")
print()

# Now compute returns for each period
# We need to find the closest dates to our targets
dates = closes.index

# YTD: from Jan 2
ytd_idx = dates[0]  # Should be Jan 2
ytd_date = ytd_idx

# Month: find closest to June 1
month_target = pd.Timestamp("2026-06-01")
month_idx = dates[dates <= month_target][-1] if any(dates <= month_target) else dates[0]

# Week: find closest to June 30
week_target = pd.Timestamp("2026-06-30")
week_idx = dates[dates <= week_target][-1] if any(dates <= week_target) else dates[0]

# Also compute 2-week for comparison
two_week_target = pd.Timestamp("2026-06-23")
two_week_idx = dates[dates <= two_week_target][-1] if any(dates <= two_week_target) else dates[0]

print("Period date mapping:")
print(f"  YTD start:   {ytd_date.date()} (idx 0)")
print(f"  1M start:    {month_idx.date()}")
print(f"  2W start:    {two_week_idx.date()}")
print(f"  1W start:    {week_idx.date()}")
print(f"  Latest:      {closes.index[-1].date()}")
print()

# Compute returns
results = []
for t in tickers:
    col = closes[t]
    if col.empty:
        continue
    name = tickers_dict.get(t, t)
    
    ytd_ret = (col.iloc[-1] / col.iloc[0] - 1) * 100
    
    # Month return
    month_vals = col.loc[month_idx:]
    month_ret = (month_vals.iloc[-1] / month_vals.iloc[0] - 1) * 100
    
    # 2-week return
    two_week_vals = col.loc[two_week_idx:]
    two_week_ret = (two_week_vals.iloc[-1] / two_week_vals.iloc[0] - 1) * 100
    
    # 1-week return
    week_vals = col.loc[week_idx:]
    week_ret = (week_vals.iloc[-1] / week_vals.iloc[0] - 1) * 100
    
    results.append({
        "Ticker": t,
        "Name": name,
        "YTD": round(ytd_ret, 2),
        "1M": round(month_ret, 2),
        "2W": round(two_week_ret, 2),
        "1W": round(week_ret, 2),
        "Latest": round(col.iloc[-1], 2)
    })

df = pd.DataFrame(results)

# Sort by 1W return descending
print("=== SORTED BY 1W RETURN (highest to lowest) ===")
sorted_1w = df.sort_values("1W", ascending=False)
for _, r in sorted_1w.iterrows():
    print(f"{r['Ticker']:6s} | {r['Name']:45s} | 1W: {r['1W']:6.2f}% | 2W: {r['2W']:6.2f}% | 1M: {r['1M']:6.2f}% | YTD: {r['YTD']:6.2f}%")

print()
print("=== SORTED BY 2W RETURN (highest to lowest) ===")
sorted_2w = df.sort_values("2W", ascending=False)
for _, r in sorted_2w.iterrows():
    print(f"{r['Ticker']:6s} | {r['Name']:45s} | 2W: {r['2W']:6.2f}% | 1W: {r['1W']:6.2f}% | 1M: {r['1M']:6.2f}% | YTD: {r['YTD']:6.2f}%")

print()
print("=== SORTED BY YTD RETURN (highest to lowest) ===")
sorted_ytd = df.sort_values("YTD", ascending=False)
for _, r in sorted_ytd.iterrows():
    print(f"{r['Ticker']:6s} | {r['Name']:45s} | YTD: {r['YTD']:6.2f}% | 1M: {r['1M']:6.2f}% | 1W: {r['1W']:6.2f}%")

# Also compute "rotation beneficiary" metric: return of X while SMH fell
# Check which dates the semis fell
print()
print("=== SMH TREND CHECK ===")
smh = closes['SMH']
for i in range(len(smh)-1, -1, -1):
    if smh.index[i] >= week_idx or i >= len(smh)-8:
        continue
    break

# Print last 10 days of SMH and SPY
print(f"{'Date':12s} | {'SMH':10s} | {'SPY':10s} | {'XLF':10s} | {'XLE':10s} | {'XLU':10s} | {'XLP':10s} | {'XLV':10s}")
print("-" * 80)
for i in range(max(0, len(closes)-15), len(closes)):
    d = closes.index[i]
    smh_v = closes['SMH'].iloc[i]
    spy_v = closes['SPY'].iloc[i]
    xlf_v = closes['XLF'].iloc[i]
    xle_v = closes['XLE'].iloc[i]
    xlu_v = closes['XLU'].iloc[i]
    xlp_v = closes['XLP'].iloc[i]
    xlv_v = closes['XLV'].iloc[i]
    print(f"{d.strftime('%Y-%m-%d'):12s} | {smh_v:>8.2f} | {spy_v:>8.2f} | {xlf_v:>8.2f} | {xle_v:>8.2f} | {xlu_v:>8.2f} | {xlp_v:>8.2f} | {xlv_v:>8.2f}")
