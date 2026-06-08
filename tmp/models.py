"""
Pydantic v2 models for the 4S well template schema.
"""
from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class WellStatus(str, Enum):
    DRILLING = "Drilling"
    COMPLETED = "Completed"
    ABANDONED = "Abandoned"
    SUSPENDED = "Suspended"
    PLANNING = "Planning"

class WellType(str, Enum):
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"
    DEVIATED = "Deviated"

class SectionStatus(str, Enum):
    COMPLETE = "Complete"
    IN_PROGRESS = "In Progress"
    NOT_STARTED = "Not Started"
    PLANNED = "Planned"

class DrillStringStatus(str, Enum):
    IN_HOLE = "In Hole"
    SURFACE = "Surface"
    LAID_DOWN = "Laid Down"

class MudType(str, Enum):
    WBM = "WBM"         # Water Based Mud
    OBM = "OBM"         # Oil Based Mud    
    FWM = "FWM"         # Fresh Water Mud

class MudStatus(str, Enum):
    CIRCULATING = "Circulating"
    STATIC = "Static"
    MIXING = "Mixing"

class DirectionalStatus(str, Enum):
    PLANNING = "Planning"
    ACTIVE = "Active"
    COMPLETE = "Complete"

class RigType(str, Enum):
    LAND = "Land"
    JACKUP = "Jackup"
    SEMI = "Semi"
    DRILLSHIP = "Drillship"

class RigStatus(str, Enum):
    ACTIVE = "Active"
    COLD_STACKED = "Cold Stacked"
    WARM_STACKED = "Warm Stacked"
    MOVING = "Moving"


# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------

class Location(BaseModel):
    country: str = ""
    state: str = ""
    county: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class OperatorContact(BaseModel):
    name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None

# --- Rig ---
class RigContact(BaseModel):
    name: str = ""
    phone: Optional[str] = None
    email: Optional[str] = None

class Rig(BaseModel):
    rig_number: str
    rig_name: str
    contractor: str = ""
    rig_type: RigType = RigType.LAND
    status: RigStatus = RigStatus.ACTIVE
    max_depth_ft: Optional[float] = None
    hp: Optional[int] = None
    contact: RigContact = Field(default_factory=RigContact)

class WellHeader(BaseModel):
    well_name: str
    afe_number: str = ""
    operator: str = ""
    users: list[str] = Field(default_factory=list)
    date_created: Optional[date] = None
    last_modified: Optional[datetime] = None
    status: WellStatus = WellStatus.PLANNING
    location: Location = Field(default_factory=Location)
    directions: Optional[str] = None
    well_type: WellType = WellType.HORIZONTAL
    spud_date: Optional[date] = None
    expected_td_date: Optional[date] = None
    operator_contact: OperatorContact = Field(default_factory=OperatorContact)
    rig: Optional[Rig] = None
    notes: Optional[str] = None

# --- Wellbore ---
class WellboreSection(BaseModel):
    name: str
    size: float                         # hole size, inches
    depth_md: float                     # measured depth, ft
    status: SectionStatus = SectionStatus.NOT_STARTED

class Wellbore(BaseModel):
    sections: list[WellboreSection] = Field(default_factory=list)

# --- Casing / Liner ---
class CsgLinerSection(BaseModel):
    name: str
    size_od_in: float
    size_id_in: float
    top_depth_md: float
    btm_depth_md: float
    status: SectionStatus = SectionStatus.NOT_STARTED

class CsgLiner(BaseModel):
    sections: list[CsgLinerSection] = Field(default_factory=list)

# --- Drill String ---
class DrillStringComponent(BaseModel):
    type: str                           # e.g. "Bit", "Mud Motor", "HWDP"
    od: Optional[float] = None          # outer diameter, inches (from JSON)
    size_od: Optional[float] = None     # outer diameter alias
    size_id: Optional[float] = None     # inner diameter, inches
    length: float = 0.0                 # ft
    wellbore_ref: Optional[str] = None  # wellbore name reference


class DrillString(BaseModel):
    name: str = ""
    total_length: float = 0.0          # ft
    wellbore_ref: Optional[str] = None  # wellbore name reference
    status: DrillStringStatus = DrillStringStatus.SURFACE
    components: list[DrillStringComponent] = Field(default_factory=list)

# --- Mud ---
class MudSection(BaseModel):
    name: str
    type: MudType
    top_depth_md: float
    btm_depth_md: float
    mw_min_ppg: float
    mw_max_ppg: float
    details: Optional[str] = None
    notes: Optional[str] = None

class Mud(BaseModel):
    sections: list[MudSection] = Field(default_factory=list)

# --- Directional ---
class SurveyStation(BaseModel):
    md: float                           # measured depth, ft
    inc: float                          # inclination, degrees
    azi: float                          # azimuth, degrees
    tvd: Optional[float] = None         # true vertical depth, ft

class Directional(BaseModel):
    status: DirectionalStatus = DirectionalStatus.PLANNING
    surveys: list[SurveyStation] = Field(default_factory=list)

# --- Geology ---
class Formation(BaseModel):
    name: str
    top_md: float                        # measured depth, ft
    btm_md: Optional[float] = None       # measured depth, ft
    top_tvd: Optional[float] = None      # true vertical depth, ft
    btm_tvd: Optional[float] = None      # true vertical depth, ft

class Geology(BaseModel):
    formations: list[Formation] = Field(default_factory=list)

# --- Other ---
class Other(BaseModel):
    rig_name: str = ""
    misc_notes: str = ""

# ---------------------------------------------------------------------------
# Root model
# ---------------------------------------------------------------------------

class Well(BaseModel):
    header: WellHeader
    wellbores: list[Wellbore] = Field(default_factory=list)
    csg_liners: list[CsgLiner] = Field(default_factory=list)
    drill_string: DrillString = Field(default_factory=DrillString)
    mud: Mud = Field(default_factory=Mud)
    directional: Directional = Field(default_factory=Directional)
    geology: Geology = Field(default_factory=Geology)
    other: Other = Field(default_factory=Other)
