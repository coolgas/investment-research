---
date: 2026-05-24
event: fomc-april-2026
type: market-brief
asset_classes:
  - equities
  - rates
  - fx
  - commodities
tickers:
  - SPY
  - QQQ
  - IWM
  - ^TNX
  - TLT
  - XLU
  - XLF
  - XLRE
  - AAPL
  - MSFT
  - NVDA
  - META
  - GOOGL
  - AMZN
  - JPM
  - GS
  - BAC
  - PLD
  - NEE
  - WMT
  - DX-Y.NYB
  - GBPUSD=X
  - GC=F
  - CL=F
tags:
  - fomc-april-2026
  - rate-hold
  - risk-on-rotation
  - higher-for-longer
  - yield-correlation
  - hot-pce-scenario
  - sector-analysis
---

# Market Brief: April 2026 FOMC — Rate Hold, Risk-On Rotation, and the Hot PCE Tail Risk

**Report Date:** May 24, 2026  
**Data As Of:** May 22, 2026 close (GBP/USD: May 24, 2026)  
**Event:** FOMC April 29, 2026 — Rate Hold at 3.50–3.75%  
**Sources:** analysis.md, report.md, post-fomc-market-analysis.md, hot-pce-scenario.md, data-refresh.md  

---

## Executive Summary

The FOMC held rates at 3.50–3.75% on April 29, 2026, in line with consensus. One dissenter preferred a 25bp cut. The Statement cited solid economic growth, softening but stable labor (unemployment ~4.3%), and elevated inflation driven by global energy prices and Middle East uncertainty.

The market read the decision as a **dovish hold** — focusing on the dissenting vote for a cut, flexible forward guidance, and absence of tightening bias. This triggered a **risk-on rotation** rather than the defensive posture the "higher-for-longer" narrative would suggest:

- QQQ surged <span class="up">+8.46%</span> post-FOMC, nearly doubling SPY's <span class="up">+4.79%</span>
- Utilities (XLU) fell <span class="down">-0.72%</span> — the only sector to decline
- Financials (XLF) flat at <span class="up">+0.04%</span>
- The SPY–10Y yield correlation tightened to <span class="num">-0.90</span> post-FOMC, 2.3x the YTD average of <span class="num">-0.39</span>

**Key risk:** The post-FOMC risk rally rests on the "hold now, cut later" narrative. A hot May PCE (ex-energy) print would unravel this, potentially driving the 10Y above 4.75% and triggering a rapid equity unwind. Our scenario model estimates a <span class="down">-4.8%</span> expected SPY drawdown conditional on a hot PCE release.

---

## Methodology

This brief synthesizes four analytical layers:

1. **Fundamental analysis** (analysis.md, report.md): Extracted from the April 29 FOMC Statement and Powell press conference transcript via direct text extraction (HTML stripping, pdftotext). Lens applied to rate-sensitive equities and EM FX.

2. **Post-FOMC market analysis** (post-fomc-market-analysis.md): Quantitative assessment of price action from Apr 29 (FOMC date) through May 22. Uses yfinance 1.4.0 for price data. Computes YTD, post-FOMC, and daily returns. SPY–10Y correlations computed over trailing 30 calendar days and the full post-FOMC window (16 trading days).

3. **Scenario analysis** (hot-pce-scenario.md): Three-model framework for a hot May PCE downside scenario:
   - **30-day beta regression:** SPY daily return vs 10Y yield daily return. Current beta: <span class="num">-0.5374</span> (1% yield move → -0.54% SPY same-day).
   - **Historical analog scaling:** Sep-Nov 2023 (10Y 4.17% → 4.99%, SPY -10.0%) used as baseline. Scaled by correlation ratio (current -0.84 / analog -0.49 = 1.71x multiplier).
   - **Multi-day compound model:** Sustained repricing over 5–10 days compounds single-day damage by 1.5x–2.0x.
   - **Primary model** is the correlation-adjusted estimate. Sector and stock betas computed over trailing 30 days vs ^TNX daily returns.

4. **Data refresh** (data-refresh.md): yfinance pull for 24 tickers across indices, sectors, stocks, commodities, and FX as of May 22 close.

**Date conventions:** YTD base = Jan 2, 2026 (Jan 1 holiday). Post-FOMC base = Apr 29, 2026. All percentages computed from adjusted close prices (auto_adjust=True).

---

## Rates

### Yield Benchmarks

| Instrument | Pre-FOMC | Current | Change | YTD Change |
|------------|---------|---------|--------|-----------|
| 10Y Yield (^TNX) | 4.35% | <span class="num">4.56%</span> | <span class="up">+21bp</span> | <span class="up">+37bp</span> |
| 5Y Yield (^FVX) | — | <span class="num">4.26%</span> | — | <span class="up">+52bp</span> |
| 3M Yield (^IRX) | — | <span class="num">3.59%</span> | — | <span class="up">+6bp</span> |
| TLT (20Y+ Treasury) | — | <span class="num">$84.68</span> | — | <span class="down">-1.25%</span> |

### Fed Decision & Forward Guidance

**Decision:** Rate hold at 3.50–3.75%, as expected. One dissenter (Miran) preferred a 25bp cut — the first dissent signaling internal pressure for easing.

**Key language from the Statement:**
- "Economic activity has been expanding at a solid pace"
- "Job gains have remained low" and "unemployment rate has been little changed" (~4.3%)
- Inflation "elevated, in part reflecting the recent increase in global energy prices"
- Middle East developments contributing to "a high level of uncertainty about the economic outlook"

**Forward guidance:** The Committee reiterated its data-dependent approach. Chair Powell described the current stance as "appropriate" and noted the Fed is "prepared to adjust the stance of policy if risks emerge." This flexible language leaves the door open for cuts if inflation moderates, reinforcing the "hold now, cut later" market narrative.

**Key date:** Next FOMC meeting: June 16–17, 2026. The May PCE release (scheduled late May/early June) will be the most important data point between meetings.

### Yield Curve Context

The 10Y has risen <span class="up">+37bp</span> YTD and <span class="up">+21bp</span> since the FOMC. The 5Y has steepened more sharply (<span class="up">+52bp</span> YTD), reflecting the repricing of intermediate-term rate expectations. The 10Y's 52-week high stands at <span class="num">4.67%</span> — current levels at <span class="num">4.56%</span> leave limited room before breaching resistance. The post-FOMC risk-on rally occurred despite the yield backup, which is analytically unusual and suggests the market is looking through near-term inflation toward a cut later this year.

---

## Equities by Sector

### Market Context

The post-FOMC period (Apr 29 → May 22) saw a powerful risk-on rotation. SPY at <span class="num">$745.64</span> is <span class="num">99.7%</span> of its 52-week high. The dominant macro variable is the SPY–10Y correlation, which tightened to <span class="num">-0.90</span> post-FOMC (vs YTD average -0.39). At these correlation levels, rate direction explains nearly every equity move.

### Broad Market

| Ticker | Name | Price | YTD Return | Post-FOMC Return | % of 52w High |
|--------|------|-------|-----------|-----------------|--------------|
| SPY | S&P 500 | <span class="num">745.64</span> | <span class="up">+9.44%</span> | <span class="up">+4.79%</span> | <span class="num">99.7%</span> |
| QQQ | Nasdaq-100 | <span class="num">717.54</span> | <span class="up">+17.18%</span> | <span class="up">+8.46%</span> | <span class="num">99.7%</span> |
| IWM | Small Caps | <span class="num">285.12</span> | <span class="up">+14.81%</span> | <span class="up">+4.79%</span> | <span class="num">99.4%</span> |

**QQQ** was the standout, gaining <span class="up">+8.46%</span> post-FOMC — nearly double the S&P 500. At <span class="num">99.7%</span> of its 52-week high, it is near all-time highs. The tech-led risk rally indicates the market's conviction that rates will move lower.

**IWM** matched the S&P's return at <span class="up">+4.79%</span> post-FOMC despite being the most rate-sensitive broad index (30-day rate beta: <span class="num">-1.00</span>). Small caps' floating-rate debt exposure and lack of pricing power make them the most vulnerable to any negative rate surprise.

### Sector ETFs

| Ticker | Sector | Price | YTD Return | Post-FOMC Return | % of 52w High | 30d Rate Beta |
|--------|--------|-------|-----------|-----------------|--------------|:-------------:|
| XLRE | Real Estate | <span class="num">44.56</span> | <span class="up">+11.09%</span> | <span class="up">+2.11%</span> | <span class="num">99.6%</span> | <span class="down">-0.49</span> |
| XLU | Utilities | <span class="num">45.35</span> | <span class="up">+5.76%</span> | <span class="down">-0.72%</span> | <span class="num">95.7%</span> | <span class="down">-0.23</span> |
| XLF | Financials | <span class="num">51.94</span> | <span class="down">-4.96%</span> | <span class="up">+0.04%</span> | <span class="num">92.6%</span> | <span class="down">-0.27</span> |

**XLRE (Real Estate, +2.11% post-FOMC):** REITs held up well despite the 10Y rising 21bp. This is not a broad-based rate-proxy trade — data center, industrial, and tower REITs have enough demand-side momentum (AI infrastructure, logistics, telco capex) to offset discount rate pressure. The threshold for a sector-wide REIT selloff is <span class="num">4.75%</span> on the 10Y. Below that, REITs with secular demand drivers can hold.

**XLU (Utilities, -0.72% post-FOMC):** The only sector to decline post-FOMC. Money rotated out of defensives into risk assets. Utilities' 30-day rate beta is low (<span class="num">-0.23</span>) because they already sold off. In a hot-PCE risk-off scenario, utilities could actually see defensive buying that partially offsets rate-driven headwinds.

**XLF (Financials, +0.04% post-FOMC):** Underwhelming given the steepening yield curve. The yield curve steepener (short rates steady, long rates rising) typically benefits bank net interest margins, but consumer banks (JPM, BAC) face loan growth pressure and deposit cost compression. The sector-wide flat return reflects the divergence between investment banks (GS positive) and consumer banks (JPM, BAC negative).

### Single-Stock Deep Dives

#### Mega-Cap Tech

| Ticker | Price | YTD Return | Post-FOMC Return | % of 52w High | 30d Rate Beta |
|--------|-------|-----------|-----------------|--------------|:-------------:|
| AAPL | <span class="num">308.82</span> | <span class="up">+14.16%</span> | <span class="up">+14.41%</span> | <span class="num">100.0%</span> | <span class="down">-0.49</span> |
| GOOGL | <span class="num">382.97</span> | <span class="up">+21.61%</span> | <span class="up">+9.44%</span> | <span class="num">95.1%</span> | <span class="down">-0.96</span> |
| AMZN | <span class="num">266.32</span> | <span class="up">+17.58%</span> | <span class="up">+1.25%</span> | <span class="num">96.8%</span> | <span class="down">-0.56</span> |
| NVDA | <span class="num">215.33</span> | <span class="up">+14.03%</span> | <span class="up">+2.91%</span> | <span class="num">91.3%</span> | <span class="down">-1.00</span> |
| MSFT | <span class="num">418.57</span> | <span class="down">-11.10%</span> | <span class="down">-1.17%</span> | <span class="num">77.7%</span> | <span class="num">+0.03</span> |
| META | <span class="num">610.26</span> | <span class="down">-6.09%</span> | <span class="down">-8.80%</span> | <span class="num">82.7%</span> | <span class="down">-0.24</span> |

**AAPL (+14.41% post-FOMC):** The standout performer. At <span class="num">100%</span> of its 52-week high, Apple is compounding multiple tailwinds: aggressive buybacks, AI positioning through Apple Intelligence, and no direct tariff exposure relative to hardware peers. The combination of peak valuation and moderate rate beta (<span class="num">-0.49</span>) creates a "double vulnerability" — a 25bp yield spike would imply a <span class="down">-4.6%</span> move toward <span class="num">$295</span>, its first significant break below <span class="num">$300</span> since the post-FOMC run.

**GOOGL (+9.44% post-FOMC):** Strong post-FOMC performance driven by low rate sensitivity relative to other mega-cap tech and ad revenue momentum. However, at a 30-day rate beta of <span class="num">-0.96</span>, GOOGL is effectively a rate proxy. A hot PCE scenario implies <span class="down">-9.0%</span> downside on a 25bp spike. At <span class="num">95.1%</span> of 52w high, there is post-FOMC momentum to lose.

**META (-8.80% post-FOMC):** The decoupling story. While mega-cap tech broadly rallied, META sold off <span class="down">-8.80%</span> — the worst performer in the universe. At <span class="num">82.7%</span> of 52-week high, it is in a different regime than peers (95–100%). The selloff is stock-specific: AI capex spending skepticism, ROI uncertainty on the metaverse pivot, and possibly regulatory overhang. Low rate beta (<span class="num">-0.24</span>) means META's trajectory is driven by company-specific factors, not macro rates.

**MSFT (-11.10% YTD, -1.17% post-FOMC):** The worst-performing mega-cap tech YTD. AI capex concerns (heavy spending on infrastructure with uncertain near-term ROI) have weighed on sentiment. Rate beta is effectively zero (<span class="num">+0.03</span>), making MSFT a portfolio hedge against rate-driven drawdowns — it is trading on stock-specific factors. At <span class="num">77.7%</span> of 52-week high, much of the rate-driven downside may already be priced in.

**NVDA (+2.91% post-FOMC):** Modest post-FOMC recovery, still only <span class="num">91.3%</span> of 52w high. The high negative rate beta (<span class="num">-1.00</span>) reflects long-duration growth profile. A 25bp spike implies <span class="down">-9.4%</span> downside toward <span class="num">$195</span>, approaching post-FOMC lows.

**AMZN (+1.25% post-FOMC):** Muted relative to mega-cap peers. Moderate rate beta (<span class="num">-0.56</span>). At <span class="num">96.8%</span> of 52w high.

#### Banks

| Ticker | Price | YTD Return | Post-FOMC Return | % of 52w High | 30d Rate Beta |
|--------|-------|-----------|-----------------|--------------|:-------------:|
| GS | <span class="num">996.73</span> | <span class="up">+9.58%</span> | <span class="up">+10.06%</span> | <span class="num">100.0%</span> | <span class="down">-1.35</span> |
| JPM | <span class="num">306.38</span> | <span class="down">-4.96%</span> | <span class="down">-0.93%</span> | <span class="num">92.0%</span> | <span class="down">-0.51</span> |
| BAC | <span class="num">51.80</span> | <span class="down">-6.89%</span> | <span class="down">-2.04%</span> | <span class="num">91.0%</span> | <span class="down">-0.34</span> |

**GS (+10.06% post-FOMC, -1.35 rate beta):** The most rate-sensitive stock in the universe. At <span class="num">100%</span> of 52w high and $996.73, GS is trading as a valuation proxy — the negative beta suggests P/E multiple compression risk outweighs the investment bank earnings benefit from higher rates. This is anomalous: investment banks typically benefit from higher rates through fixed-income trading revenue. A 25bp spike implies <span class="down">-12.7%</span> downside toward <span class="num">$870</span>, its first sub-$900 level in over a month.

**JPM (-0.93% post-FOMC):** Consumer bank headwinds persist. Higher-for-longer pressures loan growth and deposit costs without the fee-income offset that benefits GS. At <span class="num">92.0%</span> of 52w high.

**BAC (-2.04% post-FOMC):** Weakest major bank. Same consumer bank dynamics as JPM, but with higher exposure to rate-sensitive consumer credit. At <span class="num">91.0%</span> of 52w high.

#### Other Holdings

| Ticker | Price | YTD Return | Post-FOMC Return | % of 52w High | 30d Rate Beta |
|--------|-------|-----------|-----------------|--------------|:-------------:|
| PLD | <span class="num">145.90</span> | <span class="up">+13.97%</span> | <span class="up">+5.10%</span> | <span class="num">100.0%</span> | <span class="down">-0.81</span> |
| NEE | <span class="num">88.55</span> | <span class="up">+10.16%</span> | <span class="down">-5.97%</span> | <span class="num">90.5%</span> | <span class="down">-0.14</span> |
| WMT | <span class="num">120.27</span> | <span class="up">+7.08%</span> | <span class="down">-5.87%</span> | <span class="num">89.6%</span> | <span class="num">+0.01</span> |

**PLD (+5.10% post-FOMC):** Industrial/logistics REIT strength driven by structural demand from supply chain reshoring and e-commerce. At <span class="num">100%</span> of 52w high with a rate beta of <span class="num">-0.81</span> — a hot PCE scenario implies <span class="down">-7.6%</span> downside. Do not buy the dip immediately post-PCE; a mean-reversion to the 50-day moving average implies further downside even without the trigger.

**NEE (-5.97% post-FOMC):** Sold off as part of the utility sector rotation out of defensives. Low rate beta (<span class="num">-0.14</span>) means the selloff was sector-rotation, not rate-driven. Renewable energy project financing may face headwinds from higher long-term rates, but the low beta suggests this impact is already discounted.

**WMT (-5.87% post-FOMC):** Consumer defensive rotation out. Rate beta is effectively zero (<span class="num">+0.01</span>), making WMT a pure stock-specific story. Consumer margin compression from higher input costs and a softening labor market are the relevant headwinds. In a hot-PCE scenario, WMT is a relative value hedge (long WMT / short high-beta names).

---

## FX & Commodities

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|-------|-----|-----------|
| DX-Y.NYB | US Dollar Index (DXY) | <span class="num">99.32</span> | <span class="up">+0.13%</span> | <span class="up">+0.91%</span> | <span class="up">+0.40%</span> |
| GBPUSD=X | GBP/USD | <span class="num">1.3455</span> | <span class="up">+0.17%</span> | <span class="down">-0.14%</span> | <span class="down">-0.51%</span> |
| GC=F | Gold (COMEX Futures) | <span class="num">4,523.20</span> | <span class="down">-0.37%</span> | <span class="up">+4.84%</span> | <span class="down">-0.48%</span> |
| CL=F | Crude Oil (WTI Futures) | <span class="num">96.60</span> | <span class="up">+0.26%</span> | <span class="up">+68.53%</span> | <span class="down">-9.62%</span> |

### DXY (US Dollar Index)

The dollar index is at <span class="num">99.32</span>, up <span class="up">+0.91%</span> YTD and <span class="up">+0.40%</span> post-FOMC. The rate hold supports the USD through the interest rate differential channel — US rates remain elevated relative to most peers. However, the dollar strength is modest. This reflects the market's expectation that the Fed is at or near the peak, capping further USD upside. The combination of higher US rates and geopolitical risk from the Middle East is a classic negative setup for EM FX, with commodity importers and USD-debt-heavy EM currencies most vulnerable. Watch for EM central banks to respond with their own tightening or intervention.

### GBP/USD

Cable at <span class="num">1.3455</span> (May 24 weekend session data), down <span class="down">-0.14%</span> YTD and <span class="down">-0.51%</span> post-FOMC. The modest weakness reflects the USD's incremental yield advantage post-FOMC. The Bank of England's own rate trajectory will be the key driver going forward.

### Gold (GC=F)

Gold at <span class="num">$4,523.20</span>, up <span class="up">+4.84%</span> YTD but down <span class="down">-0.48%</span> post-FOMC. Gold has held its ground despite the USD strength and rising real yields — a departure from the traditional negative gold–real-yield correlation. This suggests geopolitical risk premium (Middle East uncertainty) and central bank gold buying are providing a floor. However, a hot PCE print that drives a sharp yield spike could pressure gold in the near term before safe-haven demand reasserts.

### Crude Oil (CL=F)

WTI crude at <span class="num">$96.60</span>, up an extraordinary <span class="up">+68.53%</span> YTD but down <span class="down">-9.62%</span> post-FOMC. The post-FOMC decline reflects Middle East de-escalation expectations and demand-side concerns from higher rates. The YTD surge is driven by supply disruption fears from the Middle East conflict. The interplay between geopolitical de-escalation (bearish for oil) and higher-for-longer rates (bearish for demand) creates a complex outlook. A hot PCE that triggers a broad risk-off move would likely pressure crude further in the short term.

---

## Outlook

### Short-Term Risks (1–4 Weeks)

**1. May PCE (ex-Energy) — the dominant near-term catalyst.** The entire post-FOMC risk rally rests on the "hold now, cut later" narrative. A hot core PCE print unravels this thesis, driving yields higher and equities lower through the extreme negative correlation regime.

Our scenario model estimates:

| Scenario | PCE MoM ex-energy | 10Y Target | SPY Return (Primary Model) |
|----------|-------------------|------------|:--------------------------:|
| Light hot | 0.20–0.25% | 4.76% | <span class="down">-4.1%</span> |
| Moderate hot | 0.25–0.30% | 4.81% | <span class="down">-5.1%</span> |
| Severe hot | >0.30% | 4.86% | <span class="down">-6.2%</span> |
| **Expected (if hot)** | — | 4.79% | <span class="down">-4.8%</span> |

The threshold to watch: **10Y yield at 4.75%**. Breaching this level triggers forced liquidations, gamma effects, and momentum-driven selling — potentially producing damage beyond the proportional model.

**2. Spread vulnerability by beta.** In order of expected downside under a moderate-hot PCE (25bp spike):

| Rank | Ticker | 30d Beta | Expected Downside (25bp) |
|:----:|--------|:-------:|:------------------------:|
| 1 | IWM | -1.00 | <span class="down">-9.4%</span> |
| 2 | GS | -1.35 | <span class="down">-12.7%</span> |
| 3 | XLY (Consumer Discr.) | -0.86 | <span class="down">-8.1%</span> |
| 4 | NVDA | -1.00 | <span class="down">-9.4%</span> |
| 5 | GOOGL | -0.96 | <span class="down">-9.0%</span> |
| 6 | PLD | -0.81 | <span class="down">-7.6%</span> |
| 7 | XLI (Industrials) | -0.75 | <span class="down">-7.0%</span> |
| 8 | QQQ | -0.73 | <span class="down">-6.8%</span> |
| 9 | SPY (broad market) | -0.54 | <span class="down">-5.0%</span> |
| 10 | AAPL | -0.49 | <span class="down">-4.6%</span> |

**3. Stagflationary risk.** Unlike 2023 when higher yields were driven by growth expectations (positive for equities), a hot PCE driven by sticky non-energy inflation is stagflationary — the worst scenario for equities.

### Medium-Term View (2–6 Months)

**The "hold now, cut later" narrative has evidence on its side:**
- Energy-driven inflation may prove transitory as base effects roll off
- The dissenting vote for a cut signals internal momentum toward easing
- Labor market softening, while gradual, reduces urgency for tightening
- Flexible guidance gives the Fed room to cut once inflation data cooperates

**However, three risks could delay or prevent cuts:**
1. Middle East escalation driving sustained energy price inflation
2. Sticky core services inflation (ex-energy) that doesn't moderate with energy
3. The extreme SPY–10Y correlation regime means any rate shock has outsized equity impact

### Tactical Implications

- **Short candidates for a hot PCE scenario:** IWM, NVDA, GOOGL, GS (highest rate betas, most downside)
- **Relative value hedges:** Long WMT / short IWM (zero rate correlation vs highest); Long MSFT / short GOOGL (already discounted vs at 52w high with high beta)
- **Sector rotation:** Reduce QQQ exposure toward XLF (steepener benefit partially offsets rate-equity correlation)
- **Avoid immediate post-PCE dip buying in:** GS, PLD, AAPL — all at 100% of 52w high with moderate-to-high rate beta
- **REITs:** Hold below 4.75% 10Y; reduce above that threshold

### Key Dates to Watch

| Date | Event | Significance |
|------|-------|-------------|
| Late May / Early Jun | May PCE Report | The hot-PCE trigger — most important data before next FOMC |
| Jun 16–17, 2026 | Next FOMC Meeting | Rate decision with updated dot plot and Summary of Economic Projections |
| Weekly | Jobless Claims / NFP | Labor market softening trajectory |
| Ongoing | Middle East developments | Direct driver of energy prices and safe-haven flows |

---

## Model Documentation

**Scenario model (hot-pce-scenario.md):** Three-model framework cross-validated:
1. **Regression (30-day beta-to-10Y):** SPY daily return vs ^TNX daily return over trailing 30 trading days. Current beta: -0.5374.
2. **Historical analog scaling:** Sep-Nov 2023 (10Y 4.17% → 4.99%, SPY -10.0%, correlation -0.49) scaled by current-to-analog correlation ratio (-0.84/-0.49 = 1.71x). Gives -2.1% per 10bp yield rise.
3. **Multi-day compound:** Sustained repricing over 5–10 trading days compounds single-day damage by 1.5x–2.0x factor.
- **Primary model** uses the correlation-adjusted estimate.

**Correlation:** SPY-10Y correlation computed over trailing 30 calendar days using daily returns. Post-FOMC window: Apr 29 → May 22 (16 trading days). Individual stock betas computed over same 30-day window vs ^TNX daily returns.

**Data sources:** yfinance 1.4.0. FOMC April 2026 Statement (federalreserve.gov) and Powell press conference transcript (FOMC presconf PDF).

---

## Disclaimer

This market brief is for informational purposes only and does not constitute investment advice, a solicitation, or a recommendation to buy or sell any security. All analyses are based on publicly available data and modeled scenarios that may not materialize. Past performance and historical analogs are not guarantees of future results. Model estimates involve assumptions about correlation regimes, beta stability, and market structure that may shift rapidly. Readers should conduct their own due diligence and consult with licensed financial advisors before making investment decisions. The author(s) may hold positions in securities discussed herein.