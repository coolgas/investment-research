import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

tickers = {
    "XLU": "Utilities",
    "XLP": "Consumer Staples",
    "XLV": "Health Care",
    "XLI": "Industrials",
    "XLF": "Financials",
    "XLE": "Energy",
    "XLB": "Materials",
    "XLY": "Consumer Discretionary",
    "IWM": "Russell 2000 (Small Caps)",
    "DIA": "Dow Jones (Old Economy)",
    "QQQ": "Nasdaq 100 (Tech)",
    "SMH": "Semiconductors",
    "SOXX": "Semiconductors (iShares)",
    "TLT": "20+ Year Treasury Bonds",
    "GLD": "Gold",
    "SPY": "S&P 500 (Benchmark)",
    "DXY": "US Dollar Index"
}

end_date = "2026-07-07"
ytd_start = "2026-01-02"
month_start = "2026-06-01"
week_start = "2026-06-30"

data = yf.download(
    list(tickers.keys()), 
    start=ytd_start, 
    end="2026-07-08",  # include current date
    auto_adjust=True,
    progress=False
)

print("Data columns:", data.columns.names if hasattr(data.columns, 'names') else "no multiindex")
print("Data index:", data.index[:3])
print("Data shape:", data.shape)
print("Available tickers in data:", list(data.columns.get_level_values(1).unique()) if hasattr(data.columns, 'names') else "flat")
