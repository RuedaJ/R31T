# REIT – Phase 1 (Alignment, Retrofits-lite, Governance-lite)

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## One-click demo
1) Open the app, upload `REIT_Dataset.zip` (from `/data/sample` or your own).
2) Go to **Alignment**, **Retrofits (lite)**, **Governance (lite)** tabs.

## Inputs (Phase 1)
- `assets.csv`: asset_id,country,property_type,area_ipms2_m2,...
- `energy_baselines.csv`: asset_id,year,elec_kwh,fuel_kwh,dh_kwh,carbon_intensity_kgco2e_m2yr?
- `pathways.csv` *(preferred)*: country,property_type,year,target_kgco2e_m2yr
- `retrofits.csv`: asset_id,retrofit_id,measure_type,retrofit_year,expected_kwh_saving_pct,embodied_a1a3_kgco2e_per_m2?
- `governance_checklist.csv`: item_id,category,prompt,weight,value,evidence_link

## Notes
- If `pathways.csv` is not provided, the app uses a transparent linear fallback to 2050.
- Phase 2–3 features (SFDR gating, Net-Zero trackers, PCAF, green-bond eligibility, CVaR) can be added in `services/` without changing the UI wiring.
