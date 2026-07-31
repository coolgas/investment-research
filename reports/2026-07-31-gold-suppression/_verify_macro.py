import json, sys
try:
    import yfinance as yf
except ImportError:
    print("NO_YFINANCE")
    sys.exit(0)

tickers = ["GC=F", "DX-Y.NYB", "^VIX", "HYG", "^TNX", "GBPUSD=X", "SGLD.L"]
out = {}
for t in tickers:
    try:
        df = yf.download(t, period="1y", interval="1d", progress=False, auto_adjust=False, multi_level_index=False)
        if df is None or df.empty:
            out[t] = {"error": "empty"}
            continue
        closes = df["Close"].dropna()
        last = float(closes.iloc[-1])
        last_date = str(closes.index[-1].date())
        hi = float(closes.max()); hi_d = str(closes.idxmax().date())
        lo = float(closes.min()); lo_d = str(closes.idxmin().date())
        y1 = float(closes.iloc[0]) if len(closes) > 250 else None
        ytd = None
        try:
            c2026 = closes[closes.index >= "2026-01-01"]
            if len(c2026) > 1:
                ytd = (last / float(c2026.iloc[0]) - 1) * 100
        except Exception:
            pass
        out[t] = {
            "last": round(last, 4), "last_date": last_date,
            "52w_high": round(hi, 4), "52w_high_date": hi_d,
            "52w_low": round(lo, 4), "52w_low_date": lo_d,
            "1y_ago_close": round(y1, 4) if y1 else None,
            "1y_return_pct": round((last / y1 - 1) * 100, 2) if y1 else None,
            "ytd_pct": round(ytd, 2) if ytd is not None else None,
        }
    except Exception as e:
        out[t] = {"error": str(e)}

print(json.dumps(out, indent=1))