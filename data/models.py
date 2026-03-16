from __future__ import annotations

import uuid
import getpass
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


def _new_id() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.utcnow().isoformat()


def _current_user() -> str:
    try:
        return getpass.getuser()
    except Exception:
        return "unknown"


@dataclass
class WellHeader:
    operator: str = ""
    well_name: str = ""
    api_number: str = ""
    field: str = ""
    county: str = ""
    state: str = ""
    country: str = ""
    spud_date: str = ""         # ISO date string YYYY-MM-DD
    rig_name: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class Wellbore:
    wellbore_id: str = field(default_factory=_new_id)
    name: str = ""
    wellbore_type: str = "Vertical"  # Vertical | Horizontal | Deviated
    measured_depth: float = 0.0
    true_vertical_depth: float = 0.0


@dataclass
class CasingLiner:
    id: str = field(default_factory=_new_id)
    name: str = ""
    casing_type: str = "Casing"  # Casing | Liner
    od: float = 0.0              # inches
    id_: float = 0.0             # inches
    weight: float = 0.0          # lb/ft
    grade: str = ""
    top_depth: float = 0.0       # ft
    bottom_depth: float = 0.0    # ft
    cement_top: float = 0.0      # ft


@dataclass
class MudEntry:
    id: str = field(default_factory=_new_id)
    date: str = ""               # ISO date string YYYY-MM-DD
    depth: float = 0.0           # ft
    mud_type: str = ""
    mud_weight: float = 0.0      # ppg
    viscosity: float = 0.0       # cP
    ph: float = 0.0
    chlorides: float = 0.0       # mg/L


@dataclass
class Well:
    well_id: str = field(default_factory=_new_id)
    well_name: str = ""
    header: WellHeader = field(default_factory=WellHeader)
    wellbores: list = field(default_factory=list)       # list[Wellbore]
    casings: list = field(default_factory=list)         # list[CasingLiner]
    mud_entries: list = field(default_factory=list)     # list[MudEntry]
    user_id: str = field(default_factory=_current_user)
    created_at: str = field(default_factory=_now)
    created_by: str = field(default_factory=_current_user)
    modified_at: str = field(default_factory=_now)
    modified_by: str = field(default_factory=_current_user)


@dataclass
class Project:
    project_id: str = field(default_factory=_new_id)
    project_name: str = ""
    project_type: str = "single"   # single | pad
    wells: list = field(default_factory=list)           # list[Well]
    user_id: str = field(default_factory=_current_user)
    created_at: str = field(default_factory=_now)
    created_by: str = field(default_factory=_current_user)
    modified_at: str = field(default_factory=_now)
    modified_by: str = field(default_factory=_current_user)
