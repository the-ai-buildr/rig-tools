from pydantic import BaseModel, Field
from typing import Literal


UnitSystem = Literal["us", "metric"]


# --- Hydrostatic Pressure ---

class HydrostaticPressureRequest(BaseModel):
    mud_weight: float = Field(..., description="Mud weight in ppg (US) or kg/m³ (metric)")
    depth: float = Field(..., description="True vertical depth in ft (US) or m (metric)")
    unit_system: UnitSystem = "us"


class HydrostaticPressureResponse(BaseModel):
    pressure: float = Field(..., description="Hydrostatic pressure in psi (US) or kPa (metric)")
    unit_system: UnitSystem


# --- Equivalent Mud Weight ---

class EMWRequest(BaseModel):
    pressure: float = Field(..., description="Pressure in psi (US) or kPa (metric)")
    depth: float = Field(..., gt=0, description="True vertical depth in ft (US) or m (metric) — must be > 0")
    unit_system: UnitSystem = "us"


class EMWResponse(BaseModel):
    emw: float = Field(..., description="Equivalent mud weight in ppg (US) or kg/m³ (metric)")
    unit_system: UnitSystem


# --- Kill Sheet ---

class KillSheetRequest(BaseModel):
    shut_in_drillpipe_pressure: float = Field(..., description="SIDPP in psi (US) or kPa (metric)")
    current_mud_weight: float = Field(..., description="Current mud weight in ppg (US) or kg/m³ (metric)")
    depth: float = Field(..., description="True vertical depth in ft (US) or m (metric)")
    unit_system: UnitSystem = "us"


class KillSheetResponse(BaseModel):
    kill_mud_weight: float = Field(..., description="Kill mud weight in ppg (US) or kg/m³ (metric)")
    kill_mud_weight_rounded: float = Field(..., description="Kill mud weight rounded up to nearest 0.1")
    pressure_safety_margin: float
    unit_system: UnitSystem


# --- Annular Velocity ---

class AnnularVelocityRequest(BaseModel):
    flow_rate: float = Field(..., description="Flow rate in gpm (US) or L/min (metric)")
    hole_diameter: float = Field(..., description="Hole diameter in inches (US) or mm (metric)")
    pipe_od: float = Field(..., description="Pipe OD in inches (US) or mm (metric)")
    unit_system: UnitSystem = "us"


class AnnularVelocityResponse(BaseModel):
    annular_velocity: float = Field(..., description="Annular velocity in ft/min (US) or m/min (metric)")
    annular_area: float = Field(..., description="Annular area in in² (US) or mm² (metric)")
    unit_system: UnitSystem
