#!/usr/bin/env python3
"""
Prognoza dla 2026-04-06 z perspektywy 2026-04-05 (D-1).
Używa Previous Runs API z previous_model_run=1 i modelem best_match.

Uwaga: icon_eu jest modelem deterministycznym — nie generuje precipitation_probability.
best_match korzysta z modeli ensemble i poprawnie zwraca prawdopodobieństwo opadu.
"""

import urllib.request, urllib.parse, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

params = {
    "latitude": 52.1656,
    "longitude": 20.9326,
    "models": "best_match",
    "start_date": "2026-04-06",
    "end_date": "2026-04-06",
    "hourly": "precipitation,precipitation_probability",
    "timezone": "Europe/Warsaw",
    "previous_model_run": 1,
}

url = "https://previous-runs-api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(
    params
)
req = urllib.request.Request(url, headers={"User-Agent": "raszyn/1.0"})
with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
    data = json.loads(r.read())

times = data["hourly"]["time"]
precip = data["hourly"]["precipitation"]
prob = data["hourly"]["precipitation_probability"]

print("Prognoza dla 2026-04-06 z biegu D-1 (2026-04-05), model: icon_eu")
print(f"{'Godzina':<10} {'Opad mm/h':>10} {'Prawdop. %':>11}")
print("-" * 34)
for t, p, pr in zip(times, precip, prob):
    print(f"{t[11:16]:<10} {p or 0:>10.2f} {pr or 0:>10.0f}%")
