#!/usr/bin/env python3
"""Fresh data pull: 24 tickers YTD, 2-week, 1-week metrics. Writes data-refresh.md."""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings, sys, os
warnings.filterwarnings('ignore')

# CD to workspace so relative paths work
ws = "/home/ty/workspace/investment-research/reports/2026-06-21-market-update"
os.chdir(ws)

TICKERS = [
    "SPY","QQQ","IWM","^TNX","TLT","XLU","XLF","XLRE",
    "AAPL","MSFT","NVDA","META","GOOGL","AMZN",
    "JPM","GS","BAC","WMT","PLD","NEE",
    "GC=F","CL=F","GBPUSD=X"
]

FRIENDLY = {
    "SPY":"SPY (S&P 500)","QQQ":"QQQ (Nasdaq-100)","IWM":"IWM (Russell 2000)",
    "^TNX":"10Y UST Yield","DXY":"DXY (US Dollar Index)",
    "TLT":"TLT (20+ Yr Treasuries)","XLU":"XLU (Utilities)",
    "XLF":"XLF (Financials)","XLRE":"XLRE (Real Estate)",
    "AAPL":"AAPL (Apple)","MSFT":"MSFT (Microsoft)","NVDA":"NVDA (NVIDIA)",
    "META":"META (Meta Platforms)","GOOGL":"GOOGL (Alphabet)","AMZN":"AMZN (Amazon)",
    "JPM":"JPM (JPMorgan Chase)","GS":"GS (Goldman Sachs)","BAC":"BAC (Bank of America)",
    "PLD":"PLD (Prologis)","NEE":"NEE (NextEra Energy)","WMT":"WMT (Walmart)",
    "GC=F":"Gold (GC=F)","CL=F":"Crude Oil (CL=F)","GBPUSD=X":"GBP/USD"
}

SECTION = {
    "indices":["SPY","QQQ","IWM","^TNX","DXY"],
    "sectors":["TLT","XLU","XLF","XLRE"],
    "megacap":["AAPL","MSFT","NVDA","META","GOOGL","AMZN"],
    "financials":["JPM","GS","BAC"],
    "commodities":["GC=F","CL=F"],
    "fx":["GBPUSD=X"],
    "other":["WMT","PLD","NEE"]
}
SEC_NAMES = {"indices":"Indices","sectors":"Sectors","megacap":"Mega-Cap Tech",
             "financials":"Financials","commodities":"Commodities","fx":"FX","other":"Other Notable Stocks"}

# ---- Pull Data ----
print("=== Pulling yfinance data ===", flush=True)
results = {}

# Batch 1: main tickers (no group_by to avoid auto_adjust bug)
main_dl = ["SPY","QQQ","IWM","^TNX","TLT","XLU","XLF","XLRE",
           "AAPL","MSFT","NVDA","META","GOOGL","AMZN",
           "JPM","GS","BAC","WMT","PLD","NEE"]
print(f"Downloading {len(main_dl)} main tickers...", flush=True)
df_main = yf.download(main_dl, start="2026-01-01", end="2026-06-21",
                       auto_adjust=True, threads=True, progress=False)
print(f"Main df shape: {df_main.shape}, cols sample: {df_main.columns[:3].tolist()}", flush=True)

# Process main tickers: without group_by, columns are (Field, Ticker)
for t in main_dl:
    try:
        col = ('Close', t)
        if col not in df_main.columns:
            # Try case variations
            for c in df_main.columns:
                if c[1] == t or c[1].upper() == t.upper():
                    col = c
                    break
            else:
                print(f"  SKIP {t}: no Close column found", flush=True)
                continue
        s = df_main[col].dropna()
        if len(s) < 5:
            print(f"  SKIP {t}: only {len(s)} points", flush=True)
            continue
        results[t] = s
        print(f"  {t:15s} {len(s):3d} pts  last={s.iloc[-1]:>12.2f}  {s.index[-1].date()}", flush=True)
    except Exception as e:
        print(f"  ERR {t}: {e}", flush=True)

# Batch 2: DXY separately (DX-Y.NYB)
print("Downloading DXY (DX-Y.NYB)...", flush=True)
try:
    dxy = yf.Ticker("DX-Y.NYB")
    dxy_h = dxy.history(start="2026-01-01", end="2026-06-21")
    dxy_c = dxy_h['Close'].dropna()
    if len(dxy_c) >= 5:
        results["DXY"] = dxy_c
        print(f"  DXY             {len(dxy_c):3d} pts  last={dxy_c.iloc[-1]:>12.2f}  {dxy_c.index[-1].date()}", flush=True)
    else:
        print(f"  DXY: only {len(dxy_c)} points", flush=True)
except Exception as e:
    print(f"  ERR DXY: {e}", flush=True)

# Batch 3: commodities and FX
spec_dl = ["GC=F","CL=F","GBPUSD=X"]
print(f"Downloading {len(spec_dl)} specials...", flush=True)
df_spec = yf.download(spec_dl, start="2026-01-01", end="2026-06-21",
                       auto_adjust=True, threads=True, progress=False)
for t in spec_dl:
    try:
        for c in df_spec.columns:
            if c[1] == t:
                s = df_spec[c].dropna()
                if len(s) >= 5:
                    results[t] = s
                    print(f"  {t:15s} {len(s):3d} pts  last={s.iloc[-1]:>12.2f}  {s.index[-1].date()}", flush=True)
                else:
                    print(f"  SKIP {t}: only {len(s)} points", flush=True)
                break
        else:
            print(f"  SKIP {t}: no column", flush=True)
    except Exception as e:
        print(f"  ERR {t}: {e}", flush=True)

print(f"\nTotal tickers with data: {len(results)}", flush=True)

# ---- Compute Metrics ----
print("\n=== Computing metrics ===", flush=True)

def tz_fix(s):
    """Remove tz info for consistent date comparison."""
    if hasattr(s.index, 'tz') and s.index.tz is not None:
        s = s.copy()
        s.index = s.index.tz_localize(None)
    return s

def compute(series):
    if series is None or len(series) < 5:
        return None
    series = tz_fix(series)
    latest = float(series.iloc[-1])
    latest_date = series.index[-1]
    ytd_start = float(series.iloc[0])
    ytd_pct = ((latest / ytd_start) - 1) * 100

    # 2-week: Jun 7 (Sun) -> Jun 20 (Sat). Nearest trading: >=Jun 8 -> <=Jun 19
    t_s = pd.Timestamp("2026-06-07")
    t_e = pd.Timestamp("2026-06-20")

    ms = series.index >= t_s
    me = series.index <= t_e
    if ms.any():
        tw_s_val = float(series[ms].iloc[0])
        tw_s_date = series[ms].index[0]
    else:
        tw_s_val = None; tw_s_date = None
    if me.any():
        tw_e_val = float(series[me].iloc[-1])
        tw_e_date = series[me].index[-1]
    else:
        tw_e_val = latest; tw_e_date = latest_date

    tw_pct = ((tw_e_val / tw_s_val) - 1) * 100 if (tw_s_val is not None and tw_s_val > 0) else None

    # 1-week: Jun 14 (Sun) -> Jun 20 (Sat)
    t_1w = pd.Timestamp("2026-06-14")
    m1 = series.index >= t_1w
    if m1.any() and tw_e_val is not None:
        w1_s = float(series[m1].iloc[0])
        w1_pct = ((tw_e_val / w1_s) - 1) * 100 if w1_s > 0 else None
    else:
        w1_pct = None

    return {"latest_close":latest,"latest_date":latest_date,"ytd_pct":ytd_pct,
            "ytd_start":ytd_start,"ytd_start_date":series.index[0],
            "two_week_pct":tw_pct,"two_week_start_date":tw_s_date,"two_week_end_date":tw_e_date,
            "one_week_pct":w1_pct}

metrics = {}
for t, s in results.items():
    m = compute(s)
    if m:
        metrics[t] = m
        tw_s = "N/A" if m['two_week_pct'] is None else f"{m['two_week_pct']:>+7.2f}%"
        w1_s = "N/A" if m['one_week_pct'] is None else f"{m['one_week_pct']:>+7.2f}%"
        print(f"  {t:15s} Close={m['latest_close']:>10.2f}  YTD={m['ytd_pct']:>+7.2f}%  2W={tw_s}  1W={w1_s}", flush=True)

# ---- SPY-10Y Correlation ----
print("\n=== SPY-10Y Correlation ===", flush=True)
corr_ytd = None; corr_2w = None; common_all = None; common_2w = None
latest_tnx = None; tnx_date = None; tnx_ytd_chg = None

spy_s = results.get("SPY")
tnx_s = results.get("^TNX")
if spy_s is not None and tnx_s is not None:
    spy_s = tz_fix(spy_s)
    tnx_s = tz_fix(tnx_s)
    spy_r = spy_s.pct_change().dropna()
    tnx_r = tnx_s.pct_change().dropna()
    common_all = pd.concat([spy_r, tnx_r], axis=1, join='inner')
    common_all.columns = ['SPY','TNX']
    if len(common_all) > 5:
        corr_ytd = float(common_all['SPY'].corr(common_all['TNX']))
        print(f"  YTD corr: {corr_ytd:.4f} (n={len(common_all)})", flush=True)

    t_s2 = pd.Timestamp("2026-06-07"); t_e2 = pd.Timestamp("2026-06-20")
    common_2w = common_all[(common_all.index >= t_s2) & (common_all.index <= t_e2)]
    if len(common_2w) > 3:
        corr_2w = float(common_2w['SPY'].corr(common_2w['TNX']))
        print(f"  2W corr:  {corr_2w:.4f} (n={len(common_2w)})", flush=True)

    latest_tnx = float(tnx_s.iloc[-1])
    tnx_date = tnx_s.index[-1]
    tnx_ytd_chg = float(tnx_s.iloc[-1] - tnx_s.iloc[0])
    print(f"  ^TNX: {latest_tnx:.4f} on {tnx_date.date()}, YTD chg: {tnx_ytd_chg:+.4f}", flush=True)

threshold_4_75 = latest_tnx is not None and latest_tnx >= 4.75

# ---- WRITE REPORT ----
print("\n=== Writing report ===", flush=True)

def fmt_pct(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    if v >= 0:
        return f'<span class="up">+{v:.2f}%</span>'
    return f'<span class="down">{v:.2f}%</span>'

def fmt_num(v, d=2):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    return f'<span class="num">{v:.{d}f}</span>'

L = []
L.append("# Market Data Refresh: June 21, 2026")
L.append("")
L.append(f"**Data pulled**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
spy_m = metrics.get("SPY", {})
sld = spy_m.get("latest_date", "N/A")
if hasattr(sld, 'date'): sld = sld.date()
yst = spy_m.get("ytd_start_date", "N/A")
if hasattr(yst, 'date'): yst = yst.date()
L.append(f"**Period**: YTD ({yst}) through {sld}")
L.append(f"**2-week window**: Jun 7 - Jun 20, 2026 (nearest trading days used)")
L.append(f"**1-week window**: Jun 14 - Jun 20, 2026")
L.append("")
L.append("---")
L.append("")

for sk, tl in SECTION.items():
    sn = SEC_NAMES[sk]
    valid = [t for t in tl if t in metrics]
    if not valid: continue
    L.append(f"## {sn}")
    L.append("")

    # Major moves >5%
    major = []
    for t in valid:
        m = metrics[t]
        for lbl, pct in [("YTD",m['ytd_pct']),("2-week",m['two_week_pct']),("1-week",m['one_week_pct'])]:
            if pct is not None and abs(pct) > 5:
                major.append(f"- {FRIENDLY.get(t,t)}: {fmt_pct(pct)} ({lbl})")
    if major:
        L.append("**Major moves (>5%):**")
        L.extend(major)
        L.append("")

    L.append("| Ticker | Latest Close | 2-Week % (Jun 7 -> Jun 20) | YTD % (Jan 1 -> Jun 20) | 1-Week % (Jun 14 -> Jun 20) |")
    L.append("|--------|-------------|---------------------------|-------------------------|-----------------------------|")
    for t in valid:
        m = metrics[t]
        name = FRIENDLY.get(t, t)
        L.append(f"| {name} | {fmt_num(m['latest_close'])} | {fmt_pct(m['two_week_pct'])} | {fmt_pct(m['ytd_pct'])} | {fmt_pct(m['one_week_pct'])} |")
    L.append("")

# Rates
L.append("## Rates / Yield Summary")
L.append("")
L.append("| Metric | Value |")
L.append("|--------|-------|")
if latest_tnx is not None:
    L.append(f"| 10Y UST Yield (^TNX) Latest | {fmt_num(latest_tnx, 4)} |")
    if tnx_s is not None:
        L.append(f"| ^TNX Level at YTD Start (Jan 2) | {fmt_num(float(tnx_s.iloc[0]), 4)} |")
    L.append(f"| ^TNX YTD Change (bps) | {fmt_num(tnx_ytd_chg * 100, 1) if tnx_ytd_chg is not None else 'N/A'} |")
    L.append(f"| 4.75% Trigger Threshold Breached? | {'YES' if threshold_4_75 else 'No'} |")
    if not threshold_4_75:
        L.append(f"| Distance to 4.75% Trigger | {fmt_num((4.75 - latest_tnx) * 100, 1)} bps below |")
L.append("")

# Correlation
L.append("### SPY-10Y Correlation Analysis")
L.append("")
L.append("| Period | Correlation | Daily Observations |")
L.append("|--------|------------|-------------------|")
if corr_ytd is not None:
    L.append(f"| YTD (Jan 2 - Jun 20) | {fmt_num(corr_ytd, 4)} | {fmt_num(len(common_all))} |")
else:
    L.append(f"| YTD (Jan 2 - Jun 20) | N/A | N/A |")
if corr_2w is not None:
    L.append(f"| 2-Week (Jun 7 - Jun 20) | {fmt_num(corr_2w, 4)} | {fmt_num(len(common_2w))} |")
else:
    L.append(f"| 2-Week (Jun 7 - Jun 20) | N/A | N/A |")
L.append("")
L.append("*Interpretation: Negative SPY-10Y correlation = risk-on/risk-off (stocks and bonds move inversely). Positive correlation = common macro factor (e.g., inflation, growth expectations) driving both.*")
L.append("")

# Data quality
L.append("## Data Quality Notes")
L.append("")
L.append(f"- Tickers requested: 24")
L.append(f"- Tickers with valid data: {len(metrics)}")
L.append(f"- Date range: {yst} through {sld}")
missing = [t for t in TICKERS + ["DXY"] if t not in metrics]
if missing:
    L.append(f"- Missing/no data: {', '.join(missing)}")
else:
    L.append("- All tickers accounted for.")
L.append("")
L.append("---")
L.append("")
L.append(f"*Generated automatically by Hermes Agent data refresh script on {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*")
L.append("")

content = "\n".join(L)
op = "data-refresh.md"
with open(op, "w") as f:
    f.write(content)

bc = len(content.encode('utf-8'))
print(f"\nReport written: {os.path.abspath(op)}", flush=True)
print(f"Size: {bc} bytes (need >2000: {'OK' if bc > 2000 else 'FAIL'})", flush=True)
print(f"Lines: {len(L)}", flush=True)
print("Done.", flush=True)