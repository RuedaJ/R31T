import streamlit as st
import pandas as pd
from adapters.parsers import load_phase1_zip
st.set_page_config(page_title="REIT Phase 1", page_icon=":building_construction:", layout="wide")

st.sidebar.title("REIT Phase 1")
st.sidebar.markdown("**Tabs:** Data Intake → Alignment → Retrofits (lite) → Governance (lite)")

st.title("REIT – Phase 1 (Usable MVP)")
st.success("Upload your CSVs or drop the provided **REIT_Dataset.zip** to auto-load Phase 1 demo data.")

uploaded_zip = st.file_uploader("Upload Phase 1 input bundle (.zip)", type=["zip"], accept_multiple_files=False)

if uploaded_zip:
    raw = uploaded_zip.read()
    bundle = load_phase1_zip(raw)
    st.session_state["bundle"] = bundle
    st.toast("Bundle loaded.", icon="✅")
else:
    st.info("No bundle uploaded yet. You can still navigate to tabs and upload individual CSVs there.")
