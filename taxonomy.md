# Frontmatter Taxonomy

Every `report.md` in `reports/<dir>/` carries YAML frontmatter using only the
values defined here. Adding a new value = edit this file + commit explaining
why before using it in a report. This keeps the cross-report index queryable.

## Schema

```yaml
---
date:           <ISO date, YYYY-MM-DD>           # primary time index, required
event:          <event-slug>                       # required, kebab-case
event_type:     <see event_type below>             # required, controlled
source:                                            # required, list of URLs
  - "https://..."
asset_classes:  [<see asset_classes>]              # required, list (≥1)
geography:      [<ISO-3166 alpha-2 or region>]     # required, list
sentiment:      <see sentiment>                    # required
surprise:       <see surprise>                     # required
tags:           [<see tags>]                       # optional; only values from taxonomy
key_drivers:    [<free-form short slugs>]          # optional; describe causal factors
related:        [<paths to other report.md>]       # optional; cross-references
confidence:     <high|medium|low>                  # required
analyst_notes:  <one-line>                          # optional; interpretive caveats
---
```

## Controlled vocabularies

### event_type
- `central-bank-decision` — rate decision, statement, presser
- `central-bank-minutes` — minutes release
- `central-bank-speech` — official speech (Powell, Lagarde, Ueda, etc.)
- `central-bank-testimony` — Congressional testimony
- `economic-release` — CPI, NFP, GDP, PCE, retail sales, etc.
- `earnings-release` — corporate quarterly earnings
- `earnings-guidance` — pre-announcement, mid-quarter update
- `corporate-action` — M&A, spin-off, dividend change, buyback
- `regulatory-action` — SEC/FDA/CMA decisions
- `geopolitical-event` — sanctions, conflict, election
- `market-event` — flash crash, circuit breaker, large flow
- `commodity-event` — supply shock, inventory release, OPEC decision
- `crypto-event` — major fork, ETF flow, regulatory ruling
- `analyst-meta` — synthesis comparing multiple prior events

### asset_classes
- `rates` — sovereign yields, IRS, fed funds futures
- `credit` — IG, HY, distressed
- `equities` — broad equity markets
- `fx` — broad FX category
- `USD` `EUR` `JPY` `GBP` `CHF` `CNY` `INR` `BRL` — specific FX
- `commodities` — broad
- `energy` `metals` `agri` — commodity sub-classes
- `crypto` — broad
- `BTC` `ETH` `SOL` — specific tokens
- `real-estate` — REITs, direct
- `volatility` — VIX, MOVE, options vol structure

### geography
- ISO 3166 alpha-2 country codes: `US`, `JP`, `DE`, `GB`, `CN`, `IN`, `BR`, ...
- Regions: `EMEA`, `APAC`, `LATAM`, `EU`, `MENA`, `EM`, `DM`, `GLOBAL`

### sentiment
- `hawkish` — tightening bias / restrictive
- `dovish` — easing bias / accommodative
- `neutral` — balanced or no clear direction
- `mixed` — different parts of the release point in different directions
- `bullish` `bearish` — for non-monetary contexts (earnings, sector)
- `n/a` — sentiment dimension doesn't apply

### surprise
- `above-consensus` — outcome exceeded consensus expectation
- `as-expected` — outcome at or near consensus
- `below-consensus` — outcome missed consensus
- `no-consensus` — no quantitative consensus to compare against
- `n/a` — release doesn't admit a consensus comparison

### tags (extensible; document additions here)
- `rate-decision` `rate-cut` `rate-hike` `rate-hold`
- `dot-plot` `forward-guidance`
- `qt` `qe` `balance-sheet`
- `monetary-policy` `fiscal-policy`
- `labor-market` `inflation` `growth` `yield-curve`
- `risk-on` `risk-off` `flight-to-quality` `dollar-funding`
- `china-policy` `geopolitical-risk`
- Sector: `ai-capex` `semis` `cloud` `software` `fintech` `biotech` `oil-majors` `airlines` `banks` `housing-market`
- Earnings: `earnings-beat` `earnings-miss` `guidance-raise` `guidance-cut`
- Corporate: `m&a` `buyback` `dividend-change`
- Consumer: `consumer-strength` `consumer-weakness`

## When to add to the taxonomy

If an analyst encounters a concept that doesn't fit:
1. Stop. Do not invent a tag inline.
2. Edit this file, adding the new value with a one-line description.
3. Commit the taxonomy change with a message explaining why.
4. Then use it.

Rule: **better a small set of high-quality tags than a sprawling set of synonyms.**

## Sentinel example

```yaml
---
date: 2026-05-24
event: fomc-may-2026
event_type: central-bank-decision
source:
  - "https://www.federalreserve.gov/monetarypolicy/fomcpresconf20260524.htm"
  - "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260524a.htm"
asset_classes: [rates, USD, equities]
geography: [US]
sentiment: dovish
surprise: as-expected
tags: [rate-decision, rate-hold, dot-plot, forward-guidance, monetary-policy]
key_drivers:
  - dot-plot-shifted-dovish
  - powell-acknowledged-labor-softening
related:
  - reports/2026-03-19-fomc-march/report.md
confidence: high
analyst_notes: "Tone notably more cautious than March; market positioned hawkish."
---
```
