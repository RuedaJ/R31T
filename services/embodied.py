import pandas as pd

BANDS = {
    "light":  {"embodied_min": 0,   "embodied_max": 30,  "payback_max": 3},
    "medium": {"embodied_min": 20,  "embodied_max": 80,  "payback_max": 5},
    "deep":   {"embodied_min": 80,  "embodied_max": 200, "payback_max": 8},
}

def carbon_payback(embodied_kgco2e_m2: float, annual_saving_kgco2e_m2yr: float):
    if embodied_kgco2e_m2 is None or annual_saving_kgco2e_m2yr is None or annual_saving_kgco2e_m2yr <= 0:
        return None
    try:
        return round(embodied_kgco2e_m2 / annual_saving_kgco2e_m2yr, 2)
    except ZeroDivisionError:
        return None

def classify_scope(embodied: float, payback: float) -> str:
    for label, band in BANDS.items():
        if embodied is not None and band["embodied_min"] <= embodied <= band["embodied_max"]:
            if payback is None or payback <= band["payback_max"]:
                return label
    return "outlier"
