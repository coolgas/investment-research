"""Fetch comprehensive market data with daily, YTD, and Post-FOMC returns."""
import yfinance as yf
import json
from datetime import datetime, date
import sys

TICKERS = {
    # Broad Market & Indices
    'SPY': 'S&P 500',
    'QQQ': 'Nasdaq-100',
    'IWM': 'Russell 2000',
    '^TNX': '10Y Treasury Yield',
    'DX-Y.NYB': 'US Dollar Index',
    # Sector ETFs
    'TLT': '20+ Year Treasury',
    'XLU': 'Utilities',
    'XLF': 'Financials',
    'XLRE': 'Real Estate',
    # Mega-Cap Tech
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'NVDA': 'NVIDIA',
    'META': 'Meta',
    'GOOGL': 'Alphabet',
    'AMZN': 'Amazon',
    # Banks
    'JPM': 'JPMorgan Chase',
    'GS': 'Goldman Sachs',
    'BAC': 'Bank of America',
    # Other Holdings
    'PLD': 'Prologis',
    'NEE': 'NextEra Energy',
    'WMT': 'Walmart',
    # Commodities
    'GC=F': 'Gold (Futures)',
    'CL=F': 'Crude Oil (WTI)',
    # FX
    'GBPUSD=X': 'GBP/USD',
}

# DXY is ^DX-Y.NYB but yfinance uses DX-Y.NYB
DXY_ALIAS = 'DX-Y.NYB'
TNX_ALIAS = '^TNX'

YTD_START = '2026-01-02'  # Jan 1 is holiday
FOMC_START = '2026-04-29'  # FOMC decision date

results = {}
errors = {}

for symbol, name in TICKERS.items():
    try:
        tk = yf.Ticker(symbol)
        
        # Get since Jan 2 for YTD calc, plus enough buffer for daily change
        hist = tk.history(start='2026-01-01')
        
        if hist.empty:
            errors[symbol] = 'No data returned'
            continue
        
        # Latest close and daily change
        last = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else last
        
        daily_pct = ((last - prev_close) / prev_close) * 100
        
        # YTD: find Jan 2 close
        hist_jan = hist[hist.index >= YTD_START]
        if not hist_jan.empty:
            ytd_start_close = hist_jan['Close'].iloc[0]
            ytd_pct = ((last - ytd_start_close) / ytd_start_close) * 100
        else:
            ytd_pct = None
        
        # Post-FOMC: find Apr 29 close
        hist_fomc = hist[hist.index >= FOMC_START]
        if not hist_fomc.empty:
            fomc_start_close = hist_fomc['Close'].iloc[0]
            fomc_pct = ((last - fomc_start_close) / fomc_start_close) * 100
        else:
            fomc_pct = None
        
        # Use 4 decimal places for forex pairs, 2 for everything else
        is_fx = symbol.endswith('=X') or symbol.startswith('GBP')
        decimals = 4 if is_fx else 2
        
        results[symbol] = {
            'name': name,
            'price': round(float(last), decimals),
            'prev_close': round(float(prev_close), decimals),
            'daily_pct': round(float(daily_pct), 2),
            'ytd_pct': round(float(ytd_pct), 2) if ytd_pct is not None else None,
            'fomc_pct': round(float(fomc_pct), 2) if fomc_pct is not None else None,
            'date': str(hist.index[-1].date()),
        }
    except Exception as e:
        errors[symbol] = str(e)

# For ^TNX and DXY, render yields/levels
# TNX is a yield — keep as a percentage
# DXY is an index level

output = {
    'fetched_at': datetime.now().isoformat(),
    'data_as_of': date.today().isoformat(),
    'results': results,
    'errors': errors,
}

print(json.dumps(output, indent=2, default=str))