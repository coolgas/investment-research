import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

CUTOFF = "2026-07-07"
print("=" * 80)
print("SMGB.L DIP-BUYING ANALYSIS")
print("=" * 80)

def _c(df):
    """Extract close series from yfinance dataframe (handles MultiIndex)."""
    if hasattr(df.columns, 'nlevels') and df.columns.nlevels > 1:
        return df[('Close', df.columns.get_level_values(1)[0])]
    return df['Close']

# --- 1. Pull SMGB.L data ---
print("\n[1] Pulling SMGB.L data...")
smgb = yf.download("SMGB.L", period="max", auto_adjust=True)
if smgb.empty:
    print("SMGB.L empty, trying SMGB...")
    smgb = yf.download("SMGB", period="max", auto_adjust=True)

close = _c(smgb)
print(f"SMGB.L: {len(smgb)} rows, {smgb.index[0].date()} to {smgb.index[-1].date()}")
print(f"Current close (last): {close.iloc[-1]:.2f}")
print(f"Last date: {smgb.index[-1].date()}")

# --- 2. Compute drawdown series ---
print("\n[2] Computing drawdowns...")
cummax = close.cummax()
dd_series = (close - cummax) / cummax * 100
smgb['Drawdown'] = dd_series

# Current drawdown from 2026 peak
last_row = smgb.iloc[-1]
peak_2026 = close.loc['2026-01-01':]
peak_val = peak_2026.max()
peak_date = peak_2026.idxmax()
current_dd = (close.iloc[-1] - peak_val) / peak_val * 100
print(f"\n2026 Peak: {peak_val:.2f} on {peak_date.date()}")
print(f"Current close: {close.iloc[-1]:.2f} on {smgb.index[-1].date()}")
print(f"Current drawdown from 2026 peak: {current_dd:.2f}%")

# --- 3. Historical corrections >5% ---
print("\n[3] Identifying corrections >5%...")
in_drawdown = False
corrections = []
start_idx = None
trough_idx = None
trough_dd = 0

for i in range(len(smgb)):
    dd = smgb['Drawdown'].iloc[i]
    if not in_drawdown and dd < -5:
        in_drawdown = True
        start_idx = smgb.index[i-1] if i > 0 else smgb.index[i]
        trough_idx = smgb.index[i]
        trough_dd = dd
    elif in_drawdown:
        if dd < trough_dd:
            trough_dd = dd
            trough_idx = smgb.index[i]
        # Recovery: drawdown back above 0
        if dd >= 0 or i == len(smgb)-1:
            in_drawdown = False
            end_idx = smgb.index[i] if dd >= 0 else None
            recovery = None
            if end_idx:
                recovery_days = (end_idx - trough_idx).days
            else:
                recovery_days = None
            duration_to_trough = (trough_idx - start_idx).days
            corrections.append({
                'start': start_idx,
                'trough': trough_idx,
                'end': end_idx,
                'depth': trough_dd,
                'duration_to_trough': duration_to_trough,
                'recovery_days': recovery_days
            })

print(f"Found {len(corrections)} corrections >5%")
for c in corrections:
    rec_str = f"{c['recovery_days']}d" if c['recovery_days'] else "ongoing"
    print(f"  {c['start'].date()} -> {c['trough'].date()} ({c['duration_to_trough']}d): {c['depth']:.2f}%, recovery: {rec_str}")

depths = [c['depth'] for c in corrections]
durations = [c['duration_to_trough'] for c in corrections]
recoveries = [c['recovery_days'] for c in corrections if c['recovery_days']]

print(f"\nCorrection depth stats:")
print(f"  Mean: {np.mean(depths):.2f}%")
print(f"  Median: {np.median(depths):.2f}%")
print(f"  Min: {min(depths):.2f}%")
print(f"  Max: {max(depths):.2f}%")

print(f"\nDuration to trough (days):")
print(f"  Mean: {np.mean(durations):.1f}d")
print(f"  Median: {np.median(durations):.1f}d")
if recoveries:
    print(f"\nRecovery time (days):")
    print(f"  Mean: {np.mean(recoveries):.1f}d")
    print(f"  Median: {np.median(recoveries):.1f}d")

# --- 4. Forward returns at drawdown thresholds ---
print("\n[4] Forward returns after drawdown thresholds...")

thresholds = [-10, -12, -15, -20, -25]
forward_windows = [21, 63, 126]  # 1M, 3M, 6M trading days

results = []
for thresh in thresholds:
    entry_dates = smgb[smgb['Drawdown'] <= thresh].index
    print(f"\nThreshold {thresh}%: {len(entry_dates)} entry signals")
    
    for fwd_days in forward_windows:
        fwd_label = f"{fwd_days}d"
        returns = []
        for dt in entry_dates:
            entry_price = close.loc[dt]
            fwd_idx = smgb.index.get_loc(dt) + fwd_days
            if fwd_idx < len(smgb):
                exit_price = close.iloc[fwd_idx]
                ret = (exit_price / entry_price - 1) * 100
                returns.append(ret)
        
        if returns:
            win_rate = sum(1 for r in returns if r > 0) / len(returns) * 100
            results.append({
                'threshold': thresh,
                'window': fwd_label,
                'n': len(returns),
                'mean': np.mean(returns),
                'median': np.median(returns),
                'win_rate': win_rate,
                'std': np.std(returns),
                'min': min(returns),
                'max': max(returns)
            })
            print(f"  {fwd_label}: n={len(returns)}, mean={np.mean(returns):.2f}%, median={np.median(returns):.2f}%, win_rate={win_rate:.1f}%")

# --- 5. Key support levels ---
print("\n[5] Key moving average support levels...")
sma50 = close.rolling(50).mean().iloc[-1]
sma100 = close.rolling(100).mean().iloc[-1]
sma200 = close.rolling(200).mean().iloc[-1]
current = close.iloc[-1]

print(f"Current price: {current:.2f}")
print(f"SMA50:  {sma50:.2f}  ({(current/sma50 - 1)*100:+.2f}%)")
print(f"SMA100: {sma100:.2f}  ({(current/sma100 - 1)*100:+.2f}%)")
print(f"SMA200: {sma200:.2f}  ({(current/sma200 - 1)*100:+.2f}%)")

# Support clusters: significant bounce points
local_minima = []
for i in range(1, len(smgb)-1):
    if smgb['Drawdown'].iloc[i] < -5:
        if (smgb['Drawdown'].iloc[i] <= smgb['Drawdown'].iloc[i-1] and 
            smgb['Drawdown'].iloc[i] <= smgb['Drawdown'].iloc[i+1]):
            local_minima.append({
                'date': smgb.index[i],
                'price': close.iloc[i],
                'dd': smgb['Drawdown'].iloc[i]
            })

if local_minima:
    prices = [lm['price'] for lm in local_minima]
    print(f"\nLocal minima (bounce points): {len(local_minima)} found")
    sorted_bottoms = sorted(local_minima, key=lambda x: x['dd'])
    print("Deepest bounce points:")
    for b in sorted_bottoms[:15]:
        print(f"  {b['date'].date()}: price={b['price']:.2f}, dd={b['dd']:.2f}%")

# --- 6. Compare with SMH ---
print("\n[6] SMH comparison data...")
smh = yf.download("SMH", period="max", auto_adjust=True)
print(f"SMH: {len(smh)} rows, {smh.index[0].date()} to {smh.index[-1].date()}")

smh_close = _c(smh)
smh_cummax = smh_close.cummax()
smh_dd = (smh_close - smh_cummax) / smh_cummax * 100
smh['Drawdown'] = smh_dd

# SMH corrections >5%
smh_corrections = []
in_dd = False
for i in range(len(smh)):
    dd = smh_dd.iloc[i]
    if not in_dd and dd < -5:
        in_dd = True
        s_idx = smh.index[i-1] if i > 0 else smh.index[i]
        t_idx = smh.index[i]
        t_dd = dd
    elif in_dd:
        if dd < t_dd:
            t_dd = dd
            t_idx = smh.index[i]
        if dd >= 0 or i == len(smh)-1:
            in_dd = False
            e_idx = smh.index[i] if dd >= 0 else None
            rec = None
            if e_idx:
                rec = (e_idx - t_idx).days
            smh_corrections.append({
                'start': s_idx, 'trough': t_idx, 'end': e_idx,
                'depth': t_dd, 'duration_to_trough': (t_idx - s_idx).days,
                'recovery_days': rec
            })

smh_depths = [c['depth'] for c in smh_corrections]
smh_durations = [c['duration_to_trough'] for c in smh_corrections]
print(f"SMH corrections >5%: {len(smh_corrections)}")
print(f"SMH median depth: {np.median(smh_depths):.2f}%")
print(f"SMH median duration: {np.median(smh_durations):.1f}d")

# SMH forward returns at -10%
smh_entry = smh[smh['Drawdown'] <= -10]
print(f"SMH entries at -10%: {len(smh_entry)}")
for fwd_days in [21, 63, 126]:
    rets = []
    for dt in smh_entry.index:
        ep = smh_close.loc[dt]
        fi = smh.index.get_loc(dt) + fwd_days
        if fi < len(smh):
            rets.append((smh_close.iloc[fi] / ep - 1) * 100)
    if rets:
        wr = sum(1 for r in rets if r > 0) / len(rets) * 100
        print(f"  {fwd_days}d: n={len(rets)}, mean={np.mean(rets):.2f}%, median={np.median(rets):.2f}%, win_rate={wr:.1f}%")

print("\n\nAnalysis complete.")