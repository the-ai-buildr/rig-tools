"""
Project Pydantic Models

Defines request/response shapes for drilling project CRUD operations.
"""

from typing import Optional
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    """Request body for POST /api/projects"""
    project_name: str
    project_type: str = "single_well"       # "single_well" | "pad"
    pad_name: Optional[str] = None
    surface_location_lat: Optional[float] = None
    surface_location_lon: Optional[float] = None
    field: Optional[str] = None
    operator: Optional[str] = None
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    """Request body for PUT /api/projects/{id} — all fields optional"""
    project_name: Optional[str] = None
    project_type: Optional[str] = None
    pad_name: Optional[str] = None
    surface_location_lat: Optional[float] = None
    surface_location_lon: Optional[float] = None
    field: Optional[str] = None
    operator: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    """Response shape for project endpoints"""
    id: int
    project_name: str
    project_type: str
    pad_name: Optional[str] = None
    surface_location_lat: Optional[float] = None
    surface_location_lon: Optional[float] = None
    field: Optional[str] = None
    operator: Optional[str] = None
    description: Optional[str] = None
    created_by: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    well_count: Optional[int] = 0

    class Config:
        from_attributes = True
