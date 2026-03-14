"""
Well Pydantic Models

Defines request/response shapes for well CRUD and status operations.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class WellCreate(BaseModel):
    """Request body for POST /api/wells"""
    project_id: int
    well_name: str
    well_number: Optional[str] = None
    api_number: Optional[str] = None
    well_type: Optional[str] = None
    surface_lat: Optional[float] = None
    surface_lon: Optional[float] = None
    bottom_hole_lat: Optional[float] = None
    bottom_hole_lon: Optional[float] = None
    rig_name: Optional[str] = None
    contractor: Optional[str] = None
    spud_date: Optional[str] = None
    completion_date: Optional[str] = None
    release_date: Optional[str] = None
    total_depth_planned: Optional[float] = None
    measured_depth_planned: Optional[float] = None
    true_vertical_depth_planned: Optional[float] = None
    kick_off_point: Optional[float] = None
    description: Optional[str] = None
    template_id: Optional[int] = None     # Apply pre-built or custom template


class WellUpdate(BaseModel):
    """Request body for PUT /api/wells/{id} — all fields optional"""
    well_name: Optional[str] = None
    well_number: Optional[str] = None
    api_number: Optional[str] = None
    well_type: Optional[str] = None
    surface_lat: Optional[float] = None
    surface_lon: Optional[float] = None
    bottom_hole_lat: Optional[float] = None
    bottom_hole_lon: Optional[float] = None
    rig_name: Optional[str] = None
    contractor: Optional[str] = None
    spud_date: Optional[str] = None
    completion_date: Optional[str] = None
    release_date: Optional[str] = None
    total_depth_planned: Optional[float] = None
    total_depth_actual: Optional[float] = None
    measured_depth_planned: Optional[float] = None
    measured_depth_actual: Optional[float] = None
    true_vertical_depth_planned: Optional[float] = None
    true_vertical_depth_actual: Optional[float] = None
    kick_off_point: Optional[float] = None
    description: Optional[str] = None


class StatusUpdate(BaseModel):
    """Request body for POST /api/wells/{id}/status"""
    new_status: str   # Planned | Spudded | Drilling | Completed | Suspended | Abandoned
    notes: Optional[str] = None


class WellResponse(BaseModel):
    """
    Full well response including all nested sub-data arrays.

    Nested arrays (wellbore_plan, casing_plan, etc.) are populated by
    ``Database.get_complete_well_data()`` and are empty lists when no data exists.
    """
    id: int
    project_id: int
    well_name: str
    well_number: Optional[str] = None
    api_number: Optional[str] = None
    well_type: Optional[str] = None
    surface_lat: Optional[float] = None
    surface_lon: Optional[float] = None
    bottom_hole_lat: Optional[float] = None
    bottom_hole_lon: Optional[float] = None
    rig_name: Optional[str] = None
    contractor: Optional[str] = None
    spud_date: Optional[str] = None
    completion_date: Optional[str] = None
    release_date: Optional[str] = None
    total_depth_planned: Optional[float] = None
    total_depth_actual: Optional[float] = None
    measured_depth_planned: Optional[float] = None
    measured_depth_actual: Optional[float] = None
    true_vertical_depth_planned: Optional[float] = None
    true_vertical_depth_actual: Optional[float] = None
    kick_off_point: Optional[float] = None
    current_status: str = "Planned"
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # Nested sub-data (populated by get_complete_well_data)
    wellbore_plan: List[Dict[str, Any]] = []
    wellbore_actual: List[Dict[str, Any]] = []
    casing_plan: List[Dict[str, Any]] = []
    casing_actual: List[Dict[str, Any]] = []
    tubular_plan: List[Dict[str, Any]] = []
    tubular_actual: List[Dict[str, Any]] = []
    survey_plan: List[Dict[str, Any]] = []
    survey_actual: List[Dict[str, Any]] = []
    status_history: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True
