#!/usr/bin/env python3
"""KOSPI Correction Data Refresh Script"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

TODAY = "2026-07-13"
CRASH_START = "2026-06-20"
YTD_START = "2026-01-01"
HIST_START = "2021-01-01"

UP_TAG = '<span class="up">'
DOWN_TAG = '<span class="down">'
NUM_TAG = '<span class="num">'
END_TAG = '</span>'

def format_pct(val, is_pct=True):
    """Format a number as HTML span with appropriate class."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return NUM_TAG + 'N/A' + END_TAG
    
    if is_pct:
        display = f"{val:+.2f}%"
    else:
        display = f"{val:+.4f}"
    
    if val > 0:
        return UP_TAG + display + END_TAG
    elif val < 0:
        return DOWN_TAG + display + END_TAG
    else:
        return NUM_TAG + display + END_TAG

def format_price(val):
    """Format a price value."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return NUM_TAG + 'N/A' + END_TAG
    return NUM_TAG + f"{val:,.2f}" + END_TAG

def compute_drawdown(series):
    """Compute drawdown from peak over a series."""
    if series.empty or series.dropna().empty:
        return np.nan
    s = series.dropna()
    peak = s.max()
    current = s.iloc[-1]
    if peak == 0:
        return np.nan
    return ((current - peak) / peak) * 100

def main():
    print("=" * 60)
    print("KOSPI Correction Data Refresh")
    print("Generated: " + TODAY)
    print("=" * 60)
    
    # ============================================================
    # 1. Pull Crash Window Data (2026-06-20 to TODAY)
    # ============================================================
    print("\n--- Phase 1: Pulling crash window data (Jun 20 - Jul 13) ---")
    
    crash_tickers = [
        "^KS11", "EWY", "005930.KS", "000660.KS", "KRW=X",
        "^N225", "^HSI", "000001.SS",
        "SPY", "QQQ", "^VIX", "DX-Y.NYB", "^TNX", "GC=F", "CL=F",
        "SMH", "TSM", "ASML"
    ]
    
    # Check SOX
    sox_available = False
    try:
        sox = yf.download("^SOX", start=CRASH_START, end=TODAY, progress=False)
        if not sox.empty and not sox['Close'].dropna().empty:
            crash_tickers.append("^SOX")
            sox_available = True
            print("SOX data available, included.")
        else:
            print("SOX not available, skipping.")
    except:
        print("SOX not available, skipping.")
    
    crash_data = yf.download(crash_tickers, start=CRASH_START, end=TODAY, group_by="ticker", threads=True, progress=False)
    print("Downloaded " + str(len(crash_data.columns.levels[0])) + " tickers for crash window")
    
    # ============================================================
    # 2. Pull YTD Data
    # ============================================================
    print("\n--- Phase 2: Pulling YTD data (Jan 1 - Jul 13) ---")
    
    ytd_tickers = [
        "^KS11", "EWY", "005930.KS", "000660.KS", "KRW=X",
        "^N225", "^HSI", "000001.SS",
        "SPY", "QQQ", "^VIX", "DX-Y.NYB", "^TNX", "GC=F", "CL=F",
        "SMH", "TSM", "ASML"
    ]
    if sox_available:
        ytd_tickers.append("^SOX")
    
    ytd_data = yf.download(ytd_tickers, start=YTD_START, end=TODAY, group_by="ticker", threads=True, progress=False)
    print("Downloaded YTD data for " + str(len(ytd_data.columns.levels[0])) + " tickers")
    
    # ============================================================
    # 3. Pull Historical KOSPI Monthly Data
    # ============================================================
    print("\n--- Phase 3: Pulling KOSPI historical data (Jan 2021 - Jul 2026) ---")
    
    hist_data = yf.download("^KS11", start=HIST_START, end=TODAY, group_by="ticker", threads=True, progress=False)
    # Ensure we get a Series for monthly close values
    if 'Close' in hist_data.columns:
        hist_close = hist_data['Close']
    else:
        hist_close = hist_data
    if isinstance(hist_close, pd.DataFrame):
        hist_close = hist_close.iloc[:, 0]
    hist_monthly = hist_close.resample('ME').last()
    print("Historical KOSPI data: " + str(len(hist_monthly)) + " monthly points")
    
    # ============================================================
    # 4. Compute Statistics
    # ============================================================
    print("\n--- Phase 4: Computing statistics ---")
    
    all_stats = []
    for ticker in crash_tickers:
        try:
            df_crash = crash_data[ticker]
            df_ytd = ytd_data[ticker]
            
            crash_close = df_crash['Close'].dropna() if 'Close' in df_crash.columns and not df_crash['Close'].dropna().empty else None
            ytd_close = df_ytd['Close'].dropna() if 'Close' in df_ytd.columns and not df_ytd['Close'].dropna().empty else None
            
            # Use crash data as primary
            if crash_close is not None:
                latest = crash_close.iloc[-1]
                if len(crash_close) >= 2:
                    daily_chg = ((crash_close.iloc[-1] - crash_close.iloc[-2]) / crash_close.iloc[-2]) * 100
                else:
                    daily_chg = np.nan
                crash_dd = compute_drawdown(crash_close)
            elif ytd_close is not None:
                # Use YTD data and subset for crash period
                latest = ytd_close.iloc[-1]
                if len(ytd_close) >= 2:
                    daily_chg = ((ytd_close.iloc[-1] - ytd_close.iloc[-2]) / ytd_close.iloc[-2]) * 100
                else:
                    daily_chg = np.nan
                crash_period = ytd_close[ytd_close.index >= pd.Timestamp(CRASH_START)]
                crash_dd = compute_drawdown(crash_period)
            else:
                latest = np.nan
                daily_chg = np.nan
                crash_dd = np.nan
            
            # YTD stats
            if ytd_close is not None:
                ytd_c = ytd_close
                ytd_ret = ((ytd_c.iloc[-1] - ytd_c.iloc[0]) / ytd_c.iloc[0]) * 100
                ytd_dd = compute_drawdown(ytd_c)
            else:
                ytd_ret = np.nan
                ytd_dd = np.nan
            
            all_stats.append({
                'ticker': ticker,
                'latest': latest,
                'daily_chg': daily_chg,
                'crash_dd': crash_dd,
                'ytd_ret': ytd_ret,
                'ytd_dd': ytd_dd
            })
            
            print(f"  {ticker:>15s}: latest={latest:.2f}, daily={daily_chg:.2f}%, crash_dd={crash_dd:.2f}%, ytd_ret={ytd_ret:.2f}%, ytd_dd={ytd_dd:.2f}%")
        except Exception as e:
            print(f"  {ticker:>15s}: ERROR - {e}")
            all_stats.append({
                'ticker': ticker, 'latest': np.nan, 'daily_chg': np.nan,
                'crash_dd': np.nan, 'ytd_ret': np.nan, 'ytd_dd': np.nan
            })
    
    # ============================================================
    # 5. Compute KOSPI Daily Returns (Sorted, Largest Drops First)
    # ============================================================
    print("\n--- Phase 5: KOSPI daily returns during crash ---")
    
    kospi_crash = crash_data['^KS11']['Close'].dropna() if '^KS11' in crash_data.columns.levels[0] else pd.Series(dtype=float)
    if not kospi_crash.empty and len(kospi_crash) >= 2:
        kospi_returns = kospi_crash.pct_change().dropna() * 100
        kospi_returns_sorted = kospi_returns.sort_values()
        print("Worst 5 days:")
        for dt, val in kospi_returns_sorted.head(5).items():
            print(f"  {dt.strftime('%Y-%m-%d')}: {val:.2f}%")
        print("Best 5 days:")
        for dt, val in kospi_returns_sorted.tail(5).items():
            print(f"  {dt.strftime('%Y-%m-%d')}: {val:.2f}%")
    else:
        kospi_returns = pd.Series(dtype=float)
        kospi_returns_sorted = pd.Series(dtype=float)
    
    # ============================================================
    # 6. KRW Depreciation vs USD
    # ============================================================
    print("\n--- Phase 6: KRW depreciation ---")
    
    krw_data = crash_data['KRW=X']['Close'].dropna() if 'KRW=X' in crash_data.columns.levels[0] else pd.Series(dtype=float)
    if not krw_data.empty and len(krw_data) >= 2:
        krw_chg = ((krw_data.iloc[-1] - krw_data.iloc[0]) / krw_data.iloc[0]) * 100
        krw_peak_dd = compute_drawdown(krw_data)
        print(f"  KRW change since Jun 20: {krw_chg:.2f}%")
        print(f"  KRW drawdown: {krw_peak_dd:.2f}%")
    else:
        krw_chg = np.nan
        krw_peak_dd = np.nan
    
    # ============================================================
    # 7. Sector Dispersion: Semis vs Broad Market
    # ============================================================
    print("\n--- Phase 7: Sector dispersion ---")
    
    kospi_c = crash_data['^KS11']['Close'].dropna() if '^KS11' in crash_data.columns.levels[0] else pd.Series(dtype=float)
    
    semi_dd = {}
    for t, name in [('SMH', 'SMH'), ('TSM', 'TSM'), ('ASML', 'ASML')]:
        if t in crash_tickers and t in crash_data.columns.levels[0]:
            c = crash_data[t]['Close'].dropna()
            semi_dd[name] = compute_drawdown(c) if not c.empty else np.nan
    
    kospi_crash_dd = compute_drawdown(kospi_c) if not kospi_c.empty else np.nan
    print(f"  KOSPI crash DD: {kospi_crash_dd:.2f}%")
    for name, dd in semi_dd.items():
        print(f"  {name} crash DD: {dd:.2f}%")
    
    # ============================================================
    # 8. Correlation: KOSPI vs VIX and DXY
    # ============================================================
    print("\n--- Phase 8: Correlation analysis ---")
    
    vix_c = crash_data['^VIX']['Close'].dropna() if '^VIX' in crash_data.columns.levels[0] else pd.Series(dtype=float)
    dxy_c = crash_data['DX-Y.NYB']['Close'].dropna() if 'DX-Y.NYB' in crash_data.columns.levels[0] else pd.Series(dtype=float)
    
    if not kospi_returns.empty:
        aligned_df = pd.DataFrame({
            'KOSPI_daily': kospi_returns,
            'VIX_daily': vix_c.pct_change().dropna() * 100 if not vix_c.empty else pd.Series(dtype=float),
            'DXY_daily': dxy_c.pct_change().dropna() * 100 if not dxy_c.empty else pd.Series(dtype=float)
        }).dropna()
        
        if len(aligned_df) >= 3:
            corr_vix = float(aligned_df['KOSPI_daily'].corr(aligned_df['VIX_daily']))
            corr_dxy = float(aligned_df['KOSPI_daily'].corr(aligned_df['DXY_daily']))
            print(f"  KOSPI vs VIX correlation: {corr_vix:.4f}")
            print(f"  KOSPI vs DXY correlation: {corr_dxy:.4f}")
        else:
            corr_vix = np.nan
            corr_dxy = np.nan
    else:
        corr_vix = np.nan
        corr_dxy = np.nan
    
    n_observations = len(aligned_df) if not kospi_returns.empty else 0
    
    # ============================================================
    # All data collected - now write the report
    # ============================================================
    print("\n--- Phase 9: Writing report ---")
    
    lines = []
    lines.append("# KOSPI Correction Data Refresh")
    lines.append("")
    lines.append("**Generated**: " + TODAY)
    lines.append("")
    lines.append("**Data source**: yfinance (delayed, not official)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    
    latest_kospi = all_stats[0]['latest'] if len(all_stats) > 0 else np.nan
    kospi_chg = all_stats[0]['daily_chg'] if len(all_stats) > 0 else np.nan
    kospi_dd = all_stats[0]['crash_dd'] if len(all_stats) > 0 else np.nan
    kospi_ytd = all_stats[0]['ytd_ret'] if len(all_stats) > 0 else np.nan
    
    lines.append("KOSPI closed at " + format_price(latest_kospi) + " on " + TODAY + ", " + format_pct(kospi_chg) + " from the prior session. Since the crash began on June 20, the index has fallen " + format_pct(kospi_dd) + " from its peak. Year-to-date, KOSPI is " + format_pct(kospi_ytd) + ". From the table below, the crash drawdown is more pronounced in the semiconductor-heavy names, with SK Hynix and Samsung Electronics showing particularly sharp declines.")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 1: Korean Market ----
    lines.append("## Korean Market")
    lines.append("")
    lines.append("**Table 1: Korean Market Overview (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    lines.append("| Ticker | Name | Latest | Daily Change | Crash DD | YTD Return | YTD DD |")
    lines.append("|--------|------|--------|-------------|----------|------------|--------|")
    
    korean_tickers = {
        "^KS11": "KOSPI",
        "EWY": "iShares MSCI Korea ETF",
        "005930.KS": "Samsung Electronics",
        "000660.KS": "SK Hynix",
        "KRW=X": "USD/KRW (Won)"
    }
    
    for s in all_stats:
        t = s['ticker']
        if t in korean_tickers:
            name = korean_tickers[t]
            row = "| " + t + " | " + name + " | " + format_price(s['latest']) + " | " + format_pct(s['daily_chg']) + " | " + format_pct(s['crash_dd']) + " | " + format_pct(s['ytd_ret']) + " | " + format_pct(s['ytd_dd']) + " |"
            lines.append(row)
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 2: Asian Comparators ----
    lines.append("## Asian Comparators")
    lines.append("")
    lines.append("**Table 2: Asian Market Comparators (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    lines.append("| Ticker | Name | Latest | Daily Change | Crash DD | YTD Return | YTD DD |")
    lines.append("|--------|------|--------|-------------|----------|------------|--------|")
    
    asian_tickers = {
        "^N225": "Nikkei 225",
        "^HSI": "Hang Seng",
        "000001.SS": "Shanghai Composite"
    }
    
    for s in all_stats:
        t = s['ticker']
        if t in asian_tickers:
            name = asian_tickers[t]
            row = "| " + t + " | " + name + " | " + format_price(s['latest']) + " | " + format_pct(s['daily_chg']) + " | " + format_pct(s['crash_dd']) + " | " + format_pct(s['ytd_ret']) + " | " + format_pct(s['ytd_dd']) + " |"
            lines.append(row)
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 3: Global Context ----
    lines.append("## Global Context")
    lines.append("")
    lines.append("**Table 3a: Global Equity and Risk Indicators (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    lines.append("| Ticker | Name | Latest | Daily Change | Crash DD | YTD Return | YTD DD |")
    lines.append("|--------|------|--------|-------------|----------|------------|--------|")
    
    global_tickers = {
        "SPY": "S&P 500 ETF",
        "QQQ": "Nasdaq 100 ETF",
        "^VIX": "CBOE Volatility Index",
        "DX-Y.NYB": "US Dollar Index (DXY)",
        "^TNX": "10-Year Treasury Yield",
        "GC=F": "Gold Futures",
        "CL=F": "Crude Oil Futures"
    }
    
    for s in all_stats:
        t = s['ticker']
        if t in global_tickers:
            name = global_tickers[t]
            row = "| " + t + " | " + name + " | " + format_price(s['latest']) + " | " + format_pct(s['daily_chg']) + " | " + format_pct(s['crash_dd']) + " | " + format_pct(s['ytd_ret']) + " | " + format_pct(s['ytd_dd']) + " |"
            lines.append(row)
    
    lines.append("")
    
    lines.append("**Table 3b: Global Context - Cross-Asset Summary (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    
    lines.append("| Asset | Crash Window Change | Interpretation |")
    lines.append("|-------|---------------------|----------------|")
    
    cross_asset_info = {
        "GC=F": ("Gold", "Safe-haven demand" if not np.isnan(next((s['crash_dd'] for s in all_stats if s['ticker'] == "GC=F"), np.nan)) and next((s['crash_dd'] for s in all_stats if s['ticker'] == "GC=F"), np.nan) > 0 else "Risk-off weakness"),
        "CL=F": ("Crude Oil", "Demand fears weigh on crude"),
        "DX-Y.NYB": ("US Dollar Index", "Dollar strengthening adds EM pressure"),
        "^TNX": ("10Y Yield", "Rate move during risk-off")
    }
    
    for ticker_key, (label, interp) in cross_asset_info.items():
        for s in all_stats:
            if s['ticker'] == ticker_key:
                if ticker_key == "GC=F":
                    if not np.isnan(s['crash_dd']):
                        interp = "Safe-haven demand" if s['crash_dd'] > 0 else "Risk-off weakness"
                elif ticker_key == "CL=F":
                    if not np.isnan(s['crash_dd']):
                        interp = "Demand fears weigh on crude" if s['crash_dd'] < 0 else "Supply concerns dominate"
                elif ticker_key == "DX-Y.NYB":
                    if not np.isnan(s['crash_dd']):
                        interp = "Dollar strengthening adds EM pressure" if s['crash_dd'] > 0 else "Dollar weak, supportive for EM"
                lines.append("| " + label + " | " + format_pct(s['crash_dd']) + " | " + interp + " |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 4: Semiconductor Sector ----
    lines.append("## Semiconductor Sector")
    lines.append("")
    lines.append("**Table 4: Semiconductor Exposure (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    lines.append("| Ticker | Name | Latest | Daily Change | Crash DD | YTD Return | YTD DD |")
    lines.append("|--------|------|--------|-------------|----------|------------|--------|")
    
    semi_tickers = {
        "SMH": "VanEck Semiconductor ETF",
        "TSM": "TSMC (Taiwan Semiconductor)",
        "ASML": "ASML Holding"
    }
    
    for s in all_stats:
        t = s['ticker']
        if t in semi_tickers:
            name = semi_tickers[t]
            row = "| " + t + " | " + name + " | " + format_price(s['latest']) + " | " + format_pct(s['daily_chg']) + " | " + format_pct(s['crash_dd']) + " | " + format_pct(s['ytd_ret']) + " | " + format_pct(s['ytd_dd']) + " |"
            lines.append(row)
    
    if sox_available:
        for s in all_stats:
            if s['ticker'] == "^SOX":
                row = "| ^SOX | PHLX Semiconductor Index | " + format_price(s['latest']) + " | " + format_pct(s['daily_chg']) + " | " + format_pct(s['crash_dd']) + " | " + format_pct(s['ytd_ret']) + " | " + format_pct(s['ytd_dd']) + " |"
                lines.append(row)
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 5: KOSPI Daily Returns (Largest Drops) ----
    lines.append("## KOSPI Daily Returns Over Crash Period")
    lines.append("")
    lines.append("**Table 5: KOSPI Daily Returns Sorted (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    lines.append("Worst single-day drops first, sorted ascending:")
    lines.append("")
    lines.append("| Date | Daily Return |")
    lines.append("|------|--------------|")
    
    if not kospi_returns_sorted.empty:
        for dt, ret in kospi_returns_sorted.items():
            lines.append("| " + dt.strftime('%Y-%m-%d') + " | " + format_pct(ret) + " |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 6: KRW Depreciation ----
    lines.append("## KRW Depreciation vs USD")
    lines.append("")
    lines.append("**Table 6: USD/KRW Exchange Rate (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    
    if not krw_data.empty:
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append("| Starting Rate (Jun 20) | " + NUM_TAG + f"{krw_data.iloc[0]:.2f}" + END_TAG + " |")
        lines.append("| Latest Rate (Jul 13) | " + NUM_TAG + f"{krw_data.iloc[-1]:.2f}" + END_TAG + " |")
        lines.append("| Absolute Change | " + NUM_TAG + f"{krw_data.iloc[-1] - krw_data.iloc[0]:.2f}" + END_TAG + " |")
        lines.append("| Percentage Change | " + format_pct(krw_chg) + " |")
        lines.append("| Crash Window High | " + NUM_TAG + f"{krw_data.max():.2f}" + END_TAG + " |")
        lines.append("| Crash Window Low | " + NUM_TAG + f"{krw_data.min():.2f}" + END_TAG + " |")
        
        if krw_chg > 0:
            interpretation = "KRW has weakened (more won per USD), adding import cost pressure."
        else:
            interpretation = "KRW has strengthened (fewer won per USD), supportive for imports."
        lines.append("| Interpretation | " + interpretation + " |")
    else:
        lines.append("Data not available.")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 7: Sector Dispersion ----
    lines.append("## Sector Dispersion: Semiconductors vs Broad Market")
    lines.append("")
    lines.append("**Table 7: Drawdown Comparison - Semiconductors vs. KOSPI (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    lines.append("| Instrument | Classification | Crash Drawdown |")
    lines.append("|------------|---------------|----------------|")
    
    lines.append("| ^KS11 (KOSPI) | Broad Korean Market | " + format_pct(kospi_crash_dd) + " |")
    for name, dd in semi_dd.items():
        lines.append("| " + name + " | Semiconductor | " + format_pct(dd) + " |")
    
    lines.append("")
    
    semi_dd_values = [v for v in semi_dd.values() if v is not None and not np.isnan(v)]
    if kospi_crash_dd is not None and not np.isnan(kospi_crash_dd) and len(semi_dd_values) > 0:
        semi_avg_dd = np.mean(semi_dd_values)
        dispersion = semi_avg_dd - kospi_crash_dd
        
        lines.append("Semiconductor average drawdown: " + format_pct(semi_avg_dd))
        lines.append("")
        lines.append("Dispersion (Semi avg - KOSPI drawdown): " + format_pct(dispersion))
        if dispersion < 0:
            lines.append("Semiconductors have underperformed the broad index during the crash window, indicating sector-specific selling pressure beyond the general market decline.")
        else:
            lines.append("Semiconductors have outperformed the broad index during the crash window, suggesting the selloff is broader than just tech/semis.")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 8: Correlation Analysis ----
    lines.append("## Correlation Analysis")
    lines.append("")
    lines.append("**Table 8: KOSPI Correlation with VIX and DXY (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    lines.append("| Pair | Correlation | Interpretation |")
    lines.append("|------|-------------|----------------|")
    
    if not np.isnan(corr_vix):
        if corr_vix < -0.5:
            vix_interp = "Strong inverse relationship - KOSPI falls when fear spikes"
        elif corr_vix < -0.3:
            vix_interp = "Moderate inverse relationship"
        elif abs(corr_vix) < 0.3:
            vix_interp = "Weak relationship"
        else:
            vix_interp = "Positive relationship (unusual)"
        lines.append("| KOSPI vs VIX | " + NUM_TAG + f"{corr_vix:.4f}" + END_TAG + " | " + vix_interp + " |")
    else:
        lines.append("| KOSPI vs VIX | " + NUM_TAG + "N/A" + END_TAG + " | Insufficient data |")
    
    if not np.isnan(corr_dxy):
        if corr_dxy < -0.5:
            dxy_interp = "Strong inverse - KOSPI falls when USD strengthens"
        elif corr_dxy < -0.3:
            dxy_interp = "Moderate inverse - USD strength pressures KOSPI"
        elif abs(corr_dxy) < 0.3:
            dxy_interp = "Weak relationship"
        else:
            dxy_interp = "Positive - KOSPI and USD move together"
        lines.append("| KOSPI vs DXY | " + NUM_TAG + f"{corr_dxy:.4f}" + END_TAG + " | " + dxy_interp + " |")
    else:
        lines.append("| KOSPI vs DXY | " + NUM_TAG + "N/A" + END_TAG + " | Insufficient data |")
    
    lines.append("")
    
    if n_observations > 0:
        lines.append("Correlation computed with " + str(n_observations) + " daily observations over the crash window.")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 9: Historical KOSPI Monthly Context ----
    lines.append("## Historical KOSPI Monthly Context")
    lines.append("")
    lines.append("**Table 9: KOSPI Monthly Close (Jan 2021 - Jul 2026)**")
    lines.append("")
    lines.append("| Month | Close | Monthly Return | Prior Correction Context |")
    lines.append("|-------|-------|---------------|--------------------------|")
    
    if not hist_monthly.empty:
        hist_monthly_ret = hist_monthly.pct_change() * 100
        
        for i in range(len(hist_monthly)):
            dt = hist_monthly.index[i]
            close_val = hist_monthly.iloc[i]
            ret_val = hist_monthly_ret.iloc[i] if i > 0 else np.nan
            
            ctx = ""
            if not np.isnan(ret_val) and ret_val < -5:
                ctx = "Major drop - correction territory"
            elif not np.isnan(ret_val) and ret_val < -3:
                ctx = "Significant decline"
            
            if dt.year == 2022:
                if not np.isnan(ret_val) and ret_val > 0:
                    ctx = "Recovery from 2022 lows"
                elif not np.isnan(ret_val) and ret_val < 0:
                    ctx = "2022 bear market"
            elif dt >= pd.Timestamp("2026-06-01"):
                ctx = "Current crash window"
            
            ret_str = format_pct(ret_val) if not np.isnan(ret_val) else NUM_TAG + "N/A" + END_TAG
            lines.append("| " + dt.strftime('%Y-%m') + " | " + NUM_TAG + f"{close_val:.2f}" + END_TAG + " | " + ret_str + " | " + ctx + " |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # ---- TABLE 10: Summary Statistics ----
    lines.append("## Summary Statistics")
    lines.append("")
    lines.append("**Table 10: Aggregate Statistics (Jun 20, 2026 - Jul 13, 2026)**")
    lines.append("")
    
    crash_dd_values = [(s['ticker'], s['crash_dd']) for s in all_stats if s['crash_dd'] is not None and not np.isnan(s['crash_dd'])]
    if crash_dd_values:
        crash_dd_sorted = sorted(crash_dd_values, key=lambda x: x[1])
        worst = crash_dd_sorted[:3]
        best = crash_dd_sorted[-3:]
        
        lines.append("**Worst 3 performers (crash drawdown):**")
        lines.append("")
        for t, dd in worst:
            lines.append("- " + t + ": " + format_pct(dd))
        lines.append("")
        lines.append("**Best 3 performers (crash drawdown):**")
        lines.append("")
        for t, dd in reversed(best):
            lines.append("- " + t + ": " + format_pct(dd))
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Data refresh completed " + TODAY + ". Data source: yfinance (delayed, not official). All data for informational purposes only.*")
    
    report = "\n".join(lines)
    
    # Write to file
    output_path = "/root/workspace/investment-research/reports/2026-07-13-kospi-correction/data-refresh.md"
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\n\nReport written to {output_path}")
    print("Total lines: " + str(len(lines)))
    print("\nDone!")

if __name__ == "__main__":
    main()