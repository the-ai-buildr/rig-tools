"""Project REST endpoints (`/api/projects`)."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from api.schemas import ProjectCreate, ProjectRead, ProjectUpdate
from data.repositories import projects as project_repo

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead])
def list_projects(owner_id: Optional[str] = None):
    return project_repo.list_projects(owner_id=owner_id)


@router.post("", response_model=ProjectRead, status_code=201)
def create_project(payload: ProjectCreate):
    return project_repo.create_project(**payload.model_dump())


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: str):
    project = project_repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(project_id: str, payload: ProjectUpdate):
    project = project_repo.update_project(
        project_id, **payload.model_dump(exclude_unset=True)
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: str):
    if not project_repo.delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
