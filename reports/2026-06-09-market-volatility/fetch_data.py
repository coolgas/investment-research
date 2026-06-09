#!/usr/bin/env python3
"""Fetch fresh market data for volatility-focused market report."""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date, timezone

# ── Tickers ──────────────────────────────────────────────────────────────
BROAD_TICKERS = ['SPY', 'QQQ', 'IWM', 'DIA']
SECTOR_TICKERS = ['XLF', 'XLU', 'XLRE', 'XLE', 'XLP', 'XLV', 'XLI', 'XLB', 'XLC', 'XLK', 'XLY']
RATES_TICKERS = ['^TNX', '^FVX', 'TLT']
FX_TICKERS = ['JPY=X', 'EURUSD=X', 'GBPUSD=X']
COMMODITY_TICKERS = ['GC=F', 'CL=F', 'SI=F']
VIX_TICKERS = ['^VIX']
INDIVIDUAL_TICKERS = ['AAPL', 'MSFT', 'NVDA', 'META', 'GOOGL', 'AMZN', 'JPM', 'GS', 'BAC', 'PLD', 'NEE', 'WMT']
DXY_TICKER = 'DX-Y.NYB'

ALL_TICKERS = BROAD_TICKERS + SECTOR_TICKERS + RATES_TICKERS + FX_TICKERS + COMMODITY_TICKERS + VIX_TICKERS + INDIVIDUAL_TICKERS

# ── Date Ranges ──────────────────────────────────────────────────────────
YTD_START = '2026-01-01'
POST_FOMC_START = '2026-04-29'
THIRTY_DAY_START = '2026-05-09'
FIVE_DAY_START = '2026-06-02'
END_DATE = '2026-06-09'
TODAY = date(2026, 6, 9)

# Timezone-aware stamps for comparison
YTD_START_TS = pd.Timestamp(YTD_START).tz_localize('America/New_York')
POST_FOMC_START_TS = pd.Timestamp(POST_FOMC_START).tz_localize('America/New_York')
THIRTY_DAY_START_TS = pd.Timestamp(THIRTY_DAY_START).tz_localize('America/New_York')
FIVE_DAY_START_TS = pd.Timestamp(FIVE_DAY_START).tz_localize('America/New_York')
END_DATE_TS = pd.Timestamp(END_DATE + ' 23:59:59').tz_localize('America/New_York')

# ── Helper Functions ─────────────────────────────────────────────────────
def pct_str(val):
    """Return formatted percentage string with span tags."""
    if pd.isna(val) or val is None:
        return '<span class="num">N/A</span>'
    sign = '+' if val >= 0 else ''
    css_class = 'up' if val >= 0 else 'down'
    return f'<span class="{css_class}">{sign}{val:.2f}%</span>'

def price_str(val):
    """Return formatted price string with span tag."""
    if pd.isna(val) or val is None:
        return '<span class="num">N/A</span>'
    return f'<span class="num">${val:.2f}</span>'

def compute_52wk_high_proximity(hist, latest_close):
    """Compute how close latest close is to 52-week high as percentage."""
    if hist.empty or latest_close is None:
        return None
    high_52 = hist['High'].max()
    if pd.isna(high_52) or high_52 == 0:
        return None
    return ((latest_close - high_52) / high_52) * 100

def compute_metrics(ticker_str, periods):
    """
    Fetch data and compute performance metrics for multiple periods.
    periods is a dict of {label: (start_ts, end_ts)}
    Returns dict with all metrics.
    """
    # Figure out earliest start
    all_start = min(s for s, e in periods.values())
    
    try:
        stock = yf.Ticker(ticker_str)
        hist = stock.history(start=all_start.strftime('%Y-%m-%d'), end=END_DATE)
        
        if hist.empty:
            print(f"WARNING: No data for {ticker_str}")
            return None
        
        # Convert timezone-aware index to consistent tz
        if hist.index.tz is not None:
            hist.index = hist.index.tz_convert('America/New_York')
        
        # Get latest close
        latest_close = hist['Close'].iloc[-1]
        
        results = {'latest_close': latest_close}
        
        # Compute returns for each period
        for label, (period_start, period_end) in periods.items():
            mask = (hist.index >= period_start) & (hist.index <= period_end)
            period_data = hist.loc[mask]
            if len(period_data) < 2:
                results[label] = None
            else:
                first_close = period_data['Close'].iloc[0]
                last_close = period_data['Close'].iloc[-1]
                results[label] = ((last_close - first_close) / first_close) * 100
        
        # 52-week high proximity (use data going back ~1 year)
        hist_52w = hist.tail(400)  # get enough data (~2 years of trading days)
        if len(hist_52w) > 0:
            high_52 = hist_52w['High'].max()
            if high_52 > 0:
                results['52wk_prox'] = ((latest_close - high_52) / high_52) * 100
            else:
                results['52wk_prox'] = None
        else:
            results['52wk_prox'] = None
        
        return results
        
    except Exception as e:
        print(f"ERROR fetching {ticker_str}: {e}")
        return None

# ── Main Execution ──────────────────────────────────────────────────────
# All periods use NY timezone-aware timestamps
periods = {
    'ytd': (YTD_START_TS, END_DATE_TS),
    'post_fomc': (POST_FOMC_START_TS, END_DATE_TS),
    '30d': (THIRTY_DAY_START_TS, END_DATE_TS),
    '5d': (FIVE_DAY_START_TS, END_DATE_TS),
}

# For the 52wk high, we need a longer history. Use 2025-06-09 as start.
FAR_START = pd.Timestamp('2025-06-09').tz_localize('America/New_York')

print("=" * 60)
print("FETCHING MARKET DATA FOR VOLATILITY REPORT")
print(f"Date: {TODAY}")
print("=" * 60)

# Dictionary to hold all ticker results
all_results = {}

for ticker in ALL_TICKERS:
    print(f"  Fetching {ticker}...")
    result = compute_metrics(ticker, periods)
    if result:
        all_results[ticker] = result
    else:
        print(f"  FAILED: {ticker}")

# Try DXY
print("  Fetching DX-Y.NYB (DXY)...")
dxy_result = compute_metrics(DXY_TICKER, periods)
if dxy_result:
    all_results['DXY'] = dxy_result
else:
    print("  DXY fetch failed.")

# ── SPY-10Y Daily Return Correlation ────────────────────────────────────
print("\nComputing SPY-10Y correlation...")

def get_spy_tnx_corr(spy_ticker='SPY', tnx_ticker='^TNX'):
    """Compute daily return correlation between SPY and ^TNX."""
    spy_stock = yf.Ticker(spy_ticker)
    tnx_stock = yf.Ticker(tnx_ticker)
    
    spy_hist = spy_stock.history(start='2025-06-09', end=END_DATE)
    tnx_hist = tnx_stock.history(start='2025-06-09', end=END_DATE)
    
    if spy_hist.empty or tnx_hist.empty:
        return None, None
    
    # Both use datetime64[s, America/New_York] after conversion
    spy_hist.index = spy_hist.index.tz_convert('America/New_York').normalize()
    tnx_hist.index = tnx_hist.index.tz_convert('America/New_York').normalize()
    
    spy_returns = spy_hist['Close'].pct_change().dropna()
    tnx_returns = tnx_hist['Close'].pct_change().dropna()
    
    # Merge on index - now both are NY tz so intersection works
    combined = pd.DataFrame({'spy': spy_returns, 'tnx': tnx_returns}).dropna()
    
    YTD_START_TS = pd.Timestamp('2026-01-01').tz_localize('America/New_York')
    POST_FOMC_START_TS = pd.Timestamp('2026-04-29').tz_localize('America/New_York')
    END_DATE_TS = pd.Timestamp('2026-06-09 23:59:59').tz_localize('America/New_York')
    
    def period_corr(start_ts, end_ts):
        mask = (combined.index >= start_ts) & (combined.index <= end_ts)
        subset = combined.loc[mask]
        if len(subset) < 5:
            return None
        return subset['spy'].corr(subset['tnx'])
    
    corr_ytd = period_corr(YTD_START_TS, END_DATE_TS)
    corr_pf = period_corr(POST_FOMC_START_TS, END_DATE_TS)
    
    return corr_ytd, corr_pf

corr_ytd, corr_pf = get_spy_tnx_corr()
if corr_ytd is not None:
    print(f"  SPY-^TNX YTD correlation: {corr_ytd:.4f}")
else:
    print("  SPY-^TNX YTD correlation: N/A")
if corr_pf is not None:
    print(f"  SPY-^TNX Post-FOMC correlation: {corr_pf:.4f}")
else:
    print("  SPY-^TNX Post-FOMC correlation: N/A")

# ── VIX Levels and Trends ───────────────────────────────────────────────
print("\nComputing VIX levels and trends...")
vix_stock = yf.Ticker('^VIX')
vix_hist = vix_stock.history(start='2025-06-09', end=END_DATE)

if not vix_hist.empty:
    if vix_hist.index.tz is not None:
        vix_hist.index = vix_hist.index.tz_convert('America/New_York')
    
    vix_latest = vix_hist['Close'].iloc[-1]
    
    vix_30d = vix_hist.loc[(vix_hist.index >= THIRTY_DAY_START_TS) & (vix_hist.index <= END_DATE_TS)]
    vix_30d_mean = vix_30d['Close'].mean()
    vix_30d_std = vix_30d['Close'].std()
    vix_30d_min = vix_30d['Close'].min()
    vix_30d_max = vix_30d['Close'].max()
    vix_30d_change = ((vix_latest - vix_30d['Close'].iloc[0]) / vix_30d['Close'].iloc[0]) * 100 if len(vix_30d) >= 2 else None
    
    vix_5d = vix_hist.loc[(vix_hist.index >= FIVE_DAY_START_TS) & (vix_hist.index <= END_DATE_TS)]
    vix_5d_change = ((vix_latest - vix_5d['Close'].iloc[0]) / vix_5d['Close'].iloc[0]) * 100 if len(vix_5d) >= 2 else None
    
    # YTD VIX
    vix_ytd = vix_hist.loc[(vix_hist.index >= YTD_START_TS) & (vix_hist.index <= END_DATE_TS)]
    vix_ytd_change = ((vix_latest - vix_ytd['Close'].iloc[0]) / vix_ytd['Close'].iloc[0]) * 100 if len(vix_ytd) >= 2 else None
    
    # Post-FOMC VIX
    vix_pf = vix_hist.loc[(vix_hist.index >= POST_FOMC_START_TS) & (vix_hist.index <= END_DATE_TS)]
    vix_pf_change = ((vix_latest - vix_pf['Close'].iloc[0]) / vix_pf['Close'].iloc[0]) * 100 if len(vix_pf) >= 2 else None
    
    # 52-wk high
    vix_52w_high = vix_hist['High'].max()
    vix_52w_prox = ((vix_latest - vix_52w_high) / vix_52w_high) * 100 if vix_52w_high > 0 else None
    
    print(f"  VIX Latest: {vix_latest:.2f}")
    print(f"  VIX 30d Mean: {vix_30d_mean:.2f}, Std: {vix_30d_std:.2f}")
else:
    vix_latest = vix_30d_mean = vix_30d_std = vix_30d_min = vix_30d_max = None
    vix_30d_change = vix_5d_change = vix_ytd_change = vix_pf_change = vix_52w_prox = None
    print("  No VIX data available")

# ── Sector Rotation: Pre-FOMC vs Post-FOMC ──────────────────────────────
print("\nComputing sector rotation...")
# Pre-FOMC: YTD_START to day before POST_FOMC_START
PRE_FOMC_END = pd.Timestamp('2026-04-28').tz_localize('America/New_York')
PRE_FOMC_START = YTD_START_TS

sector_pre_fomc = {}
sector_post_fomc = {}

for ticker in SECTOR_TICKERS:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start='2025-06-09', end=END_DATE)
        if hist.empty:
            continue
        if hist.index.tz is not None:
            hist.index = hist.index.tz_convert('America/New_York')
        
        # Pre-FOMC
        pre_mask = (hist.index >= PRE_FOMC_START) & (hist.index <= PRE_FOMC_END)
        pre_data = hist.loc[pre_mask]
        if len(pre_data) >= 2:
            pre_return = ((pre_data['Close'].iloc[-1] - pre_data['Close'].iloc[0]) / pre_data['Close'].iloc[0]) * 100
        else:
            pre_return = None
        
        # Post-FOMC
        post_mask = (hist.index >= POST_FOMC_START_TS) & (hist.index <= END_DATE_TS)
        post_data = hist.loc[post_mask]
        if len(post_data) >= 2:
            post_return = ((post_data['Close'].iloc[-1] - post_data['Close'].iloc[0]) / post_data['Close'].iloc[0]) * 100
        else:
            post_return = None
        
        sector_pre_fomc[ticker] = pre_return
        sector_post_fomc[ticker] = post_return
        
    except Exception as e:
        print(f"  Error with {ticker}: {e}")

# ── Currency Heatmap ────────────────────────────────────────────────────
print("\nComputing currency heatmap...")
currency_metrics = {}
for ticker in FX_TICKERS:
    result = compute_metrics(ticker, periods)
    if result:
        currency_metrics[ticker] = result

# Also try DXY
dxy_cm = compute_metrics(DXY_TICKER, periods)
if dxy_cm:
    currency_metrics['DXY'] = dxy_cm

# ── Generate Report ─────────────────────────────────────────────────────
print("\nGenerating report...")

lines = []
lines.append("# Market Data Refresh")
lines.append("")
lines.append(f"**Report Date:** {TODAY}")
lines.append("")
lines.append(f"**Data Source:** Yahoo Finance (yfinance)")
lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Broad Market Indices")
lines.append("")
lines.append(f"Performance from {YTD_START} to {END_DATE} (YTD), {POST_FOMC_START} to {END_DATE} (Post-FOMC), {THIRTY_DAY_START} to {END_DATE} (30d), {FIVE_DAY_START} to {END_DATE} (5d)")
lines.append("")
lines.append("| Ticker | Latest Close | YTD % | Post-FOMC % | 30d % | 5d % | 52-Week High Proximity |")
lines.append("|--------|-------------|-------|-------------|-------|------|----------------------|")

for ticker in BROAD_TICKERS:
    r = all_results.get(ticker)
    if r:
        lc = price_str(r['latest_close'])
        ytd = pct_str(r['ytd'])
        pf = pct_str(r['post_fomc'])
        td = pct_str(r['30d'])
        fd = pct_str(r['5d'])
        prox = pct_str(r['52wk_prox'])
        lines.append(f"| {ticker} | {lc} | {ytd} | {pf} | {td} | {fd} | {prox} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## Sector ETFs")
lines.append("")
lines.append(f"Performance from {YTD_START} to {END_DATE} (YTD), {POST_FOMC_START} to {END_DATE} (Post-FOMC), {THIRTY_DAY_START} to {END_DATE} (30d), {FIVE_DAY_START} to {END_DATE} (5d)")
lines.append("")
lines.append("| Ticker | Latest Close | YTD % | Post-FOMC % | 30d % | 5d % | 52-Week High Proximity |")
lines.append("|--------|-------------|-------|-------------|-------|------|----------------------|")

for ticker in SECTOR_TICKERS:
    r = all_results.get(ticker)
    if r:
        lc = price_str(r['latest_close'])
        ytd = pct_str(r['ytd'])
        pf = pct_str(r['post_fomc'])
        td = pct_str(r['30d'])
        fd = pct_str(r['5d'])
        prox = pct_str(r['52wk_prox'])
        lines.append(f"| {ticker} | {lc} | {ytd} | {pf} | {td} | {fd} | {prox} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## Interest Rates")
lines.append("")
lines.append(f"Performance from {YTD_START} to {END_DATE} (YTD), {POST_FOMC_START} to {END_DATE} (Post-FOMC), {THIRTY_DAY_START} to {END_DATE} (30d), {FIVE_DAY_START} to {END_DATE} (5d)")
lines.append("")
lines.append("| Ticker | Latest Close | YTD % | Post-FOMC % | 30d % | 5d % | 52-Week High Proximity |")
lines.append("|--------|-------------|-------|-------------|-------|------|----------------------|")

for ticker in RATES_TICKERS:
    r = all_results.get(ticker)
    if r:
        lc = price_str(r['latest_close'])
        ytd = pct_str(r['ytd'])
        pf = pct_str(r['post_fomc'])
        td = pct_str(r['30d'])
        fd = pct_str(r['5d'])
        prox = pct_str(r['52wk_prox'])
        lines.append(f"| {ticker} | {lc} | {ytd} | {pf} | {td} | {fd} | {prox} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## Foreign Exchange")
lines.append("")
lines.append(f"Performance from {YTD_START} to {END_DATE} (YTD), {POST_FOMC_START} to {END_DATE} (Post-FOMC), {THIRTY_DAY_START} to {END_DATE} (30d), {FIVE_DAY_START} to {END_DATE} (5d)")
lines.append("")
lines.append("| Ticker | Latest Close | YTD % | Post-FOMC % | 30d % | 5d % | 52-Week High Proximity |")
lines.append("|--------|-------------|-------|-------------|-------|------|----------------------|")

for label, r in currency_metrics.items():
    if r:
        lc = price_str(r['latest_close'])
        ytd = pct_str(r['ytd'])
        pf = pct_str(r['post_fomc'])
        td = pct_str(r['30d'])
        fd = pct_str(r['5d'])
        prox = pct_str(r['52wk_prox'])
        name = label.replace('=X', '')
        lines.append(f"| {name} | {lc} | {ytd} | {pf} | {td} | {fd} | {prox} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## Commodities")
lines.append("")
lines.append(f"Performance from {YTD_START} to {END_DATE} (YTD), {POST_FOMC_START} to {END_DATE} (Post-FOMC), {THIRTY_DAY_START} to {END_DATE} (30d), {FIVE_DAY_START} to {END_DATE} (5d)")
lines.append("")
lines.append("| Ticker | Latest Close | YTD % | Post-FOMC % | 30d % | 5d % | 52-Week High Proximity |")
lines.append("|--------|-------------|-------|-------------|-------|------|----------------------|")

for ticker in COMMODITY_TICKERS:
    r = all_results.get(ticker)
    if r:
        lc = price_str(r['latest_close'])
        ytd = pct_str(r['ytd'])
        pf = pct_str(r['post_fomc'])
        td = pct_str(r['30d'])
        fd = pct_str(r['5d'])
        prox = pct_str(r['52wk_prox'])
        lines.append(f"| {ticker} | {lc} | {ytd} | {pf} | {td} | {fd} | {prox} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## VIX (CBOE Volatility Index)")
lines.append("")
lines.append(f"Performance from {YTD_START} to {END_DATE} (YTD), {POST_FOMC_START} to {END_DATE} (Post-FOMC), {THIRTY_DAY_START} to {END_DATE} (30d), {FIVE_DAY_START} to {END_DATE} (5d)")
lines.append("")
lines.append("| Ticker | Latest Close | YTD % | Post-FOMC % | 30d % | 5d % | 52-Week High Proximity |")
lines.append("|--------|-------------|-------|-------------|-------|------|----------------------|")

for ticker in VIX_TICKERS:
    r = all_results.get(ticker)
    if r:
        lc = price_str(r['latest_close'])
        ytd = pct_str(r['ytd'])
        pf = pct_str(r['post_fomc'])
        td = pct_str(r['30d'])
        fd = pct_str(r['5d'])
        prox = pct_str(r['52wk_prox'])
        lines.append(f"| {ticker} | {lc} | {ytd} | {pf} | {td} | {fd} | {prox} |")

lines.append("")
lines.append("### VIX Trend Analysis")
lines.append("")
if vix_latest is not None:
    lines.append(f"- **Current VIX:** {price_str(vix_latest)}")
    if vix_30d_mean is not None:
        lines.append(f"- **30-Day Mean (2026-05-09 to 2026-06-09):** {price_str(vix_30d_mean)}")
    if vix_30d_std is not None:
        lines.append(f"- **30-Day Std Dev:** {price_str(vix_30d_std)}")
    if vix_30d_min is not None and vix_30d_max is not None:
        lines.append(f"- **30-Day Range:** {price_str(vix_30d_min)} - {price_str(vix_30d_max)}")
    if vix_30d_change is not None:
        lines.append(f"- **30-Day Change:** {pct_str(vix_30d_change)}")
    if vix_5d_change is not None:
        lines.append(f"- **5-Day Change:** {pct_str(vix_5d_change)}")
    
    # Trend assessment
    if vix_5d_change is not None and vix_30d_change is not None:
        if vix_5d_change > 5 and vix_30d_change > 5:
            trend = "VIX is rising sharply in both the short and medium term -- elevated fear/uncertainty."
        elif vix_5d_change < -5 and vix_30d_change < -5:
            trend = "VIX is declining sharply in both the short and medium term -- improving sentiment."
        elif vix_5d_change > 0 and vix_30d_change < 0:
            trend = "VIX is rising in the short term but lower over the medium term -- recent volatility spike."
        elif vix_5d_change < 0 and vix_30d_change > 0:
            trend = "VIX is declining in the short term but elevated over the medium term -- settling after a volatile period."
        else:
            trend = "VIX showing moderate directional movement."
        lines.append(f"- **Trend Assessment:** {trend}")
    
    if vix_latest < 15:
        lines.append(f"- **Volatility Regime:** Low (VIX < 15) -- complacent market environment.")
    elif vix_latest < 20:
        lines.append(f"- **Volatility Regime:** Moderate (VIX 15-20) -- normal market conditions.")
    elif vix_latest < 25:
        lines.append(f"- **Volatility Regime:** Elevated (VIX 20-25) -- increased uncertainty.")
    elif vix_latest < 30:
        lines.append(f"- **Volatility Regime:** High (VIX 25-30) -- significant stress.")
    else:
        lines.append(f"- **Volatility Regime:** Extreme (VIX > 30) -- crisis-level fear.")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## Individual Stocks")
lines.append("")
lines.append(f"Performance from {YTD_START} to {END_DATE} (YTD), {POST_FOMC_START} to {END_DATE} (Post-FOMC), {THIRTY_DAY_START} to {END_DATE} (30d), {FIVE_DAY_START} to {END_DATE} (5d)")
lines.append("")
lines.append("| Ticker | Latest Close | YTD % | Post-FOMC % | 30d % | 5d % | 52-Week High Proximity |")
lines.append("|--------|-------------|-------|-------------|-------|------|----------------------|")

for ticker in INDIVIDUAL_TICKERS:
    r = all_results.get(ticker)
    if r:
        lc = price_str(r['latest_close'])
        ytd = pct_str(r['ytd'])
        pf = pct_str(r['post_fomc'])
        td = pct_str(r['30d'])
        fd = pct_str(r['5d'])
        prox = pct_str(r['52wk_prox'])
        lines.append(f"| {ticker} | {lc} | {ytd} | {pf} | {td} | {fd} | {prox} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## SPY-10Y Treasury Yield Correlation")
lines.append("")
lines.append("Daily return correlation between SPY (S&P 500 ETF) and ^TNX (10-Year Treasury Yield)")
lines.append("")
lines.append("| Period | Date Range | Correlation | Interpretation |")
lines.append("|--------|-----------|------------|---------------|")
if corr_ytd is not None:
    interp_ytd = "Stocks and bonds moving together (risk-on/risk-off regime)" if corr_ytd > 0 else "Stocks and bonds diverging (rotation into/out of bonds)"
    lines.append(f"| YTD | {YTD_START} to {END_DATE} | {corr_ytd:.4f} | {interp_ytd} |")
else:
    lines.append(f"| YTD | {YTD_START} to {END_DATE} | N/A | Insufficient data |")
if corr_pf is not None:
    interp_pf = "Stocks and bonds moving together (risk-on/risk-off regime)" if corr_pf > 0 else "Stocks and bonds diverging (rotation into/out of bonds)"
    lines.append(f"| Post-FOMC | {POST_FOMC_START} to {END_DATE} | {corr_pf:.4f} | {interp_pf} |")
else:
    lines.append(f"| Post-FOMC | {POST_FOMC_START} to {END_DATE} | N/A | Insufficient data |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## Sector Rotation: Pre-FOMC vs Post-FOMC")
lines.append("")
lines.append("Comparing sector performance in the pre-FOMC period (2026-01-01 to 2026-04-28) vs post-FOMC period (2026-04-29 to 2026-06-09)")
lines.append("")
lines.append("| Sector | Ticker | Pre-FOMC % | Post-FOMC % | Rotation Delta |")
lines.append("|--------|--------|-----------|------------|---------------|")

sector_names = {
    'XLF': 'Financials', 'XLU': 'Utilities', 'XLRE': 'Real Estate',
    'XLE': 'Energy', 'XLP': 'Consumer Staples', 'XLV': 'Health Care',
    'XLI': 'Industrials', 'XLB': 'Materials', 'XLC': 'Communication Services',
    'XLK': 'Technology', 'XLY': 'Consumer Discretionary'
}

for ticker in SECTOR_TICKERS:
    pre = sector_pre_fomc.get(ticker)
    post = sector_post_fomc.get(ticker)
    if pre is not None and post is not None:
        delta = post - pre
        pre_s = pct_str(pre)
        post_s = pct_str(post)
        delta_s = pct_str(delta)
        name = sector_names.get(ticker, ticker)
        lines.append(f"| {name} | {ticker} | {pre_s} | {post_s} | {delta_s} |")

lines.append("")
lines.append("### Rotation Observations")
lines.append("")

pf_sorted = sorted([(t, sector_post_fomc[t]) for t in SECTOR_TICKERS if t in sector_post_fomc and sector_post_fomc[t] is not None], key=lambda x: x[1], reverse=True)
pre_sorted = sorted([(t, sector_pre_fomc[t]) for t in SECTOR_TICKERS if t in sector_pre_fomc and sector_pre_fomc[t] is not None], key=lambda x: x[1], reverse=True)

if pf_sorted:
    best_pf = sector_names.get(pf_sorted[0][0], pf_sorted[0][0])
    worst_pf = sector_names.get(pf_sorted[-1][0], pf_sorted[-1][0])
    lines.append(f"- **Best post-FOMC sector:** {best_pf} ({pct_str(pf_sorted[0][1])})")
    lines.append(f"- **Worst post-FOMC sector:** {worst_pf} ({pct_str(pf_sorted[-1][1])})")

if pre_sorted:
    best_pre = sector_names.get(pre_sorted[0][0], pre_sorted[0][0])
    worst_pre = sector_names.get(pre_sorted[-1][0], pre_sorted[-1][0])
    lines.append(f"- **Best pre-FOMC sector:** {best_pre} ({pct_str(pre_sorted[0][1])})")
    lines.append(f"- **Worst pre-FOMC sector:** {worst_pre} ({pct_str(pre_sorted[-1][1])})")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## Currency Heatmap")
lines.append("")
lines.append(f"Performance from {YTD_START} to {END_DATE} (YTD), {POST_FOMC_START} to {END_DATE} (Post-FOMC), {THIRTY_DAY_START} to {END_DATE} (30d), {FIVE_DAY_START} to {END_DATE} (5d)")
lines.append("")
lines.append("| Currency | Latest Close | YTD % | Post-FOMC % | 30d % | 5d % | 52-Week High Proximity |")
lines.append("|----------|-------------|-------|-------------|-------|------|----------------------|")

for label, r in currency_metrics.items():
    if r:
        lc = price_str(r['latest_close'])
        ytd = pct_str(r['ytd'])
        pf = pct_str(r['post_fomc'])
        td = pct_str(r['30d'])
        fd = pct_str(r['5d'])
        prox = pct_str(r['52wk_prox'])
        name = label.replace('=X', '')
        lines.append(f"| {name} | {lc} | {ytd} | {pf} | {td} | {fd} | {prox} |")

lines.append("")
lines.append("### USD Strength Assessment")
lines.append("")

dxy_r = currency_metrics.get('DXY')
if dxy_r and dxy_r['ytd'] is not None:
    if dxy_r['ytd'] > 3:
        usd_assessment = "USD is significantly stronger YTD -- broad dollar strength pressuring FX pairs."
    elif dxy_r['ytd'] > 1:
        usd_assessment = "USD is moderately stronger YTD -- mild dollar strength."
    elif dxy_r['ytd'] > -1:
        usd_assessment = "USD is roughly flat YTD -- no clear directional trend."
    elif dxy_r['ytd'] > -3:
        usd_assessment = "USD is moderately weaker YTD -- mild dollar weakness supporting FX pairs."
    else:
        usd_assessment = "USD is significantly weaker YTD -- broad dollar weakness."
    lines.append(f"- DXY YTD change: {pct_str(dxy_r['ytd'])}")
    lines.append(f"- Assessment: {usd_assessment}")

# JPY
jpy_r = currency_metrics.get('JPY=X')
if jpy_r and jpy_r['ytd'] is not None:
    lines.append(f"- JPY/USD YTD: {pct_str(jpy_r['ytd'])} -- {'JPY weakening' if jpy_r['ytd'] > 0 else 'JPY strengthening'} vs USD")

# EUR
eur_r = currency_metrics.get('EURUSD=X')
if eur_r and eur_r['ytd'] is not None:
    lines.append(f"- EUR/USD YTD: {pct_str(eur_r['ytd'])} -- {'EUR strengthening' if eur_r['ytd'] > 0 else 'EUR weakening'} vs USD")

# GBP
gbp_r = currency_metrics.get('GBPUSD=X')
if gbp_r and gbp_r['ytd'] is not None:
    lines.append(f"- GBP/USD YTD: {pct_str(gbp_r['ytd'])} -- {'GBP strengthening' if gbp_r['ytd'] > 0 else 'GBP weakening'} vs USD")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## Data Quality Notes")
lines.append("")
lines.append("- All data sourced from Yahoo Finance via yfinance.")
lines.append(f"- Report date: {TODAY}. All period returns use the exact date ranges specified.")
lines.append("- 52-Week High Proximity shows percentage distance from the 52-week high (negative means below high, positive would mean new high).")
lines.append("- Timezone-aware datetime comparisons were used to ensure correct date range filtering.")
lines.append("")

# Write the file
output_file = '/root/workspace/investment-research/reports/2026-06-09-market-volatility/data-refresh.md'
with open(output_file, 'w') as f:
    f.write('\n'.join(lines))

print(f"\nReport written to {output_file}")
print(f"Total lines: {len(lines)}")
print("DONE.")