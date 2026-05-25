---
date: 2026-05-25
event: hot-pce-may-2026-scenario
type: scenario-analysis
asset_classes:
  - equities
  - rates
tickers:
  - SPY
  - QQQ
  - XLU
  - XLF
  - XLRE
  - IWM
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
tags:
  - pce
  - inflation
  - downside-scenario
  - rate-spike
  - yield-correlation
  - higher-for-longer
  - hot-pce
  - scenario-model
confidence: medium-high
analyst_notes: Baseline data from yfinance 5/24/2026 close. Correlation computed over trailing 30 days. Individual stock betas computed over trailing 30 days vs ^TNX daily returns. Historical analogs from 2022-2026 data. Correlation-adjusted multiplier uses Sep-Nov 2023 as the baseline analog (corr = -0.49) and scales proportionally to current 30d correlation of -0.84.
---

# Hot May PCE (ex-Energy) Downside Scenario

**Analysis Date:** May 24, 2026  |  **Data As Of:** May 22, 2026 Close

**Prerequisite Reading:** `post-fomc-market-analysis.md`, `analysis.md`, `report.md`

## 1. Scenario Framework

### Trigger

May PCE (ex-energy) prints hot — above consensus. The April FOMC analysis (`post-fomc-market-analysis.md`) explicitly flagged this risk: if core PCE ex-energy surprises to the upside, it unravels the "hold now, cut later" narrative that has fueled the post-FOMC risk rally. The SPY-10Y correlation of -0.84 (30-day trailing) means rates are the dominant equity driver — a yield spike translates directly into equity losses.

### Key Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| Current 10Y | 4.56% | ^TNX close |
| SPY-10Y correlation (30d trailing) | **-0.84** | Rolling 30d calculation |
| SPY-10Y correlation (post-FOMC reported) | -0.90 | `post-fomc-market-analysis.md` |
| SPY | $745.64 | yfinance |
| SPY % of 52w high | 99.7% | yfinance |
| 10Y 52w high | 4.67% | yfinance |

### Yield Spike Scenarios

| Scenario | PCE MoM ex-energy | 10Y Impact | 10Y Target |
|----------|-------------------|------------|------------|
| Light hot | 0.20-0.25% | +15-20bp | 4.71-4.76% |
| Moderate hot | 0.25-0.30% | +20-25bp | 4.76-4.81% |
| Severe hot | >0.30% | +25-30bp | 4.81-4.86% |

A 10Y move to 4.75% was the threshold identified in the `post-fomc-market-analysis.md` report as the trigger for a rapid unwind of the post-FOMC risk rally.

## 2. Methodology

Three independent modeling approaches are cross-validated:

### A. Regression (30-day beta-to-10Y)

SPY daily return-to-10Y return beta over trailing 30 days: **-0.5374**. A 1% move in 10Y yield → -0.54% move in SPY on the same trading day.

A 20bp yield spike (4.56% → 4.76%) represents a +4.39% relative return in the yield level, implying a **-2.4% single-day SPY drawdown** from the regression alone.

### B. Historical analog scaling

Periods with high SPY-10Y negative correlation at similar yield levels (4.5-5.0%) are referenced. The current 30-day correlation of -0.84 is unprecedented relative to these analogs — the closest analog (Sep-Nov 2023, 10Y=4.17%→4.99%) had a correlation of only -0.49. Applying a **correlation multiplier of 1.71x** to the Sep-Nov 2023 analog damage of -1.2% per 10bp gives **-2.1% per 10bp** of yield rise.

### C. Multi-day compound model

The regression gives a single-day snapshot. A sustained hot-PCE repricing over 5-10 trading days compounds. Historical analogs suggest a cumulative factor of **1.5x to 2.0x** the single-day regression estimate as the market re-rates term premium, inflation expectations, and the Fed reaction function.

### Confidence Interval

| Scenario | 30d β Regression (single-day) | Correlation-Adjusted (primary) | Upper Bound (1.5x) | Lower Bound (2.0x) |
|----------|:---:|:---:|:---:|:---:|
| 20bp to 4.76% | -2.4% | **-4.1%** | -3.5% | -4.7% |
| 25bp to 4.81% | -2.9% | **-5.1%** | -4.4% | -5.9% |
| 30bp to 4.86% | -3.5% | **-6.2%** | -5.3% | -7.1% |

**Primary model** (correlation-adjusted) is used for the remainder of this report. Confidence intervals reflect the range between 1.5x and 2.0x compound factors.

## 3. Sector Impact Ranking

### Sorted by expected downside (25bp moderate-hot scenario)

| Rank | Ticker | Sector | 30d β | 20bp | 25bp | 30bp | Key Driver |
|------|--------|--------|:-----:|:----:|:----:|:----:|-----------|
| 1 | **IWM** | Small Caps | -1.00 | -7.5% | -9.4% | -11.3% | Highest rate sensitivity; small caps levered to credit conditions |
| 2 | **XLY** | Consumer Discr. | -0.86 | -6.5% | -8.1% | -9.7% | Duration-sensitive; consumer spending tied to financing costs |
| 3 | **XLI** | Industrials | -0.75 | -5.6% | -7.0% | -8.4% | CapEx cycle vulnerable to higher rates |
| 4 | **QQQ** | Nasdaq-100 | -0.73 | -5.5% | -6.8% | -8.2% | Long-duration growth; high multiple compression risk |
| 5 | **XLRE** | Real Estate | -0.49 | -3.7% | -4.6% | -5.6% | Direct discount rate proxy; 10Y > 4.75% triggers REIT selloff |
| 6 | **SPY** | S&P 500 | -0.54 | -4.0% | -5.0% | -6.1% | Broad market reference |
| 7 | **XLF** | Financials | -0.27 | -2.0% | -2.5% | -3.0% | Steepener benefit partially offsets rate headwind |
| 8 | **XLU** | Utilities | -0.23 | -1.8% | -2.2% | -2.6% | Defensive bid; already sold off post-FOMC (-0.72%) |

### Sector Commentary

**IWM (Small Caps)** leads losses — a 25bp spike implies -9.4% downside. Small caps have the highest rate beta (-1.00), are levered to floating-rate debt, and lack the pricing power of large caps. They are the most crowded "hot PCE" short.

**XLY (Consumer Discretionary)** is the second-hardest hit — consumer spending is financed, and a higher discount rate compresses the present value of discretionary purchases. The -0.86 beta reflects this.

**XLU and XLRE** merit a special note. Both sectors _should_ be the most rate-sensitive (utilities are bond proxies, REITs are discount-rate driven). However:
- XLU has a **-0.23 beta** — utilities have already been sold off post-FOMC (-0.72%) and may see a defensive bid if hot PCE triggers a macro risk-off trade alongside the rate spike
- XLRE has a **-0.49 beta** — REITs at 99.6% of 52w high could get a rate-driven pullback, but data center/industrial REITs have enough demand-side momentum to partially offset (per `post-fomc-market-analysis.md`)

**XLF (Financials, -0.27)** is the least impacted sector — the steepening yield curve (short rates unchanged, long rates rising) improves bank NIMs, providing a partial offset to the rate-equity correlation.

## 4. Individual Stock Downside

### Sorted by expected downside (25bp moderate-hot scenario)

| Rank | Ticker | Current Price | 30d β | 20bp | 25bp | 30bp | 30bp Target | % of 52w High |
|------|--------|:---:|:-----:|:----:|:----:|:----:|:-----:|:-----:|
| 1 | **GS** | $996.73 | -1.35 | -10.1% | -12.7% | -15.2% | $845 | 100% |
| 2 | **NVDA** | $215.33 | -1.00 | -7.5% | -9.4% | -11.2% | $191 | 91.3% |
| 3 | **GOOGL** | $382.97 | -0.96 | -7.2% | -9.0% | -10.8% | $342 | 95.1% |
| 4 | **PLD** | $145.90 | -0.81 | -6.1% | -7.6% | -9.1% | $133 | 100% |
| 5 | **AMZN** | $266.32 | -0.56 | -4.2% | -5.3% | -6.3% | $249 | 96.8% |
| 6 | **AAPL** | $308.82 | -0.49 | -3.7% | -4.6% | -5.5% | $292 | 100% |
| 7 | **JPM** | $306.38 | -0.51 | -3.8% | -4.8% | -5.8% | $289 | 92.0% |
| 8 | **BAC** | $51.80 | -0.34 | -2.6% | -3.2% | -3.8% | $50 | 91.0% |
| 9 | **META** | $610.26 | -0.24 | -1.8% | -2.3% | -2.7% | $594 | 77.4% |
| 10 | **NEE** | $88.55 | -0.14 | -1.1% | -1.3% | -1.6% | $87 | 90.5% |
| 11 | **WMT** | $120.27 | +0.01 | ~0% | ~0% | ~0% | $120 | 89.6% |
| 12 | **MSFT** | $418.57 | +0.03 | ~0% | ~0% | ~0% | $420 | 77.7% |

### Stock Commentary

**GS (-1.35 β)** is the most rate-sensitive stock in the universe. The -1.35 beta means a 1% 10Y yield move triggers a 1.35% GS decline. This is anomalous for an investment bank — typically, higher rates benefit fixed-income trading. The negative beta suggests GS is trading as a valuation proxy (100% of 52w high, P/E multiple compression risk) rather than on its earnings composition. GS at $996.73 could see $846 on a 30bp spike — its first sub-$850 level in over a month.

**NVDA and GOOGL** have high negative betas (-1.00 and -0.96 respectively) reflecting their long-duration growth profiles. NVDA at $215 ($191 on 30bp) would approach its post-FOMC lows — the 91.3% of 52w high means less "fatigue" room than peers. GOOGL at $383 is 95.1% of 52w high and has post-FOMC momentum (+9.44%) to lose.

**MSFT and WMT** are near-zero beta to 10Y. MSFT at 77.7% of 52w high and WMT at 89.6% are trading on stock-specific factors (AI CapEx concerns for MSFT; consumer margin compression for WMT). They are **hedges within the portfolio** — a hot-PCE scenario affects them minimally through the rate channel.

**META** has a low beta (-0.24) but is already at 77.4% of 52w high, deeply discounted. The low beta suggests META's stock-specific headwinds (capex skepticism, AI ROI uncertainty) have decoupled it from macro rates entirely. The modest additional downside (-2.3% on 25bp) reflects this.

**AAPL at 100% of 52w high** with a -0.49 beta is a "double vulnerability" — it's at its peak valuation with moderate rate sensitivity. A 25bp spike to $295 would be its first significant break below $300 since the post-FOMC run.

## 5. Historical Analog Validation

### Analog 1: Jul-Oct 2023 (10Y 3.86% → 4.99%)

- **10Y move:** +113bp over ~4 months
- **SPY peak-to-trough:** -10.0%
- **30d correlation at 10Y peak:** -0.25
- **Damage per 10bp:** -0.8%

While the yield move was far larger (+113bp), the equity damage per 10bp was lower (-0.8%) because the correlation regime was much weaker (-0.25 vs current -0.84). The current environment is fundamentally different — rates are _the_ dominant equity driver now in a way they were not in 2023.

### Analog 2: Sep-Nov 2023 (10Y 4.17% → 4.99%)

- **10Y move:** +82bp over ~2 months
- **SPY peak-to-trough:** -10.0%
- **30d correlation at 10Y peak:** -0.25
- **Damage per 10bp:** -1.2%

A tighter window around the 10Y's surge to 5.0%. QQQ -12.0%, IWM -14.6%, XLRE -12.8% during this period. SPY -10.0% on +82bp of yield rise = -1.2% per 10bp. This is the **baseline analog**.

### Analog 3: Jan-Jun 2022 (10Y 1.63% → 3.48%)

- **10Y move:** +185bp over ~6 months
- **SPY peak-to-trough:** -23.0%
- **Damage per 10bp:** -1.2%

Same per-10bp damage as Sep-Nov 2023, but from a lower base. The equity damage per 10bp appears relatively consistent at **-1.0% to -1.2% per 10bp** across historical bear-steepening episodes, but from much lower correlation regimes (-0.20 to -0.49).

### Correlation Regime Shift: The Key Differentiator

The current 30-day SPY-10Y correlation of **-0.84** is far beyond any previous analog. The closest analog peak was -0.49 (Sep-Nov 2023). This regime difference is the strongest argument for a more severe per-10bp equity impact today.

| Period | 30d Correlation | Damage per 10bp |
|--------|:---:|:---:|
| Jul-Oct 2023 | -0.25 | -0.8% |
| Sep-Nov 2023 | -0.49 | -1.2% |
| Jan-Jun 2022 | -0.20 | -1.2% |
| Jan-Mar 2025 | -0.54 | -4.4%* |
| **Current** | **-0.84** | **-2.1% (modeled)** |

*Jan-Mar 2025 was confounded by tariff escalation — the -4.4% per 10bp is an overestimate for a rates-only shock.

### Validation Summary

The correlation-adjusted model (-2.1% per 10bp) sits between the 2023 analog (-1.2%) and the 2025 tariff-confounded event (-4.4%). It is grounded in the proportional scaling of the Sep-Nov 2023 analog by the correlation ratio (-0.84/-0.49 = 1.71x). This is our **primary model**.

## 6. Probability-Weighted Outcomes

### Conditional on Hot PCE Occurring

If May PCE (ex-energy) prints hot, the sub-scenario probabilities and consequent SPY expected returns are:

| Sub-scenario | Probability (conditional) | 10Y Target | SPY Return | SPY Target |
|-------------|:---:|:---:|:---:|:---:|
| Light hot (0.20-0.25%) | 50% | 4.76% | -4.1% | $715 |
| Moderate hot (0.25-0.30%) | 30% | 4.81% | -5.1% | $707 |
| Severe hot (>0.30%) | 20% | 4.86% | -6.2% | $700 |
| **Expected (if hot)** | **100%** | **4.79%** | **-4.8%** | **$709** |

Expected SPY return conditional on hot PCE: **-4.8%** (probability-weighted across sub-scenarios).

### Unconditional Expected Move by PCE Probability

The unconditional expected move depends on the _ex-ante_ probability of a hot print:

| P(hot PCE) | Expected SPY Return | Expected SPY Target | Interpretation |
|:---:|:---:|:---:|:---|
| **30%** | **-1.4%** | $735 | Low conviction hot — market may already be pricing this in |
| **50%** | **-2.4%** | $728 | Coin flip — significant asymmetry in positioning |
| **70%** | **-3.4%** | $720 | High conviction — market would be mispriced if this is correct |

### Expected Move Matrix

| P(hot PCE) | Light (50%) | Moderate (30%) | Severe (20%) | Weighted Total |
|:---:|:---:|:---:|:---:|:---:|
| 30% | -0.62% | -0.46% | -0.37% | **-1.44%** |
| 50% | -1.03% | -0.77% | -0.62% | **-2.40%** |
| 70% | -1.44% | -1.08% | -0.86% | **-3.36%** |

## 7. Key Risks & Caveats

1. **Correlation may rise further.** The post-FOMC correlation was reported at -0.90; our 30-day estimate is -0.84. If correlation tightens further after the PCE print, actual damage may exceed the model's primary estimate.

2. **Non-linear regime change.** At -0.84 correlation, the equity market is already in an extreme regime. If the 10Y breaches 4.75% — the threshold identified in `post-fomc-market-analysis.md` — forced liquidations, gamma effects, and momentum-driven selling could produce damage well beyond the proportional model.

3. **Safe-haven unwind.** A hot PCE would simultaneously imply higher yields AND higher inflation expectations. Unlike 2023, when higher yields were driven by growth expectations (good for equities), a hot PCE driven by sticky non-energy inflation is stagflationary — the worst scenario for equities.

4. **Stock-specific tail risks.** GS (-1.35 β) and PLD (-0.81 β) at 100% of 52w high face disproportionate re-rating risk. AAPL at 100% is also vulnerable. META and MSFT, already at 77% of 52w high, may actually be _less_ vulnerable — much of the rate-driven downside may already be priced in.

5. **Data recency.** This analysis uses 30-day trailing betas based on data through May 22, 2026. Betas shift rapidly in high-correlation regimes. Re-estimate weekly while the -0.80+ regime persists.

6. **Jan-Mar 2025 analog confound.** The Jan-Mar 2025 period had a starting 10Y of 4.57% (nearly identical to current) and saw SPY -10.0% on only +23bp of yield rise. However, this was a tariff-escalation period, not a pure rate shock. The -4.4% per 10bp from that analog is not used as the primary estimate but represents a **tail-risk scenario** if a hot PCE also reignites trade-policy fears.

## 8. Positioning Recommendations

- **Tactical short candidates:** IWM, NVDA, GOOGL, GS (highest rate beta; most downside)
- **Relative value hedges:** Long WMT / short IWM (zero correlation to rates vs highest); Long MSFT / short GOOGL (already discounted vs at 52w high with high beta)
- **Sector rotation:** Reduce QQQ exposure toward XLF (steepener benefit partially offsets the rate-equity correlation)
- **Avoid:** REITs if 10Y stays above 4.75% — per the prior analysis, XLRE holds up until 4.75%, after which the discount-rate damage outweighs demand momentum
- **Warning:** Do not buy the dip in GS, PLD, or AAPL immediately post-PCE — all three are at 100% of 52w high with moderate-to-high rate beta, and a mean-reversion to their 50-day moving averages implies further downside even without the hot-PCE trigger

## Data Sources

- yfinance 1.4.0 (price data for ^TNX, SPY, QQQ, IWM, XLU, XLRE, XLF, XLY, XLI, AAPL, GOOGL, MSFT, NVDA, META, AMZN, JPM, BAC, GS, PLD, NEE, WMT)
- Prior analysis: `post-fomc-market-analysis.md`, `analysis.md`, `report.md` in `reports/2026-05-24-fomc-april-2026/`
- All calculations in `scripts/market_data.json`, `scripts/compute_scenario.py`
