import yfinance as yf
import json
from datetime import datetime, date

# Ticker mappings: display_name -> yfinance symbol
tickers = {
    'SPY': 'SPY',
    'QQQ': 'QQQ',
    'IWM': 'IWM',
    'TLT': 'TLT',
    'XLU': 'XLU',
    'XLF': 'XLF',
    'XLRE': 'XLRE',
    '^TNX': '^TNX',
    'AAPL': 'AAPL',
    'MSFT': 'MSFT',
    'NVDA': 'NVDA',
    'META': 'META',
    'GOOGL': 'GOOGL',
    'AMZN': 'AMZN',
    'JPM': 'JPM',
    'GS': 'GS',
    'BAC': 'BAC',
    'PLD': 'PLD',
    'NEE': 'NEE',
    'WMT': 'WMT',
    'gold': 'GC=F',
    'crude': 'CL=F',
    'DXY': 'DX-Y.NYB',
    'GBP/USD': 'GBPUSD=X',
}

# Periods
ytd_start = '2026-01-01'
fomc_start = '2026-04-29'
today = date.today().isoformat()

results = {}
errors = {}

for display_name, symbol in tickers.items():
    try:
        tk = yf.Ticker(symbol)

        # Download from start of 2026 to get YTD data
        hist = tk.history(start='2025-12-31', end=today)

        if hist.empty:
            errors[display_name] = 'No data returned'
            continue

        # Latest price and daily change
        latest_close = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) >= 2 else latest_close
        daily_change = latest_close - prev_close
        daily_pct = (daily_change / prev_close) * 100

        # YTD: from Jan 1 2026
        ytd_mask = hist.index >= ytd_start
        ytd_hist = hist[ytd_mask]
        if len(ytd_hist) >= 1:
            # Use first trading day of 2026 as YTD base
            ytd_open_base = ytd_hist['Close'].iloc[0]
            # Actually better: use the Jan 2 first close or Jan 1
            # Let's get the close on the first trading day of the year
            hist_2025_2026 = tk.history(start='2025-12-30', end=today)
            ytd_mask2 = hist_2025_2026.index >= ytd_start
            ytd_hist2 = hist_2025_2026[ytd_mask2]
            if len(ytd_hist2) >= 1:
                ytd_base = ytd_hist2['Close'].iloc[0]
            else:
                ytd_base = latest_close
            ytd_pct = ((latest_close - ytd_base) / ytd_base) * 100
        else:
            ytd_pct = 0

        # Post-FOMC: from Apr 29 2026
        pfomc_mask = hist.index >= fomc_start
        pfomc_hist = hist[pfomc_mask]
        if len(pfomc_hist) >= 1:
            pfomc_base = pfomc_hist['Close'].iloc[0]
            pfomc_pct = ((latest_close - pfomc_base) / pfomc_base) * 100
        else:
            pfomc_pct = 0

        results[display_name] = {
            'symbol': symbol,
            'price': round(float(latest_close), 2),
            'daily_pct': round(float(daily_pct), 2),
            'ytd_pct': round(float(ytd_pct), 2),
            'post_fomc_pct': round(float(pfomc_pct), 2),
            'as_of_date': str(hist.index[-1].date()),
        }

    except Exception as e:
        errors[display_name] = str(e)

output = {
    'fetched_at': datetime.now().isoformat(),
    'results': results,
    'errors': errors,
}

print(json.dumps(output, indent=2, default=str))