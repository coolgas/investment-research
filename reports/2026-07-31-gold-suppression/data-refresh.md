# Gold Market Data Refresh

Gold-focused market data pulled from Yahoo Finance (yfinance) on **2026-07-31**. "GC=F" is the COMEX gold futures continuous contract; all prices are daily closes unless noted. No values are estimated; where Yahoo returned no data the field is marked n/a.

## 1. Gold price action - current cycle (GC=F, 2021-01-04 to 2026-07-31)

*Table 1: Gold (GC=F) cycle statistics, 2021-01-04 to 2026-07-31, daily closes.*

| Metric | Value |
|---|---|
| Cycle / all-time high (close) | <span class="num">5,318.40</span> USD on <span class="num">2026-01-29</span> |
| Intraday high (same episode) | <span class="num">5,586.20</span> USD on <span class="num">2026-01-29</span> |
| Latest close | <span class="num">4,098.60</span> USD (<span class="num">2026-07-31</span>) |
| Drawdown from cycle high | <span class="down">-22.94%</span> |
| 3-month return (vs close of <span class="num">2026-04-30</span>) | <span class="down">-11.18%</span> |
| 6-month return (vs close of <span class="num">2026-01-31</span>) | <span class="down">-13.05%</span> |
| 12-month return (vs close of <span class="num">2025-07-31</span>) | <span class="up">+24.46%</span> |
| Total return since <span class="num">2021-01-04</span> | <span class="up">+110.76%</span> |

## 2. 2008 crisis episode (GC=F, 2007-01-02 to 2012-12-28)

*Table 2: 2008 financial crisis gold episode, 2007-01-02 to 2012-12-28, daily closes.*

| Metric | Value |
|---|---|
| Pre-crisis peak (close) | <span class="num">1,003.20</span> USD on <span class="num">2008-03-18</span> |
| Crisis trough (close) | <span class="num">704.90</span> USD on <span class="num">2008-11-13</span> |
| Max drawdown, peak to trough | <span class="down">-29.73%</span> |
| Days from peak to trough | <span class="num">240</span> |
| First close back above pre-crisis peak | <span class="num">2009-09-11</span> (<span class="num">302</span> days after trough) |

Context: the market leadership peak print was 2008-03-18 at 1,003.20 USD; gold bottomed 2008-11-13 at 704.90 USD (-29.73%), then took 302 days to reclaim the March 2008 high (2009-09-11).

## 3. Forward returns: 2008 episode vs current cycle

*Table 3: Forward returns from 2008 peak/trough (dates as listed) versus current standing, all GC=F closes. Current-cycle forward returns are not yet observable (n/a).*

| Start point | Start date | +1 year | +2 years | +3 years |
|---|---|---|---|---|
| 2008 crisis trough | <span class="num">2008-11-13</span> | <span class="up">+58.33%</span> | <span class="up">+93.70%</span> | <span class="up">+153.58%</span> |
| 2008 pre-crisis peak | <span class="num">2008-03-18</span> | <span class="down">-11.41%</span> | <span class="up">+12.38%</span> | n/a |
| Current cycle (standing) | <span class="num">2026-07-31</span> | n/a (no forward data) | n/a | n/a |

As of 2026-07-31 the current cycle sits at a drawdown of -22.94% from its 2026-01-29 high, versus the -29.73% peak-to-trough drawdown of the 2008 episode. In 2008, buying the trough returned +58.33% (1y, to 2009-11-13), +93.70% (2y, to 2010-11-13) and +153.58% (3y, to 2011-11-13); buying the March 2008 peak was still -11.41% one year later but +12.38% by 2010-03-18. These are historical outcomes, not forecasts for the current cycle.

## 4. Correlations - suppression drivers (daily closes)

Note: the ticker "DXY" returned no data from Yahoo download; the US Dollar Index was pulled as **DX-Y.NYB** in both windows.

*Table 4a: Daily close-to-close RETURN correlation (Pearson), 2008 window 2007-01-02 to 2012-12-28 vs current window 2021-01-04 to 2026-07-31.*

| Pair | 2008 window | Current window | Match? |
|---|---|---|---|
| GC=F vs ^TNX (10y yield) | <span class="down">-0.02</span> | <span class="down">-0.24</span> | same sign (both negative) |
| GC=F vs DXY (USD index) | <span class="down">-0.38</span> | <span class="down">-0.39</span> | match (both negative, similar magnitude) |
| GC=F vs SPY (equities) | <span class="up">+0.03</span> | <span class="up">+0.11</span> | both positive but weak |

*Table 4b: Correlation of daily CLOSE LEVELS (Pearson), same windows.*

| Pair | 2008 window | Current window |
|---|---|---|
| GC=F vs ^TNX (10y yield) | <span class="down">-0.85</span> | <span class="up">+0.52</span> |
| GC=F vs DXY (USD index) | <span class="down">-0.18</span> | <span class="down">-0.08</span> |

*Table 4c: Oct 2008 deleveraging sub-window (2008-09-15 to 2008-10-31), daily returns; October 2008 monthly returns.*

| Metric | Value |
|---|---|
| GC=F vs SPY return corr, 2008-09-15 to 2008-10-31 | <span class="down">-0.22</span> |
| GC=F vs DXY return corr, 2008-09-15 to 2008-10-31 | <span class="down">-0.40</span> |
| October 2008 monthly return, GC=F | <span class="down">-18.01%</span> |
| October 2008 monthly return, SPY | <span class="down">-16.52%</span> |
| October 2008 monthly return, DXY | <span class="up">+7.78%</span> |
| GC=F drawdown, 2008-09-15 to 2008-11-30 (trough <span class="num">2008-11-13</span>) | <span class="down">-22.02%</span> |

**Read of the evidence.** The rising-USD suppression pattern matches: GC=F vs DXY daily-return correlation is negative in both windows (-0.38 in 2007-2012, -0.39 in 2021-2026) and strengthens to -0.40 inside the Oct 2008 crash window, i.e. a surging dollar was the daily driver of gold weakness in the crisis. The falling-yield driver does NOT show up as a positive daily GC=F vs ^TNX correlation in either window (-0.02 then, -0.24 now); the level correlation flipped sign (-0.85 then, +0.52 now) simply because yields fell for a decade while gold rose, whereas both trended together over 2021-2026. On the deleveraging claim: gold fell hard alongside stocks in October 2008 (gold -18.01%, SPY -16.52% for the month) and drew down -22.02% from the Sept 2008 peak to the 2008-11-13 trough; however the daily-frequency GC=F vs SPY return correlation stayed negative (-0.22) over 2008-09-15 to 2008-10-31, so at daily frequency the data show USD strength, not equity beta, as the proximate driver of gold selling.

## 5. SGLD.L fund profile (LSE, as of 2026-07-31)

*Table 5: SGLD.L fields verbatim from yfinance Ticker.info, fetched 2026-07-31.*

| Field | Value |
|---|---|
| longName | Invesco Physical Gold ETC |
| shortName | INVESCO PHYSICAL MARKETS PUBLIC |
| currency | USD |
| quoteType | EQUITY |
| exchange | LSE |
| exchangeTimezoneName | Europe/London |
| regularMarketPrice | <span class="num">388.35</span> |
| sharesOutstanding | <span class="num">122271000</span> |
| fiftyTwoWeekHigh | <span class="num">534.03</span> |
| fiftyTwoWeekLow | <span class="num">308.55</span> |
| symbol | SGLD.L |
| fundFamily | n/a (not present in Yahoo .info payload) |
| name | n/a (not present in Yahoo .info payload) |
| holdings / TER | n/a (Yahoo FundsData holdings empty; TER not provided by Yahoo .info) |

fast_info.last_price = <span class="num">388.35</span> USD; fast_info.year_high = <span class="num">534.03</span>; fast_info.year_low = <span class="num">308.55</span>.

*Table 5b: SGLD.L 1-year history (2025-07-31 to 2026-07-31) plus comparison vs GLD (SPDR Gold Shares) and GC=F.*

| Metric | SGLD.L (USD) | GLD (USD) | GC=F (USD) |
|---|---|---|---|
| Latest close | <span class="num">388.35</span> | <span class="num">371.54</span> | <span class="num">4,098.60</span> |
| 52-week high (close) | <span class="num">509.85</span> on <span class="num">2026-03-02</span> | <span class="num">495.90</span> | <span class="num">5,318.40</span> |
| 52-week low (close) | <span class="num">317.63</span> on <span class="num">2025-07-31</span> | <span class="num">300.96</span> | <span class="num">3,293.20</span> |
| 1-year return | <span class="up">+22.26%</span> | <span class="up">+20.81%</span> | <span class="up">+24.46%</span> |
| YTD return (vs 2025-12-31 close) | <span class="down">-6.38%</span> | <span class="down">-6.25%</span> | n/a |

**What the data say about SGLD.L.** Yahoo identifies it as "Invesco Physical Gold ETC" (longName), currency **USD**, quoteType EQUITY (Yahoo's classification for this LSE listing), exchange LSE. It is therefore a USD-denominated, physically-backed gold ETC listed on the LSE, not a GBP-denominated product. SGLD.L 1-year return (+22.26%) tracks GC=F (+24.46%) less the sterling appreciation of +1.73% over the year, consistent with USD denomination. Price levels differ between SGLD.L, GLD and the futures contract because each share represents a different fraction of one ounce of gold (unit sizes and fee drag differ); the daily return series are the comparable metric. Note: the .info payload is small (2.2 KB) and contains no fundFamily, TER, category or holdings breakdown; treat TER and holdings as unverified from Yahoo data.

## 6. GBPUSD 1-year trend (2025-07-31 to 2026-07-31)

*Table 6: GBPUSD (GBPUSD=X), 2025-07-31 to 2026-07-31, daily closes.*

| Metric | Value |
|---|---|
| Latest | <span class="num">1.3487</span> on <span class="num">2026-07-31</span> |
| One year ago | <span class="num">1.3258</span> on <span class="num">2025-07-31</span> |
| 1-year change | <span class="up">+1.73%</span> (sterling up vs USD) |
| 52-week high | <span class="num">1.3825</span> on <span class="num">2026-01-29</span> |
| 52-week low | <span class="num">1.3022</span> on <span class="num">2025-11-05</span> |

Implication for a GBP-based investor: with GBPUSD up 1.73% over the year, USD-denominated SGLD.L returns were roughly 1.7pp lower in GBP terms than in USD terms over the same period; the FX direction matters for entry points.

## Data notes

- Source: Yahoo Finance via yfinance (delayed/unofficial data); cross-verify against exchange feeds before publication.
- As-of date: 2026-07-31 (last trading day in the dataset).
- US Dollar Index pulled as DX-Y.NYB; the symbol "DXY" returned no data from yf.download.
- Correlations are Pearson on daily closes (levels) and on daily close-to-close returns; returns use aligned trading days.
- Current-cycle forward returns are not yet observable and are marked n/a rather than estimated.
- Rounding: prices 2 decimals (4 for FX), percentages 2 decimals, correlations 2 decimals.
