"""Lightweight entity models returned by the repository layer.

These replace the former SQLModel table classes. They are plain Pydantic models
with the same field names the rest of the app already accesses (``user.email``,
``project.name``, ``record.document`` …), so repositories can hydrate Supabase
rows into them without changing call sites. Persistence/identity now lives in
Supabase (auth.users + the public tables); these are read models only.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class _Entity(BaseModel):
    # Ignore any extra columns Supabase returns that we don't model here.
    model_config = ConfigDict(extra="ignore")


class User(_Entity):
    id: str
    username: Optional[str] = None
    full_name: str = ""
    email: Optional[str] = None
    role: str = "viewer"
    is_active: bool = True
    preferences: dict = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AppSettings(_Entity):
    id: str = "global"
    app_name: str = "Rig Tools"
    default_color_scheme: str = "light"
    default_accent: str = "blue"
    default_units: str = "imperial"
    updated_at: Optional[datetime] = None


class Project(_Entity):
    id: str
    name: str
    project_type: str = "single"
    description: Optional[str] = None
    status: str = "planned"
    owner_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WellRecord(_Entity):
    id: str
    project_id: Optional[str] = None
    well_name: str
    api_number: Optional[str] = None
    status: str = "Planning"
    well_type: str = "Horizontal"
    document: dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
