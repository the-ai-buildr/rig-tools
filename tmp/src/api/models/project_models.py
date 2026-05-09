"""
Pydantic v2 schemas for the Projects API.
Mirrors data/models.py dataclasses — used only in api/routes/ and api/db/.

Produced by: backend-agent / fastapi-routes skill
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Nested schemas
# ---------------------------------------------------------------------------

class WellHeaderSchema(BaseModel):
    operator: str = ""
    well_name: str = ""
    api_number: str = ""
    field: str = ""
    county: str = ""
    state: str = ""
    country: str = ""
    spud_date: str = ""
    rig_name: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class WellboreSchema(BaseModel):
    wellbore_id: str = ""
    name: str = ""
    wellbore_type: str = "Vertical"
    measured_depth: float = 0.0
    true_vertical_depth: float = 0.0


class CasingLinerSchema(BaseModel):
    id: str = ""
    name: str = ""
    casing_type: str = "Casing"
    od: float = 0.0
    id_: float = 0.0
    weight: float = 0.0
    grade: str = ""
    top_depth: float = 0.0
    bottom_depth: float = 0.0
    cement_top: float = 0.0


class MudEntrySchema(BaseModel):
    id: str = ""
    date: str = ""
    depth: float = 0.0
    mud_type: str = ""
    mud_weight: float = 0.0
    viscosity: float = 0.0
    ph: float = 0.0
    chlorides: float = 0.0


# ---------------------------------------------------------------------------
# Well schemas
# ---------------------------------------------------------------------------

class WellCreate(BaseModel):
    well_name: str = Field(..., min_length=1)


class WellUpdate(BaseModel):
    well_name: Optional[str] = None
    header: Optional[WellHeaderSchema] = None
    wellbores: Optional[list[WellboreSchema]] = None
    casings: Optional[list[CasingLinerSchema]] = None
    mud_entries: Optional[list[MudEntrySchema]] = None


class WellRead(BaseModel):
    well_id: str
    well_name: str
    header: WellHeaderSchema
    wellbores: list[WellboreSchema]
    casings: list[CasingLinerSchema]
    mud_entries: list[MudEntrySchema]
    user_id: str
    created_at: str
    created_by: str
    modified_at: str
    modified_by: str


# ---------------------------------------------------------------------------
# Project schemas
# ---------------------------------------------------------------------------

class ProjectCreate(BaseModel):
    project_name: str = Field(..., min_length=1)
    project_type: str = Field("single", pattern="^(single|pad)$")


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    project_type: Optional[str] = Field(None, pattern="^(single|pad)$")


class ProjectRead(BaseModel):
    project_id: str
    project_name: str
    project_type: str
    wells: list[WellRead]
    user_id: str
    created_at: str
    created_by: str
    modified_at: str
    modified_by: str


class ProjectListItem(BaseModel):
    """Lightweight project summary for list views."""
    project_id: str
    project_name: str
    project_type: str
    well_count: int
    modified_at: str
    created_by: str
