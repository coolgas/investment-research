#!/usr/bin/env python3
"""Send market-brief.pdf to +447493244044 via signal-cli JSON-RPC HTTP API."""
import json, urllib.request, os, sys, base64

PDF_PATH = "/home/ty/workspace/investment-research/reports/2026-05-24-fomc-april-2026/market-brief.pdf"
RPC_URL = "http://127.0.0.1:8081/api/v1/rpc"

with open(PDF_PATH, "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode("ascii")

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "send",
    "params": {
        "recipient": ["+447493244044"],
        "message": {
            "textbody": "Market Brief: April 2026 FOMC — Rate Hold, Risk-On Rotation, and the Hot PCE Tail Risk"
        },
        "attachments": [pdf_b64]
    }
}

req = urllib.request.Request(
    RPC_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

resp = urllib.request.urlopen(req, timeout=60)
body = resp.read().decode("utf-8")
result = json.loads(body)

print("Response:", json.dumps(result, indent=2))

if "error" in result and result["error"]:
    print(f"ERROR: {result['error']}", file=sys.stderr)
    sys.exit(1)

results_list = result.get("result", {}).get("results", [])
for r in results_list:
    rtype = r.get("type", "UNKNOWN")
    print(f"Result type: {rtype}")
    if rtype != "SUCCESS":
        print(f"FAILED: {r}", file=sys.stderr)
        sys.exit(1)

print("All results type:SUCCESS")