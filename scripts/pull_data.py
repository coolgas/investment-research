import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Define tickers
tickers = {
    'indices': ['SPY', 'QQQ', 'IWM'],
    'sectors': ['XLU', 'XLRE', 'XLF', 'XLY', 'XLI'],
    'stocks': ['AAPL', 'GOOGL', 'MSFT', 'NVDA', 'META', 'AMZN', 'JPM', 'BAC', 'GS', 'PLD', 'NEE', 'WMT'],
    'yields': ['^TNX', '^FVX', '^IRX', '^TYX']
}

all_tickers = [t for group in tickers.values() for t in group]
print(f"Pulling {len(all_tickers)} tickers...", flush=True)

# Pull 6 months of daily data
data = yf.download(all_tickers, period='6mo', actions=False, auto_adjust=True)

# Get the latest close prices
prices = {}
for t in all_tickers:
    try:
        if t.startswith('^'):
            prices[t] = float(data['Close'][t].dropna().iloc[-1])
        else:
            prices[t] = float(data['Close'][t].dropna().iloc[-1])
    except Exception as e:
        try:
            tk = yf.Ticker(t)
            hist = tk.history(period='5d')
            prices[t] = float(hist['Close'].iloc[-1])
        except:
            prices[t] = None

# Pull 52-week high data
one_year = yf.download(all_tickers, period='1y', actions=False, auto_adjust=True)
high_52w = {}
for t in all_tickers:
    try:
        if t.startswith('^'):
            high_52w[t] = float(one_year['Close'][t].max())
        else:
            high_52w[t] = float(one_year['Close'][t].max())
    except:
        high_52w[t] = None

# Calculate % of 52w high
pct_of_52w_high = {}
dist_to_52w_high = {}
for t in all_tickers:
    if prices[t] and high_52w[t]:
        pct_of_52w_high[t] = (prices[t] / high_52w[t]) * 100
        dist_to_52w_high[t] = ((prices[t] - high_52w[t]) / high_52w[t]) * 100
    else:
        pct_of_52w_high[t] = None
        dist_to_52w_high[t] = None

print("\n=== Current Prices ===", flush=True)
for t in all_tickers:
    if prices[t]:
        print(f"{t:8s}: ${prices[t]:>8.2f}  52w high: ${high_52w[t]:>8.2f}  % of 52w: {pct_of_52w_high[t]:>5.1f}%  dist: {dist_to_52w_high[t]:>+.1f}%", flush=True)

print("\n=== Yields ===", flush=True)
for t in tickers['yields']:
    if prices[t]:
        print(f"{t:8s}: {prices[t]:>.2f}%", flush=True)

# Calculate SPY vs 10Y correlation
spy_close = data['Close']['SPY'].dropna()
tnx_close = data['Close']['^TNX'].dropna()

common_dates = spy_close.index.intersection(tnx_close.index)
spy_aligned = spy_close.loc[common_dates]
tnx_aligned = tnx_close.loc[common_dates]

spy_returns = spy_aligned.pct_change().dropna()
tnx_returns = tnx_aligned.pct_change().dropna()

common_ret_dates = spy_returns.index.intersection(tnx_returns.index)
spy_ret = spy_returns.loc[common_ret_dates]
tnx_ret = tnx_returns.loc[common_ret_dates]

full_corr = np.corrcoef(spy_ret, tnx_ret)[0, 1]
recent = spy_ret.iloc[-30:]
recent_tnx = tnx_ret.loc[recent.index]
recent_corr = np.corrcoef(recent, recent_tnx)[0, 1]
mid = spy_ret.iloc[-60:]
mid_tnx = tnx_ret.loc[mid.index]
mid_corr = np.corrcoef(mid, mid_tnx)[0, 1]

print(f"\n=== Correlation Analysis ===", flush=True)
print(f"Full 6mo SPY vs 10Y:        {full_corr:>+.4f}", flush=True)
print(f"Last 60 days SPY vs 10Y:    {mid_corr:>+.4f}", flush=True)
print(f"Last 30 days SPY vs 10Y:    {recent_corr:>+.4f}", flush=True)

# Beta: SPY daily return per 1% 10Y yield change
slope = np.polyfit(tnx_ret.values, spy_ret.values, 1)[0]
print(f"\nSPY daily beta to 10Y return: {slope:>.4f}", flush=True)
print(f"(i.e., 1% change in 10Y yield → {slope*100:>.2f}% change in SPY)", flush=True)

# Expected SPY moves for various 10Y spikes
current_10y = prices['^TNX']
for bp in [15, 20, 25, 30]:
    pct_yield_move = (bp / 100) / current_10y
    expected_spy_return = slope * pct_yield_move
    expected_spy_index = prices['SPY'] * (1 + expected_spy_return)
    print(f"\n{bp}bp 10Y spike ({bp/100:+.2%} abs): +{pct_yield_move*100:.2f}% yield return -> SPY {expected_spy_return*100:+.2f}% -> SPY ${expected_spy_index:.2f}", flush=True)

# Rolling 30d correlation history
spy_ret_series = spy_ret
tnx_ret_series = tnx_ret.loc[spy_ret_series.index]
rolling_corr_30d = spy_ret_series.rolling(30).corr(tnx_ret_series)
print(f"\n=== Rolling 30d SPY vs 10Y Correlation ===", flush=True)
print(f"Current (last datapoint): {rolling_corr_30d.iloc[-1]:>+.4f}", flush=True)
print(f"Max: {rolling_corr_30d.max():>+.4f}", flush=True)
print(f"Min: {rolling_corr_30d.min():>+.4f}", flush=True)
print(f"Mean: {rolling_corr_30d.mean():>+.4f}", flush=True)

# Now calculate individual stock betas to 10Y for the regression
# For each stock, regress its return on 10Y return
print(f"\n=== Individual Stock Betas to 10Y (30-day) ===", flush=True)
stock_betas = {}
for ticker in tickers['stocks'] + tickers['indices'] + tickers['sectors']:
    try:
        t_close = data['Close'][ticker].dropna()
        common = t_close.index.intersection(tnx_close.index)
        t_close_a = t_close.loc[common]
        tnx_a = tnx_close.loc[common]
        t_ret = t_close_a.pct_change().dropna()
        tnx_ret_a = tnx_a.pct_change().dropna()
        cr = t_ret.index.intersection(tnx_ret_a.index)
        t_ret = t_ret.loc[cr]
        tnx_r = tnx_ret_a.loc[cr]
        
        # last 30 days
        t_ret_30 = t_ret.iloc[-30:]
        tnx_r_30 = tnx_r.loc[t_ret_30.index]
        
        if len(t_ret_30) > 5:
            beta = np.polyfit(tnx_r_30.values, t_ret_30.values, 1)[0]
            stock_betas[ticker] = float(beta)
            print(f"{ticker:8s}: beta={beta:>+.4f}", flush=True)
    except Exception as e:
        print(f"{ticker:8s}: ERROR", flush=True)
        stock_betas[ticker] = None

# Save output for report
output = {
    'prices': {str(k): round(float(v), 2) if v else None for k, v in prices.items()},
    'high_52w': {str(k): round(float(v), 2) if v else None for k, v in high_52w.items()},
    'pct_of_52w': {str(k): round(float(v), 1) if v else None for k, v in pct_of_52w_high.items()},
    'current_10y': round(float(current_10y), 2),
    'corr_6mo': round(float(full_corr), 4),
    'corr_60d': round(float(mid_corr), 4),
    'corr_30d': round(float(recent_corr), 4),
    'spy_beta_to_10y': round(float(slope), 4),
    'betas': {str(k): round(float(v), 4) if v else None for k, v in stock_betas.items()},
}

with open('/home/ty/workspace/investment-research/scripts/market_data.json', 'w') as f:
    json.dump(output, f, indent=2)
print("\n\nData saved to market_data.json", flush=True)