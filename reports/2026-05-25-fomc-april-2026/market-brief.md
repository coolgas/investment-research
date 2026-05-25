---
date: 2026-05-25
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
  - XLY
  - XLI
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
  - reflation-regime
---

<style>
span.up { font-weight: bold; color: #008000; }
span.down { font-weight: bold; color: #CC0000; }
span.num { font-weight: bold; color: #000080; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th { background: #000080; color: white; padding: 6px 10px; text-align: center; }
td { padding: 4px 10px; text-align: center; }
tr:nth-child(even) { background: #f5f5f5; }
tr:nth-child(odd) { background: #ffffff; }
caption { font-weight: bold; margin-bottom: 4px; }
</style>

# Market Brief: April 2026 FOMC -- Rate Hold, Risk-On Rotation, and the Hot PCE Tail Risk

**Report Date:** May 25, 2026
**Data As Of:** May 22, 2026 close (all equities, bonds, rates, commodities, FX)
**Event:** FOMC April 29, 2026 -- Rate Hold at 3.50-3.75%
**Sources:** analysis.md, report.md, post-fomc-market-analysis.md, hot-pce-scenario.md, data-refresh.md

---

## 1. Executive Summary

The FOMC held rates at 3.50-3.75% on April 29, 2026, in line with consensus. One dissenter -- Miran -- preferred a 25bp cut, marking the first public internal dissent signaling pressure for easing. The Statement cited solid economic growth, softening but stable labor (unemployment ~4.3%), and elevated inflation driven by global energy prices and Middle East uncertainty.

The market read the decision as a **dovish hold**. Rather than retreating to defensives on the "higher-for-longer" signal, investors rotated aggressively into risk assets:

- QQQ surged <span class="up">+8.46%</span> post-FOMC, nearly doubling SPY's <span class="up">+4.79%</span>
- Utilities (XLU: <span class="down">-0.72%</span>) were the only sector to decline -- money flowed out of defensives
- Financials (XLF: <span class="up">+0.04%</span>) barely moved despite the steepening yield curve
- Small caps (IWM: <span class="up">+4.79%</span>) matched the S&P 500, confirming broad participation
- The SPY-10Y daily returns correlation tightened to <span class="num">-0.90</span> post-FOMC -- 2.3x the YTD average of <span class="num">-0.39</span>, signaling rates are now the dominant equity driver on a daily basis

The reflation regime remains intact: SPY and 10Y yields have both risen YTD, producing a positive levels-direction correlation of <span class="num">+0.45</span>. But within this bullish medium-term structure, daily rate moves now carry amplified negative equity impact.

SPY at <span class="num">$745.64</span> is <span class="num">99.7%</span> of its 52-week high. The 10Y yield at <span class="num">4.56%</span> has risen <span class="up">+37bp</span> YTD and <span class="up">+21bp</span> since the FOMC, leaving only <span class="num">11bp</span> of headroom before the 52-week high of <span class="num">4.67%</span>. The DXY at <span class="num">99.32</span> is up <span class="up">+0.91%</span> YTD and <span class="up">+0.40%</span> post-FOMC. Gold at <span class="num">$4,521</span> is up <span class="up">+4.79%</span> YTD but down <span class="down">-0.53%</span> post-FOMC. WTI crude at <span class="num">$96.60</span> has surged <span class="up">+68.53%</span> YTD on Middle East supply disruption but declined <span class="down">-9.62%</span> post-FOMC.

**Key risk:** The post-FOMC rally rests on the "hold now, cut later" narrative. A hot May PCE (ex-energy) print would unravel this thesis. Our three-model scenario framework estimates a <span class="down">-4.8%</span> expected SPY drawdown conditional on a hot print, with severe cases reaching <span class="down">-6.2%</span>. The 10Y above <span class="num">4.75%</span> would mark the threshold for forced liquidations and momentum-driven selling.

---

## 2. Methodology

This brief synthesizes four analytical layers:

**Fundamental analysis** (analysis.md, report.md): Direct text extraction from the April 29 FOMC Statement (HTML stripping) and Powell press conference transcript (pdftotext). Lens: rate-sensitive equities and EM FX. Confidence: medium -- policy language is high-confidence; sector and FX implications are reasoned inferences.

**Post-FOMC market analysis** (post-fomc-market-analysis.md): Quantitative assessment of price action from Apr 29 through May 22. yfinance 1.4.0 for all price data. Computes YTD (Jan 2 through May 22), post-FOMC (Apr 29 through May 22), and daily returns. SPY-10Y correlations computed over the full post-FOMC window (16 trading days) and trailing 30 calendar days.

**Scenario analysis** (hot-pce-scenario.md): Three-model cross-validated framework for a hot May PCE ex-energy downside scenario:
- **30-day beta regression:** SPY daily return-to-10Y return beta over trailing 30 trading days. Current beta: <span class="num">-0.5374</span> (a 1% move in 10Y yield implies a -0.54% SPY same-day move).
- **Historical analog scaling:** Sep-Nov 2023 baseline (10Y 4.17% to 4.99%, SPY -10.0%, analog correlation -0.49), scaled by correlation ratio: current -0.84 / analog -0.49 = 1.71x multiplier. Primary model yields -2.1% per 10bp yield rise.
- **Multi-day compound model:** Sustained repricing over 5-10 trading days compounds single-day damage by 1.5x-2.0x.

**Data refresh** (data-refresh.md): yfinance 1.4.0 pull for 24 tickers across indices, sectors, stocks, commodities, and FX. All closes as of May 22, 2026 (Friday).

**Date conventions:** YTD base = Jan 2, 2026 (Jan 1 is a market holiday). Post-FOMC base = Apr 29, 2026 (FOMC decision date). 30-day trailing beta computed from the 30 trading days preceding May 22. All percentages from adjusted close prices (auto_adjust=True, no group_by in yf.download()).

**Correlation note:** Two correlation metrics appear in source documents and serve different purposes:
- **Daily returns correlation** (post-fomc-market-analysis, hot-pce-scenario): SPY daily return vs ^TNX daily yield change. Post-FOMC: <span class="num">-0.90</span>. Used in the scenario model and trading analysis. This is the primary metric for rate sensitivity.
- **Levels/trend correlation** (data-refresh): Directional consistency over the full period. YTD: <span class="num">+0.45</span>. Confirms the reflation regime -- both SPY and yields have risen YTD. This is the context for why equities rallied despite yield backup.

---

## 3. Rates & Fixed Income

### Yield Benchmarks

| Instrument | Pre-FOMC | Current | Post-FOMC Change | YTD Change |
|------------|----------|---------|-----------------|-----------|
| 10Y Yield (^TNX) | 4.35% | <span class="num">4.56%</span> | <span class="up">+21bp</span> | <span class="up">+37bp</span> |
| 5Y Yield (^FVX) | -- | <span class="num">4.26%</span> | -- | <span class="up">+52bp</span> |
| 3M Yield (^IRX) | -- | <span class="num">3.59%</span> | -- | <span class="up">+6bp</span> |
| TLT (20Y+ Treasury) | -- | <span class="num">$84.68</span> | <span class="down">-0.83%</span> | <span class="down">-1.25%</span> |

### Fed Decision & Forward Guidance

**Decision:** Rate hold at 3.50-3.75%, as expected. One dissenter -- Miran -- preferred a 25bp cut, the first dissent publicly signaling internal pressure for easing.

**Key language from the April 29 Statement (source-01):**
- "Economic activity has been expanding at a solid pace"
- "Job gains have remained low" and "unemployment rate has been little changed" (~4.3%)
- Inflation "elevated, in part reflecting the recent increase in global energy prices"
- Middle East developments contributing to "a high level of uncertainty about the economic outlook"

**Forward guidance:** Data-dependent posture reiterated. Powell described the current stance as "appropriate" and noted the Fed is "prepared to adjust the stance of policy if risks emerge." This flexible language leaves the door open for cuts if inflation moderates, reinforcing the "hold now, cut later" market narrative.

**Next FOMC meeting:** June 16-17, 2026. The May PCE release (late May / early June) will be the most important data point between meetings.

### Yield Curve Context

The 10Y has risen <span class="up">+37bp</span> YTD and <span class="up">+21bp</span> post-FOMC. The 5Y has steepened more sharply (<span class="up">+52bp</span> YTD), reflecting repricing of intermediate-term rate expectations. The 10Y's 52-week high is <span class="num">4.67%</span> -- current levels at <span class="num">4.56%</span> leave only <span class="num">11bp</span> of headroom.

TLT (long-duration Treasuries) has declined <span class="down">-1.25%</span> YTD and <span class="down">-0.83%</span> post-FOMC, confirming the bear-steepening bias.

The SPY-10Y daily returns correlation of <span class="num">-0.90</span> (post-FOMC) vs <span class="num">-0.39</span> (YTD average) marks a sharp intensification: rates have become the dominant equity driver. A 10Y breach of <span class="num">4.75%</span> -- the threshold from our scenario analysis -- could trigger forced liquidations and momentum-driven selling disproportionate to the yield move itself.

### The Two-Correlation Regime

| Correlation Metric | Period | Value | Interpretation |
|-------------------|--------|:-----:|---------------|
| Daily returns (SPY vs ^TNX delta) | Post-FOMC (Apr 29 -- May 22) | <span class="num">-0.90</span> | Extreme negative -- rates dominate daily equity moves |
| Daily returns (SPY vs ^TNX delta) | YTD (Jan 2 -- May 22) | <span class="num">-0.39</span> | Negative but within historical range |
| Daily returns (SPY vs ^TNX delta) | 30-day trailing | <span class="num">-0.84</span> | Input to scenario model; confirms intensification |
| Levels direction (SPY price vs ^TNX level) | YTD (Jan 2 -- May 22) | <span class="num">+0.45</span> | Reflation regime: both higher YTD |
| Levels direction (SPY price vs ^TNX level) | Post-FOMC (Apr 29 -- May 22) | <span class="num">+0.46</span> | Steady -- no regime shift in levels despite daily inversion |

The medium-term reflation regime is intact: growth expectations lift both equities and yields together. But the daily returns correlation has intensified to an extreme negative, meaning any yield backup now translates into amplified daily equity losses. This is the cross-current: bulls own the trend, but rates own the daily tape.

---

## 4. Equities by Sector

### Broad Market

| Ticker | Name | Price | YTD Return | Post-FOMC Return | % of 52w High |
|--------|------|-------|-----------|-----------------|--------------|
| SPY | S&P 500 | <span class="num">745.64</span> | <span class="up">+9.44%</span> | <span class="up">+4.79%</span> | <span class="num">99.7%</span> |
| QQQ | Nasdaq-100 | <span class="num">717.54</span> | <span class="up">+17.18%</span> | <span class="up">+8.46%</span> | <span class="num">99.7%</span> |
| IWM | Small Caps (Russell) | <span class="num">285.12</span> | <span class="up">+14.81%</span> | <span class="up">+4.79%</span> | <span class="num">99.4%</span> |

**QQQ** led with <span class="up">+8.46%</span> post-FOMC -- nearly double SPY -- confirming a classic tech-led risk rally. At <span class="num">99.7%</span> of 52-week high, Nasdaq-100 names are near all-time highs.

**IWM** matched SPY at <span class="up">+4.79%</span> post-FOMC despite being the most rate-sensitive broad index (30-day rate beta: <span class="num">-1.00</span>). Small caps carry floating-rate debt exposure and lack the pricing power of large caps, making them the most vulnerable index to any negative rate surprise. A 25bp yield spike implies <span class="down">-9.4%</span> downside for IWM.

**SPY** at <span class="num">99.7%</span> of 52w high leaves minimal room for error. The post-FOMC rally has pushed valuations to upper trailing ranges. A negative catalyst -- particularly a hot PCE -- would find a crowded long setup with limited support before the 50-day moving average.

### Sector ETFs

| Ticker | Sector | Price | YTD Return | Post-FOMC Return | % of 52w High | 30d Rate Beta |
|--------|--------|-------|-----------|-----------------|--------------|:-------------:|
| QQQ | Nasdaq-100 | <span class="num">717.54</span> | <span class="up">+17.18%</span> | <span class="up">+8.46%</span> | <span class="num">99.7%</span> | <span class="down">-0.73</span> |
| XLRE | Real Estate | <span class="num">44.56</span> | <span class="up">+11.09%</span> | <span class="up">+2.11%</span> | <span class="num">99.6%</span> | <span class="down">-0.49</span> |
| XLY | Consumer Discr. | -- | <span class="up">+0.90%</span> | <span class="up">+2.00%</span> | <span class="num">95.9%</span> | <span class="down">-0.86</span> |
| XLI | Industrials | -- | <span class="up">+9.03%</span> | <span class="up">+1.08%</span> | <span class="num">96.3%</span> | <span class="down">-0.75</span> |
| XLU | Utilities | <span class="num">45.35</span> | <span class="up">+5.76%</span> | <span class="down">-0.72%</span> | <span class="num">95.7%</span> | <span class="down">-0.23</span> |
| XLF | Financials | <span class="num">51.94</span> | <span class="down">-4.96%</span> | <span class="up">+0.04%</span> | <span class="num">92.6%</span> | <span class="down">-0.27</span> |

**Nasdaq-100 / QQQ (+8.46% post-FOMC):** The risk-on leader. The tech rally reflects market conviction that the next rate move is down. Moderate rate beta (<span class="num">-0.73</span>) means QQQ is not the most vulnerable to a rate shock, but at <span class="num">99.7%</span> of 52w high it has the most to lose in a drawdown.

**XLRE (+2.11% post-FOMC):** REITs held up despite the 10Y rising 21bp. Data center, industrial, and tower REITs carry enough demand-side momentum (AI infrastructure, logistics reshoring, telco capex) to offset discount rate pressure. The sector-level selloff threshold is <span class="num">4.75%</span> on the 10Y. Below that, secular-demand REITs can hold. At <span class="num">99.6%</span> of 52w high.

**XLY (+2.00% post-FOMC, rate beta -0.86):** Consumer Discretionary posted a modest gain but carries the second-highest sector rate beta. Consumer spending is financed, and higher discount rates compress the present value of discretionary purchases. This is the second-most vulnerable sector to a hot PCE after small caps. YTD return of just <span class="up">+0.90%</span> reflects low conviction.

**XLU (-0.72% post-FOMC):** The only sector to decline post-FOMC. Defensives were sold to fund the risk-on rotation. Utilities' low rate beta (<span class="num">-0.23</span>) reflects that much of the rate-driven damage has already been absorbed. In a hot-PCE macro risk-off scenario, XLU could see a defensive bid that partially offsets rate headwinds.

**XLF (+0.04% post-FOMC):** Flat despite a steepening yield curve that should benefit bank NIMs. The sector-wide stagnation reflects divergence: investment banks (GS) rallied while consumer banks (JPM, BAC) declined under loan growth and deposit cost pressure. XLF carries the lowest rate beta (<span class="num">-0.27</span>) and is YTD negative at <span class="down">-4.96%</span>.

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

**AAPL (+14.41% post-FOMC):** The standout performer. At <span class="num">100%</span> of 52-week high, Apple compounds multiple tailwinds -- aggressive buybacks, AI positioning (Apple Intelligence), and no direct tariff exposure relative to hardware peers. The combination of peak valuation and moderate rate beta (<span class="num">-0.49</span>) creates a "double vulnerability": a 25bp yield spike implies <span class="down">-4.6%</span> downside toward <span class="num">$295</span>, its first break below <span class="num">$300</span> since the post-FOMC run. **Sentiment:** Bullish on fundamentals; cautious on near-term rate-driven exposure at 52w high.

**GOOGL (+9.44% post-FOMC):** Strong post-FOMC performance on ad revenue momentum and AI pipeline. However, GOOGL is a rate proxy: the 30-day rate beta of <span class="num">-0.96</span> is the second-highest among mega-cap tech. A 25bp spike implies <span class="down">-9.0%</span> downside toward <span class="num">$348</span>. At <span class="num">95.1%</span> of 52w high with YTD <span class="up">+21.61%</span> (best in cohort), GOOGL has the most to give back in a rate shock. **Sentiment:** Strong momentum offset by highest vulnerability to rate repricing among mega-caps.

**AMZN (+1.25% post-FOMC):** Muted relative to peers. Moderate rate beta (<span class="num">-0.56</span>). At <span class="num">96.8%</span> of 52w high. AWS growth and retail margin expansion provide fundamental support, but the muted post-FOMC move suggests AMZN is not the marginal rate-sensitive trade in this cohort. **Sentiment:** Neutral to constructive -- balanced risk/reward relative to both high-beta (GOOGL, NVDA) and distressed (MSFT, META) peers.

**NVDA (+2.91% post-FOMC):** Modest post-FOMC recovery leaves NVDA at only <span class="num">91.3%</span> of 52w high -- the second-lowest in mega-cap tech. The high negative rate beta (<span class="num">-1.00</span>) reflects its long-duration growth profile: future AI infrastructure revenue is heavily discounted at higher rates. A 25bp spike implies <span class="down">-9.4%</span> downside toward <span class="num">$195</span>, approaching post-FOMC lows. **Sentiment:** High conviction short candidate in a hot PCE scenario; best-in-class AI fundamentals but extreme rate sensitivity.

**MSFT (-11.10% YTD, -1.17% post-FOMC):** The worst YTD mega-cap performer. AI capex spending concerns and Azure growth deceleration questions have weighed on sentiment. Rate beta is effectively zero (<span class="num">+0.03</span>), making MSFT a **portfolio hedge** against rate-driven drawdowns -- it trades on company-specific fundamentals, not macro rates. At <span class="num">77.7%</span> of 52w high (lowest in cohort), much of the rate-driven downside may already be priced in. In a hot PCE scenario, MSFT is minimally affected through the rate channel. **Sentiment:** Cautious on fundamentals (capex cycle concerns); attractive as a hedge against rate-driven portfolio risk.

**META (-8.80% post-FOMC):** The decoupling story. META sold off <span class="down">-8.80%</span> while mega-cap peers rallied -- the only name to post a material post-FOMC decline aside from MSFT's marginal <span class="down">-1.17%</span>. At <span class="num">82.7%</span> of 52w high, it is in a fundamentally different regime than peers at 95-100%. The selloff is stock-specific: AI capex skepticism, ROI uncertainty, and regulatory overhang. Low rate beta (<span class="num">-0.24</span>) means META's trajectory is driven by company-specific factors. The deep discount could attract value-oriented buyers but does not imply a near-term catalyst. A 25bp spike adds only <span class="down">-2.3%</span> downside through the rate channel. **Sentiment:** Bearish near-term (stock-specific headwinds dominate); potential value entry but no catalyst for rerating.

#### Banks

| Ticker | Price | YTD Return | Post-FOMC Return | % of 52w High | 30d Rate Beta |
|--------|-------|-----------|-----------------|--------------|:-------------:|
| GS | <span class="num">996.73</span> | <span class="up">+9.58%</span> | <span class="up">+10.06%</span> | <span class="num">100.0%</span> | <span class="down">-1.35</span> |
| JPM | <span class="num">306.38</span> | <span class="down">-4.96%</span> | <span class="down">-0.93%</span> | <span class="num">92.0%</span> | <span class="down">-0.51</span> |
| BAC | <span class="num">51.80</span> | <span class="down">-6.89%</span> | <span class="down">-2.04%</span> | <span class="num">91.0%</span> | <span class="down">-0.34</span> |

**GS (+10.06% post-FOMC, -1.35 rate beta):** The most rate-sensitive stock in the tracked universe and the strongest post-FOMC bank performer -- a paradoxical combination. At <span class="num">100%</span> of 52w high and <span class="num">$996.73</span>, GS is trading as a valuation proxy rather than on its earnings composition. The -1.35 beta implies P/E multiple compression risk outweighs the investment banking earnings benefit from higher rates. This is anomalous: investment banks typically benefit from higher rates through fixed-income trading revenue, but the market is pricing GS as a duration asset. A 25bp spike implies <span class="down">-12.7%</span> downside toward <span class="num">$870</span>, its first sub-$900 level in over a month. **Sentiment:** Best post-FOMC bank performer but single highest-conviction short candidate in a hot PCE scenario. Beta anomaly warrants monitoring.

**JPM (-0.93% post-FOMC):** Consumer bank headwinds persist. Higher-for-longer compresses loan growth and deposit costs without the fee-income offset available to GS. At <span class="num">92.0%</span> of 52w high. Moderate rate beta (<span class="num">-0.51</span>) implies <span class="down">-4.8%</span> downside on a 25bp spike. The diversified franchise provides buffer, but consumer banking is the weak segment. **Sentiment:** Neutral -- diversified stability but no catalyst for re-rating.

**BAC (-2.04% post-FOMC):** Weakest major bank. Same consumer-bank dynamics as JPM but with higher exposure to rate-sensitive consumer credit and commercial real estate. At <span class="num">91.0%</span> of 52w high. Lower rate beta (<span class="num">-0.34</span>) means BAC suffers less direct rate-driven damage than JPM, but stock-specific credit quality headwinds dominate. A 25bp spike implies <span class="down">-3.2%</span> downside toward <span class="num">$50</span>. **Sentiment:** Cautious -- consumer credit and CRE exposure are structural headwinds that higher rates exacerbate.

**Bank sector takeaway:** GS (+10.06% post-FOMC) vs consumer banks (JPM -0.93%, BAC -2.04%) reflects the fee-based vs interest-based revenue trade-off. XLF's flat post-FOMC return of <span class="up">+0.04%</span> confirms the sector-wide net headwind.

#### Other Holdings

| Ticker | Price | YTD Return | Post-FOMC Return | % of 52w High | 30d Rate Beta |
|--------|-------|-----------|-----------------|--------------|:-------------:|
| PLD | <span class="num">145.90</span> | <span class="up">+13.97%</span> | <span class="up">+5.10%</span> | <span class="num">100.0%</span> | <span class="down">-0.81</span> |
| NEE | <span class="num">88.55</span> | <span class="up">+10.16%</span> | <span class="down">-5.97%</span> | <span class="num">90.5%</span> | <span class="down">-0.14</span> |
| WMT | <span class="num">120.27</span> | <span class="up">+7.08%</span> | <span class="down">-5.87%</span> | <span class="num">89.6%</span> | <span class="num">+0.01</span> |

**PLD (+5.10% post-FOMC):** Industrial/logistics REIT driven by structural demand from supply chain reshoring and e-commerce. At <span class="num">100%</span> of 52w high with a rate beta of <span class="num">-0.81</span> -- a hot PCE implies <span class="down">-7.6%</span> downside toward <span class="num">$135</span>. The "double vulnerability" at 52w high with meaningful rate sensitivity makes timing critical. Do not buy the dip post-PCE without confirmation that the 10Y has stabilized below <span class="num">4.75%</span>. **Sentiment:** Constructive on structural demand, but rate sensitivity at 52w high requires disciplined entry.

**NEE (-5.97% post-FOMC):** Sold off as part of the utility rotation out of defensives. Low rate beta (<span class="num">-0.14</span>) means the selloff was sector-rotation-driven, not rate-driven. Renewable energy project financing may face headwinds from higher long-term rates, but the low beta suggests this impact is discounted. NEE at <span class="num">90.5%</span> of 52w high with a YTD gain of <span class="up">+10.16%</span> -- the selloff is mean-reversion within a constructive YTD trend. In a hot-PCE risk-off scenario, NEE could see a defensive bid partially offsetting rate headwinds. **Sentiment:** Neutral with defensive tilt -- selloff appears rotational rather than structural.

**WMT (-5.87% post-FOMC):** Consumer defensive sold as money rotated into risk. Rate beta is effectively zero (<span class="num">+0.01</span>) -- WMT is a pure stock-specific story. Consumer margin compression from higher input costs and a softening labor market are the relevant headwinds. At <span class="num">89.6%</span> of 52w high with a YTD gain of <span class="up">+7.08%</span>. In a hot-PCE scenario, WMT is the strongest **relative value hedge**: long WMT paired against short high-beta names (IWM, GOOGL, GS). **Sentiment:** Defensive hold -- near-zero rate sensitivity makes it portfolio ballast, but consumer margin compression is an earnings risk.

---

## 5. Sector Rotation

### Post-FOMC Capital Flows

The post-FOMC period (Apr 29 -- May 22) produced a clear rotation pattern:

| Direction | Sectors | Post-FOMC Return | Driver |
|-----------|---------|:---:|--------|
| **Risk-on inflows** | QQQ (Nasdaq-100) | <span class="up">+8.46%</span> | Dovish hold narrative; "next move is a cut" |
| | SPY (S&P 500) | <span class="up">+4.79%</span> | Broad participation |
| | IWM (Small Caps) | <span class="up">+4.79%</span> | Breadth confirmation |
| | XLRE (Real Estate) | <span class="up">+2.11%</span> | Secular demand offsets rate headwind |
| | XLY (Consumer Discr.) | <span class="up">+2.00%</span> | Modest risk-on participation |
| | XLI (Industrials) | <span class="up">+1.08%</span> | CapEx cycle resilience |
| **Stalled** | XLF (Financials) | <span class="up">+0.04%</span> | Consumer bank drag offsets GS gains |
| **Rotated out** | XLU (Utilities) | <span class="down">-0.72%</span> | Defensives sold to fund risk-on |
| | NEE (NextEra) | <span class="down">-5.97%</span> | Utility rotation amplified |
| | WMT (Walmart) | <span class="down">-5.87%</span> | Consumer defensive rotation out |
| | META (Meta) | <span class="down">-8.80%</span> | Stock-specific decoupling |

### Interpretation

The market focused on three dovish elements: (1) the dissenting vote for a cut as a signal the next move is down, (2) the "flexible and data-dependent" language as dovish optionality, and (3) the absence of explicit tightening bias. These signals overwhelmed the higher-for-longer rate level, producing a classic risk-on rotation: tech and growth in, defensives and bonds out.

The extreme SPY-10Y daily returns correlation of <span class="num">-0.90</span> post-FOMC (vs YTD <span class="num">-0.39</span>) signals that rates became the dominant equity driver after the meeting. Nearly every daily equity move in the post-FOMC window was explainable by rate direction. This regime intensification means:
- Any further yield backup above <span class="num">4.60%</span> could trigger rapid equity drawdowns
- Conversely, a rate cut signal would be violently positive for equities
- Sectors with high rate beta (IWM, XLY) would experience exaggerated moves in either direction

### The Rotation's Fragility

The rotation is built on the "hold now, cut later" narrative. The May PCE ex-energy print is the first test of this thesis. If core PCE surprises to the upside, the reflation regime's positive levels correlation does not protect against the extreme negative daily returns correlation -- the daily damage would be amplified precisely because the market is so tightly coupled to rates. A reversal of the rotation would look like: QQQ and growth names sold, defensives bid, and banks caught between steepener benefit and loan-loss fears.

---

## 6. FX & Commodities

| Ticker | Name | Price | Daily % | YTD % | Post-FOMC % |
|--------|------|-------|-------|-----|-----------|
| DX-Y.NYB | US Dollar Index (DXY) | <span class="num">99.32</span> | <span class="up">+0.13%</span> | <span class="up">+0.91%</span> | <span class="up">+0.40%</span> |
| GBPUSD=X | GBP/USD | <span class="num">1.3433</span> | <span class="down">-0.01%</span> | <span class="down">-0.30%</span> | <span class="down">-0.68%</span> |
| GC=F | Gold (COMEX Futures) | <span class="num">4521.00</span> | <span class="down">-0.41%</span> | <span class="up">+4.79%</span> | <span class="down">-0.53%</span> |
| CL=F | Crude Oil (WTI Futures) | <span class="num">96.60</span> | <span class="up">+0.26%</span> | <span class="up">+68.53%</span> | <span class="down">-9.62%</span> |

### DXY (US Dollar Index)

The dollar index at <span class="num">99.32</span> is up <span class="up">+0.91%</span> YTD and <span class="up">+0.40%</span> post-FOMC. The rate hold supports the USD through the interest rate differential channel -- US rates remain elevated relative to most peers. However, the dollar's strength is modest: the market expects the Fed is at or near the peak, capping further USD upside. The combination of higher US rates and geopolitical risk from the Middle East creates a classic negative setup for EM FX. Commodity importers and USD-debt-heavy EM currencies (BRL, ZAR, TRY) are most vulnerable. EM central banks may respond with tightening or intervention. The DXY ticked higher from the prior report's <span class="num">99.02</span> to <span class="num">99.32</span>, reflecting incremental dollar demand.

### GBP/USD

Cable at <span class="num">1.3433</span>, down <span class="down">-0.30%</span> YTD and <span class="down">-0.68%</span> post-FOMC. Weaker than the prior report's <span class="num">1.3483</span>. The incremental weakness reflects the USD's yield advantage and UK-specific headwinds. The Bank of England's rate trajectory and UK inflation data remain the key drivers.

### Gold (GC=F)

Gold at <span class="num">$4,521</span>, up <span class="up">+4.79%</span> YTD but down <span class="down">-0.53%</span> post-FOMC. Gold has held ground despite USD strength and rising yields -- a departure from the traditional negative gold-real-yield correlation. This suggests geopolitical risk premium (Middle East uncertainty) and central bank buying are providing a floor. The modest post-FOMC decline and further daily drop (<span class="down">-0.41%</span>) suggest some safe-haven unwinding alongside the risk-on rotation. A hot PCE that drives a sharp yield spike could pressure gold further before safe-haven demand reasserts. Gold ticked down from <span class="num">$4,523</span> to <span class="num">$4,521</span> between reports.

### Crude Oil (CL=F)

WTI crude at <span class="num">$96.60</span>, up <span class="up">+68.53%</span> YTD on Middle East supply disruption fears but down <span class="down">-9.62%</span> post-FOMC. The post-FOMC decline likely reflects de-escalation expectations and demand-side concerns from higher rates slowing economic activity. The interplay between geopolitical de-escalation (bearish) and disrupted supply (bullish) creates a complex outlook. A hot PCE that triggers a broad risk-off move would pressure crude further in the short term through the demand-expectations channel.

---

## 7. Outlook

### Short-Term Risks (1-4 Weeks)

**1. May PCE (ex-Energy) -- the dominant near-term catalyst.** The post-FOMC risk rally rests entirely on the "hold now, cut later" narrative. A hot core PCE print unravels this thesis, driving yields higher and equities lower through the extreme negative daily returns correlation regime.

Our three-model scenario framework estimates:

| Scenario | PCE MoM ex-energy | 10Y Target | SPY Return (Primary Model) |
|----------|-------------------|------------|:--------------------------:|
| Light hot | 0.20-0.25% | 4.76% | <span class="down">-4.1%</span> |
| Moderate hot | 0.25-0.30% | 4.81% | <span class="down">-5.1%</span> |
| Severe hot | >0.30% | 4.86% | <span class="down">-6.2%</span> |
| **Expected (if hot)** | -- | 4.79% | <span class="down">-4.8%</span> |

The primary model is the correlation-adjusted estimate, scaled from the Sep-Nov 2023 analog by the correlation ratio (-0.84 / -0.49 = 1.71x). Upper bound (1.5x compound): -3.5% to -5.3%. Lower bound (2.0x compound): -4.7% to -7.1%.

The threshold to watch: **10Y yield at 4.75%**. Breaching this level triggers the forced-liquidation and momentum-selling dynamics identified in the post-FOMC analysis.

**2. Sector and stock vulnerability -- expected downside under moderate-hot PCE (25bp spike):**

| Rank | Ticker | 30d Beta | Expected Downside (25bp) | % of 52w High |
|:----:|--------|:-------:|:------------------------:|:-------------:|
| 1 | GS | -1.35 | <span class="down">-12.7%</span> | 100.0% |
| 2 | IWM | -1.00 | <span class="down">-9.4%</span> | 99.4% |
| 3 | NVDA | -1.00 | <span class="down">-9.4%</span> | 91.3% |
| 4 | GOOGL | -0.96 | <span class="down">-9.0%</span> | 95.1% |
| 5 | XLY (Consumer Discr.) | -0.86 | <span class="down">-8.1%</span> | 95.9% |
| 6 | PLD | -0.81 | <span class="down">-7.6%</span> | 100.0% |
| 7 | QQQ | -0.73 | <span class="down">-6.8%</span> | 99.7% |
| 8 | SPY (broad market) | -0.54 | <span class="down">-5.0%</span> | 99.7% |
| 9 | AAPL | -0.49 | <span class="down">-4.6%</span> | 100.0% |

Note: GS, PLD, and AAPL are all at <span class="num">100%</span> of 52w high -- the "double vulnerability" names.

**3. Stagflationary risk.** Unlike 2023, when higher yields were driven by growth expectations (positive for equities), a hot PCE driven by sticky non-energy inflation is stagflationary -- the worst scenario for equities.

**4. Correlation regime may tighten further.** The post-FOMC daily returns correlation hit <span class="num">-0.90</span>, exceeding our 30-day model input of <span class="num">-0.84</span>. If the PCE print drives correlation even tighter, actual damage may exceed model estimates.

**5. Non-linear threshold effects.** At <span class="num">-0.84</span> correlation, the market is already in an extreme regime above any historical analog. Breaching <span class="num">4.75%</span> on the 10Y could produce forced liquidations, gamma effects, and momentum-driven selling that overshoots the proportional model.

### Medium-Term View (2-6 Months)

**The "hold now, cut later" narrative has supporting evidence:**
- Energy-driven inflation may prove transitory as base effects roll off
- The dissenting vote signals internal momentum toward easing
- Labor market softening reduces urgency for tightening
- Flexible guidance gives the Fed room to cut once inflation data cooperates
- Powell's "prepared to adjust" language reduces tail risk of further tightening

**Three risks could delay or prevent cuts:**
1. Middle East escalation driving sustained energy price inflation -- the most exogenous risk
2. Sticky core services inflation (ex-energy) that does not moderate -- the May PCE is the first test
3. The extreme SPY-10Y daily returns correlation means any rate shock has outsized equity impact -- a second-derivative risk that could itself tighten financial conditions

### Tactical Implications

- **Short candidates for a hot PCE scenario:** GS, IWM, NVDA, GOOGL -- highest rate betas, most downside in a yield spike
- **Relative value hedges (pairs):** Long WMT / short IWM (zero rate correlation vs highest); Long MSFT / short GOOGL (already discounted vs rate proxy at near-52w high); Long MSFT / short NVDA (near-zero rate beta vs -1.00)
- **Sector rotation hedge:** Reduce QQQ exposure toward XLF -- steepener benefit partially offsets rate-equity correlation; XLF has the lowest sector rate beta
- **Avoid immediate post-PCE dip buying in:** GS, PLD, AAPL -- all three at <span class="num">100%</span> of 52w high with moderate-to-high rate beta. Mean-reversion to 50-day moving averages implies further downside even without the hot-PCE trigger
- **REITs:** Hold PLD/XLRE below 4.75% 10Y; reduce above that threshold where discount-rate damage outweighs demand momentum
- **NEE and WMT:** Hold as portfolio ballast -- low-to-zero rate beta means they do not amplify rate-driven drawdowns. META and MSFT also qualify as low-beta hedges within tech

### Key Dates

| Date | Event | Significance |
|------|-------|-------------|
| Late May / Early June | May PCE Report | The hot-PCE trigger -- most important data point before next FOMC |
| Jun 16-17, 2026 | Next FOMC Meeting | Rate decision with updated dot plot and Summary of Economic Projections |
| Weekly | Jobless Claims / NFP | Labor market softening trajectory |
| Ongoing | Middle East developments | Direct driver of energy prices and USD safe-haven flows |

---

## 8. Data Sources

**Primary sources (this report):**
- analysis.md -- raw FOMC analysis from Statement and transcript
- report.md -- initial FOMC report with lens analysis
- post-fomc-market-analysis.md -- quantitative market reaction, Apr 29-May 22
- hot-pce-scenario.md -- three-model downside scenario framework
- data-refresh.md -- yfinance 1.4.0 data pull, 24 tickers, May 22 close

**External data:**
- FOMC April 2026 Statement: federalreserve.gov/newsevents/pressreleases/monetary20260429a.htm
- Powell press conference transcript: federalreserve.gov/mediacenter/files/FOMCpresconf20260429.pdf
- yfinance 1.4.0 -- all price data for equities, bonds, rates, commodities, FX
- All calculations: auto_adjust=True, no group_by in yf.download()

**Methodology notes:**
- DXY via DX-Y.NYB (US Dollar Index futures) -- the spot USDX index is not directly available via yfinance
- YTD base: Jan 2, 2026 (Jan 1 is a holiday)
- Post-FOMC base: Apr 29, 2026 (FOMC decision date)
- 30-day trailing: 30 trading days preceding May 22, 2026
- SPY-10Y daily returns correlation: daily SPY return vs daily ^TNX yield change
- SPY-10Y levels correlation: SPY price level vs ^TNX yield level over the period
- Sector and individual stock 30-day betas: regression vs ^TNX daily return, trailing 30 trading days
- Scenario model primary estimate: correlation-adjusted historical analog scaling (Sep-Nov 2023 baseline x 1.71x correlation multiplier)

---

## 9. Disclaimer

This market brief is for informational purposes only and does not constitute investment advice, a solicitation, or a recommendation to buy or sell any security. All analyses are based on publicly available data and modeled scenarios that may not materialize. Past performance and historical analogs are not guarantees of future results. Model estimates involve assumptions about correlation regimes, beta stability, and market structure that may shift rapidly. The three-model scenario framework (regression, historical analog scaling, compound model) produces estimates with wide confidence intervals; actual outcomes may differ materially. Readers should conduct their own due diligence and consult with licensed financial advisors before making investment decisions. The author(s) may hold positions in securities discussed herein.