# Golden JSON
from __future__ import annotations

LUMI = { # in pb^-1
    "2022": 7980.5,
    "2022EE": 26671.6,
    "2022All": 34652.1,
    "2023": 18084.4,
    "2023BPix": 9692.1,
    "2023All": 27776.5,
    "2022-2023": 62428.6,
    "2024": 108960.0,
    "2024C": 7240.0,
    "2024D": 7960.0,
    "2024E": 11320.0,
    "2024F": 27760.0,
    "2024G": 37770.0,
    "2024H": 5440.0,
    "2024I": 11470.0,
    "2025C": 20780.0,
    "2025E": 14000.0,
    "2025D": 25290.0,
    "2025F": 30350.0,
    # 2025G ongoing
    "2018": 59830.0,
    "2017": 41480.0,
    "2016": 36330.0,
    "Run2": 137640.0,
}

jecs = {
    "JES": "JES_jes",
    "JER": "JER",
}

jmsr = {
    "JMS": "JMS",
    "JMR": "JMR",
}

jec_shifts = []
for key in jecs:
    for shift in ["up", "down"]:
        jec_shifts.append(f"{key}_{shift}")

jmsr_shifts = []
for key in jmsr:
    for shift in ["up", "down"]:
        jmsr_shifts.append(f"{key}_{shift}")
