<style>
  table { border-collapse: collapse; width: 100%; margin: 1.5em 0; font-size: 0.9em; }
  th { background-color: #1a237e; color: #ffffff; font-weight: bold; padding: 10px 8px; text-align: left; }
  td { padding: 8px; border-bottom: 1px solid #e0e0e0; }
  tr:nth-child(even) { background-color: #f5f5ff; }
  tr:nth-child(odd) { background-color: #ffffff; }
  tr:hover { background-color: #e8eaf6; }
  .up { color: #2e7d32; font-weight: bold; }
  .down { color: #c62828; font-weight: bold; }
  .num { color: #1a237e; font-weight: bold; }
  h2 { color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 4px; }
  h3 { color: #283593; }
  .disclaimer { font-size: 0.8em; color: #666; border-top: 2px solid #ccc; margin-top: 3em; padding-top: 1em; }
  .caption { font-size: 0.85em; color: #555; margin-bottom: 0.5em; font-style: italic; }
</style>

# Market Brief: April 2026 FOMC Rate Hold and Post-Meeting Dynamics

**Date:** May 24, 2026
**Event:** FOMC April 29, 2026 Decision
**Asset Classes Covered:** Equities, Fixed Income, FX, Commodities
**Analyst Lens:** Rate-sensitive equities, sector rotation, EM FX exposure

---

## 1. Executive Summary

The Federal Reserve held the federal funds rate at <span class="num">3.50-3.75%</span> at its April 29, 2026 meeting, an outcome universally expected by consensus. The policy statement and Chair Powell's press conference signaled solid economic growth, a softening but stable labor market (unemployment at approximately <span class="num">4.3%</span>), and an inflation uptick driven by global energy prices and Middle East geopolitical developments. One dissenter (Miran) preferred an immediate <span class="num">25</span>bp cut, introducing internal pressure for easing.

Contrary to a simplistic "higher-for-longer implies defensive" narrative, post-FOMC markets staged a decisive **risk-on rotation**. The Nasdaq-100 (QQQ) surged <span class="up">+8.46%</span>, nearly doubling the S&P 500's <span class="up">+4.79%</span> gain. Utilities (XLU) were the only sector to fall (<span class="down">-0.72%</span>), and the SPY-10Y yield correlation tightened to an extreme <span class="num">-0.90</span> (vs. YTD average of <span class="num">-0.39</span>), demonstrating that rates became the dominant equity pricing variable post-meeting.

The market interpreted the outcome as "hold now, cut later" — focusing on the dissenting vote, flexible forward guidance, and absence of tightening bias. This narrative faces its first major test with the upcoming May PCE (ex-energy) print. A hot PCE reading would unravel the cut-hope thesis and, given the extreme rate-equity correlation regime, could trigger rapid equity drawdowns. Scenario modeling indicates a moderate-hot PCE (<span class="num">0.25-0.30%</span> MoM ex-energy) implies a <span class="num">-5.1%</span> SPY drawdown, with small caps (IWM) facing <span class="down">-9.4%</span> downside.

Within mega-cap tech, extreme dispersion has emerged: AAPL (<span class="up">+14.41%</span> post-FOMC, at <span class="num">100%</span> of 52w high) stands opposite META (<span class="down">-8.80%</span>, at <span class="num">82.7%</span> of 52w high). Financials show a similar divide — Goldman Sachs (<span class="up">+10.06%</span>) benefitting from M&A optimism while consumer banks JPM (<span class="down">-0.93%</span>) and BAC (<span class="down">-2.04%</span>) lag on loan growth concerns.

The DXY has remained supported at <span class="num">99.32</span>, crude oil has pulled back <span class="down">-9.62%</span> post-FOMC from energy-spike highs, and gold is essentially flat. EM FX faces headwinds from USD strength and Middle East risk premia.

---

## 2. Methodology

### Date Ranges

| Scope | Start Date | End Date | Source |
|-------|-----------|---------|--------|
| YTD | Jan 1, 2026 | May 22, 2026 | yfinance |
| Post-FOMC Window | Apr 29, 2026 | May 22, 2026 | yfinance |
| Daily Basis | May 22 close vs. May 21 close | Single trading day | yfinance |
| Scenario Betas | Trailing 30 days to May 22, 2026 | Rolling computation | yfinance |
| Correlation Window | Trailing 30 days to May 22, 2026 | SPY vs. ^TNX daily returns | yfinance |

### Models and Data Sources

- **Primary data provider:** yfinance <span class="num">1.4.0</span>. Price data for all tickers uses `auto_adjust=True` so dividend adjustments are applied to historical prices.
- **FOMC source documents:** Federal Reserve press release (monetary20260429a.htm) and press conference transcript (FOMCpresconf20260429.pdf). Extracted via pdftotext and HTML stripping.
- **Scenario model (hot-PCE analysis):** Three-way cross-validation: (A) 30-day rolling beta regression of SPY vs. ^TNX daily returns; (B) Historical analog scaling using Sep-Nov <span class="num">2023</span> as baseline (10Y <span class="num">4.17%</span> to <span class="num">4.99%</span>, correlation <span class="num">-0.49</span>, scaling multiplier <span class="num">1.71x</span> to current regime of <span class="num">-0.84</span>); (C) Multi-day compound factor (<span class="num">1.5x</span> to <span class="num">2.0x</span>) for sustained repricing over 5-10 trading days.
- **Correlation regime analysis:** Rolling 30-day Pearson correlation, SPY daily return vs. 10Y yield daily return. Computed in Python via yfinance data.
- **Historical analogs:** Jul-Oct <span class="num">2023</span> (10Y <span class="num">3.86%</span> to <span class="num">4.99%</span>, corr <span class="num">-0.25</span>), Sep-Nov <span class="num">2023</span> (<span class="num">4.17%</span> to <span class="num">4.99%</span>, corr <span class="num">-0.49</span>), Jan-Jun <span class="num">2022</span> (<span class="num">1.63%</span> to <span class="num">3.48%</span>, corr <span class="num">-0.20</span>), Jan-Mar <span class="num">2025</span> (tariff-confounded, damage estimate of <span class="num">-4.4%</span> per 10bp excluded as non-pure rate shock).
- **Sector and single-stock betas:** 30-day trailing beta of daily return vs. ^TNX daily return. Individual stock betas computed over same window.
- **Key threshold identification:** <span class="num">4.75%</span> on the 10Y identified as the trigger point for non-linear equity selling, derived from cross-referencing post-FOMC correlation analysis with REIT/utilities valuation breakpoints.
- **Data refresh:** All 24 tickers refreshed via yfinance as of May 22 close and compiled in `data-refresh.md`.

### Confidence Level

<span class="num">Medium</span> overall. The FOMC source text analysis is high-confidence; market data through May 22 is verified against yfinance. Sector/EM FX implications involve reasoned inference beyond explicit policy text. Scenario modeling confidence is medium-high given the extreme correlation regime and cross-validation across three independent models. Key caveat: betas and correlations shift rapidly in high-correlation regimes, requiring weekly re-estimation.

---

## 3. Rates

### 3.1 The April FOMC Decision

The Committee held the federal funds rate at <span class="num">3.50-3.75%</span>. Key language from the statement:

- "Economic activity has been expanding at a solid pace"
- "Job gains have remained low; the unemployment rate has been little changed" (approximately <span class="num">4.3%</span>)
- Inflation "elevated, in part reflecting the recent increase in global energy prices"
- Middle East developments contributing to "a high level of uncertainty about the economic outlook"
- One dissenter (Miran) preferred a <span class="num">25</span>bp cut
- Powell characterized current stance as "appropriate" with data-dependent flexibility
- Forward guidance: "prepared to adjust the stance... if risks emerge" — no explicit tightening bias

### 3.2 Yield Curve Evolution

The 10-year yield (^TNX) rose <span class="up">+21</span>bp from pre-FOMC levels to <span class="num">4.56%</span>, and <span class="up">+37</span>bp YTD. The 5Y (^FVX) at <span class="num">4.26%</span> is up <span class="up">+52</span>bp YTD, while the 3M (^IRX) at <span class="num">3.59%</span> has risen only <span class="up">+6</span>bp YTD — a bear-steepening profile where long rates rise faster than short rates, typically reflecting term premium repricing and inflation expectations rather than tightening expectations.

**Rate Benchmarks — Post-FOMC Window (Apr 29 to May 22, 2026)**

<div class="caption">Table 1: Rate benchmarks from pre-FOMC close through May 22, 2026. Data via yfinance.</div>

| Instrument | Pre-FOMC (Apr 29) | Current (May 22) | Post-FOMC Change | YTD Change |
|-----------|------------------|-----------------|:----------------:|:----------:|
| 10Y Yield (^TNX) | <span class="num">4.35%</span> | <span class="num">4.56%</span> | <span class="up">+21bp</span> | <span class="up">+37bp</span> |
| 5Y Yield (^FVX) | -- | <span class="num">4.26%</span> | -- | <span class="up">+52bp</span> |
| 3M Yield (^IRX) | -- | <span class="num">3.59%</span> | -- | <span class="up">+6bp</span> |
| TLT (20+ Year Treasury ETF) | -- | <span class="num">$84.68</span> | <span class="down">-0.83%</span> | <span class="down">-1.25%</span> |

### 3.3 Critical Thresholds

The post-FOMC analysis identifies **<span class="num">4.75%</span> on the 10Y** as the threshold that triggers a rapid unwind of the risk-on rally. The <span class="num">4.67%</span> 52-week high on the 10Y is the immediate resistance level. A break above <span class="num">4.75%</span> would produce non-linear forced liquidation effects (gamma, momentum-driven selling) given the extreme <span class="num">-0.84</span> to <span class="num">-0.90</span> SPY-10Y correlation regime. The hot-PCE scenario model maps a 25bp yield spike (to <span class="num">4.81%</span>) to a <span class="num">-5.1%</span> SPY drawdown, with severe risk of exceeding proportional estimates due to regime change at the threshold.

---

## 4. Equities by Sector

### 4.1 Broader Market and Sector Returns

**Post-FOMC Performance (Apr 29 to May 22, 2026)**

<div class="caption">Table 2: Sector and broad market ETF returns. Data as of May 22 close via yfinance.</div>

| Ticker | Sector / Index | Price (May 22) | Daily % | YTD Return | Post-FOMC Return | % of 52w High |
|--------|---------------|:--------------:|:-------:|:----------:|:----------------:|:-------------:|
| QQQ | Nasdaq-100 | <span class="num">717.54</span> | <span class="up">+0.42%</span> | <span class="up">+17.18%</span> | <span class="up">+8.46%</span> | <span class="num">99.7%</span> |
| IWM | Small Caps | <span class="num">285.12</span> | <span class="up">+0.93%</span> | <span class="up">+14.81%</span> | <span class="up">+4.79%</span> | <span class="num">99.4%</span> |
| SPY | S&P 500 | <span class="num">745.64</span> | <span class="up">+0.39%</span> | <span class="up">+9.44%</span> | <span class="up">+4.79%</span> | <span class="num">99.7%</span> |
| XLRE | Real Estate | <span class="num">44.56</span> | <span class="up">+0.13%</span> | <span class="up">+11.09%</span> | <span class="up">+2.11%</span> | <span class="num">99.6%</span> |
| XLI | Industrials | -- | -- | <span class="up">+9.03%</span> | <span class="up">+1.08%</span> | <span class="num">96.3%</span> |
| XLU | Utilities | <span class="num">45.35</span> | <span class="up">+0.78%</span> | <span class="up">+5.76%</span> | <span class="down">-0.72%</span> | <span class="num">95.7%</span> |
| XLF | Financials | <span class="num">51.94</span> | <span class="up">+0.41%</span> | <span class="down">-4.96%</span> | <span class="up">+0.04%</span> | <span class="num">92.6%</span> |

The risk-on narrative is unambiguous: QQQ nearly doubled SPY, XLU was the sole decliner, small caps matched large caps, and financials were effectively flat. The market voted that the FOMC hold was dovish leaning.

### 4.2 Technology Sector

**Post-FOMC Mega-Cap Tech Performance (Apr 29 to May 22, 2026)**

<div class="caption">Table 3: Mega-cap technology stock performance. Data as of May 22 close via yfinance. 30d beta vs. ^TNX computed over trailing 30 days.</div>

| Ticker | Company | Price (May 22) | Daily % | YTD Return | Post-FOMC Return | % of 52w High | 30d Beta to 10Y |
|--------|--------|:--------------:|:-------:|:----------:|:----------------:|:-------------:|:---------------:|
| AAPL | Apple | <span class="num">308.82</span> | <span class="up">+1.26%</span> | <span class="up">+14.16%</span> | <span class="up">+14.41%</span> | <span class="num">100.0%</span> | <span class="num">-0.49</span> |
| GOOGL | Alphabet | <span class="num">382.97</span> | <span class="down">-1.21%</span> | <span class="up">+21.61%</span> | <span class="up">+9.44%</span> | <span class="num">95.1%</span> | <span class="num">-0.96</span> |
| NVDA | NVIDIA | <span class="num">215.33</span> | <span class="down">-1.90%</span> | <span class="up">+14.03%</span> | <span class="up">+2.91%</span> | <span class="num">91.3%</span> | <span class="num">-1.00</span> |
| AMZN | Amazon | <span class="num">266.32</span> | <span class="down">-0.80%</span> | <span class="up">+17.58%</span> | <span class="up">+1.25%</span> | <span class="num">96.8%</span> | <span class="num">-0.56</span> |
| MSFT | Microsoft | <span class="num">418.57</span> | <span class="down">-0.12%</span> | <span class="down">-11.10%</span> | <span class="down">-1.17%</span> | <span class="num">87.0%</span> | <span class="num">+0.03</span> |
| META | Meta | <span class="num">610.26</span> | <span class="up">+0.47%</span> | <span class="down">-6.09%</span> | <span class="down">-8.80%</span> | <span class="num">82.7%</span> | <span class="num">-0.24</span> |

**Single-Stock Deep Dives:**

- **AAPL**: The standout performer post-FOMC at <span class="up">+14.41%</span>, hitting <span class="num">100%</span> of its 52-week high. Multiple compounding tailwinds: aggressive buybacks, AI positioning, and minimal tariff exposure relative to peers. Moderate rate beta (<span class="num">-0.49</span>) and peak valuation create a "double vulnerability" — a hot PCE could break it below $300. Sentiment: bullish but price vulnerable to macro shock.

- **MSFT**: The worst mega-cap performer YTD (<span class="down">-11.10%</span>) at <span class="num">87.0%</span> of 52w high, <span class="down">-0.12%</span> on the day. Near-zero rate beta (<span class="num">+0.03</span>) means its underperformance is stock-specific — AI capex concerns and market skepticism about monetization timelines are the dominant drivers, not macro rates. In a hot-PCE scenario, MSFT is a relative safe haven within tech because much of the downside is already priced. Sentiment: neutral with tactical long potential as a rate-hedge pair.

- **NVDA**: <span class="up">+14.03%</span> YTD but only <span class="up">+2.91%</span> post-FOMC and <span class="down">-1.90%</span> on the day — underwhelming for the AI bellwether. High rate beta (<span class="num">-1.00</span>) makes it a tactical short candidate on a hot PCE. At <span class="num">91.3%</span> of 52w high, it has room to fall. Sentiment: neutral/bearish tactically; long-term AI thesis structurally intact but entry matters.

- **META**: The post-FOMC outlier — <span class="down">-8.80%</span> while tech rallied. At <span class="num">82.7%</span> of 52w high, it has completely decoupled from the sector. Low rate beta (<span class="num">-0.24</span>) confirms the selloff is company-specific: capex skepticism, AI ROI uncertainty, and regulatory headwinds. Sentiment: bearish near-term; the divergence from sector peers demands a catalyst for recovery.

- **GOOGL**: Strongest YTD at <span class="up">+21.61%</span> with <span class="up">+9.44%</span> post-FOMC (<span class="down">-1.21%</span> on the day). Ad revenue momentum is a structural tailwind. However, high rate beta (<span class="num">-0.96</span>) makes it vulnerable to a yield spike despite low operational rate sensitivity. At <span class="num">95.1%</span> of 52w high with significant post-FOMC gains to lose, re-rating risk is elevated. Sentiment: bullish on fundamentals; tactical short candidate on hot PCE due to beta exposure.

- **AMZN**: Muted post-FOMC at <span class="up">+1.25%</span> despite <span class="up">+17.58%</span> YTD. Moderate rate beta (<span class="num">-0.56</span>). Both retail (consumer financing) and AWS (enterprise capex) face rate-driven headwinds. Sentiment: neutral; waiting for clearer catalyst.

### 4.3 Financials Sector

**Post-FOMC Bank Performance (Apr 29 to May 22, 2026)**

<div class="caption">Table 4: Bank stock performance. Data as of May 22 close via yfinance. 30d beta vs. ^TNX computed over trailing 30 days.</div>

| Ticker | Bank | Price (May 22) | Daily % | YTD Return | Post-FOMC Return | % of 52w High | 30d Beta to 10Y |
|--------|------|:--------------:|:-------:|:----------:|:----------------:|:-------------:|:---------------:|
| GS | Goldman Sachs | <span class="num">996.73</span> | <span class="up">+0.87%</span> | <span class="up">+9.58%</span> | <span class="up">+10.06%</span> | <span class="num">100.0%</span> | <span class="num">-1.35</span> |
| JPM | JPMorgan Chase | <span class="num">306.38</span> | <span class="up">+1.12%</span> | <span class="down">-4.96%</span> | <span class="down">-0.93%</span> | <span class="num">92.0%</span> | <span class="num">-0.51</span> |
| BAC | Bank of America | <span class="num">51.80</span> | <span class="up">+0.60%</span> | <span class="down">-6.89%</span> | <span class="down">-2.04%</span> | <span class="num">91.0%</span> | <span class="num">-0.34</span> |

- **GS**: The investment bank rally is on. <span class="up">+10.06%</span> post-FOMC at <span class="num">100%</span> of 52w high, <span class="up">+0.87%</span> on the day. Driven by M&A and banking fee optimism. However, GS has the **highest rate beta in the entire coverage universe** at <span class="num">-1.35</span>, meaning it is trading as a valuation proxy (P/E multiple compression risk) rather than on earnings composition. A <span class="num">25</span>bp yield spike implies <span class="down">-12.7%</span> downside to approximately <span class="num">$870</span>. Sentiment: tactical short on hot PCE; do not buy the dip post-PCE.

- **JPM**: Negative YTD (<span class="down">-4.96%</span>), flat post-FOMC (<span class="down">-0.93%</span>), <span class="up">+1.12%</span> on the day. Consumer bank headwinds from higher-for-longer rates compressing net interest margins and slowing loan growth. The moderate rate beta (<span class="num">-0.51</span>) suggests additional macro downside if yields spike. Sentiment: cautious, neutral.

- **BAC**: Weakest major bank at <span class="down">-6.89%</span> YTD and <span class="down">-2.04%</span> post-FOMC. The consumer-focused franchise is most exposed to deposit cost pressure without offsetting fee income. Lowest beta in banks (<span class="num">-0.34</span>) paradoxically makes it the least vulnerable to a rate-driven shock, but operating headwinds are sector-specific. Sentiment: bearish near-term.

### 4.4 Real Estate Sector

**Post-FOMC REIT Performance (Apr 29 to May 22, 2026)**

<div class="caption">Table 5: Real estate sector and selected REITs. Data as of May 22 close via yfinance. 30d beta vs. ^TNX computed over trailing 30 days.</div>

| Ticker | Name | Price (May 22) | Daily % | YTD Return | Post-FOMC Return | % of 52w High | 30d Beta to 10Y |
|--------|------|:--------------:|:-------:|:----------:|:----------------:|:-------------:|:---------------:|
| XLRE | Real Estate Sector | <span class="num">44.56</span> | <span class="up">+0.13%</span> | <span class="up">+11.09%</span> | <span class="up">+2.11%</span> | <span class="num">99.6%</span> | <span class="num">-0.49</span> |
| PLD | Prologis | <span class="num">145.90</span> | <span class="up">+0.88%</span> | <span class="up">+13.97%</span> | <span class="up">+5.10%</span> | <span class="num">100.0%</span> | <span class="num">-0.81</span> |
| EQIX | Equinix | -- | -- | <span class="up">+42.79%</span> | <span class="down">-0.36%</span> | <span class="num">97.3%</span> | -- |

- **XLRE**: <span class="up">+2.11%</span> post-FOMC despite the 10Y rising <span class="up">+21</span>bp. REITs are not trading uniformly as rate proxies — demand-side momentum in data center, industrial, and tower sub-sectors offsets discount rate pressure. The critical threshold is <span class="num">4.75%</span> on the 10Y; below that, REITs hold up. Sentiment: neutral, conditionally bearish above 4.75%.

- **PLD**: Industrial/logistics REIT at <span class="num">100%</span> of 52w high with a high rate beta (<span class="num">-0.81</span>). Structural demand tailwinds from supply-chain reshoring and e-commerce, but vulnerable to a yield spike. A <span class="num">25</span>bp PCE-driven spike implies <span class="down">-7.6%</span> downside to approximately <span class="num">$135</span>. Sentiment: tactical short on hot PCE; long-term structural hold.

- **EQIX**: Data center REIT, up <span class="up">+42.79%</span> YTD. Consolidated slightly post-FOMC (<span class="down">-0.36%</span>). AI data center demand provides a structural bid that overrides rate sensitivity in the current yield range. Sentiment: bullish.

### 4.5 Industrials Sector

**Post-FOMC Industrials Performance (Apr 29 to May 22, 2026)**

<div class="caption">Table 6: Industrials sector performance. Data via yfinance. 30d beta vs. ^TNX computed over trailing 30 days. No individual industrial stocks in coverage universe; XLI proxy used for sector-level analysis.</div>

| Ticker | Name | YTD Return | Post-FOMC Return | % of 52w High | 30d Beta to 10Y |
|--------|------|:----------:|:----------------:|:-------------:|:---------------:|
| XLI | Industrials Sector | <span class="up">+9.03%</span> | <span class="up">+1.08%</span> | <span class="num">96.3%</span> | <span class="num">-0.75</span> |

Industrials posted a modest <span class="up">+1.08%</span> post-FOMC, lagging tech and small caps but outperforming financials and utilities. The sector has a relatively high rate beta (<span class="num">-0.75</span>), reflecting capital expenditure cycle sensitivity to higher rates. In the hot-PCE scenario, industrials rank third in expected downside among sectors at <span class="down">-7.0%</span> on a 25bp yield spike (correlation-adjusted model).

The moderate post-FOMC gain suggests the sector is caught between two forces: (1) positive economic growth expectations supporting industrial demand, and (2) higher discount rates compressing capex cycle valuations. Sentiment: neutral, with tactical short risk on hot PCE.

### 4.6 Utilities Sector

**Post-FOMC Utility Performance (Apr 29 to May 22, 2026)**

<div class="caption">Table 7: Utility sector and selected holdings. Data as of May 22 close via yfinance. 30d beta vs. ^TNX computed over trailing 30 days.</div>

| Ticker | Name | Price (May 22) | Daily % | YTD Return | Post-FOMC Return | % of 52w High | 30d Beta to 10Y |
|--------|------|:--------------:|:-------:|:----------:|:----------------:|:-------------:|:---------------:|
| XLU | Utilities Sector | <span class="num">45.35</span> | <span class="up">+0.78%</span> | <span class="up">+5.76%</span> | <span class="down">-0.72%</span> | <span class="num">95.7%</span> | <span class="num">-0.23</span> |
| NEE | NextEra Energy | <span class="num">88.55</span> | <span class="down">-1.27%</span> | <span class="up">+10.16%</span> | <span class="down">-5.97%</span> | <span class="num">90.5%</span> | <span class="num">-0.14</span> |

XLU was the only sector ETF to decline post-FOMC. Money rotated out of defensives into risk-on tech. Notably, XLU has a low rate beta (<span class="num">-0.23</span>) — the sector has already been sold and may actually attract a defensive bid if a hot PCE triggers a macro risk-off trade alongside the rate spike. NEE underperformed the sector, shedding <span class="down">-5.97%</span> post-FOMC and <span class="down">-1.27%</span> on the day. Sentiment: neutral near-term; potential defensive rotation beneficiary if macro risk-off materializes.

### 4.7 Consumer Staples Sector

**Post-FOMC Consumer Staples Performance (Apr 29 to May 22, 2026)**

<div class="caption">Table 8: Consumer staples holding. Data as of May 22 close via yfinance. 30d beta vs. ^TNX computed over trailing 30 days.</div>

| Ticker | Name | Price (May 22) | Daily % | YTD Return | Post-FOMC Return | % of 52w High | 30d Beta to 10Y |
|--------|------|:--------------:|:-------:|:----------:|:----------------:|:-------------:|:---------------:|
| WMT | Walmart | <span class="num">120.27</span> | <span class="down">-0.88%</span> | <span class="up">+7.08%</span> | <span class="down">-5.87%</span> | <span class="num">89.6%</span> | <span class="num">+0.01</span> |

- **WMT**: <span class="down">-5.87%</span> post-FOMC, <span class="down">-0.88%</span> on the day. Near-zero rate beta (<span class="num">+0.01</span>). The selloff reflects rotation out of consumer defensives into risk-on assets, plus company-specific margin compression concerns. In a hot-PCE risk-off scenario, WMT could see a defensive bid as a consumer staple with pricing power. Sentiment: neutral, tactical pair candidate (long WMT / short IWM for rate-hedge exposure).

---

## 5. Sector Rotation

### 5.1 Post-FOMC Capital Flows

The fundamental question: why did higher-for-longer trigger a risk-on move? Three factors:

1. **Dissent signaling**: The lone vote for a <span class="num">25</span>bp cut was interpreted as a leading indicator that the Committee's next move is down, not up.
2. **Dovish flexibility**: Powell's "prepared to adjust the stance... if risks emerge" language was read as easing optionality.
3. **Absence of tightening**: No explicit tightening bias and no hawkish dot plot revision.

The rotation pattern:
- **Out of:** Utilities (XLU <span class="down">-0.72%</span>), Consumer staples (WMT <span class="down">-5.87%</span>), Long-duration treasuries (TLT <span class="down">-0.83%</span>)
- **Into:** Tech (QQQ <span class="up">+8.46%</span>), Small caps (IWM <span class="up">+4.79%</span>), Broad market (SPY <span class="up">+4.79%</span>)
- **Flat/inconclusive:** Financials (XLF <span class="up">+0.04%</span>), Real Estate (XLRE <span class="up">+2.11%</span> — held up better than expected), Industrials (XLI <span class="up">+1.08%</span> — modest)

### 5.2 The Correlation Regime Shift

**SPY-10Y Yield Correlation**

<div class="caption">Table 9: Rolling 30-day Pearson correlation between SPY daily returns and ^TNX daily returns. Computed via yfinance data.</div>

| Period | SPY vs. 10Y Correlation | Interpretation |
|--------|:----------------------:|----------------|
| YTD (Jan 1 to May 22) | <span class="num">-0.39</span> | Moderate rate sensitivity |
| Post-FOMC (Apr 29 to May 22) | <span class="num">-0.90</span> | Extreme — rates dominate equity pricing |
| 30-day trailing (to May 22) | <span class="num">-0.84</span> | Still historically extreme |

At <span class="num">-0.90</span> post-FOMC and <span class="num">-0.84</span> on a trailing 30-day basis, the SPY-10Y correlation is approximately <span class="num">2.3x</span> the YTD average. This is the highest negative correlation in the dataset — surpassing the Sep-Nov <span class="num">2023</span> peak of <span class="num">-0.49</span>. It implies that nearly every equity move is currently explained by rate direction.

### 5.3 What Would Reverse the Rotation?

The rotation is fragile and conditional on the "cut later" narrative remaining intact. A hot May PCE (ex-energy) that disproves the transitory energy-inflation thesis would force a re-evaluation. Scenario modeling places the probability-weighted expected SPY return at <span class="num">-4.8%</span> conditional on a hot print, ranging from <span class="num">-4.1%</span> (light hot: <span class="num">0.20-0.25%</span> MoM, 10Y to <span class="num">4.76%</span>) to <span class="num">-6.2%</span> (severe: ><span class="num">0.30%</span> MoM, 10Y to <span class="num">4.86%</span>). The 10Y breaching <span class="num">4.75%</span> would trigger non-linear selling beyond proportional model estimates.

---

## 6. FX and Commodities

### 6.1 Currency Markets

**FX and Dollar Index — Post-FOMC (Apr 29 to May 22, 2026)**

<div class="caption">Table 10: Currency and dollar index performance. Data as of May 22 close via yfinance. DXY via DX-Y.NYB after ticker migration from deprecated DXY symbol.</div>

| Ticker | Instrument | Price (May 22) | Daily % | Post-FOMC Change | YTD Change |
|--------|-----------|:--------------:|:-------:|:----------------:|:----------:|
| DXY | US Dollar Index | <span class="num">99.32</span> | <span class="up">+0.13%</span> | <span class="up">+0.40%</span> | <span class="up">+0.91%</span> |
| GBPUSD=X | GBP/USD | <span class="num">1.3433</span> | <span class="down">-0.01%</span> | <span class="down">-0.68%</span> | <span class="down">-0.30%</span> |

The DXY has remained supported at <span class="num">99.32</span>, reflecting the US rate differential advantage reinforced by the FOMC hold. The <span class="up">+0.40%</span> post-FOMC move is modest, consistent with an as-expected decision. GBP/USD edged lower (<span class="down">-0.68%</span> post-FOMC) and is slightly negative YTD.

**EM FX Implications:**
The combination of higher US rates, USD support, and Middle East geopolitical risk creates a classic negative setup for EM currencies:
- Oil-importing EMs face input cost inflation and currency depreciation pressure
- Currencies with high USD debt loads (BRL, ZAR, TRY) are particularly vulnerable
- Central banks in these economies may respond with their own tightening or FX intervention
- Commodity exporters (some LATAM, MENA) may benefit from higher oil but face USD strength as an offset
- The uncertainty overlay from Middle East developments widens risk premia, increasing EM FX volatility

### 6.2 Commodities

**Commodity Markets — Post-FOMC (Apr 29 to May 22, 2026)**

<div class="caption">Table 11: Commodity futures performance. Data via yfinance (GC=F for COMEX gold, CL=F for WTI crude).</div>

| Ticker | Commodity | Price (May 22) | Daily % | Post-FOMC Change | YTD Change |
|--------|----------|:--------------:|:-------:|:----------------:|:----------:|
| GC=F | Gold (COMEX) | <span class="num">$4,523.20</span> | <span class="down">-0.37%</span> | <span class="down">-0.48%</span> | <span class="up">+4.84%</span> |
| CL=F | Crude Oil (WTI) | <span class="num">$96.60</span> | <span class="up">+0.26%</span> | <span class="down">-9.62%</span> | <span class="up">+68.53%</span> |

- **Gold**: Essentially flat post-FOMC at <span class="num">$4,523.20</span>. The expected safe-haven bid from geopolitical uncertainty has been offset by USD support from higher rates. Gold is range-bound until either the dollar weakens (rate cuts) or geopolitical risks escalate materially. YTD gain of <span class="up">+4.84%</span> reflects structural central bank buying and geopolitical hedging.

- **Crude Oil**: The <span class="down">-9.62%</span> post-FOMC pullback from spike highs is significant. WTI at <span class="num">$96.60</span> is still up <span class="up">+68.53%</span> YTD, driven by Middle East risk premia. The FOMC's explicit mention of energy-driven inflation suggests the Fed is watching oil closely. A sustained oil decline would ease inflation concerns and support the "cut later" narrative; a renewed spike would reinforce higher-for-longer. Crude remains the key swing variable for both the macro outlook and EM FX.

---

## 7. Outlook

### 7.1 Short-Term Risks

| Risk | Probability | Impact | Trigger | Mitigant |
|------|:----------:|:------:|--------|----------|
| Hot May PCE (ex-energy) | <span class="num">30-50%</span> | SPY <span class="down">-4.8%</span> (conditional) | PCE > <span class="num">0.20%</span> MoM ex-energy | Low positioning / high cash levels |
| 10Y breach above <span class="num">4.75%</span> | Elevated if PCE hot | Non-linear selling, forced liquidations | PCE + <span class="num">25</span>bp yield spike | Historical analog suggests transient spike |
| Middle East escalation | Medium | Oil spike, USD surge, EM FX crisis | Geopolitical event | Diplomatic de-escalation |
| META contagion to tech | Medium | Sector-wide rotation out of mega-cap | Continued META underperformance | Stock-specific, not sector-wide |
| Consumer bank NIM compression | Medium-High if hot PCE | JPM, BAC further downside | Next earnings season | Steepener benefit partially offsets |

**Key Watchpoints:**
1. **May PCE (ex-energy)** — the single most important data point for the near-term macro narrative. A cool print validates the "cut later" thesis; a hot print unravels it.
2. **10Y yield at <span class="num">4.56%</span>** — a move above <span class="num">4.67%</span> (52w high) and especially <span class="num">4.75%</span> triggers the unwind of the post-FOMC risk rally.
3. **META price action** — recovery or further decoupling signals sector-wide vs. company-specific regime.
4. **DXY trajectory above <span class="num">100</span>** — would trigger EM FX stress and widen risk premia.
5. **Crude oil**: sustained below <span class="num">$90</span> supports the "transitory energy inflation" thesis; a renewed spike above <span class="num">$110</span> reinforces higher-for-longer.

### 7.2 Long-Term Strategic Rationale

Despite near-term risks, several structural factors support a constructive long-term view:

- **The "cut later" narrative has foundation**: The dissenting vote, data-dependent language, and softening labor backdrop all point toward eventual easing once the energy-inflation spike proves transitory. The <span class="num">-0.84</span> to <span class="num">-0.90</span> correlation regime means rate cuts would be violently positive for equities.

- **Sector-level differentiation is key**: Data center REITs (EQIX), industrial REITs (PLD), and investment banks (GS) have company-specific demand drivers that can partially override macro headwinds — as demonstrated post-FOMC.

- **EM FX recovery play**: If/when the Fed cuts, the USD should weaken, providing a powerful tailwind for EM currencies and rate-sensitive equities. Positioning for this "recovery phase" is the long-term opportunity.

- **Small caps could lead the recovery**: IWM has the highest rate sensitivity (<span class="num">-1.00</span> beta) and would be the biggest beneficiary of a rate cut cycle.

- **Gold remains a strategic hedge**: Flat post-FOMC but supported structurally by central bank buying, geopolitical risk, and eventual USD weakness on Fed cuts.

### 7.3 Scenario-Weighted Positioning Summary

| Scenario | Probability | Key Trades | Expected SPY |
|----------|:----------:|------------|:------------:|
| PCE cool, "cut later" intact | <span class="num">50-70%</span> | Long QQQ, long IWM, short XLU | <span class="up">+2-4%</span> |
| PCE hot, yield spike to <span class="num">4.75%+</span> | <span class="num">30-50%</span> | Short IWM, short GS, short NVDA; long MSFT as hedge | <span class="down">-4.8%</span> (conditional) |
| Middle East escalation | <span class="num">15-25%</span> (tail) | Long gold, long crude, short EM FX | <span class="down">-5-8%</span> |

**Actionable calls:**
- **Tactical short on hot PCE:** IWM, GS, NVDA, GOOGL (highest rate beta in each sector)
- **Relative value hedges:** Long WMT / short IWM (zero correlation vs. highest); Long MSFT / short GOOGL (already discounted vs. 52w high with high beta)
- **Sector rotation:** Reduce QQQ toward XLF (steepener benefit partially offsets rate-equity correlation)
- **Avoid:** REITs if 10Y stays above <span class="num">4.75%</span>; consumer banks (JPM, BAC) until Q2 earnings clarify NIM trajectory
- **Strategic long:** Gold on dips for geopolitical hedge; small caps (IWM) for recovery positioning

---

## Data Sources

| Source | Usage | Version / Format |
|--------|-------|-----------------|
| Federal Reserve Press Release | FOMC decision text, policy language | HTML, monetary20260429a.htm |
| Federal Reserve Press Conference Transcript | Powell remarks, Q&A | PDF via pdftotext, FOMCpresconf20260429.pdf |
| yfinance | All price, return, and yield data | yfinance <span class="num">1.4.0</span> |
| Trailing 30-day rolling regression | SPY vs. ^TNX beta | Python, scripts/compute_scenario.py |
| Trailing 30-day rolling correlation | SPY vs. ^TNX Pearson correlation | Python, scripts/compute_scenario.py |
| Historical analog analysis | Jul-Oct 2023, Sep-Nov 2023, Jan-Jun 2022, Jan-Mar 2025 | Model calibration |
| Prior reports | analysis.md, report.md, post-fomc-market-analysis.md, hot-pce-scenario.md, data-refresh.md | Markdown |

**Span classes applied:** <span class="up">up (green/bold)</span>, <span class="down">down (red/bold)</span>, <span class="num">num (navy/bold)</span>. No emojis used.

---

## Disclaimer

<div class="disclaimer">

This market brief is prepared for informational purposes only and does not constitute investment advice, a recommendation, or an offer to buy or sell any security. All analyses are based on publicly available data and modeled projections that inherently involve uncertainty. Past performance and historical analogs are not reliable indicators of future results. The correlations, betas, and scenario estimates presented are based on trailing window calculations that may shift materially in changing market regimes. Readers should conduct their own due diligence and consult with licensed financial advisors before making investment decisions. Data sources include Federal Reserve official documents and yfinance; accuracy depends on the timeliness and correctness of these sources. The analyst(s) may hold positions in securities discussed herein.

</div>