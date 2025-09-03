import streamlit as st, pandas as pd
from services.crrem_alignment import compute_operational_intensity, derive_pathway_targets, misalignment_year
import plotly.express as px

st.set_page_config(page_title="Alignment", page_icon="📊", layout="wide")
st.title("📊 Alignment (CRREM-style) & Misalignment Year")

assets = st.session_state.get("assets_df")
energy  = st.session_state.get("energy_df")

assets_u = st.file_uploader("assets.csv", type=["csv"], key="assets_align")
energy_u = st.file_uploader("energy_baselines.csv", type=["csv"], key="energy_align")
path_u   = st.file_uploader("pathways.csv (preferred)", type=["csv"], key="pathways_align")

if assets_u: assets = pd.read_csv(assets_u)
if energy_u: energy  = pd.read_csv(energy_u)
pathways = pd.read_csv(path_u) if path_u else st.session_state.get("pathways_df")

if assets is None or energy is None:
    st.warning("Upload **assets.csv** and **energy_baselines.csv** to proceed.")
    st.stop()

op = compute_operational_intensity(energy, assets)

if pathways is None or pathways.empty:
    st.info("No pathways.csv provided — generating a transparent fallback (linear descent to 2050).")
    pth = derive_pathway_targets(
        pathways=pd.DataFrame(columns=["country","property_type","year","target_kgco2e_m2yr"]),
        assets=assets,
        baseline_years=energy[["year"]]
    )
else:
    pth = derive_pathway_targets(pathways, assets, energy[["year"]])

res, joined = misalignment_year(op, pth)

st.subheader("Portfolio Snapshot")
aligned_pct = round(100 * (res["status"]=="Aligned").mean(), 1)
c1,c2,c3 = st.columns(3)
c1.metric("Assets", len(res))
c2.metric("Aligned %", f"{aligned_pct}%")
c3.metric("Median Misalignment Year", int(res["misalignment_year"].median()) if res["misalignment_year"].notna().any() else None)

st.subheader("Per-Asset Results")
st.dataframe(res)

st.download_button("Download results (CSV)", res.to_csv(index=False).encode("utf-8"), "alignment_results.csv", "text/csv")

st.subheader("Visual – Current vs. Target (latest year)")
latest_year = joined["year"].max()
latest = joined.loc[joined["year"]==latest_year].copy()
fig = px.scatter(latest, x="target_kgco2e_m2yr", y="operational_intensity",
                 color="asset_id", labels={"target_kgco2e_m2yr":"Target (kgCO2e/m²·yr)",
                                           "operational_intensity":"Actual (kgCO2e/m²·yr)"},
                 title=f"Actual vs Target – {latest_year}")
st.plotly_chart(fig, use_container_width=True)
