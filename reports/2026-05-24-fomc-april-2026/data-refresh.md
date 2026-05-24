---
date: 2026-05-24
event: fomc-april-2026
type: data-refresh
source: yfinance
data_as_of: 2026-05-22 close
---

# Data Refresh: YFinance Market Data

**Data as of:** May 22, 2026 Close | **Refreshed:** May 24, 2026

## Market Indices and Sectors

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|---------|-------|-------------|
| SPY | S&P 500 | 745.64 | +0.39 | +9.44 | +4.79 |
| QQQ | Nasdaq-100 | 717.54 | +0.42 | +17.18 | +8.46 |
| IWM | Small Caps (Russell 2000) | 285.12 | +0.93 | +14.81 | +4.79 |
| XLU | Utilities Select Sector | 45.35 | +0.78 | +5.76 | -0.72 |
| XLF | Financials Select Sector | 51.94 | +0.41 | -4.96 | +0.04 |
| XLRE | Real Estate Select Sector | 44.56 | +0.13 | +11.09 | +2.11 |

## Fixed Income and Rates

| Ticker | Name | Price/Yield | Daily % | YTD % | Post-FOMC % |
|--------|------|-------------|---------|-------|-------------|
| ^TNX | 10-Year Treasury Yield | 4.56% | -0.61 | +8.86 | +3.17 |
| TLT | 20+ Year Treasury Bond ETF | 84.68 | +0.55 | -1.25 | -0.83 |

## Mega-Cap Tech

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|---------|-------|-------------|
| AAPL | Apple Inc. | 308.82 | +1.26 | +14.16 | +14.41 |
| MSFT | Microsoft Corp. | 418.57 | -0.12 | -11.10 | -1.17 |
| NVDA | NVIDIA Corp. | 215.33 | -1.90 | +14.03 | +2.91 |
| META | Meta Platforms | 610.26 | +0.47 | -6.09 | -8.80 |
| GOOGL | Alphabet Inc. | 382.97 | -1.21 | +21.61 | +9.44 |
| AMZN | Amazon.com Inc. | 266.32 | -0.80 | +17.58 | +1.25 |

## Financials

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|---------|-------|-------------|
| JPM | JPMorgan Chase | 306.38 | +1.12 | -4.96 | -0.93 |
| GS | Goldman Sachs | 996.73 | +0.87 | +9.58 | +10.06 |
| BAC | Bank of America | 51.80 | +0.60 | -6.89 | -2.04 |

## Real Estate and Utilities

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|---------|-------|-------------|
| PLD | ProLogis (Industrial REIT) | 145.90 | +0.88 | +13.97 | +5.10 |
| NEE | NextEra Energy | 88.55 | -1.27 | +10.16 | -5.97 |
| WMT | Walmart (Consumer Defensive) | 120.27 | -0.88 | +7.08 | -5.87 |

## Commodities and FX

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|---------|-------|-------------|
| GC=F | Gold Futures | 4523.20 | -0.37 | +4.84 | -0.48 |
| CL=F | Crude Oil (WTI) Futures | 96.60 | +0.26 | +68.53 | -9.62 |
| DX-Y.NYB | US Dollar Index (DXY) | 99.32 | +0.13 | +0.91 | +0.40 |
| GBPUSD=X | GBP/USD | 1.34 | +0.01 | -0.30 | -0.67 |

## Notes

- **YTD %** calculated from Jan 2, 2026 (first trading day of the year) to May 22 close.
- **Post-FOMC %** calculated from Apr 29, 2026 (FOMC decision day) close to May 22 close.
- **Daily %** is the change from the previous trading day's close.
- Equities data sourced from yfinance (auto_adjust=True) via Python. Futures data (GC=F, CL=F) reflects continuous contract pricing.
- The 10Y yield (^TNX) is reported in yield percentage points, not price. Daily/YTD/Post-FOMC % changes are relative percent changes in the yield level.