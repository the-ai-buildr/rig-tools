"""
Pure Python dataclass models for Projects, Wells, and related entities.
No Streamlit, FastAPI, or framework imports — safe for calcs/ and API layers.

Produced by: backend-agent / data-layer
"""
from __future__ import annotations

import json
import uuid
import getpass
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _new_id() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _current_user() -> str:
    try:
        return getpass.getuser()
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# Sub-entities
# ---------------------------------------------------------------------------

@dataclass
class WellHeader:
    operator: str = ""
    well_name: str = ""
    api_number: str = ""
    field: str = ""
    county: str = ""
    state: str = ""
    country: str = ""
    spud_date: str = ""           # ISO date string YYYY-MM-DD
    rig_name: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class Wellbore:
    wellbore_id: str = field(default_factory=_new_id)
    name: str = ""
    wellbore_type: str = "Vertical"   # Vertical | Horizontal | Deviated
    measured_depth: float = 0.0
    true_vertical_depth: float = 0.0


@dataclass
class CasingLiner:
    id: str = field(default_factory=_new_id)
    name: str = ""
    casing_type: str = "Casing"   # Casing | Liner
    od: float = 0.0               # inches
    id_: float = 0.0              # inches (trailing _ avoids clash with built-in id)
    weight: float = 0.0           # lb/ft
    grade: str = ""
    top_depth: float = 0.0        # ft
    bottom_depth: float = 0.0     # ft
    cement_top: float = 0.0       # ft


@dataclass
class MudEntry:
    id: str = field(default_factory=_new_id)
    date: str = ""                # ISO date string YYYY-MM-DD
    depth: float = 0.0            # ft
    mud_type: str = ""
    mud_weight: float = 0.0       # ppg
    viscosity: float = 0.0        # cP
    ph: float = 0.0
    chlorides: float = 0.0        # mg/L


# ---------------------------------------------------------------------------
# Core entities
# ---------------------------------------------------------------------------

@dataclass
class Well:
    well_id: str = field(default_factory=_new_id)
    well_name: str = ""
    header: WellHeader = field(default_factory=WellHeader)
    wellbores: list = field(default_factory=list)     # list[Wellbore]
    casings: list = field(default_factory=list)        # list[CasingLiner]
    mud_entries: list = field(default_factory=list)    # list[MudEntry]
    user_id: str = field(default_factory=_current_user)
    created_at: str = field(default_factory=_now)
    created_by: str = field(default_factory=_current_user)
    modified_at: str = field(default_factory=_now)
    modified_by: str = field(default_factory=_current_user)


@dataclass
class Project:
    project_id: str = field(default_factory=_new_id)
    project_name: str = ""
    project_type: str = "single"  # single | pad
    wells: list = field(default_factory=list)          # list[Well]
    user_id: str = field(default_factory=_current_user)
    created_at: str = field(default_factory=_now)
    created_by: str = field(default_factory=_current_user)
    modified_at: str = field(default_factory=_now)
    modified_by: str = field(default_factory=_current_user)


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def project_to_dict(project: Project) -> dict:
    """Serialize a Project dataclass to a plain dict (JSON-safe)."""
    return asdict(project)


def _wellheader_from_dict(d: dict) -> WellHeader:
    return WellHeader(**{k: v for k, v in d.items() if k in WellHeader.__dataclass_fields__})


def _wellbore_from_dict(d: dict) -> Wellbore:
    return Wellbore(**{k: v for k, v in d.items() if k in Wellbore.__dataclass_fields__})


def _casing_from_dict(d: dict) -> CasingLiner:
    return CasingLiner(**{k: v for k, v in d.items() if k in CasingLiner.__dataclass_fields__})


def _mud_from_dict(d: dict) -> MudEntry:
    return MudEntry(**{k: v for k, v in d.items() if k in MudEntry.__dataclass_fields__})


def _well_from_dict(d: dict) -> Well:
    well = Well(
        well_id=d.get("well_id", _new_id()),
        well_name=d.get("well_name", ""),
        header=_wellheader_from_dict(d.get("header", {})),
        wellbores=[_wellbore_from_dict(wb) for wb in d.get("wellbores", [])],
        casings=[_casing_from_dict(c) for c in d.get("casings", [])],
        mud_entries=[_mud_from_dict(m) for m in d.get("mud_entries", [])],
        user_id=d.get("user_id", _current_user()),
        created_at=d.get("created_at", _now()),
        created_by=d.get("created_by", _current_user()),
        modified_at=d.get("modified_at", _now()),
        modified_by=d.get("modified_by", _current_user()),
    )
    return well


def project_from_dict(d: dict) -> Project:
    """Reconstruct a Project dataclass from a plain dict."""
    return Project(
        project_id=d.get("project_id", _new_id()),
        project_name=d.get("project_name", ""),
        project_type=d.get("project_type", "single"),
        wells=[_well_from_dict(w) for w in d.get("wells", [])],
        user_id=d.get("user_id", _current_user()),
        created_at=d.get("created_at", _now()),
        created_by=d.get("created_by", _current_user()),
        modified_at=d.get("modified_at", _now()),
        modified_by=d.get("modified_by", _current_user()),
    )


def project_to_json(project: Project) -> str:
    """Serialize a Project to a JSON string."""
    return json.dumps(project_to_dict(project), indent=2)


def project_from_json(json_str: str) -> Project:
    """Deserialize a Project from a JSON string. Raises ValueError on bad JSON."""
    return project_from_dict(json.loads(json_str))
