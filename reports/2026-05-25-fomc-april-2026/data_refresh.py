#!/usr/bin/env python3
"""Pull yfinance data for 24 tickers and produce data-refresh.md for 2026-05-25."""

import yfinance as yf
import pandas as pd
from datetime import datetime, date

# ── Tickers ──────────────────────────────────────────────────────────────
TICKERS = [
    # Broad Market
    "SPY", "QQQ", "IWM", "^TNX", "DX-Y.NYB",
    # Sectors
    "TLT", "XLU", "XLF", "XLRE",
    # Mega-Cap Tech
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    # Banks
    "JPM", "GS", "BAC",
    # Other Holdings
    "PLD", "NEE", "WMT",
    # Commodities & FX
    "GC=F", "CL=F", "GBPUSD=X",
]

NAMES = {
    "SPY": "S&P 500",
    "QQQ": "Nasdaq-100",
    "IWM": "Small Caps (Russell)",
    "^TNX": "10Y Treasury Yield",
    "DX-Y.NYB": "US Dollar Index (DXY)",
    "TLT": "20+ Year Treasury",
    "XLU": "Utilities",
    "XLF": "Financials",
    "XLRE": "Real Estate",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "META": "Meta",
    "GOOGL": "Alphabet",
    "AMZN": "Amazon",
    "JPM": "JPMorgan Chase",
    "GS": "Goldman Sachs",
    "BAC": "Bank of America",
    "PLD": "Prologis",
    "NEE": "NextEra Energy",
    "WMT": "Walmart",
    "GC=F": "Gold (Futures)",
    "CL=F": "Crude Oil (WTI)",
    "GBPUSD=X": "GBP/USD",
}

YTD_BASE = "2026-01-02"   # First trading day of 2026 (Jan 1 holiday)
FOMC_BASE = "2026-04-29"  # FOMC April decision date

print("=== Fetching yfinance data for 24 tickers ===")
print(f"Period: {YTD_BASE} to 2026-05-26 (exclusive)")
print(f"YTD base: {YTD_BASE}  |  FOMC base: {FOMC_BASE}")

# ── Pull daily data ──────────────────────────────────────────────────────
# IMPORTANT: do NOT use group_by='ticker' with auto_adjust=True
# Access as df['Close'][ticker]
print("\nDownloading daily data...")
df = yf.download(
    TICKERS,
    start=YTD_BASE,
    end="2026-05-26",     # exclusive, gets through May 25
    auto_adjust=True,
    progress=False,
)
print(f"Shape: {df.shape}")
print(f"Columns levels: {df.columns.nlevels}")
print(f"Date range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")

# ── Build results ────────────────────────────────────────────────────────
results = []

for ticker in TICKERS:
    try:
        close_series = df['Close'][ticker].dropna()
        if len(close_series) < 2:
            print(f"  SKIP {ticker}: insufficient data ({len(close_series)} rows)")
            results.append({'ticker': ticker, 'name': NAMES[ticker], 'error': f'insufficient data ({len(close_series)} rows)'})
            continue

        # Latest close
        latest_date = close_series.index[-1]
        latest_close = float(close_series.iloc[-1])

        # Daily % change
        if len(close_series) >= 2:
            prev_close = float(close_series.iloc[-2])
            daily_pct = round((latest_close - prev_close) / prev_close * 100, 2)
        else:
            daily_pct = None

        # YTD % (from first available date on/after YTD_BASE)
        ytd_value = close_series.iloc[0]
        ytd_pct = round((latest_close - float(ytd_value)) / float(ytd_value) * 100, 2)

        # Post-FOMC % (from Apr 29 or nearest)
        fomc_data = close_series[close_series.index >= pd.Timestamp(FOMC_BASE)]
        if len(fomc_data) > 0:
            fomc_base_val = float(fomc_data.iloc[0])
            fomc_pct = round((latest_close - fomc_base_val) / fomc_base_val * 100, 2)
        else:
            fomc_pct = None

        results.append({
            'ticker': ticker,
            'name': NAMES[ticker],
            'close': latest_close,
            'close_date': latest_date.strftime('%Y-%m-%d'),
            'daily_pct': daily_pct,
            'ytd_pct': ytd_pct,
            'fomc_pct': fomc_pct,
        })

        print(f"  {ticker:12s} close={latest_close:>12.4f}  daily={daily_pct:>+7.2f}%  ytd={ytd_pct:>+7.2f}%  fomc={fomc_pct:>+7.2f}%  date={latest_date.strftime('%Y-%m-%d')}")

    except Exception as e:
        print(f"  ERROR {ticker}: {e}")
        results.append({'ticker': ticker, 'name': NAMES[ticker], 'error': str(e)})

# ── Helper: span class ───────────────────────────────────────────────────
def span_pct(val, decimals=2):
    """Format a percentage with appropriate span class."""
    if val is None:
        return '<span class="num">N/A</span>'
    if abs(val) < 0.005:
        return f'<span class="num">{val:+.{decimals}f}%</span>'
    if val > 0:
        return f'<span class="up">{val:+.{decimals}f}%</span>'
    return f'<span class="down">{val:+.{decimals}f}%</span>'

def span_price(val, decimals=2, is_yield=False):
    """Format a price. For yields (^TNX), include % suffix."""
    if val is None:
        return '<span class="num">N/A</span>'
    if is_yield:
        return f'<span class="num">{val:.{decimals}f}%</span>'
    # Gold futures can be 4 digits, use comma formatting
    if abs(val) >= 1000:
        return f'<span class="num">{val:,.{decimals}f}</span>'
    return f'<span class="num">{val:.{decimals}f}</span>'

def corr_class(r):
    """Span class for correlation coefficient."""
    if r is None:
        return "num"
    if r < -0.3:
        return "down"
    if r > 0.3:
        return "up"
    return "num"

def corr_interpret(r):
    """Human-readable interpretation of correlation strength."""
    if r is None:
        return "N/A"
    a = abs(r)
    if a < 0.2:
        return "Negligible"
    if a < 0.4:
        return "Weak"
    if a < 0.6:
        return "Moderate"
    if a < 0.8:
        return "Strong"
    return "Very strong"

# ── Identify close dates per asset class ─────────────────────────────────
close_dates = {}
for r in results:
    if 'close_date' in r:
        cls = r['close_date']
        close_dates[cls] = close_dates.get(cls, []) + [r['ticker']]

# ── SPY-10Y Correlation ──────────────────────────────────────────────────
print("\n--- SPY-10Y Correlation ---")
corr_df = yf.download(["SPY", "^TNX"], start=YTD_BASE, end="2026-05-26", auto_adjust=True, progress=False)
corr_spy = corr_df['Close']['SPY'].dropna()
corr_tnx = corr_df['Close']['^TNX'].dropna()
common_idx = corr_spy.index.intersection(corr_tnx.index)
spy_rets = corr_spy[common_idx].pct_change().dropna()
tnx_chg = corr_tnx[common_idx].diff().dropna()
common = spy_rets.index.intersection(tnx_chg.index)
spy_r = spy_rets[common]
tnx_c = tnx_chg[common]
corr_full = spy_r.corr(tnx_c)
corr_n = len(spy_r)
corr_rolling = spy_r.rolling(20).corr(tnx_c)
corr_latest_20 = corr_rolling.iloc[-1]
post_fomc_mask = spy_r.index >= pd.Timestamp(FOMC_BASE)
corr_post = spy_r[post_fomc_mask].corr(tnx_c[post_fomc_mask]) if post_fomc_mask.sum() > 5 else None
corr_post_n = post_fomc_mask.sum()
print(f"  Full ({corr_n}d): {corr_full:+.4f}  |  20d rolling: {corr_latest_20:+.4f}  |  Post-FOMC ({corr_post_n}d): {corr_post:+.4f}")

# ── Generate markdown ────────────────────────────────────────────────────
report_date = "2026-05-25"
data_as_of = "2026-05-25"

# Build close-date description
date_desc_parts = []
for dt in sorted(close_dates.keys()):
    tickers_str = ", ".join(close_dates[dt][:5])
    if len(close_dates[dt]) > 5:
        tickers_str += f" +{len(close_dates[dt])-5} more"
    date_desc_parts.append(f"{', '.join(close_dates[dt])}: {dt}")
date_desc = "; ".join(date_desc_parts)

def row_line(ticker, is_yield=False, decimals=None):
    r = next((x for x in results if x['ticker'] == ticker), None)
    if r is None:
        return f"| {ticker} | ERROR | - | - | - | - |"
    if decimals is None:
        decimals = 3 if ticker == '^TNX' else 2
    close_str = span_price(r.get('close'), decimals=decimals, is_yield=(ticker == '^TNX'))
    daily_str = span_pct(r.get('daily_pct'))
    ytd_str = span_pct(r.get('ytd_pct'))
    fomc_str = span_pct(r.get('fomc_pct'))
    return f"| {ticker} | {r['name']} | {close_str} | {daily_str} | {ytd_str} | {fomc_str} |"

md = f"""---
date: {report_date}
event: fomc-april-2026
type: data-refresh
source: yfinance
data_as_of: {data_as_of}
tags:
  - data-refresh
  - yfinance
---

# Data Refresh: May 25, 2026

**Latest close data by asset class.** Equities close May 22 (Friday). Commodities, DXY close May 25 (Monday). GBP/USD closes continuously.
**Periods:** Daily change (prev close) | YTD (Jan 2, 2026) | Post-FOMC (Apr 29, 2026)

## Broad Market & Indices

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|-------|-----|-----------|
{row_line("SPY")}
{row_line("QQQ")}
{row_line("IWM")}
{row_line("^TNX", is_yield=True)}
{row_line("DX-Y.NYB")}

## Sector ETFs

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|-------|-----|-----------|
{row_line("TLT")}
{row_line("XLU")}
{row_line("XLF")}
{row_line("XLRE")}

## Mega-Cap Tech

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|-------|-----|-----------|
{row_line("AAPL")}
{row_line("MSFT")}
{row_line("NVDA")}
{row_line("META")}
{row_line("GOOGL")}
{row_line("AMZN")}

## Banks

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|-------|-----|-----------|
{row_line("JPM")}
{row_line("GS")}
{row_line("BAC")}

## Other Holdings

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|-------|-----|-----------|
{row_line("PLD")}
{row_line("NEE")}
{row_line("WMT")}

## Commodities & FX

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|-------|-----|-----------|
{row_line("GC=F")}
{row_line("CL=F")}
{row_line("GBPUSD=X", decimals=4)}

## SPY-10Y Correlation

Daily SPY returns vs 10Y yield absolute change. Negative = equities fall as yields rise (rate-sensitivity regime).

| Period | N | Pearson r | Interpretation |
|--------|---|----------|---------------|
| YTD (Jan 2+) | <span class="num">{corr_n}</span> | <span class="{corr_class(corr_full)}">{corr_full:+.4f}</span> | {corr_interpret(corr_full)} negative correlation |
| 20-Day Rolling | <span class="num">20</span> | <span class="{corr_class(corr_latest_20)}">{corr_latest_20:+.4f}</span> | {corr_interpret(corr_latest_20)} negative correlation |
| Post-FOMC (Apr 29+) | <span class="num">{corr_post_n}</span> | <span class="{corr_class(corr_post)}">{corr_post:+.4f}</span> | {corr_interpret(corr_post)} negative correlation |

## Notes

- Data via yfinance. Close dates: equities May 22 (Friday), commodities/DXY May 25 (Monday), GBP/USD continuous.
- YTD base: Jan 2, 2026 (Jan 1 is a holiday). Post-FOMC base: Apr 29, 2026 (FOMC decision date).
- Gold via GC=F (COMEX futures). Crude oil via CL=F (WTI futures).
- DXY via DX-Y.NYB (US Dollar Index futures). GBP/USD via GBPUSD=X.
- Span classes: up (green), down (red), num (neutral). No emojis.
- YTD changes use auto_adjust=True in yfinance, so dividend adjustments are applied to historical prices.
- 10Y Treasury Yield (^TNX) displayed as raw yield percentage, not price.
"""

# Write output
output_path = "/home/ty/workspace/investment-research/reports/2026-05-25-fomc-april-2026/data-refresh.md"
with open(output_path, 'w') as f:
    f.write(md)

print(f"\n✓ Wrote {output_path}")
print(f"  Characters: {len(md)}")

# ── Summary stats ────────────────────────────────────────────────────────
successful = sum(1 for r in results if 'close' in r)
failed = sum(1 for r in results if 'error' in r)
print(f"\nResults: {successful} tickers pulled, {failed} errors")