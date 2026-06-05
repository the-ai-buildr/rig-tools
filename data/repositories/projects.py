"""Project CRUD."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select

from data.tables import Project


def _now() -> datetime:
    return datetime.now(timezone.utc)


def list_projects(session: Session, owner_id: Optional[str] = None) -> list[Project]:
    stmt = select(Project)
    if owner_id:
        stmt = stmt.where(Project.owner_id == owner_id)
    return list(session.exec(stmt).all())


def get_project(session: Session, project_id: str) -> Optional[Project]:
    return session.get(Project, project_id)


def create_project(
    session: Session,
    *,
    name: str,
    project_type: str = "single",
    description: Optional[str] = None,
    status: str = "planned",
    owner_id: Optional[str] = None,
) -> Project:
    project = Project(
        name=name,
        project_type=project_type,
        description=description,
        status=status,
        owner_id=owner_id,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def update_project(session: Session, project_id: str, **fields) -> Optional[Project]:
    project = session.get(Project, project_id)
    if not project:
        return None
    for key, value in fields.items():
        if hasattr(project, key):
            setattr(project, key, value)
    project.updated_at = _now()
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def delete_project(session: Session, project_id: str) -> bool:
    project = session.get(Project, project_id)
    if not project:
        return False
    session.delete(project)
    session.commit()
    return True
