import streamlit as st, pandas as pd
from services.governance import readiness_score

st.set_page_config(page_title="Governance", page_icon="🏛️", layout="wide")
st.title("🏛️ Governance – Readiness (Lite)")

gov_u = st.file_uploader("governance_checklist.csv", type=["csv"])
if not gov_u:
    st.info("Upload **governance_checklist.csv** (item_id,category,prompt,weight,value,evidence_link).")
    st.stop()

gov = pd.read_csv(gov_u)
res = readiness_score(gov)

c1,c2 = st.columns(2)
c1.metric("Governance Readiness %", f"{res['readiness_pct']}%")
c2.metric("Minimum items complete", "Yes" if res["complete_minimum"] else "No")

st.dataframe(gov)
