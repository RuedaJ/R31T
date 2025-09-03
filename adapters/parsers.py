import io, zipfile, pandas as pd
from typing import Dict

def _read_csv_from_zip(zf: zipfile.ZipFile, name: str, **kwargs) -> pd.DataFrame:
    with zf.open(name) as f:
        return pd.read_csv(f, **kwargs)

def load_phase1_zip(zip_bytes: bytes) -> Dict[str, pd.DataFrame]:
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    names = {n for n in zf.namelist()}
    out = {}
    # Best-effort reads; adapt to your actual bundle structure
    def read_or_none(n, **kw):
        try: return _read_csv_from_zip(zf, n, **kw)
        except KeyError: return None

    # Try a few common locations
    out["assets"]   = read_or_none("assets.csv")
    out["energy"]   = read_or_none("energy_baselines.csv")
    out["retro"]    = read_or_none("retrofits.csv")
    out["gov"]      = read_or_none("governance_checklist.csv")
    out["pathways_csv"] = read_or_none("pathways.csv")

    # Alternative nested path (like 'REIT Dataset/…')
    if out["assets"] is None:
        out["assets"] = read_or_none("REIT Dataset/assets.csv")
    if out["energy"] is None:
        out["energy"] = read_or_none("REIT Dataset/energy_baselines.csv")
    if out["retro"] is None:
        out["retro"] = read_or_none("REIT Dataset/retrofits.csv")
    if out["gov"] is None:
        out["gov"] = read_or_none("REIT Dataset/governance_checklist.csv")
    if out["pathways_csv"] is None:
        out["pathways_csv"] = read_or_none("REIT Dataset/pathways.csv")

    return out
