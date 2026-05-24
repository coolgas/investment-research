"""
yfinance data refresh for FOMC April 2026 report.
Pulls latest prices, daily%, YTD%, post-FOMC% for all tracked tickers.
Handles yfinance multi-index columns (newer versions).
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date
import sys

TODAY = date(2026, 5, 24)
YTD_START = "2026-01-01"
FOMC_DATE = "2026-04-29"

TICKERS = {
    "SPY": "SPY", "QQQ": "QQQ", "IWM": "IWM", "TLT": "TLT",
    "XLU": "XLU", "XLF": "XLF", "XLRE": "XLRE",
    "^TNX": "^TNX",
    "AAPL": "AAPL", "MSFT": "MSFT", "NVDA": "NVDA",
    "META": "META", "GOOGL": "GOOGL", "AMZN": "AMZN",
    "JPM": "JPM", "GS": "GS", "BAC": "BAC",
    "PLD": "PLD", "NEE": "NEE", "WMT": "WMT",
    "Gold": "GC=F", "Crude": "CL=F",
    "DXY": "DX-Y.NYB", "GBP/USD": "GBPUSD=X",
}


def extract_close(data, ticker_str):
    """Extract the Close series from a yfinance DataFrame regardless of column format."""
    if data is None or data.empty:
        return pd.Series(dtype=float)

    cols = data.columns

    # MultiIndex case: (Close, TICKER)
    if isinstance(cols, pd.MultiIndex):
        if ("Close", ticker_str) in cols:
            return data[("Close", ticker_str)].dropna()
        # Try without ticker suffix
        close_cols = [c for c in cols if c[0] == "Close"]
        if close_cols:
            return data[close_cols[0]].dropna()

    # Simple Index case: 'Close' is a column
    if "Close" in cols:
        return data["Close"].dropna()

    # Fallback: first column
    return data.iloc[:, 0].dropna()


def safe_download(ticker_str, start, end):
    """Download price data with error handling."""
    try:
        data = yf.download(ticker_str, start=start, end=end, progress=False, auto_adjust=True)
        if data.empty:
            return None
        return data
    except Exception as e:
        print(f"  WARN: {ticker_str} download failed: {e}", file=sys.stderr)
        return None


def pct_change_from_close(data, ticker_str):
    """Calculate % change between first and last close in the series."""
    close = extract_close(data, ticker_str)
    if len(close) < 2:
        return None
    first = close.iloc[0]
    last = close.iloc[-1]
    if first == 0 or pd.isna(first) or pd.isna(last):
        return None
    return ((last / first) - 1) * 100


def latest_close(data, ticker_str):
    """Get latest close and its date."""
    close = extract_close(data, ticker_str)
    if close.empty:
        return None, None
    return close.iloc[-1], close.index[-1].date()


def get_daily_change(ticker_str):
    """Get daily % change for a ticker over a 5-day window."""
    try:
        data = yf.download(ticker_str, period="5d", progress=False, auto_adjust=True)
        close = extract_close(data, ticker_str)
        if len(close) < 2:
            return None
        prev = close.iloc[-2]
        curr = close.iloc[-1]
        if prev == 0 or pd.isna(prev) or pd.isna(curr):
            return None
        return ((curr / prev) - 1) * 100
    except Exception as e:
        print(f"  WARN: {ticker_str} daily change failed: {e}", file=sys.stderr)
        return None


def main():
    results = []
    latest_date_global = None

    for display_name, yf_ticker in TICKERS.items():
        print(f"Processing {display_name} ({yf_ticker})...", file=sys.stderr)

        # YTD period
        ytd_data = safe_download(yf_ticker, YTD_START, TODAY.isoformat())
        latest_price, ld = latest_close(ytd_data, yf_ticker)
        if ld and latest_date_global is None:
            latest_date_global = ld
        ytd_pct = pct_change_from_close(ytd_data, yf_ticker) if ytd_data is not None else None

        # Post-FOMC period
        fomc_data = safe_download(yf_ticker, FOMC_DATE, TODAY.isoformat())
        fomc_pct = pct_change_from_close(fomc_data, yf_ticker) if fomc_data is not None else None

        # Daily change
        daily_pct = get_daily_change(yf_ticker)

        results.append({
            "ticker": display_name,
            "yf_ticker": yf_ticker,
            "latest_price": latest_price,
            "latest_date": ld,
            "daily_pct": daily_pct,
            "ytd_pct": ytd_pct,
            "fomc_pct": fomc_pct,
        })

        price_str = f"{latest_price:.2f}" if latest_price else "N/A"
        print(f"  Price: {price_str}, Date: {ld}", file=sys.stderr)

    as_of = str(latest_date_global) if latest_date_global else str(TODAY)

    # --- Build output ---
    lines = []
    lines.append("---")
    lines.append("date: 2026-05-24")
    lines.append("event: fomc-april-2026")
    lines.append("type: data-refresh")
    lines.append("source: yfinance")
    lines.append("data_as_of: " + as_of)
    lines.append("---")
    lines.append("")
    lines.append("# Data Refresh: yfinance Market Data")
    lines.append("")
    lines.append("As of close on " + as_of + ".")
    lines.append("")

    equities = ["SPY", "QQQ", "IWM", "TLT", "XLU", "XLF", "XLRE",
                "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN",
                "JPM", "GS", "BAC", "PLD", "NEE", "WMT"]
    eq_names = {
        "SPY": "S&P 500", "QQQ": "Nasdaq-100", "IWM": "Russell 2000",
        "TLT": "20Y+ Treasury Bonds", "XLU": "Utilities", "XLF": "Financials",
        "XLRE": "Real Estate", "AAPL": "Apple", "MSFT": "Microsoft",
        "NVDA": "NVIDIA", "META": "Meta Platforms", "GOOGL": "Alphabet",
        "AMZN": "Amazon", "JPM": "JPMorgan Chase", "GS": "Goldman Sachs",
        "BAC": "Bank of America", "PLD": "Prologis", "NEE": "NextEra Energy",
        "WMT": "Walmart"
    }

    # For ^TNX (yield), prices are yield percentages. Compute bp changes directly.
    tnx_row = next((r for r in results if r["ticker"] == "^TNX"), None)
    tnx_daily_bp = tnx_row["daily_pct"] if tnx_row and tnx_row["daily_pct"] is not None else None
    tnx_ytd_bp = tnx_row["ytd_pct"] if tnx_row and tnx_row["ytd_pct"] is not None else None
    tnx_fomc_bp = tnx_row["fomc_pct"] if tnx_row and tnx_row["fomc_pct"] is not None else None

    # For TNX, the % changes from yfinance are in yield% units (e.g. 4.56->4.77 = +0.21)
    # For bp, multiply by 100.
    # Wait — actually, if latest is 4.56 and prior is 4.35, the % change is (4.56/4.35-1)*100 = +4.83%
    # That's not right for yield bp. We need absolute yield difference in bp.
    # Let me calculate actual bp changes separately.

    lines.append("## Equities and Sector ETFs")
    lines.append("")
    lines.append("| Ticker | Name | Last Price | Daily % | YTD % | Post-FOMC % |")
    lines.append("|--------|------|-----------|---------|-------|-------------|")

    for tk in equities:
        r = next((r for r in results if r["ticker"] == tk), None)
        if r:
            price = f"{r['latest_price']:.2f}" if r['latest_price'] else "N/A"
            d = f"{r['daily_pct']:+.2f}%" if r['daily_pct'] is not None else "N/A"
            y = f"{r['ytd_pct']:+.2f}%" if r['ytd_pct'] is not None else "N/A"
            f = f"{r['fomc_pct']:+.2f}%" if r['fomc_pct'] is not None else "N/A"
            lines.append(f"| {tk} | {eq_names.get(tk, '')} | {price} | {d} | {y} | {f} |")

    lines.append("")

    # TNX row — compute bp changes directly from raw close values
    lines.append("## Rate Benchmarks")
    lines.append("")
    lines.append("| Ticker | Name | Last Yield | Daily (bp) | YTD (bp) | Post-FOMC (bp) |")
    lines.append("|--------|------|-----------|-----------|----------|----------------|")

    if tnx_row and tnx_row["latest_price"]:
        try:
            tnx_price = tnx_row["latest_price"]
            tnx_price_str = f"{tnx_price:.2f}%"

            # Compute bp changes from raw downloaded data
            tnx_yf = "^TNX"
            ytd_data_tnx = safe_download(tnx_yf, YTD_START, TODAY.isoformat())
            fomc_data_tnx = safe_download(tnx_yf, FOMC_DATE, TODAY.isoformat())

            # Daily bp
            daily_tnx_data = yf.download(tnx_yf, period="5d", progress=False, auto_adjust=True)
            daily_tnx_close = extract_close(daily_tnx_data, tnx_yf)
            if len(daily_tnx_close) >= 2:
                daily_bp = (daily_tnx_close.iloc[-1] - daily_tnx_close.iloc[-2]) * 100
                daily_bp_str = f"{daily_bp:+.1f}bp"
            else:
                daily_bp_str = "N/A"

            # YTD bp
            ytd_close = extract_close(ytd_data_tnx, tnx_yf)
            if len(ytd_close) >= 2:
                ytd_bp = (ytd_close.iloc[-1] - ytd_close.iloc[0]) * 100
                ytd_bp_str = f"{ytd_bp:+.1f}bp"
            else:
                ytd_bp_str = "N/A"

            # Post-FOMC bp
            fomc_close = extract_close(fomc_data_tnx, tnx_yf)
            if len(fomc_close) >= 2:
                fomc_bp = (fomc_close.iloc[-1] - fomc_close.iloc[0]) * 100
                fomc_bp_str = f"{fomc_bp:+.1f}bp"
            else:
                fomc_bp_str = "N/A"

            lines.append(f"| ^TNX | 10Y Treasury Yield | {tnx_price_str} | {daily_bp_str} | {ytd_bp_str} | {fomc_bp_str} |")
        except Exception as e:
            lines.append(f"| ^TNX | 10Y Treasury Yield | {tnx_price_str} | N/A | N/A | N/A |")

    lines.append("")

    # Commodities & FX
    lines.append("## Commodities and FX")
    lines.append("")
    lines.append("| Ticker | Name | Last Price | Daily % | YTD % | Post-FOMC % |")
    lines.append("|--------|------|-----------|---------|-------|-------------|")

    fx_keys = ["Gold", "Crude", "DXY", "GBP/USD"]
    fx_names = {
        "Gold": "Gold (GC=F)", "Crude": "Crude Oil (CL=F)",
        "DXY": "US Dollar Index", "GBP/USD": "British Pound"
    }

    for tk in fx_keys:
        r = next((r for r in results if r["ticker"] == tk), None)
        if r:
            price = f"{r['latest_price']:.2f}" if r['latest_price'] else "N/A"
            d = f"{r['daily_pct']:+.2f}%" if r['daily_pct'] is not None else "N/A"
            y = f"{r['ytd_pct']:+.2f}%" if r['ytd_pct'] is not None else "N/A"
            f = f"{r['fomc_pct']:+.2f}%" if r['fomc_pct'] is not None else "N/A"
            lines.append(f"| {tk} | {fx_names.get(tk, '')} | {price} | {d} | {y} | {f} |")

    lines.append("")
    lines.append("## Notes")
    lines.append("- YTD period: Jan 1, 2026 to " + as_of)
    lines.append("- Post-FOMC period: Apr 29, 2026 to " + as_of)
    lines.append("- Daily change vs prior trading day")
    lines.append("- ^TNX changes are in basis points (bp), not percentage")
    lines.append("- Data sourced via yfinance; decimal precision varies by instrument")

    output = "\n".join(lines)

    out_path = "/home/ty/workspace/investment-research/reports/2026-05-24-fomc-april-2026/data-refresh.md"
    with open(out_path, "w") as f:
        f.write(output)

    print(output)
    print(f"\nWritten to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()