# Investment Research

Structured analyses of macroeconomic releases, equity events, sector signals, and other investment-relevant data. Produced by TY's Hermes agent OS (orchestrator + analyst + cleaner subagents).

## Layout

```
reports/<YYYY-MM-DD>-<topic-slug>/
├── raw/                 ← cleaner output: fetched source material, lightly normalized
│   ├── source1.md
│   ├── source2.md
│   └── ...
├── analysis.md          ← analyst output: structured analysis, evidence trail
└── report.md            ← synthesizer output: final deliverable (FRONTMATTER REQUIRED)
```

`report.md` is the canonical artifact for each event. It carries the YAML frontmatter
described in `taxonomy.md` and a detailed markdown body underneath. Cross-correlation
queries (over time, across asset classes, across event types) all key off that frontmatter.

## Adding a new report

The orchestrator handles this end-to-end. From any Hermes chat session (terminal or Signal):

> Produce a research report on `<topic>`. Sources: `<urls>`. Lens: `<angle>`.

The `research-report-workflow` skill kicks in. Cleaner fetches → analyst writes analysis → synthesizer produces `report.md` with proper frontmatter → orchestrator notifies via Signal.

## Querying across reports (Stage 2+)

Once enough reports exist (~10+), `tools/index.py` reads frontmatter from every
`report.md` into a SQLite index for queries like *"all dovish FOMC events
since 2025"* or *"reports touching both rates and equities, sorted by date"*.
Until then, simple shell tools work fine:

```bash
# all dovish reports
grep -lA1 'sentiment: dovish' reports/*/report.md

# tag frequency
yq '.tags[]' reports/*/report.md | sort | uniq -c | sort -rn
```

## Taxonomy

`taxonomy.md` defines the controlled vocabularies for frontmatter fields.
Analysts must consult it and only use values defined there. New tags require
an explicit edit to `taxonomy.md` (and a commit explaining why).
# investment-research
