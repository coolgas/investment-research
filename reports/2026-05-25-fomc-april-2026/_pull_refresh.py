#!/usr/bin/env python3
"""Pull yfinance data and generate data-refresh.md for May 25, 2026."""
import yfinance as yf
from datetime import datetime, date

WORKSPACE = "/home/ty/workspace/investment-research/reports/2026-05-25-fomc-april-2026"
TODAY = date.today().isoformat()
FETCHED_AT = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

# --- TICKERS ---
# yfinance symbols; display name tracked separately
TICKER_YF = [
    "SPY", "QQQ", "IWM", "^TNX", "DX-Y.NYB",  # Broad market
    "TLT", "XLU", "XLF", "XLRE",              # Sector ETFs
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",  # Mega-cap tech
    "JPM", "GS", "BAC",                       # Banks
    "PLD", "NEE", "WMT",                      # Other holdings
    "GC=F", "CL=F", "GBPUSD=X",               # Commodities & FX
]

TICKER_DISPLAY = {
    "SPY": "S&P 500", "QQQ": "Nasdaq-100", "IWM": "Small Caps (Russell)",
    "^TNX": "10Y Treasury Yield", "DX-Y.NYB": "US Dollar Index (DXY)",
    "TLT": "20+ Year Treasury", "XLU": "Utilities", "XLF": "Financials", "XLRE": "Real Estate",
    "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "NVIDIA", "META": "Meta",
    "GOOGL": "Alphabet", "AMZN": "Amazon",
    "JPM": "JPMorgan Chase", "GS": "Goldman Sachs", "BAC": "Bank of America",
    "PLD": "Prologis", "NEE": "NextEra Energy", "WMT": "Walmart",
    "GC=F": "Gold (Futures)", "CL=F": "Crude Oil (WTI)", "GBPUSD=X": "GBP/USD",
}

SECTION_BROAD = ["SPY", "QQQ", "IWM", "^TNX", "DX-Y.NYB"]
SECTION_SECTORS = ["TLT", "XLU", "XLF", "XLRE"]
SECTION_TECH = ["AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN"]
SECTION_BANKS = ["JPM", "GS", "BAC"]
SECTION_OTHER = ["PLD", "NEE", "WMT"]
SECTION_COMMODITIES = ["GC=F", "CL=F", "GBPUSD=X"]

# --- PULL DATA ---
print(f"Pulling data for {len(TICKER_YF)} tickers from 2025-12-30 to {TODAY}...")
df = yf.download(
    TICKER_YF,
    start="2025-12-30",
    end=TODAY,
    auto_adjust=True,
    threads=True,
)
print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()[:5]}...")

# With auto_adjust=True and no group_by, we get MultiIndex columns: ('Close','SPY'), etc.
# Already adjusted: 'Close' is the adjusted close.

available_tickers = set(df['Close'].columns)
print(f"Available tickers: {sorted(available_tickers)}")

def get_close(ticker):
    """Get close price series for a ticker, handling ^TNX special case."""
    yf_sym = ticker
    if yf_sym == "^TNX":
        # ^TNX is a rate not a price; use Adj Close or Close
        if yf_sym in df['Close'].columns:
            return df['Close'][yf_sym]
    if yf_sym in df['Close'].columns:
        return df['Close'][yf_sym]
    return None

# --- COMPUTE METRICS ---
results = {}

for ticker in TICKER_YF:
    close_series = get_close(ticker)
    if close_series is None or close_series.dropna().empty:
        print(f"WARNING: No data for {ticker}")
        continue
    
    close_series = close_series.dropna()
    if len(close_series) < 2:
        print(f"WARNING: Insufficient data for {ticker} ({len(close_series)} rows)")
        continue
    
    latest_close = close_series.iloc[-1]
    prev_close = close_series.iloc[-2]
    daily_pct = ((latest_close - prev_close) / prev_close) * 100
    
    latest_date = str(close_series.index[-1].date())
    
    # YTD: first trading day in 2026
    ytd_mask = close_series.index >= "2026-01-01"
    ytd_data = close_series[ytd_mask]
    if len(ytd_data) >= 1:
        ytd_base = ytd_data.iloc[0]
        ytd_pct = ((latest_close - ytd_base) / ytd_base) * 100
    else:
        ytd_pct = 0.0
    
    # Post-FOMC: Apr 29, 2026
    fomc_mask = close_series.index >= "2026-04-29"
    fomc_data = close_series[fomc_mask]
    if len(fomc_data) >= 1:
        fomc_base = fomc_data.iloc[0]
        fomc_pct = ((latest_close - fomc_base) / fomc_base) * 100
    else:
        fomc_pct = 0.0
    
    results[ticker] = {
        "price": round(float(latest_close), 2),
        "daily_pct": round(float(daily_pct), 2),
        "ytd_pct": round(float(ytd_pct), 2),
        "fomc_pct": round(float(fomc_pct), 2),
        "as_of": latest_date,
    }

print(f"\nComputed metrics for {len(results)} tickers")

# --- SPY-10Y Correlation ---
spy_close = get_close("SPY")
tnx_close = get_close("^TNX")

corr_note = ""
if spy_close is not None and tnx_close is not None:
    # Align on dates since Jan 1 2026
    common = spy_close.index.intersection(tnx_close.index)
    common = common[common >= "2026-01-01"]
    if len(common) >= 10:
        spy_aligned = spy_close[common]
        tnx_aligned = tnx_close[common]
        spy_returns = spy_aligned.pct_change().dropna()
        tnx_changes = tnx_aligned.diff().dropna()
        # Correlation of SPY daily % change vs 10Y yield daily bp change
        aligned_idx = spy_returns.index.intersection(tnx_changes.index)
        spy_ret = spy_returns[aligned_idx]
        tnx_chg = tnx_changes[aligned_idx]
        if len(spy_ret) >= 10:
            price_corr = spy_ret.corr(tnx_chg)
        else:
            price_corr = None
        
        # Also compute rolling 20-day correlation
        if len(spy_ret) >= 20:
            rolling_corr = spy_ret.rolling(20).corr(tnx_chg).iloc[-1]
        else:
            rolling_corr = None
        
        # Also post-FOMC correlation
        pfomc_mask = aligned_idx >= "2026-04-29"
        if pfomc_mask.sum() >= 5:
            corr_pfomc = spy_ret[pfomc_mask].corr(tnx_chg[pfomc_mask])
        else:
            corr_pfomc = None
        
        corr_note = (
            f"SPY-10Y daily return correlation (YTD): {price_corr:+.3f}. "
            f"20-day rolling: {rolling_corr:+.3f}." if price_corr is not None and rolling_corr is not None 
            else f"SPY-10Y daily return correlation (YTD): {price_corr:+.3f}." if price_corr is not None
            else ""
        )
        if corr_pfomc is not None:
            corr_note += f" Post-FOMC: {corr_pfomc:+.3f}."
    else:
        corr_note = "Insufficient data for SPY-10Y correlation."

print(f"\nSPY-10Y Correlation: {corr_note}")

# --- GENERATE MARKDOWN ---

def span(val, is_pct=True):
    """Return span-wrapped value with up/down/num class."""
    if is_pct:
        cls = "num" if abs(val) < 0.005 else ("up" if val > 0 else "down")
        return f'<span class="{cls}">{val:+.2f}%</span>'
    else:
        cls = "num"
        return f'<span class="{cls}">{val}</span>'

def render_table(tickers_list):
    """Render markdown table rows for given tickers."""
    rows = []
    for tkr in tickers_list:
        if tkr not in results:
            continue
        r = results[tkr]
        name = TICKER_DISPLAY.get(tkr, tkr)
        # For ^TNX, display as percentage
        if tkr == "^TNX":
            price_str = f'<span class="num">{r["price"]:.2f}%</span>'
        elif tkr in ("GBPUSD=X",):
            price_str = f'<span class="num">{r["price"]:.4f}</span>'
        elif r["price"] >= 1000:
            price_str = f'<span class="num">{r["price"]:.2f}</span>'
        else:
            price_str = f'<span class="num">{r["price"]:.2f}</span>'
        rows.append(
            f"| {tkr} | {name} | {price_str} | {span(r['daily_pct'])} | {span(r['ytd_pct'])} | {span(r['fomc_pct'])} |"
        )
    return "\n".join(rows)

lines = []
lines.append("---")
lines.append(f"date: {TODAY}")
lines.append("event: fomc-april-2026")
lines.append("type: data-refresh")
lines.append("source: yfinance")
lines.append(f"data_as_of: {TODAY}")
lines.append("tags:")
lines.append("  - data-refresh")
lines.append("  - yfinance")
lines.append("---")
lines.append("")
lines.append(f"# Data Refresh: {TODAY}")
lines.append("")
lines.append(f"**Latest close data by asset class.** Data pulled via yfinance as of {FETCHED_AT} UTC.")
lines.append("**Periods:** Daily change (prev close) | YTD (first trading day of 2026) | Post-FOMC (Apr 29, 2026)")
lines.append("")

table_header = "| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |"
table_sep = "|--------|------|-------|-------|-----|-----------|"

# Broad Market
lines.append("## Broad Market & Indices")
lines.append("")
lines.append(table_header)
lines.append(table_sep)
lines.append(render_table(SECTION_BROAD))
lines.append("")

# Sector ETFs
lines.append("## Sector ETFs")
lines.append("")
lines.append(table_header)
lines.append(table_sep)
lines.append(render_table(SECTION_SECTORS))
lines.append("")

# Mega-Cap Tech
lines.append("## Mega-Cap Tech")
lines.append("")
lines.append(table_header)
lines.append(table_sep)
lines.append(render_table(SECTION_TECH))
lines.append("")

# Banks
lines.append("## Banks")
lines.append("")
lines.append(table_header)
lines.append(table_sep)
lines.append(render_table(SECTION_BANKS))
lines.append("")

# Other Holdings
lines.append("## Other Holdings")
lines.append("")
lines.append(table_header)
lines.append(table_sep)
lines.append(render_table(SECTION_OTHER))
lines.append("")

# Commodities & FX
lines.append("## Commodities & FX")
lines.append("")
lines.append(table_header)
lines.append(table_sep)
lines.append(render_table(SECTION_COMMODITIES))
lines.append("")

# SPY-10Y Correlation
lines.append("## SPY-10Y Correlation")
lines.append("")
lines.append(f"<span class=\"num\">{corr_note}</span>")
lines.append("")

# Notes
lines.append("## Notes")
lines.append("")
lines.append(f"- Data via **yfinance**. All prices reflect most recent available close as of <span class=\"num\">{TODAY}</span>.")
lines.append("- YTD return computed from first trading day of 2026 to latest close.")
lines.append("- Post-FOMC return computed from Apr 29, 2026 close (FOMC decision date) to latest close.")
lines.append("- Gold via GC=F (COMEX futures). Crude oil via CL=F (WTI futures).")
lines.append("- DXY via DX-Y.NYB (US Dollar Index futures). GBP/USD via GBPUSD=X.")
lines.append("- Span classes: <span class=\"up\">up</span> (green), <span class=\"down\">down</span> (red), <span class=\"num\">num</span> (navy).")
lines.append("- YTD changes use auto_adjust=True in yfinance, so dividend adjustments are applied to historical prices.")

output = "\n".join(lines) + "\n"
outpath = f"{WORKSPACE}/data-refresh.md"
with open(outpath, "w") as f:
    f.write(output)

print(f"\nWrote {len(lines)} lines to {outpath}")

# Print summary diagnostics
print(f"\n=== DIAGNOSTICS ===")
print(f"Tickers with data: {len(results)}")
for tkr in sorted(results.keys()):
    r = results[tkr]
    print(f"  {tkr:12s}: ${r['price']:>10.2f}  daily={r['daily_pct']:>+7.2f}%  ytd={r['ytd_pct']:>+7.2f}%  fomc={r['fomc_pct']:>+7.2f}%  as_of={r['as_of']}")

missing = [t for t in TICKER_YF if t not in results]
if missing:
    print(f"\nMISSING TICKERS: {missing}")
