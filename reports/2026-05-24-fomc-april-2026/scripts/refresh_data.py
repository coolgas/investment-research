#!/usr/bin/env python3
"""Pull latest yfinance data for all report tickers and save as data-refresh.md."""

import yfinance as yf
import pandas as pd
import sys, os

WORKSPACE = "/home/ty/workspace/investment-research/reports/2026-05-24-fomc-april-2026"

TICKERS = [
    "SPY", "QQQ", "IWM", "TLT", "XLU", "XLF", "XLRE",
    "^TNX",
    "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
    "JPM", "GS", "BAC",
    "PLD", "NEE", "WMT",
]

COMMODITY_TICKERS = {
    "GLD": "Gold (GLD ETF)",
    "CL=F": "Crude Oil (WTI Futures)",
    "DX-Y.NYB": "DXY (US Dollar Index)",
    "GBPUSD=X": "GBP/USD",
}

NAMES = {
    "SPY": "S&P 500", "QQQ": "Nasdaq-100", "IWM": "Small Caps",
    "TLT": "20+ Year Treasuries", "XLU": "Utilities",
    "XLF": "Financials", "XLRE": "Real Estate",
    "^TNX": "10Y Yield",
    "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "NVIDIA",
    "META": "Meta", "GOOGL": "Alphabet", "AMZN": "Amazon",
    "JPM": "JPMorgan", "GS": "Goldman Sachs", "BAC": "BofA",
    "PLD": "Prologis", "NEE": "NextEra Energy", "WMT": "Walmart",
}

CATEGORIES = [
    ("Broad Market & Sector ETFs", ["SPY", "QQQ", "IWM", "TLT", "XLU", "XLF", "XLRE"]),
    ("Rate Benchmarks", ["^TNX"]),
    ("Mega-Cap Tech", ["AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN"]),
    ("Banks", ["JPM", "GS", "BAC"]),
    ("Other Holdings", ["PLD", "NEE", "WMT"]),
    ("Commodities & FX", list(COMMODITY_TICKERS.keys())),
]

YTD_START = "2026-01-01"
FOMC_DATE = "2026-04-29"
TODAY_STR = "2026-05-22"


def span_cls(val, fmt=".2f"):
    if val is None or pd.isna(val):
        return '<span class="num">N/A</span>'
    if val > 0:
        return f'<span class="up">+{val:{fmt}}</span>'
    elif val < 0:
        return f'<span class="down">{val:{fmt}}</span>'
    return '<span class="num">0.00</span>'


def fmt_price(val, fmt=".2f"):
    if val is None or pd.isna(val):
        return '<span class="num">N/A</span>'
    return f'<span class="num">{val:{fmt}}</span>'


def extract(df, ticker):
    if df is None or df.empty:
        return None
    if isinstance(df.columns, pd.MultiIndex):
        col = ("Close", ticker)
        if col not in df.columns:
            col = ("Adj Close", ticker)
            if col not in df.columns:
                return None
    else:
        if ticker not in df.columns:
            return None
        col = ticker
    close = df[col].dropna()
    if len(close) < 2:
        return None
    latest_price = float(close.iloc[-1])
    prev_close = float(close.iloc[-2])
    daily_pct = (latest_price - prev_close) / prev_close * 100
    ytd = close.loc[YTD_START:]
    if len(ytd) >= 1:
        ytd_start = float(ytd.iloc[0])
        ytd_pct = (latest_price - ytd_start) / ytd_start * 100
    else:
        ytd_pct = None
    fomc = close.loc[FOMC_DATE:]
    if len(fomc) >= 1:
        fomc_start = float(fomc.iloc[0])
        fomc_pct = (latest_price - fomc_start) / fomc_start * 100
    else:
        fomc_pct = None
    return (latest_price, daily_pct, ytd_pct, fomc_pct)


def main():
    comm_tickers = list(COMMODITY_TICKERS.keys())
    all_names = {**NAMES, **COMMODITY_TICKERS}

    print("Downloading equities data...", file=sys.stderr)
    eq = yf.download(TICKERS, start="2025-12-15", end="2026-05-25", auto_adjust=True)
    print(f"  Shape: {eq.shape}", file=sys.stderr)

    print("Downloading commodities/FX data...", file=sys.stderr)
    cq = yf.download(comm_tickers, start="2025-12-15", end="2026-05-25", auto_adjust=True)
    print(f"  Shape: {cq.shape}", file=sys.stderr)

    results = {}
    for t in TICKERS:
        r = extract(eq, t)
        results[t] = r
        if r is not None:
            print(f"  {all_names[t]:30s} {t:10s} price={r[0]:10.2f} daily={r[1]:+.2f}%  ytd={r[2]:+.2f}%  fomc={r[3]:+.2f}%", file=sys.stderr)
        else:
            print(f"  {all_names[t]:30s} {t:10s} FAILED", file=sys.stderr)

    for t in comm_tickers:
        r = extract(cq, t)
        results[t] = r
        if r is not None:
            print(f"  {all_names[t]:30s} {t:10s} price={r[0]:10.2f} daily={r[1]:+.2f}%  ytd={r[2]:+.2f}%  fomc={r[3]:+.2f}%", file=sys.stderr)
        else:
            print(f"  {all_names[t]:30s} {t:10s} FAILED", file=sys.stderr)

    lines = []
    lines.append("---")
    lines.append("date: 2026-05-24")
    lines.append("event: fomc-april-2026")
    lines.append("type: data-refresh")
    lines.append("source: yfinance")
    lines.append(f"data_as_of: {TODAY_STR}")
    lines.append("tags:")
    lines.append("  - data-refresh")
    lines.append("  - yfinance")
    lines.append("---")
    lines.append("")
    lines.append("# Data Refresh: May 24, 2026")
    lines.append("")
    lines.append(f"**Data as of close:** {TODAY_STR}  ")
    lines.append("**Periods:** Daily change (prev close) | YTD (Jan 1, 2026) | Post-FOMC (Apr 29, 2026)")
    lines.append("")

    for cat_title, tickers in CATEGORIES:
        lines.append(f"## {cat_title}")
        lines.append("")
        lines.append("| Ticker | Name | Price | Daily | YTD | Post-FOMC |")
        lines.append("|--------|------|-------|-------|-----|-----------|")
        for t in tickers:
            name = all_names.get(t, t)
            r = results.get(t)
            if r is None:
                lines.append(f"| {t} | {name} | <span class=\"num\">N/A</span> | <span class=\"num\">N/A</span> | <span class=\"num\">N/A</span> | <span class=\"num\">N/A</span> |")
                continue
            price, daily, ytd, fomc = r
            lines.append(f"| {t} | {name} | {fmt_price(price)} | {span_cls(daily)} | {span_cls(ytd)} | {span_cls(fomc)} |")
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append(f"- Data via yfinance. Close of {TODAY_STR}.")
    lines.append("- YTD base: Jan 1, 2026. Post-FOMC base: Apr 29, 2026 (FOMC decision date).")
    lines.append("- Gold proxied by GLD ETF. Crude oil via CL=F (WTI futures).")
    lines.append("- DXY via DX-Y.NYB (US Dollar Index futures). GBP/USD via GBPUSD=X.")
    lines.append("- Span classes: up (green), down (red), num (neutral). No emojis.")
    lines.append("")

    output = "\n".join(lines)
    out_path = os.path.join(WORKSPACE, "data-refresh.md")
    print(f"Writing to: {out_path}", file=sys.stderr)
    with open(out_path, "w") as f:
        f.write(output)
    print(f"Wrote {len(output)} bytes", file=sys.stderr)
    print(f"File exists after write: {os.path.exists(out_path)}", file=sys.stderr)
    # Print to stdout for capture
    print(output)


if __name__ == "__main__":
    main()