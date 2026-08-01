# Trade Ideas Analysis: Rotation (Financials) vs Semi Dip Buying

**Date:** 2026-07-07
**Data Source:** yfinance (2021-01-01 to 2026-07-06 daily)

---

## Current State

### Semi Drawdown Magnitude

| Ticker | Current | 1W Chg | YTD% | Drawdown from Hi | Days Since Peak |
|--------|---------|--------|------|-----------------|----------------|
| SMH    | 604.30  | -7.87% | +60.04% | -9.66% | 14 |
| SOXX   | 581.51  | -9.25% | +83.03% | -11.22% | 14 |
| NVDA   | 195.55  | -2.27% | +3.96% | -17.05% | 53 |
| TSM    | 451.79  | -5.40% | +40.92% | -5.40% | 6 |
| ASML   | 1825.07 | -8.26% | +49.12% | -8.26% | 6 |
| AMAT   | 592.79  | -18.01% | +109.01% | -18.01% | 6 |
| LRCX   | 350.20  | -19.18% | +80.15% | -19.18% | 6 |
| KLAC   | 233.31  | -22.67% | +72.95% | -22.67% | 6 |

SMH (semi ETF) is -9.66% from its June 22 high (14 days ago). SOXX is -11.22% from peak.

The semi equipment names got hit hardest: KLAC -22.67%, LRCX -19.18%, AMAT -18.01%. In contrast, NVDA (which peaked May 14, already correcting for 53 days) is only -2.27% this week, suggesting the weakness is rotating within semis from GPU/design into equipment.

### Rotation Magnitude

| Ticker | Current | 1W Chg | YTD% | From 52W High |
|--------|---------|--------|------|--------------|
| XLF    | 56.14   | +4.72% | +0.88% | 0.00% (at 52W high) |
| IUFS.L | 16.52   | +4.09% | +0.00% | 0.00% (at 52W high) |
| XLV    | 161.96  | +2.08% | +5.36% | -1.09% from high |

XLF and IUFS.L are both at fresh 52-week highs. XLF is only +0.88% YTD -- this is a catch-up rotation from a flat year, not an acceleration of an existing uptrend.

### Macro Environment

- SPY: 751.28, +0.60% 1W, +9.82% YTD (near all-time high, -0.84% from peak)
- VIX: 15.57 (elevated but not panic territory)
- SMH-XLF 30-day rolling correlation: -0.358 (turned negative, confirming rotation)
- 1-year avg SMH-XLF correlation: +0.254 (normally positive)
- 5-year avg: +0.420

The negative correlation confirms a genuine rotation out of semis into financials, not a macro-driven selloff.

---

## Trade 1: Follow Rotation Into IUFS.L (Financials)

### Room Left Analysis

Both XLF and IUFS.L are at 52-week highs. This is not a case of chasing extended momentum. XLF is essentially flat YTD (+0.88%). The rotation has just brought it back to breakeven for the year.

However, the +4.09% weekly move in IUFS.L (and +4.72% in XLF) is in the 93rd percentile of weekly returns for these ETFs over the past 5 years.

### Historical Duration of XLF Relative Outperformance

Over the past 5 years (2021-2026):

- **Median XLF > SPY streak:** 2 weeks
- **Mean XLF > SPY streak:** 2.7 weeks
- **Maximum streak:** 6 weeks
- **Current streak:** 3 weeks (already above median)

The rotation is already 3 weeks old. Historically, these streaks tend to exhaust after 2-3 weeks. However, the median is skewed by many short streaks (2 weeks is the mode), and the maximum of 6 weeks suggests there can be meaningful additional room in exceptional cases.

### Forward Returns After +4% XLF Weekly Surges

Historical data (16 occurrences of XLF surging >4% in a week):

| Horizon | Mean Return | Median Return | Positive % | Samples |
|---------|------------|---------------|-----------|---------|
| 1 week  | -0.11%     | -0.01%        | 50%       | 16 |
| 2 weeks | -0.59%     | +0.07%        | 50%       | 16 |
| 4 weeks | +0.33%     | +1.55%        | 56%       | 16 |
| 8 weeks | +0.06%     | -0.77%        | 38%       | 16 |
| 12 weeks| +2.70%     | +2.44%        | 62%       | 16 |

**Key finding:** After a +4% weekly surge, XLF is essentially flat-to-slightly-negative over the next 1-2 months statistically. There is no persistent momentum. The forward return distribution is roughly centered on zero with wide variance.

For IUFS.L specifically (16 occurrences of >4% weekly surges):

| Horizon | Mean Return | Median Return | Positive % |
|---------|------------|---------------|-----------|
| 1 week  | -0.17%     | -0.24%        | 50% |
| 2 weeks | -0.11%     | +0.04%        | 50% |
| 4 weeks | +0.36%     | +1.40%        | 56% |
| 8 weeks | -0.61%     | -0.44%        | 31% |
| 12 weeks| +0.76%     | +1.99%        | 56% |

Same pattern: flat forward returns, modest negative bias at 8 weeks, slight positive at 12 weeks.

### Risk: Rotation Reversal / Semi Snap-Back

When XLF has surged (>2%) while SMH was negative (true rotation weeks):
- Historical count: 15 of 63 strong XLF weeks (24%)
- SMH performance the following week: mean -0.41%, median +0.58%, positive 67% of the time
- XLF performance the following week: mean -0.02%, median -0.11%

67% of the time, SMH bounces back positive the following week after a rotation week. The median bounce is +0.58%. This is weak but consistent with the mean-reversion pattern typical of rotation trades.

### Trade 1 Summary

**Bull case:** Financials are starting from a flat YTD base, so the rotation has more room mechanically than chasing something already extended. IUFS.L is at 52-week highs but only because it was flat for months.

**Bear case:** Historically, after a +4% weekly surge, forward returns are flat for 1-3 months. The median streak of relative outperformance is only 2 weeks (currently at 3). Data suggests chasing the rotation after a week like this has been a breakeven proposition historically.

**Risk/reward:** Unfavorable from a timing perspective based on historical patterns. The first week of the rotation was the move. Forward returns are centered on zero.

---

## Trade 2: Wait in Cash / Buy the Semi Dip

### Drawdown Context

**Current SMH drawdown:** -9.66% from peak (June 22 high, 14 days ago)
**Current SOXX drawdown:** -11.22% from peak

### Historical SMH Corrections >5% (2021-2026)

**25 completed corrections detected over 5+ years.**

**Depth Distribution:**

| Metric | Value |
|--------|-------|
| Median | -8.57% |
| Mean   | -11.50% |
| 25th percentile | -13.04% |
| 75th percentile | -6.17% |
| Minimum (shallowest) | -5.13% |
| Maximum (deepest) | -45.30% |

**Duration Distribution (days from peak to trough):**

| Metric | Value |
|--------|-------|
| Median | 13 days |
| Mean   | 59 days |
| 25th percentile | 6 days |
| 75th percentile | 33 days |

**Recovery Time (days from trough back to prior peak):**

| Metric | Value |
|--------|-------|
| Median | 9 days |
| Mean   | 23 days |
| Range  | 1 - 243 days |

**Where does -9.66% rank?**
Current drawdown is the 10th deepest out of 25 completed corrections. That places it at the 40th percentile -- deeper than 9 out of 25 corrections but shallower than 15. This is a moderate correction historically.

### Key Observations

1. **Median correction depth is -8.57%** -- The current -9.66% drawdown is slightly deeper than the median. This means roughly half of all SMH corrections have been shallower than where we are now.

2. **Median time to trough is 13 days** -- We are at day 14 since the June 22 peak. The median correction reaches its trough in 13 days. This suggests we may be at or near the trough zone statistically.

3. **Median recovery time from trough is only 9 days** -- Once the trough is in, half of all corrections recover fully within 9 days.

4. **The deepest corrections (2022 bear market) were -45%** -- This is not that environment. VIX at 15.57, SPY near all-time highs, no macro crisis. The 2022 drawdown dominates the mean depth statistic.

### Forward Returns After Hitting Specific Drawdown Levels

**After -10% SMH drawdown (20 occurrences):**

| Horizon | Mean | Median | Positive % | Samples |
|---------|------|--------|-----------|---------|
| 21 days (1M) | +6.83% | +5.08% | 82% | 17 |
| 63 days (3M) | +12.90% | +10.97% | 76% | 17 |
| 126 days (6M) | +21.73% | +20.59% | 80% | 15 |

**After -15% SMH drawdown (14 occurrences):**

| Horizon | Mean | Median | Positive % | Samples |
|---------|------|--------|-----------|---------|
| 21 days | +3.40% | +3.28% | 79% | 14 |
| 63 days | -1.71% | -1.65% | 50% | 14 |
| 126 days | +4.37% | +1.97% | 57% | 14 |

**After -20% SMH drawdown (8 occurrences):**

| Horizon | Mean | Median | Positive % | Samples |
|---------|------|--------|-----------|---------|
| 21 days | -0.41% | -2.19% | 38% | 8 |
| 63 days | +10.50% | +10.61% | 75% | 8 |
| 126 days | +10.42% | +12.34% | 75% | 8 |

**Key findings:**

- **Buying at -10% drawdown has historically been very profitable.** 82% positive at 1 month, mean +6.83%. This is the strongest signal in the data.

- **Buying at -15% drawdown shows a dip in 3-month returns** (mean -1.71%, only 50% positive). This suggests -15% drawdowns sometimes materialize during macro events that take longer to recover. However, at 6 months, returns turn positive.

- **Buying at -20% drawdown shows negative short-term momentum** (only 38% positive at 1 month) but strong recovery by 3 months (+10.50%).

- The SMH is currently at -9.66% drawdown from peak. It has NOT yet hit the -10% threshold for SMH itself (though SOXX is at -11.22% and individual names are much deeper). If it reaches -10%, the historical 1-month forward return is +6.83% with 82% probability of being positive.

### What Happens After a Rotation Week (SMH Next Week)?

After weeks where XLF >+2% and SMH is negative:
- SMH next week: positive 67% of the time
- Median SMH return: +0.58%

There is a mild mean-reversion tendency. SMH tends to bounce in the week following a rotation week.

### Key Support Levels

| Ticker | Current | SMA50 | SMA100 | SMA200 | 30d Low |
|--------|---------|-------|--------|--------|---------|
| SMH    | 604.30  | 582.05 (+3.82%) | 495.92 (+21.85%) | 427.23 | 567.88 |
| SOXX   | 581.51  | 548.45 (+6.03%) | 452.15 (+28.61%) | 377.57 | 524.46 |
| NVDA   | 195.55  | 209.66 (-6.73%) | 197.05 (-0.76%) | 191.12 | 192.53 |
| AMAT   | 592.79  | 493.77 (+20.05%) | 428.13 (+38.46%) | 340.85 | 427.36 |
| LRCX   | 350.20  | 322.61 (+8.55%) | 278.16 (+25.90%) | 223.64 | 302.03 |
| KLAC   | 233.31  | 209.77 (+11.22%) | 181.80 (+28.33%) | 152.38 | 184.22 |

**Notable:** NVDA is already trading below its SMA50 and SMA100. SMA200 at 191.12 is the next major support (currently at 195.55, only -2.32% away).

SMH itself is still above its SMA50 (582.05), which is about 3.8% below current levels. This is the nearest major support. The 30-day low of 567.88 is a secondary support level.

Individual semi equipment names (AMAT, LRCX, KLAC) all have their SMA50s far below current prices (8-20% below), meaning they are in uncharted territory for this move -- there is no nearby technical support from moving averages.

### Trade 2 Summary

**Bull case for dip buying:** The -9.66% SMH drawdown is near the historical median. 14 days since peak is near the median time-to-trough of 13 days. Historically, buying after -10% drawdowns yields +6.83% in 1 month with 82% win rate. The macro backdrop is benign (VIX 15.57, SPY near ATH). After rotation weeks, SMH bounces 67% of the time.

**Bear case for dip buying:** Individual semi equipment names are down 18-23% in one week. This is faster and deeper than typical corrections in those names. NVDA has been correcting for 53 days and is -17% from peak. The rotation could have more room if the market decides financials/healthcare are structurally cheap relative to semis. The SMH-XLF correlation has turned sharply negative (-0.358), unusual and potentially signaling more rotation ahead.

**Risk/reward:** Favorable from a statistical perspective. Historical pattern strongly favors buying SMH at -10% drawdowns. However, the speed of the semi equipment selloff (18-23% in one week) is unusual and warrants caution on individual names. At the ETF level (SMH), the data is supportive.

---

## Comparison Table

| Dimension | Trade 1: Follow Rotation (XLF/IUFS.L) | Trade 2: Buy Semi Dip (SMH) |
|-----------|----------------------------------------|------------------------------|
| **Expected 1M return** | ~0% (historical flat after +4% weeks) | +5 to +7% (82% win rate at -10% DD) |
| **Expected 3M return** | ~0% | +11 to +13% (76% win rate) |
| **Downside risk** | Moderate: rotation reverses, semis snap back, financials have no earnings catalyst | Moderate: drawdown deepens to -15% or worse before recovering |
| **Max historical drawdown from here** | ~3-5% (median PAUSE in streaks is ~1 week pullback) | Could go to -15% to -30% in severe cases (2022 analog) |
| **Time horizon** | Short-term tactical (1-4 weeks) | Medium-term (1-6 months) |
| **Conviction level** | Low: historical data shows flat forward returns after +4% weeks | Moderate-High: strong historical pattern of recovery after -10% drawdowns |

### Summary Assessment

The data favors Trade 2 (buying the semi dip) over Trade 1 (chasing the rotation) for the following reasons:

1. **Statistical edge:** Buying SMH at -10% drawdowns has produced positive 1M returns 82% of the time (mean +6.83%). Chasing a +4% XLF week has produced flat forward returns with no statistical edge.

2. **Current positioning:** The selloff is 14 days old, near the median 13-day correction duration. The drawdown depth (-9.66%) is at the 40th percentile of all corrections. We are at/near the median trough zone.

3. **Macro context:** Not a macro panic (VIX 15.57, SPY near ATH). This is profit-taking rotation out of an extended sector. Such corrections tend to be shallower and faster-recovering than macro-driven drawdowns.

4. **Caveat:** The equipment names (AMAT, LRCX, KLAC) have no nearby technical support and are declining at a pace that suggests more downside risk. A SMH position (diversified across semi holdings) is safer than picking individual equipment names.

5. **Risk management:** If the -10% level holds, the odds strongly favor a bounce. If the drawdown continues past -15%, forward returns become mixed at the 3-month horizon but still positive at 6 months (mean +10.50%).

### Suggested Framework

- **If SMH hits -10% from peak (~602):** Favorable risk/reward to initiate or add. Historical 1M forward return +6.83%.
- **If SMH hits -12% (~589):** More attractive. Closer to deeper corrections where multi-month returns are strong.
- **Stop-loss consideration:** If SMH breaks below -15% (~569), the 3-month return profile becomes mixed (50% positive), suggesting a need for longer time horizon.
- **For IUFS.L/XLF:** The data does not support adding after a +4% week. Best approach would be to wait for a pullback within the uptrend to enter.

---

**Disclaimer:** This analysis presents historical data and statistical patterns only. Past performance does not guarantee future results. Not investment advice. All trading involves risk of loss.
