"""
Well Routes — /api/wells

Endpoints:
    POST   /api/wells              Create a new well inside a project
    GET    /api/wells/{id}         Get a well with all nested sub-data
    PUT    /api/wells/{id}         Update well header fields
    POST   /api/wells/{id}/status  Change well operational status
    DELETE /api/wells/{id}         Delete well and all its sub-data
"""

from fastapi import APIRouter, Depends, HTTPException, status

from api.auth import get_current_user
from api.database import Database
from api.models import WellCreate, WellResponse, WellUpdate, StatusUpdate

router = APIRouter()
db = Database()


async def _assert_well_ownership(well_id: int, user_id: int) -> dict:
    """
    Helper: fetch a well and confirm it belongs to *user_id*.

    Returns the well dict on success, raises HTTPException otherwise.
    """
    well = await db.get_well_by_id(well_id)
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    project = await db.get_project_by_id(well["project_id"])
    if not project or project["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return well


@router.post("", response_model=WellResponse, status_code=status.HTTP_201_CREATED)
async def create_well(
    well: WellCreate,
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new well inside an existing project.

    Optionally pass ``template_id`` to pre-populate wellbore, casing,
    tubular, and survey data from a saved template.
    """
    project = await db.get_project_by_id(well.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project["created_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    well_id = await db.create_well(well.model_dump())

    if well.template_id:
        template = await db.get_template_by_id(well.template_id)
        if template and template.get("template_data"):
            await db.apply_template_to_well(well_id, template["template_data"])

    return await db.get_complete_well_data(well_id)


@router.get("/{well_id}", response_model=WellResponse)
async def get_well(
    well_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Return a well with all nested sub-data:
    wellbore, casing, tubulars, surveys, and status history.
    """
    await _assert_well_ownership(well_id, current_user["id"])
    return await db.get_complete_well_data(well_id)


@router.put("/{well_id}", response_model=WellResponse)
async def update_well(
    well_id: int,
    well_update: WellUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Partially update well header fields. Only supplied fields are changed."""
    await _assert_well_ownership(well_id, current_user["id"])
    await db.update_well(well_id, well_update.model_dump(exclude_unset=True))
    return await db.get_complete_well_data(well_id)


@router.post("/{well_id}/status", response_model=WellResponse)
async def update_well_status(
    well_id: int,
    status_update: StatusUpdate,
    current_user: dict = Depends(get_current_user),
):
    """
    Transition the well to a new operational status.

    Valid statuses: Planned → Spudded → Drilling → Completed → Suspended → Abandoned.
    Each transition is recorded in ``status_history``.
    """
    await _assert_well_ownership(well_id, current_user["id"])
    await db.update_well_status(
        well_id=well_id,
        new_status=status_update.new_status,
        user_id=current_user["id"],
        notes=status_update.notes,
    )
    return await db.get_complete_well_data(well_id)


@router.delete("/{well_id}", status_code=status.HTTP_200_OK)
async def delete_well(
    well_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Delete a well and all associated wellbore, casing, tubular, and survey data."""
    await _assert_well_ownership(well_id, current_user["id"])
    await db.delete_well(well_id)
    return {"message": "Well deleted successfully"}
