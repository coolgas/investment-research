#!/usr/bin/env python3
"""Send market brief PDF via signal-cli."""
import subprocess
import os

# Read numbers from the temp file
with open('/tmp/signal_numbers.txt') as f:
    for line in f:
        line = line.strip()
        if line.startswith('send='):
            send_num = line.split('=', 1)[1]
        elif line.startswith('recip='):
            recip_num = line.split('=', 1)[1]

print(f'Sending from: {send_num}, to: {recip_num}')

pdf_path = '/home/ty/workspace/investment-research/reports/2026-05-24-fomc-april-2026/market-brief.pdf'
message = 'Market Brief: April 2026 FOMC — PDF attached with key data points and scenarios.'

cmd = [
    'signal-cli',
    '--account', send_num,
    'send',
    '-m', message,
    '-a', pdf_path,
    recip_num
]

print(f'Running: {" ".join(cmd)}')
result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print(f'STDOUT: {result.stdout}')
print(f'STDERR: {result.stderr}')
print(f'Exit code: {result.returncode}')
