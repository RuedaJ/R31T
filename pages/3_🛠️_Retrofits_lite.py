import streamlit as st, pandas as pd
from services.embodied import carbon_payback, classify_scope

st.set_page_config(page_title="Retrofits (lite)", page_icon="🛠️", layout="wide")
st.title("🛠️ Retrofits – Carbon Payback (Lite)")

retro_u  = st.file_uploader("retrofits.csv", type=["csv"], key="retro_lite")
energy_u = st.file_uploader("energy_baselines.csv (for annual savings)", type=["csv"], key="energy_lite")
assets_u = st.file_uploader("assets.csv (to get area)", type=["csv"], key="assets_lite")

if not retro_u or not energy_u or not assets_u:
    st.info("Upload **retrofits.csv**, **energy_baselines.csv**, and **assets.csv**.")
    st.stop()

retro = pd.read_csv(retro_u)
energy = pd.read_csv(energy_u)
assets = pd.read_csv(assets_u)

kg_per_kwh = 0.233
baseline = energy.merge(assets[["asset_id","area_ipms2_m2"]], on="asset_id", how="left")
baseline = baseline.sort_values("year").groupby("asset_id").tail(1).copy()
baseline["kwh_per_m2"] = ((baseline[["elec_kwh","fuel_kwh","dh_kwh"]].sum(axis=1))
                          / baseline["area_ipms2_m2"])
baseline = baseline[["asset_id","kwh_per_m2"]]

df = retro.merge(baseline, on="asset_id", how="left")
df["annual_saving_kgco2e_m2yr"] = (df["expected_kwh_saving_pct"].fillna(0)/100.0) * df["kwh_per_m2"] * kg_per_kwh
df["carbon_payback_years"] = df.apply(lambda r: carbon_payback(r["embodied_a1a3_kgco2e_per_m2"],
                                                               r["annual_saving_kgco2e_m2yr"]), axis=1)
df["benchmark_scope"] = df.apply(lambda r: classify_scope(r["embodied_a1a3_kgco2e_per_m2"], r["carbon_payback_years"]),
                                 axis=1)

st.dataframe(df[["asset_id","retrofit_id","measure_type","embodied_a1a3_kgco2e_per_m2","annual_saving_kgco2e_m2yr","carbon_payback_years","benchmark_scope"]])

st.download_button("Download retrofit paybacks (CSV)", df.to_csv(index=False).encode("utf-8"),
                   "retrofit_carbon_payback.csv", "text/csv")

st.caption("Phase 2 will replace proxy factors with country- & carrier-specific emission factors and full ROI/IRR.")
