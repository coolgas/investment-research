import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def squeeze_close(df):
    """Extract a 1D Series from yfinance Close column, handling MultiIndex."""
    c = df['Close']
    if isinstance(c.columns, pd.MultiIndex):
        return c.stack().droplevel(1).squeeze()
    return c.squeeze()

print("Pulling 5yr SPY+TNX history for analog analysis...", flush=True)
spy_full = yf.download('SPY', period='5y', actions=False, auto_adjust=True)
tnx_full = yf.download('^TNX', period='5y', actions=False, auto_adjust=True)

spy_c = squeeze_close(spy_full)
tnx_c = squeeze_close(tnx_full)

common = spy_c.index.intersection(tnx_c.index)
spy_aligned = spy_c.loc[common]
tnx_aligned = tnx_c.loc[common]

spy_ret = spy_aligned.pct_change().dropna()
tnx_ret = tnx_aligned.pct_change().dropna()

common_ret = spy_ret.index.intersection(tnx_ret.index)
spy_r = spy_ret.loc[common_ret]
tnx_r = tnx_ret.loc[common_ret]

rolling_corr = spy_r.rolling(30).corr(tnx_r)

# SPECIFIC ANALOG 1: Sep-Oct 2023 bear steepening
print("\n\n=== ANALOG 1: Jul-Oct 2023 Bear Steepening (10Y: 4.0% -> 5.0%) ===", flush=True)
sep2023_spy = spy_aligned.loc['2023-07-01':'2023-10-31']
sep2023_tnx = tnx_aligned.loc['2023-07-01':'2023-10-31']
sep2023_corr = rolling_corr.loc['2023-07-01':'2023-10-31']
tnx_peak_date = sep2023_tnx.idxmax()
print(f"10Y start (Jul 1): {sep2023_tnx.iloc[0]:.2f}%", flush=True)
print(f"10Y end (Oct 31): {sep2023_tnx.iloc[-1]:.2f}%", flush=True)
print(f"10Y peak ({tnx_peak_date.date()}): {sep2023_tnx.max():.2f}%", flush=True)
spy_max = sep2023_spy.max()
spy_min = sep2023_spy.min()
spy_dd = (spy_min / spy_max - 1) * 100
print(f"SPY start: ${sep2023_spy.iloc[0]:.2f}", flush=True)
print(f"SPY end: ${sep2023_spy.iloc[-1]:.2f}", flush=True)
print(f"SPY peak-to-trough: {spy_dd:.1f}%", flush=True)
print(f"Corr range: {sep2023_corr.min():+.3f} to {sep2023_corr.max():+.3f}", flush=True)
print(f"Corr at 10Y peak: {rolling_corr.loc[tnx_peak_date]:+.3f}", flush=True)

ten_y_change_1 = sep2023_tnx.max() - sep2023_tnx.min()
damage_per_10bp_1 = spy_dd / (ten_y_change_1 * 100 / 10)
print(f"Damage per 10bp: {damage_per_10bp_1:.1f}%", flush=True)

# ANALOG 2: Jan-Jun 2022 (Rate hike cycle)
print("\n\n=== ANALOG 2: Jan-Jun 2022 ===", flush=True)
spy_2022 = spy_aligned.loc['2022-01-01':'2022-06-30']
tnx_2022 = tnx_aligned.loc['2022-01-01':'2022-06-30']
corr_2022 = rolling_corr.loc['2022-01-01':'2022-06-30']
print(f"10Y start: {tnx_2022.iloc[0]:.2f}%", flush=True)
print(f"10Y end: {tnx_2022.iloc[-1]:.2f}%", flush=True)
print(f"10Y peak ({tnx_2022.idxmax().date()}): {tnx_2022.max():.2f}%", flush=True)
spy_2022_peak = spy_2022.max()
spy_2022_trough = spy_2022.min()
spy_dd_2 = (spy_2022_trough / spy_2022_peak - 1) * 100
print(f"SPY peak-to-trough: {spy_dd_2:.1f}%", flush=True)
print(f"Corr range: {corr_2022.min():+.3f} to {corr_2022.max():+.3f}", flush=True)
ten_y_change_2 = tnx_2022.max() - tnx_2022.iloc[0]
damage_per_10bp_2 = spy_dd_2 / (ten_y_change_2 * 100 / 10) if ten_y_change_2 > 0 else 0
print(f"Damage per 10bp: {damage_per_10bp_2:.1f}%", flush=True)

# ANALOG 3: Sep-Nov 2023 (tighter window around 5% peak)
print("\n\n=== ANALOG 3: Sep-Nov 2023 (tight window, 10Y 4.3%->5.0%) ===", flush=True)
oct2023_spy = spy_aligned.loc['2023-09-01':'2023-11-30']
oct2023_tnx = tnx_aligned.loc['2023-09-01':'2023-11-30']
oct2023_corr = rolling_corr.loc['2023-09-01':'2023-11-30']
print(f"10Y start: {oct2023_tnx.iloc[0]:.2f}%", flush=True)
print(f"10Y peak ({oct2023_tnx.idxmax().date()}): {oct2023_tnx.max():.2f}%", flush=True)
spy_oct_max = oct2023_spy.max()
spy_oct_min = oct2023_spy.min()
spy_dd_3 = (spy_oct_min / spy_oct_max - 1) * 100
print(f"SPY peak-to-trough: {spy_dd_3:.1f}%", flush=True)
print(f"Corr range: {oct2023_corr.min():+.3f} to {oct2023_corr.max():+.3f}", flush=True)
print(f"Corr at 10Y peak: {rolling_corr.loc[oct2023_tnx.idxmax()]:+.3f}", flush=True)
ten_y_change_3 = oct2023_tnx.max() - oct2023_tnx.iloc[0]
damage_per_10bp_3 = spy_dd_3 / (ten_y_change_3 * 100 / 10) if ten_y_change_3 > 0 else 0
print(f"Damage per 10bp: {damage_per_10bp_3:.1f}%", flush=True)

# Sector breakdown for Oct 2023
print("\n--- Oct 2023 Sector Breakdown (peak-to-trough) ---", flush=True)
sectors = {'XLU': 'Utilities', 'XLRE': 'Real Estate', 'XLF': 'Financials', 'QQQ': 'Nasdaq-100', 'IWM': 'Small Caps'}
for ticker, name in sectors.items():
    s = yf.download(ticker, start='2023-09-01', end='2023-11-30', actions=False, auto_adjust=True)
    sc = squeeze_close(s)
    peak = sc.max()
    trough = sc.min()
    dd = (trough / peak - 1) * 100
    print(f"  {ticker:6s} ({name:15s}): peak ${peak:.2f} -> trough ${trough:.2f} = {dd:+.1f}%", flush=True)

# ANALOG 4: Jan-Mar 2025
print("\n\n=== ANALOG 4: Jan-Mar 2025 ===", flush=True)
spy_2025 = spy_aligned.loc['2025-01-01':'2025-03-31']
tnx_2025 = tnx_aligned.loc['2025-01-01':'2025-03-31']
corr_2025 = rolling_corr.loc['2025-01-01':'2025-03-31']
print(f"10Y start: {tnx_2025.iloc[0]:.2f}%", flush=True)
print(f"10Y peak ({tnx_2025.idxmax().date()}): {tnx_2025.max():.2f}%", flush=True)
spy_2025_peak = spy_2025.max()
spy_2025_trough = spy_2025.min()
spy_dd_5 = (spy_2025_trough / spy_2025_peak - 1) * 100
print(f"SPY peak-to-trough: {spy_dd_5:.1f}%", flush=True)
print(f"Corr range: {corr_2025.min():+.3f} to {corr_2025.max():+.3f}", flush=True)
ten_y_change_5 = tnx_2025.max() - tnx_2025.iloc[0]
damage_per_10bp_5 = spy_dd_5 / (ten_y_change_5 * 100 / 10) if ten_y_change_5 > 0 else 0
print(f"Damage per 10bp: {damage_per_10bp_5:.1f}%", flush=True)

# Summary comparison
print("\n\n=== SUMMARY: Damage per 10bp ===", flush=True)
print(f"Jul-Oct 2023 (4.0%->5.0%): {damage_per_10bp_1:.1f}% per 10bp", flush=True)
print(f"Sep-Nov 2023 (4.3%->5.0%): {damage_per_10bp_3:.1f}% per 10bp", flush=True)
print(f"Jan-Jun 2022:              {damage_per_10bp_2:.1f}% per 10bp", flush=True)
print(f"Jan-Mar 2025:              {damage_per_10bp_5:.1f}% per 10bp", flush=True)

# Projection for current scenario
current_10y = tnx_aligned.iloc[-1]
current_spy = spy_aligned.iloc[-1]
print(f"\n\n=== Current scenario: 10Y={current_10y:.2f}% SPY=${current_spy:.2f} ===", flush=True)

# Use the avg of the most relevant analogs (Jul-Oct 2023 and Sep-Nov 2023)
avg_per_10bp = (damage_per_10bp_1 + damage_per_10bp_3) / 2
print(f"\nUsing average of 2023 analogs: {avg_per_10bp:.1f}% per 10bp", flush=True)
for bp in [20, 30]:
    damage = avg_per_10bp * (bp / 10)
    spy_target = current_spy * (1 + damage/100)
    print(f"  +{bp}bp to {current_10y + bp/100:.2f}%: SPY {damage:+.1f}% -> ${spy_target:.2f}", flush=True)

# Best case (min damage analog) and worst case (max damage analog)
best = min(damage_per_10bp_1, damage_per_10bp_2, damage_per_10bp_3, damage_per_10bp_5)
worst = max(damage_per_10bp_1, damage_per_10bp_2, damage_per_10bp_3, damage_per_10bp_5)
print(f"\nBest case ({best:.1f}%/10bp):", flush=True)
for bp in [20, 30]:
    d = best * (bp / 10)
    print(f"  +{bp}bp: SPY {d:+.1f}% -> ${current_spy * (1 + d/100):.2f}", flush=True)
print(f"\nWorst case ({worst:.1f}%/10bp):", flush=True)
for bp in [20, 30]:
    d = worst * (bp / 10)
    print(f"  +{bp}bp: SPY {d:+.1f}% -> ${current_spy * (1 + d/100):.2f}", flush=True)

print("\nDone.", flush=True)