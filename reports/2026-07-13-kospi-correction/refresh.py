import yfinance as yf
import pandas as pd
from datetime import datetime

OUT = "/root/workspace/investment-research/reports/2026-07-13-kospi-correction/data-refresh.md"

# === PULL DATA ===
tickers_kr = ["^KS11", "EWY", "005930.KS", "000660.KS", "KRW=X"]
tickers_asia = ["^N225", "^HSI", "000001.SS"]
tickers_global = ["SPY", "QQQ", "^VIX", "DX-Y.NYB", "^TNX", "GC=F", "CL=F"]
tickers_semi = ["SMH", "TSM", "ASML"]
all_tickers = tickers_kr + tickers_asia + tickers_global + tickers_semi

data = yf.download(all_tickers, start="2026-06-19", end=None, group_by="ticker", threads=True)
data_ytd = yf.download(all_tickers, start="2026-01-01", end=None, group_by="ticker", threads=True)

# Historical KOSPI monthly for comparison
ks_hist = yf.download("^KS11", start="2021-01-01", end=None, interval="1mo")
ks_monthly = ks_hist["Close"].squeeze()
if isinstance(ks_monthly, pd.DataFrame):
    ks_monthly = ks_monthly.iloc[:, 0]

def safe_val(s, idx):
    try:
        v = float(s.iloc[idx])
        return v
    except:
        return None

def compute_metrics(closes):
    """Return (latest, daily_chg%, crash_dd%, ytd_ret%, ytd_dd%)"""
    if len(closes) < 2:
        return None, None, None, None, None
    latest = float(closes.iloc[-1])
    prev = float(closes.iloc[-2])
    daily = ((latest / prev) - 1) * 100
    peak = float(closes.max())
    dd = ((latest / peak) - 1) * 100
    return latest, daily, dd

def ytd_metrics(series):
    if len(series) < 2:
        return None, None
    start_v = float(series.iloc[0])
    end_v = float(series.iloc[-1])
    ret = ((end_v / start_v) - 1) * 100
    peak_v = float(series.max())
    dd = ((end_v / peak_v) - 1) * 100
    return ret, dd

def span(v, pct=True):
    if v is None:
        return "N/A"
    if pct:
        s = f"{v:+.2f}%"
    else:
        s = f"{v:,.2f}"
    if v > 0:
        return f'<span class="up">{s}</span>'
    elif v < 0:
        return f'<span class="down">{s}</span>'
    else:
        return f'<span class="num">{s}</span>'

lines = []
lines.append("# KOSPI 深度调整数据报告")
lines.append("")
lines.append(f"**生成日期**: {datetime.now().strftime('%Y-%m-%d')}")
lines.append("")
lines.append("**数据来源**: yfinance（延迟数据，非官方）")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 摘要")
lines.append("")

# Get latest KOSPI number
ks11_close = data[("^KS11", "Close")].dropna()
ks_latest, ks_daily, ks_dd = compute_metrics(ks11_close)
ks_ytd_close = data_ytd[("^KS11", "Close")].dropna()
ks_ytd_ret, ks_ytd_dd = ytd_metrics(ks_ytd_close)

lines.append(f"KOSPI 今日收于 <span class=\"num\">{ks_latest:,.2f}</span>，日变动 {span(ks_daily)}。自6月20日高点以来，回调幅度达 {span(ks_dd)}。年初至今仍上涨 {span(ks_ytd_ret)}，但从YTD高点回撤 {span(ks_ytd_dd)}。")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 韩国市场")
lines.append("")
lines.append("**表1：韩国市场概览 (2026-06-20 至 2026-07-13)**")
lines.append("")
lines.append("| 代码 | 名称 | 最新价 | 日变动 | 回调幅度 | YTD回报 | YTD回撤 |")
lines.append("|------|------|--------|--------|----------|---------|---------|")

names_kr = {"^KS11": "KOSPI", "EWY": "iShares MSCI Korea", "005930.KS": "三星电子", "000660.KS": "SK海力士", "KRW=X": "美元/韩元"}
for t in tickers_kr:
    c = data[(t, "Close")].dropna()
    latest, daily, dd = compute_metrics(c)
    cy = data_ytd[(t, "Close")].dropna()
    yret, ydd = ytd_metrics(cy)
    name = names_kr.get(t, t)
    latest_str = f'<span class="num">{latest:,.0f}</span>' if latest and latest > 100 else f'<span class="num">{latest:,.2f}</span>'
    lines.append(f"| {t} | {name} | {latest_str} | {span(daily)} | {span(dd)} | {span(yret)} | {span(ydd)} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## 亚洲市场对比")
lines.append("")
lines.append("**表2：亚洲市场对比 (2026-06-20 至 2026-07-13)**")
lines.append("")
lines.append("| 代码 | 名称 | 最新价 | 日变动 | 回调幅度 | YTD回报 | YTD回撤 |")
lines.append("|------|------|--------|--------|----------|---------|---------|")

names_asia = {"^N225": "日经225", "^HSI": "恒生指数", "000001.SS": "上证综指"}
for t in tickers_asia:
    c = data[(t, "Close")].dropna()
    latest, daily, dd = compute_metrics(c)
    cy = data_ytd[(t, "Close")].dropna()
    yret, ydd = ytd_metrics(cy)
    name = names_asia.get(t, t)
    latest_str = f'<span class="num">{latest:,.2f}</span>'
    lines.append(f"| {t} | {name} | {latest_str} | {span(daily)} | {span(dd)} | {span(yret)} | {span(ydd)} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## 全球背景")
lines.append("")
lines.append("**表3：全球市场指标 (2026-06-20 至 2026-07-13)**")
lines.append("")
lines.append("| 代码 | 名称 | 最新价 | 日变动 | 回调幅度 | YTD回报 | YTD回撤 |")
lines.append("|------|------|--------|--------|----------|---------|---------|")

names_global = {"SPY": "标普500 ETF", "QQQ": "纳斯达克100 ETF", "^VIX": "VIX恐慌指数", 
                "DX-Y.NYB": "美元指数(DXY)", "^TNX": "美国10年期国债收益率", 
                "GC=F": "黄金期货", "CL=F": "原油期货(WTI)"}
for t in tickers_global:
    c = data[(t, "Close")].dropna()
    latest, daily, dd = compute_metrics(c)
    cy = data_ytd[(t, "Close")].dropna()
    yret, ydd = ytd_metrics(cy)
    name = names_global.get(t, t)
    latest_str = f'<span class="num">{latest:,.2f}</span>'
    lines.append(f"| {t} | {name} | {latest_str} | {span(daily)} | {span(dd)} | {span(yret)} | {span(ydd)} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## 半导体板块")
lines.append("")
lines.append("**表4：半导体板块 (2026-06-20 至 2026-07-13)**")
lines.append("")
lines.append("| 代码 | 名称 | 最新价 | 日变动 | 回调幅度 | YTD回报 | YTD回撤 |")
lines.append("|------|------|--------|--------|----------|---------|---------|")

names_semi = {"SMH": "VanEck半导体ETF", "TSM": "台积电", "ASML": "ASML"}
for t in tickers_semi:
    c = data[(t, "Close")].dropna()
    latest, daily, dd = compute_metrics(c)
    cy = data_ytd[(t, "Close")].dropna()
    yret, ydd = ytd_metrics(cy)
    name = names_semi.get(t, t)
    latest_str = f'<span class="num">{latest:,.2f}</span>'
    lines.append(f"| {t} | {name} | {latest_str} | {span(daily)} | {span(dd)} | {span(yret)} | {span(ydd)} |")

# === KOSPI largest daily drops ===
lines.append("")
lines.append("---")
lines.append("")
lines.append("## KOSPI 最大单日跌幅")
lines.append("")
lines.append("**表5：KOSPI最大单日跌幅 (2026-06-20 至 2026-07-13)**")
lines.append("")
lines.append("| 日期 | 收盘价 | 日变动 |")
lines.append("|------|--------|--------|")

daily_ret = ks11_close.pct_change().dropna()
daily_ret_sorted = daily_ret.sort_values()
for date, ret in daily_ret_sorted.head(10).items():
    close_val = float(ks11_close.loc[date])
    lines.append(f"| {date.strftime('%Y-%m-%d')} | <span class=\"num\">{close_val:,.2f}</span> | {span(float(ret)*100)} |")

# === Historical KOSPI corrections ===
lines.append("")
lines.append("---")
lines.append("")
lines.append("## KOSPI 历史调整对比")
lines.append("")
lines.append("**表6：KOSPI历史重大调整 (2021-2026)**")
lines.append("")  
lines.append("| 时期 | 峰值 | 谷值 | 跌幅 | 恢复月数 |")
lines.append("|------|------|------|------|----------|")

# Compute historical drawdowns > 15%
ks_vals = [float(ks_monthly.iloc[i]) for i in range(len(ks_monthly))]
ks_dates = [ks_monthly.index[i] for i in range(len(ks_monthly))]

peak_val = ks_vals[0]
peak_date = ks_dates[0]
drawdowns = []

for i in range(1, len(ks_vals)):
    if ks_vals[i] > peak_val:
        if peak_val > 0:
            dd = (ks_vals[i-1] / peak_val - 1) * 100
            if dd < -10:
                # Check recovery
                recovery_months = "未恢复"
                for j in range(i, len(ks_vals)):
                    if ks_vals[j] >= peak_val:
                        recovery_months = j - i + 1
                        break
                drawdowns.append((f"{peak_date.strftime('%Y-%m')}-{ks_dates[i-1].strftime('%Y-%m')}", 
                                  peak_val, ks_vals[i-1], dd, recovery_months))
        peak_val = ks_vals[i]
        peak_date = ks_dates[i]
    elif ks_vals[i] < peak_val:
        continue

drawdowns.sort(key=lambda x: x[3])
for period, peak_v, trough_v, dd, rec in drawdowns[:5]:
    rec_str = f"{rec}个月" if isinstance(rec, int) else str(rec)
    lines.append(f"| {period} | <span class=\"num\">{peak_v:,.0f}</span> | <span class=\"num\">{trough_v:,.0f}</span> | {span(dd)} | {rec_str} |")

# === Dispersion analysis ===
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 板块离散度分析")
lines.append("")
lines.append("**表7：板块表现离散度 (2026-06-20 至 2026-07-13)**")
lines.append("")
lines.append("| 板块 | 代表标的 | 回调幅度 |")
lines.append("|------|----------|----------|")

# Compute for each group
for group_name, group_tickers in [("韩国综合", tickers_kr), ("亚洲其他", tickers_asia), ("全球基准", tickers_global[:5]), ("半导体", tickers_semi)]:
    for t in group_tickers:
        c = data[(t, "Close")].dropna()
        _, _, dd = compute_metrics(c)
        name = {**names_kr, **names_asia, **names_global, **names_semi}.get(t, t)
        lines.append(f"| {group_name} | {name} | {span(dd)} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## 相关性矩阵")
lines.append("")
lines.append("**表8：KOSPI与其他资产相关性 (2026-06-20 至 2026-07-13)**")
lines.append("")
lines.append("| 资产 | 与KOSPI相关性 |")
lines.append("|------|---------------|")

# Compute daily returns correlation
ks11_ret = ks11_close.pct_change().dropna()
for label, t in [("标普500", "SPY"), ("纳斯达克100", "QQQ"), ("VIX", "^VIX"), ("DXY", "DX-Y.NYB"), ("10Y收益率", "^TNX"), ("黄金", "GC=F")]:
    try:
        other_close = data[(t, "Close")].dropna()
        other_ret = other_close.pct_change().dropna()
        common_idx = ks11_ret.index.intersection(other_ret.index)
        if len(common_idx) > 5:
            corr = ks11_ret.loc[common_idx].corr(other_ret.loc[common_idx])
            lines.append(f"| {label} | <span class=\"num\">{corr:.3f}</span> |")
    except:
        pass

# === YTD KOSPI monthly ===
lines.append("")
lines.append("---")
lines.append("")
lines.append("## KOSPI 月度表现 (2026年)")
lines.append("")
lines.append("**表9：KOSPI月度涨跌 (2026年1月-7月)**")
lines.append("")
lines.append("| 月份 | 收盘价 | 月涨跌 |")
lines.append("|------|--------|--------|")

ks_ytd_monthly = ks_ytd_close.resample("ME").last()
monthly_vals = [float(ks_ytd_monthly.iloc[i]) for i in range(len(ks_ytd_monthly))]
monthly_dates = [ks_ytd_monthly.index[i] for i in range(len(ks_ytd_monthly))]
prev_v = None
for i, (date, v) in enumerate(zip(monthly_dates, monthly_vals)):
    if prev_v is not None:
        m_ret = ((v/prev_v)-1)*100
    else:
        m_ret = None
    lines.append(f"| {date.strftime('%Y-%m')} | <span class=\"num\">{v:,.2f}</span> | {span(m_ret)}")
    prev_v = v

with open(OUT, "w") as f:
    f.write("\n".join(lines))

print(f"Written {len(lines)} lines to {OUT}")
print(f"KOSPI latest: {ks_latest:,.2f}, DD: {ks_dd:+.2f}%")