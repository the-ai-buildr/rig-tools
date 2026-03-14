"""
Project Routes — /api/projects

Endpoints:
    POST   /api/projects              Create a new project
    GET    /api/projects              List all projects for the current user
    GET    /api/projects/{id}         Get a single project by ID
    GET    /api/projects/{id}/wells   List wells belonging to a project
    PUT    /api/projects/{id}         Update project metadata
    DELETE /api/projects/{id}         Delete project and all child wells
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.auth import get_current_user
from api.database import Database
from api.models import ProjectCreate, ProjectResponse, ProjectUpdate, WellResponse

router = APIRouter()
db = Database()


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    current_user: dict = Depends(get_current_user),
):
    """Create a new drilling project owned by the authenticated user."""
    data = project.model_dump()
    data["created_by"] = current_user["id"]
    project_id = await db.create_project(data)
    return await db.get_project_by_id(project_id)


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    project_type: Optional[str] = Query(None, description="Filter: single_well | pad"),
    current_user: dict = Depends(get_current_user),
):
    """Return all projects owned by the current user, with optional type filter."""
    return await db.get_all_projects(user_id=current_user["id"], project_type=project_type)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Return a single project. Raises 403 if the project belongs to another user."""
    project = await db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project["created_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return project


@router.get("/{project_id}/wells", response_model=List[WellResponse])
async def list_project_wells(
    project_id: int,
    well_status: Optional[str] = Query(None, alias="status", description="Filter by well status"),
    current_user: dict = Depends(get_current_user),
):
    """Return all wells for a given project, with optional status filter."""
    project = await db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project["created_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await db.get_wells_by_project(project_id, status=well_status)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Partially update project metadata (only supplied fields are changed)."""
    project = await db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project["created_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.update_project(project_id, project_update.model_dump(exclude_unset=True))
    return await db.get_project_by_id(project_id)


@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
async def delete_project(
    project_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Delete a project and cascade-delete all child wells and their sub-data."""
    project = await db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project["created_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.delete_project(project_id)
    return {"message": "Project deleted successfully"}
