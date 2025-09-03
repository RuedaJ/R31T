from pydantic import BaseModel, Field
from typing import Optional, Literal

PropertyType = Literal["office","retail","industrial","residential","hotel","mixed","other"]

class Asset(BaseModel):
    asset_id: str
    country: str
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    property_type: PropertyType
    area_ipms2_m2: float = Field(gt=0)
    year_built: Optional[int] = None
    epc_label: Optional[str] = None
    grid_region: Optional[str] = None

class EnergyBaseline(BaseModel):
    asset_id: str
    year: int
    elec_kwh: float = Field(ge=0)
    fuel_kwh: float = Field(ge=0)
    dh_kwh: float = Field(ge=0)
    carbon_intensity_kgco2e_m2yr: Optional[float] = Field(default=None, ge=0)

class RetrofitRow(BaseModel):
    asset_id: str
    retrofit_id: str
    measure_type: Literal["envelope","HVAC","lighting","refrigerants","PV","controls","other"]
    retrofit_year: int
    capex_per_m2_eur: Optional[float] = Field(default=None, ge=0)
    expected_kwh_saving_pct: Optional[float] = Field(default=None, ge=0, le=100)
    embodied_a1a3_kgco2e_per_m2: Optional[float] = Field(default=None, ge=0)
    materials_ref: Optional[str] = None

class PathwayPoint(BaseModel):
    country: str
    property_type: PropertyType
    year: int
    target_kgco2e_m2yr: float = Field(ge=0)

class GovernanceItem(BaseModel):
    item_id: str
    category: str
    prompt: str
    weight: float = Field(ge=0, le=1)
    value: Optional[float] = Field(default=None, ge=0, le=1)
    evidence_link: Optional[str] = None

class CoverageSummary(BaseModel):
    assets_required: int
    assets_present: int
    energy_rows_required: int
    energy_rows_present: int

    @property
    def coverage_pct(self) -> float:
        denom = max(self.assets_required + self.energy_rows_required, 1)
        num = self.assets_present + self.energy_rows_present
        return round(100 * num / denom, 1)
