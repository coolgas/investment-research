"""Refresh yfinance data - per-ticker last-valid approach for mixed close dates."""
import json, pandas as pd, yfinance as yf

TICKERS = ["SPY","QQQ","IWM","TLT","XLU","XLF","XLRE",
    "^TNX","AAPL","MSFT","NVDA","META","GOOGL","AMZN",
    "JPM","GS","BAC","PLD","NEE","WMT",
    "GC=F","CL=F","DX-Y.NYB","GBPUSD=X"]

NAMES = {
    "SPY":"S&P 500","QQQ":"Nasdaq-100","IWM":"Small Caps (Russell)",
    "TLT":"20+ Year Treasury","XLU":"Utilities","XLF":"Financials",
    "XLRE":"Real Estate","^TNX":"10Y Treasury Yield",
    "AAPL":"Apple","MSFT":"Microsoft","NVDA":"NVIDIA",
    "META":"Meta","GOOGL":"Alphabet","AMZN":"Amazon",
    "JPM":"JPMorgan Chase","GS":"Goldman Sachs","BAC":"Bank of America",
    "PLD":"Prologis","NEE":"NextEra Energy","WMT":"Walmart",
    "GC=F":"Gold (Futures)","CL=F":"Crude Oil (WTI)",
    "DX-Y.NYB":"US Dollar Index (DXY)","GBPUSD=X":"GBP/USD",
}

df = yf.download(TICKERS, start="2025-12-30", end="2026-05-26", auto_adjust=True, progress=False)
close = df['Close']

ytd_base_date = "2026-01-02"
pf_base_date = "2026-04-29"

results = {}
for t in TICKERS:
    series = close[t].dropna()
    if len(series) < 2:
        results[t] = {"name": NAMES[t], "price": None}
        continue
    
    # Latest valid price & its date
    cur = float(series.iloc[-1])
    cur_date = series.index[-1].strftime('%Y-%m-%d')
    
    # Previous valid price for daily change
    prev = float(series.iloc[-2])
    
    # YTD base: find closest to Jan 2, or first available in 2026
    ytd_series = series[series.index >= ytd_base_date]
    ytd_base = float(ytd_series.iloc[0]) if len(ytd_series) > 0 else float(series.iloc[0])
    
    # Post-FOMC base: closest to Apr 29
    pf_series = series[series.index >= pf_base_date]
    pf_base = float(pf_series.iloc[0]) if len(pf_series) > 0 else float(series.iloc[0])
    
    daily_pct = ((cur / prev) - 1) * 100
    ytd_pct = ((cur / ytd_base) - 1) * 100
    pf_pct = ((cur / pf_base) - 1) * 100
    
    results[t] = {
        "name": NAMES[t],
        "price": round(cur, 2),
        "date": cur_date,
        "daily_pct": round(daily_pct, 2),
        "ytd_pct": round(ytd_pct, 2),
        "pf_pct": round(pf_pct, 2),
    }

# Output as JSON for downstream formatting
print(json.dumps({"results": results}, indent=2))