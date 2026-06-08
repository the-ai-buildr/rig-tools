"""Pydantic request/response schemas for the REST API."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from tmp.models import Well


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------
class UserCreate(BaseModel):
    username: str
    full_name: str = ""
    email: str
    role: str = "viewer"
    password: str


class UserRead(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
    role: str
    is_active: bool
    preferences: dict = {}
    created_at: datetime
    updated_at: datetime


class UserPreferences(BaseModel):
    """Partial per-user preferences payload (all fields optional for PATCH)."""

    color_scheme: Optional[str] = None  # dark | light
    accent: Optional[str] = None
    sidebar_collapsed: Optional[bool] = None
    units: Optional[str] = None  # imperial | metric


# ---------------------------------------------------------------------------
# App settings (global, single row)
# ---------------------------------------------------------------------------
class AppSettingsRead(BaseModel):
    id: str
    app_name: str
    default_color_scheme: str
    default_accent: str
    default_units: str
    updated_at: datetime


class AppSettingsUpdate(BaseModel):
    app_name: Optional[str] = None
    default_color_scheme: Optional[str] = None
    default_accent: Optional[str] = None
    default_units: Optional[str] = None


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------
class ProjectCreate(BaseModel):
    name: str
    project_type: str = "single"
    description: Optional[str] = None
    status: str = "planned"
    owner_id: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    project_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    owner_id: Optional[str] = None


class ProjectRead(BaseModel):
    id: str
    name: str
    project_type: str
    description: Optional[str] = None
    status: str
    owner_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Wells
# ---------------------------------------------------------------------------
class WellCreate(BaseModel):
    well: Well
    project_id: Optional[str] = None
    api_number: Optional[str] = None


class WellRead(BaseModel):
    id: str
    project_id: Optional[str] = None
    well_name: str
    api_number: Optional[str] = None
    status: str
    well_type: str
    well: Well
    created_at: datetime
    updated_at: datetime
