"""
Well Sub-Data Routes — /api/wells/{id}/...

Handles all data that lives *inside* a well:
    Wellbore sections (hole sections)
    Casing strings
    Tubular strings (drill string components, BHA)
    Directional survey points (including bulk import)

All endpoints are mounted under /api/wells via the routes/__init__.py
registration, so paths here start with /{well_id}/...
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.auth import get_current_user
from api.database import Database
from api.models import (
    CasingStringCreate, CasingStringResponse,
    SurveyPointCreate, SurveyPointResponse,
    TubularStringCreate, TubularStringResponse,
    WellboreSectionCreate, WellboreSectionResponse,
)

router = APIRouter()
db = Database()


# ── Ownership guard ────────────────────────────────────────────────────────────

async def _assert_ownership(well_id: int, user_id: int) -> dict:
    """Fetch the well and confirm it belongs to *user_id*."""
    well = await db.get_well_by_id(well_id)
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    project = await db.get_project_by_id(well["project_id"])
    if not project or project["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return well


# ── Wellbore Sections ──────────────────────────────────────────────────────────

@router.post("/{well_id}/wellbore", response_model=WellboreSectionResponse, status_code=201)
async def add_wellbore_section(
    well_id: int,
    section: WellboreSectionCreate,
    current_user: dict = Depends(get_current_user),
):
    """Add a planned or actual hole section to a well."""
    await _assert_ownership(well_id, current_user["id"])
    data = section.model_dump()
    data["well_id"] = well_id
    section_id = await db.add_wellbore_section(data)
    return await db.get_wellbore_section_by_id(section_id)


@router.get("/{well_id}/wellbore", response_model=List[WellboreSectionResponse])
async def get_wellbore_sections(
    well_id: int,
    is_plan: Optional[bool] = Query(None, description="True = plan, False = actual"),
    current_user: dict = Depends(get_current_user),
):
    """Return all wellbore sections for a well, optionally filtered by plan/actual."""
    await _assert_ownership(well_id, current_user["id"])
    return await db.get_wellbore_sections(well_id, is_plan=is_plan)


# ── Casing Strings ─────────────────────────────────────────────────────────────

@router.post("/{well_id}/casing", response_model=CasingStringResponse, status_code=201)
async def add_casing_string(
    well_id: int,
    casing: CasingStringCreate,
    current_user: dict = Depends(get_current_user),
):
    """Add a planned or installed casing string."""
    await _assert_ownership(well_id, current_user["id"])
    data = casing.model_dump()
    data["well_id"] = well_id
    casing_id = await db.add_casing_string(data)
    return await db.get_casing_string_by_id(casing_id)


@router.get("/{well_id}/casing", response_model=List[CasingStringResponse])
async def get_casing_strings(
    well_id: int,
    is_plan: Optional[bool] = Query(None, description="True = plan, False = actual"),
    current_user: dict = Depends(get_current_user),
):
    """Return all casing strings, optionally filtered by plan/actual."""
    await _assert_ownership(well_id, current_user["id"])
    return await db.get_casing_strings(well_id, is_plan=is_plan)


# ── Tubular Strings ────────────────────────────────────────────────────────────

@router.post("/{well_id}/tubulars", response_model=TubularStringResponse, status_code=201)
async def add_tubular_string(
    well_id: int,
    tubular: TubularStringCreate,
    current_user: dict = Depends(get_current_user),
):
    """Add a planned or actual drill string / BHA component."""
    await _assert_ownership(well_id, current_user["id"])
    data = tubular.model_dump()
    data["well_id"] = well_id
    tubular_id = await db.add_tubular_string(data)
    return await db.get_tubular_string_by_id(tubular_id)


@router.get("/{well_id}/tubulars", response_model=List[TubularStringResponse])
async def get_tubular_strings(
    well_id: int,
    is_plan: Optional[bool] = Query(None, description="True = plan, False = actual"),
    current_user: dict = Depends(get_current_user),
):
    """Return all tubular string entries, optionally filtered by plan/actual."""
    await _assert_ownership(well_id, current_user["id"])
    return await db.get_tubular_strings(well_id, is_plan=is_plan)


# ── Directional Surveys ────────────────────────────────────────────────────────

@router.post("/{well_id}/surveys", response_model=SurveyPointResponse, status_code=201)
async def add_survey_point(
    well_id: int,
    survey: SurveyPointCreate,
    current_user: dict = Depends(get_current_user),
):
    """Add a single directional survey station."""
    await _assert_ownership(well_id, current_user["id"])
    data = survey.model_dump()
    data["well_id"] = well_id
    survey_id = await db.add_survey_point(data)
    return await db.get_survey_point_by_id(survey_id)


@router.post("/{well_id}/surveys/bulk", response_model=List[SurveyPointResponse], status_code=201)
async def add_survey_points_bulk(
    well_id: int,
    surveys: List[SurveyPointCreate],
    current_user: dict = Depends(get_current_user),
):
    """
    Bulk-import survey stations.

    Accepts a JSON array of survey points and inserts them in one operation.
    Useful for importing from LAS / CSV files on the frontend.
    """
    await _assert_ownership(well_id, current_user["id"])
    created = []
    for survey in surveys:
        data = survey.model_dump()
        data["well_id"] = well_id
        sid = await db.add_survey_point(data)
        created.append(await db.get_survey_point_by_id(sid))
    return created


@router.get("/{well_id}/surveys", response_model=List[SurveyPointResponse])
async def get_survey_points(
    well_id: int,
    survey_type: Optional[str] = Query(None, description="plan | actual"),
    current_user: dict = Depends(get_current_user),
):
    """Return all directional survey stations, optionally filtered by type."""
    await _assert_ownership(well_id, current_user["id"])
    return await db.get_survey_points(well_id, survey_type=survey_type)


@router.delete("/{well_id}/surveys", status_code=status.HTTP_200_OK)
async def delete_survey_points(
    well_id: int,
    survey_type: Optional[str] = Query(None, description="plan | actual | omit for all"),
    current_user: dict = Depends(get_current_user),
):
    """Delete survey stations. Omit ``survey_type`` to wipe both plan and actual."""
    await _assert_ownership(well_id, current_user["id"])
    await db.delete_survey_points(well_id, survey_type=survey_type)
    return {"message": "Survey points deleted successfully"}
