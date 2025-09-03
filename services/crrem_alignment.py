import pandas as pd
from typing import Tuple

def compute_operational_intensity(baseline: pd.DataFrame, assets: pd.DataFrame) -> pd.DataFrame:
    df = baseline.copy()
    df = df.merge(assets[["asset_id","area_ipms2_m2","country","property_type"]], on="asset_id", how="left")
    kg_per_kwh = 0.233
    df["operational_intensity"] = df.get("carbon_intensity_kgco2e_m2yr")
    if "operational_intensity" not in df:
        df["operational_intensity"] = None
    mask = df["operational_intensity"].isna()
    df.loc[mask, "operational_intensity"] = ((df.loc[mask, ["elec_kwh","fuel_kwh","dh_kwh"]].sum(axis=1))
                                             / df.loc[mask, "area_ipms2_m2"]).clip(lower=0) * kg_per_kwh
    return df

def derive_pathway_targets(pathways: pd.DataFrame, assets: pd.DataFrame, baseline_years: pd.DataFrame) -> pd.DataFrame:
    pth = pathways.copy()
    if "year" in pth.columns:
        pth["year"] = pth["year"].astype(int)
    yrs = sorted(set(baseline_years["year"].tolist() + [2030,2035,2040,2045,2050]))
    idx = assets[["asset_id","country","property_type"]].assign(key=1)           .merge(pd.DataFrame({"year": yrs, "key":[1]*len(yrs)}), on="key").drop(columns="key")
    idx = idx.merge(pth, on=["country","property_type","year"], how="left")

    def fill_group(g):
        if g["target_kgco2e_m2yr"].notna().any():
            g["target_kgco2e_m2yr"] = g["target_kgco2e_m2yr"].interpolate(limit_direction="both")
            return g
        start = 30.0
        slope = (0 - start) / (2050 - g["year"].min())
        g["target_kgco2e_m2yr"] = (start + slope * (g["year"] - g["year"].min())).clip(lower=0)
        return g
    idx = idx.groupby(["asset_id","country","property_type"], group_keys=False).apply(fill_group)
    return idx

def misalignment_year(op: pd.DataFrame, targets: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = op.merge(targets[["asset_id","year","target_kgco2e_m2yr"]], on=["asset_id","year"], how="left")
    df["aligned"] = df["operational_intensity"] <= df["target_kgco2e_m2yr"]
    res = df.sort_values(["asset_id","year"]).groupby("asset_id").apply(
        lambda g: pd.Series({
            "misalignment_year": int(g.loc[g["aligned"], "year"].min()) if g["aligned"].any() else None,
            "current_intensity": float(g.loc[g["year"]==g["year"].max(),"operational_intensity"].iloc[0]),
            "current_target": float(g.loc[g["year"]==g["year"].max(),"target_kgco2e_m2yr"].iloc[0]),
        })
    ).reset_index()
    from datetime import datetime
    this_year = datetime.now().year
    def status(y):
        if y is None:
            return "Misaligned"
        return "Aligned" if y <= this_year else "Misaligned"
    res["status"] = res["misalignment_year"].apply(status)
    return res, df
