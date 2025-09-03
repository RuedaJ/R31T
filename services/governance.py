import pandas as pd

REQUIRED_MIN = {"Board oversight","Scope coverage","Targets","Monitoring"}

def readiness_score(checklist: pd.DataFrame) -> dict:
    df = checklist.copy()
    df["weight"] = df["weight"].fillna(0)
    df["value"] = df["value"].fillna(0)
    denom = max(df["weight"].sum(), 1)
    score = (df["weight"] * df["value"]).sum() / denom
    present = set(df.loc[df["value"]>=0, "category"].unique().tolist())
    complete = REQUIRED_MIN.issubset(present)
    return {"readiness_pct": round(100*score,1), "complete_minimum": bool(complete)}
