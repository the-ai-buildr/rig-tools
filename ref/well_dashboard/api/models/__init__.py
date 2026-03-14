"""
Pydantic Models Package — Well Dashboard API

All request/response models are defined here and re-exported for easy importing.

Usage:
    from api.models import WellCreate, WellResponse, ProjectCreate
"""

from api.models.auth_models import UserCreate, UserLogin, UserResponse
from api.models.project_models import ProjectCreate, ProjectResponse, ProjectUpdate
from api.models.well_models import (
    WellCreate,
    WellResponse,
    WellUpdate,
    StatusUpdate,
)
from api.models.wellbore_models import (
    WellboreSectionCreate,
    WellboreSectionResponse,
    CasingStringCreate,
    CasingStringResponse,
    TubularStringCreate,
    TubularStringResponse,
    SurveyPointCreate,
    SurveyPointResponse,
)
from api.models.template_models import TemplateCreate, TemplateResponse
from api.models.export_models import ExportRequest, ExportResponse

__all__ = [
    # Auth
    "UserCreate", "UserLogin", "UserResponse",
    # Projects
    "ProjectCreate", "ProjectResponse", "ProjectUpdate",
    # Wells
    "WellCreate", "WellResponse", "WellUpdate", "StatusUpdate",
    # Wellbore sub-data
    "WellboreSectionCreate", "WellboreSectionResponse",
    "CasingStringCreate", "CasingStringResponse",
    "TubularStringCreate", "TubularStringResponse",
    "SurveyPointCreate", "SurveyPointResponse",
    # Templates
    "TemplateCreate", "TemplateResponse",
    # Export
    "ExportRequest", "ExportResponse",
]
