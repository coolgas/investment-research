import yfinance as yf
tnx = yf.download('^TNX', period='5y', actions=False, auto_adjust=True)
print("type:", type(tnx))
print("columns:", tnx.columns.tolist())
print(tnx.head(2))
tnx_c = tnx['Close']
print("tnx_c type:", type(tnx_c))
print("tnx_c iloc[0]:", tnx_c.iloc[0])
print("type iloc[0]:", type(tnx_c.iloc[0]))
print("value:", float(tnx_c.iloc[0]))