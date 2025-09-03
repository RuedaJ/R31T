import pandas as pd
from services.crrem_alignment import compute_operational_intensity, derive_pathway_targets, misalignment_year

def test_alignment_smoke():
    assets = pd.DataFrame([{"asset_id":"A1","country":"ES","property_type":"office","area_ipms2_m2":1000}])
    energy  = pd.DataFrame([{"asset_id":"A1","year":2024,"elec_kwh":100000,"fuel_kwh":0,"dh_kwh":0}])
    pth = pd.DataFrame([{"country":"ES","property_type":"office","year":2024,"target_kgco2e_m2yr":20}])
    op = compute_operational_intensity(energy, assets)
    p = derive_pathway_targets(pth, assets, energy[["year"]])
    res, joined = misalignment_year(op, p)
    assert "misalignment_year" in res.columns
