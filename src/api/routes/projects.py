"""
FastAPI router for Projects — CRUD for projects and their nested wells.

Prefix: /projects  (external: /api/projects via asgi.py mount)

All routes use Depends(get_db) — swap api/db/projects.py to switch backend.

Produced by: backend-agent / fastapi-routes skill
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_file_db
from api.models.project_models import (
    ProjectCreate, ProjectRead, ProjectUpdate, ProjectListItem,
    WellCreate, WellRead, WellUpdate,
)
from api.db import projects as db

router = APIRouter(tags=["Projects"])


def _project_or_404(client, project_id: str) -> dict:
    data, err = db.read_project(client, project_id)
    if err or data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err or "Project not found")
    return data


# ---------------------------------------------------------------------------
# Project endpoints
# ---------------------------------------------------------------------------

@router.get("", response_model=list[ProjectListItem])
async def list_projects(client: Annotated[None, Depends(get_file_db)]):
    """List all projects (summary)."""
    data, err = db.read_projects(client)
    if err:
        raise HTTPException(status_code=500, detail=err)
    return [
        ProjectListItem(
            project_id=p["project_id"],
            project_name=p["project_name"],
            project_type=p["project_type"],
            well_count=len(p.get("wells", [])),
            modified_at=p["modified_at"],
            created_by=p["created_by"],
        )
        for p in data
    ]


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: ProjectCreate,
    client: Annotated[None, Depends(get_file_db)],
):
    """Create a new project."""
    data, err = db.create_project(client, body.model_dump())
    if err or data is None:
        raise HTTPException(status_code=500, detail=err)
    return data


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: str, client: Annotated[None, Depends(get_file_db)]):
    """Get a single project by ID."""
    return _project_or_404(client, project_id)


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: str,
    body: ProjectUpdate,
    client: Annotated[None, Depends(get_file_db)],
):
    """Update project metadata."""
    _project_or_404(client, project_id)
    data, err = db.update_project(client, project_id, body.model_dump(exclude_none=True))
    if err or data is None:
        raise HTTPException(status_code=500, detail=err)
    return data


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str, client: Annotated[None, Depends(get_file_db)]):
    """Delete a project and all its wells."""
    _project_or_404(client, project_id)
    ok, err = db.delete_project(client, project_id)
    if not ok:
        raise HTTPException(status_code=500, detail=err)


# ---------------------------------------------------------------------------
# Well endpoints (nested under project)
# ---------------------------------------------------------------------------

@router.post("/{project_id}/wells", response_model=WellRead, status_code=status.HTTP_201_CREATED)
async def add_well(
    project_id: str,
    body: WellCreate,
    client: Annotated[None, Depends(get_file_db)],
):
    """Add a new well to a project."""
    _project_or_404(client, project_id)
    data, err = db.create_well(client, project_id, body.model_dump())
    if err or data is None:
        raise HTTPException(status_code=500, detail=err)
    return data


@router.put("/{project_id}/wells/{well_id}", response_model=WellRead)
async def update_well(
    project_id: str,
    well_id: str,
    body: WellUpdate,
    client: Annotated[None, Depends(get_file_db)],
):
    """Update a well inside a project."""
    _project_or_404(client, project_id)
    data, err = db.update_well(client, project_id, well_id, body.model_dump(exclude_none=True))
    if err or data is None:
        raise HTTPException(status_code=404, detail=err or "Well not found")
    return data


@router.delete("/{project_id}/wells/{well_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_well(
    project_id: str,
    well_id: str,
    client: Annotated[None, Depends(get_file_db)],
):
    """Delete a well from a project."""
    _project_or_404(client, project_id)
    ok, err = db.delete_well(client, project_id, well_id)
    if not ok:
        raise HTTPException(status_code=404, detail=err or "Well not found")
