import yfinance as yf
import json
from datetime import datetime

tickers = {
    'SPY': 'S&P 500 ETF',
    'QQQ': 'Nasdaq-100 ETF',
    'IWM': 'Russell 2000 ETF',
    'TLT': '20+ Year Treasury ETF',
    'XLU': 'Utilities Select Sector',
    'XLF': 'Financials Select Sector',
    'XLRE': 'Real Estate Select Sector',
    '^TNX': '10Y Treasury Yield',
    'AAPL': 'Apple Inc',
    'MSFT': 'Microsoft Corp',
    'NVDA': 'NVIDIA Corp',
    'META': 'Meta Platforms',
    'GOOGL': 'Alphabet Inc',
    'AMZN': 'Amazon.com Inc',
    'JPM': 'JPMorgan Chase',
    'GS': 'Goldman Sachs',
    'BAC': 'Bank of America',
    'PLD': 'Prologis Inc',
    'NEE': 'NextEra Energy',
    'WMT': 'Walmart Inc',
    'GC=F': 'Gold Futures',
    'CL=F': 'Crude Oil WTI Futures',
    'DX-Y.NYB': 'US Dollar Index',
    'GBPUSD=X': 'GBP/USD',
}

results = {}
errors = {}

for symbol, name in tickers.items():
    try:
        tk = yf.Ticker(symbol)
        hist = tk.history(period='5d')
        if hist.empty:
            errors[symbol] = 'No data returned'
            continue
        
        last = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else last
        
        hist_1y = tk.history(period='1y')
        high_52w = hist_1y['High'].max() if not hist_1y.empty else None
        
        change = last - prev_close
        change_pct = (change / prev_close) * 100
        
        info = {}
        try:
            info_raw = tk.info
            if info_raw:
                info['marketCap'] = info_raw.get('marketCap')
                info['volume'] = info_raw.get('volume')
                info['avgVolume'] = info_raw.get('averageVolume')
                info['forwardPE'] = info_raw.get('forwardPE')
                info['trailingPE'] = info_raw.get('trailingPE')
                info['dividendYield'] = info_raw.get('dividendYield')
                info['sector'] = info_raw.get('sector')
        except:
            pass
        
        results[symbol] = {
            'name': name,
            'price': round(float(last), 2),
            'change': round(float(change), 2),
            'change_pct': round(float(change_pct), 2),
            'prev_close': round(float(prev_close), 2),
            'high_52w': round(float(high_52w), 2) if high_52w else None,
            'pct_of_52w_high': round(float(last / high_52w) * 100, 1) if high_52w and high_52w > 0 else None,
            'info': info,
            'timestamp': str(hist.index[-1]),
        }
    except Exception as e:
        errors[symbol] = str(e)

output = {
    'fetched_at': datetime.now().isoformat(),
    'results': results,
    'errors': errors,
}

print(json.dumps(output, indent=2, default=str))
