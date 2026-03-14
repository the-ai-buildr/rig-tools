"""
Wellbore Sub-Data Pydantic Models

Covers:
    - Wellbore sections (hole sections)
    - Casing strings (conductor, surface, intermediate, production, liner)
    - Tubular strings (drill string components, BHA)
    - Directional survey points
"""

from typing import Optional
from pydantic import BaseModel


# ── Wellbore Sections ─────────────────────────────────────────────────────────

class WellboreSectionCreate(BaseModel):
    """Request body for POST /api/wells/{id}/wellbore"""
    section_name: str
    section_type: str = "intermediate"   # surface | intermediate | production | other
    top_md: Optional[float] = None
    bottom_md: Optional[float] = None
    top_tvd: Optional[float] = None
    bottom_tvd: Optional[float] = None
    hole_size: Optional[float] = None
    hole_size_unit: str = "in"
    mud_weight: Optional[float] = None
    mud_type: Optional[str] = None
    description: Optional[str] = None
    is_plan: bool = True                  # True = planned, False = actual


class WellboreSectionResponse(WellboreSectionCreate):
    id: int
    well_id: int

    class Config:
        from_attributes = True


# ── Casing Strings ────────────────────────────────────────────────────────────

class CasingStringCreate(BaseModel):
    """Request body for POST /api/wells/{id}/casing"""
    string_name: str
    string_type: str = "intermediate"    # conductor | surface | intermediate | production | liner
    top_md: Optional[float] = None
    bottom_md: Optional[float] = None
    top_tvd: Optional[float] = None
    bottom_tvd: Optional[float] = None
    casing_od: Optional[float] = None    # Outer diameter in inches
    casing_id: Optional[float] = None    # Inner diameter in inches
    weight: Optional[float] = None       # lb/ft
    grade: Optional[str] = None
    connection: Optional[str] = None
    cement_top_md: Optional[float] = None
    cement_bottom_md: Optional[float] = None
    cement_volume: Optional[float] = None
    installed_date: Optional[str] = None  # Only applicable for actual
    description: Optional[str] = None
    is_plan: bool = True


class CasingStringResponse(CasingStringCreate):
    id: int
    well_id: int

    class Config:
        from_attributes = True


# ── Tubular Strings ───────────────────────────────────────────────────────────

class TubularStringCreate(BaseModel):
    """Request body for POST /api/wells/{id}/tubulars"""
    string_name: str
    string_type: str = "drill_string"    # drill_string | BHA | liner | etc.
    component_name: Optional[str] = None
    top_md: Optional[float] = None
    bottom_md: Optional[float] = None
    outer_diameter: Optional[float] = None
    inner_diameter: Optional[float] = None
    weight: Optional[float] = None       # lb/ft
    length: Optional[float] = None       # ft
    grade: Optional[str] = None
    connection: Optional[str] = None
    material: Optional[str] = None
    description: Optional[str] = None
    is_plan: bool = True


class TubularStringResponse(TubularStringCreate):
    id: int
    well_id: int

    class Config:
        from_attributes = True


# ── Directional Survey Points ─────────────────────────────────────────────────

class SurveyPointCreate(BaseModel):
    """Request body for POST /api/wells/{id}/surveys"""
    md: float                             # Measured depth (ft)
    inclination: float                    # Degrees from vertical
    azimuth: float                        # Degrees from true north
    tvd: Optional[float] = None
    northing: Optional[float] = None
    easting: Optional[float] = None
    vertical_section: Optional[float] = None
    dls: Optional[float] = None           # Dog-leg severity (°/100ft)
    tool_face: Optional[float] = None
    section: Optional[str] = None
    survey_type: str = "plan"             # "plan" | "actual"
    survey_date: Optional[str] = None
    survey_company: Optional[str] = None
    tool_type: Optional[str] = None


class SurveyPointResponse(SurveyPointCreate):
    id: int
    well_id: int

    class Config:
        from_attributes = True
