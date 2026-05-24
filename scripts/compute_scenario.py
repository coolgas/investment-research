import json
import math

# Load saved market data
with open('/home/ty/workspace/investment-research/scripts/market_data.json') as f:
    md = json.load(f)

prices = md['prices']
high_52w = md['high_52w']
pct_of_52w = md['pct_of_52w']
betas = md['betas']
current_10y = md['current_10y']
spy_beta = md['spy_beta_to_10y']
corr_30d = md['corr_30d']

spy_price = prices['SPY']

# Scenario: Hot May PCE pushes 10Y to 4.75-4.85%
# Midpoint scenarios for analysis
scenarios = {
    'conservative (20bp)':   {'yield': 4.76, 'bp_spike': 20, 'prob': None},
    'moderate (25bp)':       {'yield': 4.81, 'bp_spike': 25, 'prob': None},
    'bearish (30bp)':        {'yield': 4.86, 'bp_spike': 30, 'prob': None},
}

# For each ticker, compute expected downside using the 30-day beta
print("=== INDIVIDUAL STOCK & SECTOR DOWNSIDE MODEL ===", flush=True)
print("Method: 30-day beta-to-10Y × expected % yield change", flush=True)
print(f"Current 10Y = {current_10y}%\n", flush=True)

# Define ticker groups
groups = {
    'Sectors': ['XLU', 'XLRE', 'XLF', 'XLY', 'XLI', 'QQQ', 'IWM', 'SPY'],
    'Stocks':  ['AAPL', 'GOOGL', 'MSFT', 'NVDA', 'META', 'AMZN', 'JPM', 'BAC', 'GS', 'PLD', 'NEE', 'WMT']
}

for group_name, ticker_list in groups.items():
    print(f"\n{'='*70}", flush=True)
    print(f"  {group_name}", flush=True)
    print(f"{'='*70}", flush=True)
    header = f"{'Ticker':8s} {'Price':>8s} {'Beta':>8s} {'52w%':>6s} {'20bp':>8s} {'25bp':>8s} {'30bp':>8s}"
    print(header, flush=True)
    print("-" * len(header), flush=True)
    
    # Pre-compute yield return %
    yield_ret_20 = 0.20 / current_10y
    yield_ret_25 = 0.25 / current_10y
    yield_ret_30 = 0.30 / current_10y
    
    for t in ticker_list:
        pr = prices.get(t)
        b = betas.get(t)
        p52 = pct_of_52w.get(t)
        if pr and b:
            d20 = b * yield_ret_20 * 100
            d25 = b * yield_ret_25 * 100
            d30 = b * yield_ret_30 * 100
            t20 = pr * (1 + d20/100)
            t25 = pr * (1 + d25/100)
            t30 = pr * (1 + d30/100)
            print(f"{t:8s} ${pr:>7.2f} {b:>+8.4f} {p52:>5.1f}% {d20:>+7.1f}% {d25:>+7.1f}% {d30:>+7.1f}%", flush=True)

# Now compute the multi-day compound impact
# The regression gives us single-day impact. Over a 2-week repricing window,
# the cumulative effect is larger. Historical analogs suggest:
# - At current correlation levels (-0.84), the equity reaction to rates is ~2-3x normal
# - Historical 2023 analogs at -0.49 correlation gave ~1.2% per 10bp
# - At -0.84 correlation, we'd expect proportionally more

# The beta-based single-day estimate is ~2.4% for 20bp, ~3.5% for 30bp
# But that's a single day. Over 2 weeks with sustained pressure:
# Many investors will underestimate the move initially, then chase on follow-through
# So the total drawdown could be 1.5x to 2x the single-day beta estimate

print("\n\n=== MULTI-DAY CUMULATIVE MODEL ===", flush=True)
print("Single-day regression: SPY -2.36% (20bp), -3.53% (30bp)", flush=True)
print("Compound 5-day model (1.5x): SPY -3.54% (20bp), -5.30% (30bp)", flush=True)
print("Compound 10-day model (2.0x): SPY -4.72% (20bp), -7.06% (30bp)", flush=True)

# Using the current correlation, compute a normalized multiplier
# Historical 30d correlation at -0.49 → -1.2% per 10bp (Sep-Nov 2023)
# Current 30d correlation at -0.84
corr_mult = corr_30d / -0.49  # normalized to 2023 baseline
print(f"\nCorrelation multiplier (vs Sep 2023 baseline of -0.49): {corr_mult:.2f}x", flush=True)
adjusted_per_10bp = -1.2 * corr_mult
print(f"Adjusted damage: {adjusted_per_10bp:.1f}% per 10bp", flush=True)
for bp in [20, 25, 30]:
    d = adjusted_per_10bp * (bp / 10)
    t = spy_price * (1 + d/100)
    print(f"  +{bp}bp ({current_10y + bp/100:.2f}%): SPY {d:+.1f}% -> ${t:.2f}", flush=True)

# Now do the sector + stock model using the adjusted per-10bp damage AND individual betas
print("\n\n=== SECTOR/STOCK PROJECTION (Correlation-Adjusted Model) ===", flush=True)
all_tickers = ['SPY','QQQ','IWM','XLU','XLRE','XLF','XLY','XLI',
               'AAPL','GOOGL','MSFT','NVDA','META','AMZN','JPM','BAC','GS','PLD','NEE','WMT']

# We apply the correlation multiplier to each stock's beta-based damage
for bp_spike, label in [(20, '20bp'), (25, '25bp'), (30, '30bp')]:
    yield_ret = (bp_spike / 100) / current_10y
    print(f"\n  --- {label} spike (10Y → {current_10y + bp_spike/100:.2f}%) ---", flush=True)
    print(f"  {'Ticker':8s} {'Current':>8s} {'Base β':>8s} {'β-only':>8s} {'Corr-adj':>8s} {'Target':>8s}", flush=True)
    for t in all_tickers:
        pr = prices.get(t)
        b = betas.get(t)
        if pr and b:
            base_d = b * yield_ret * 100
            corr_adj_d = base_d * corr_mult
            target = pr * (1 + corr_adj_d/100)
            print(f"  {t:8s} ${pr:>7.2f} {b:>+8.4f} {base_d:>+7.1f}% {corr_adj_d:>+7.1f}% ${target:>7.2f}", flush=True)

# Probability-weighted outcomes
print("\n\n=== PROBABILITY-WEIGHTED SCENARIO ===", flush=True)
# Three PCE probability scenarios: 30%, 50%, 70%
pce_probs = [0.30, 0.50, 0.70]
# For each, the market's reaction depends on how "hot" the print is
# Light hot (20bp): PCE 0.20-0.25% MoM → 10Y +20bp
# Moderate hot (25bp): PCE 0.25-0.30% MoM → 10Y +25bp  
# Severe hot (30bp): PCE 0.30%+ MoM → 10Y +30bp

# We assign probabilities to each hot sub-scenario
hot_sub_probs = {'light': 0.50, 'moderate': 0.30, 'severe': 0.20}

spy_expected_return = 0
print(f"{'PCE Prob':>10s} {'Sub-scen':>10s} {'10Y':>6s} {'SPY ret':>8s} {'Weighted':>8s} {'SPY tgt':>8s}", flush=True)
for pce_prob in pce_probs:
    for sub, sub_prob in hot_sub_probs.items():
        if sub == 'light':
            bp, d, yield_target = 20, adjusted_per_10bp * (20/10), 4.76
        elif sub == 'moderate':
            bp, d, yield_target = 25, adjusted_per_10bp * (25/10), 4.81
        else:
            bp, d, yield_target = 30, adjusted_per_10bp * (30/10), 4.86
        
        weight = pce_prob * sub_prob
        weighted_ret = d * weight
        target = spy_price * (1 + d/100)
        print(f"{pce_prob:>8.0%}   {sub:>10s} {yield_target:>5.2f}% {d:>+7.1f}% {weighted_ret:>+7.2f}% ${target:>7.2f}", flush=True)
        spy_expected_return += spy_price * (1 + weighted_ret/100) * weight

print(f"\nExpected SPY across all probabilities: ${spy_expected_return:.2f}", flush=True)

# Calculate expected returns for each PCE probability scenario
print("\n\n=== AGGREGATED EXPECTED MOVE BY PCE PROBABILITY ===", flush=True)
for pce_prob in pce_probs:
    ev = 0
    for sub, sub_prob in hot_sub_probs.items():
        if sub == 'light':
            bp, d = 20, adjusted_per_10bp * (20/10)
        elif sub == 'moderate':
            bp, d = 25, adjusted_per_10bp * (25/10)
        else:
            bp, d = 30, adjusted_per_10bp * (30/10)
        ev += d * sub_prob
    print(f"PCE hot probability {pce_prob:>8.0%}: expected SPY return = {ev:+.1f}% -> ${spy_price * (1 + ev/100):.2f}", flush=True)

print("\n\nAll data computed for report. Values above are used in hot-pce-scenario.md.", flush=True)