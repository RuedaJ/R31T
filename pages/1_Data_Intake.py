import streamlit as st, pandas as pd
from rules.validators import basic_checks_assets, basic_checks_energy

st.set_page_config(page_title="Data Intake", page_icon="📥", layout="wide")
st.title("📥 Data Intake & Validation")

def read_csv(label):
    return st.file_uploader(f"Upload **{label}** CSV", type=["csv"], key=f"{label}_u")

assets_u = read_csv("assets.csv (required)")
energy_u = read_csv("energy_baselines.csv (required)")
retro_u  = read_csv("retrofits.csv (optional)")
gov_u    = read_csv("governance_checklist.csv (optional)")
path_u   = st.file_uploader("Upload **pathways.csv** (optional, preferred)", type=["csv"])

bundle = st.session_state.get("bundle")

def df_or_none(upload, key_in_bundle):
    if upload:
        return pd.read_csv(upload)
    if bundle and key_in_bundle in bundle and isinstance(bundle[key_in_bundle], pd.DataFrame):
        return bundle[key_in_bundle]
    return None

assets = df_or_none(assets_u, "assets")
energy = df_or_none(energy_u, "energy")
retro  = df_or_none(retro_u, "retro")
gov    = df_or_none(gov_u, "gov")
pathways = pd.read_csv(path_u) if path_u else (bundle.get("pathways_csv") if bundle else None)

# store for other tabs
if assets is not None: st.session_state["assets_df"] = assets
if energy is not None: st.session_state["energy_df"] = energy
if pathways is not None: st.session_state["pathways_df"] = pathways

cols = st.columns(4)
if assets is not None:
    with cols[0]: st.metric("Assets rows", len(assets))
if energy is not None:
    with cols[1]: st.metric("Energy rows", len(energy))
if retro is not None:
    with cols[2]: st.metric("Retrofit rows", len(retro))
if pathways is not None:
    with cols[3]: st.metric("Pathway points", len(pathways))

errs = []
if assets is not None: errs += basic_checks_assets(assets)
if energy is not None and assets is not None: errs += basic_checks_energy(energy, assets)

if errs:
    st.error("Validation issues detected:")
    for e in errs: st.markdown(f"- {e}")
else:
    st.success("Basic validations passed (Phase 1).")

if assets is not None and energy is not None:
    req = len(assets) + len(energy["asset_id"].unique())
    got = len(assets.dropna()) + len(energy.dropna())
    coverage = round(100 * got / max(req,1), 1)
    st.metric("Data Coverage %", f"{coverage}%")

st.caption("Phase 1 validations are intentionally lightweight. Phase 2 adds full data contracts & stricter unit checks.")
