import pandas as pd

def basic_checks_assets(df: pd.DataFrame) -> list[str]:
    errs = []
    if "area_ipms2_m2" in df.columns and (df["area_ipms2_m2"] <= 0).any():
        errs.append("Found assets with non-positive area_ipms2_m2.")
    if "asset_id" in df.columns and df["asset_id"].duplicated().any():
        errs.append("Duplicate asset_id found.")
    return errs

def basic_checks_energy(df: pd.DataFrame, assets: pd.DataFrame) -> list[str]:
    errs = []
    if "asset_id" in df.columns and set(df["asset_id"]) - set(assets["asset_id"]):
        errs.append("Energy rows exist for unknown asset_id (referential integrity).")
    energy_cols = [c for c in ["elec_kwh","fuel_kwh","dh_kwh"] if c in df.columns]
    if energy_cols and (df[energy_cols] < 0).any().any():
        errs.append("Negative energy values detected.")
    return errs
