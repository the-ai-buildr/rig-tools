"""Project CRUD via the Supabase ``projects`` table (service-role client)."""
from __future__ import annotations

from typing import Optional

from data.entities import Project
from data.supabase_client import get_service_client


def list_projects(owner_id: Optional[str] = None) -> list[Project]:
    client = get_service_client()
    query = client.table("projects").select("*")
    if owner_id:
        query = query.eq("owner_id", owner_id)
    return [Project.model_validate(row) for row in (query.execute().data or [])]


def get_project(project_id: str) -> Optional[Project]:
    client = get_service_client()
    rows = (
        client.table("projects").select("*").eq("id", project_id).limit(1).execute().data
    )
    return Project.model_validate(rows[0]) if rows else None


def create_project(
    *,
    name: str,
    project_type: str = "single",
    description: Optional[str] = None,
    status: str = "planned",
    owner_id: Optional[str] = None,
) -> Project:
    client = get_service_client()
    row = {
        "name": name,
        "project_type": project_type,
        "description": description,
        "status": status,
        "owner_id": owner_id,
    }
    res = client.table("projects").insert(row).execute().data
    return Project.model_validate(res[0])


def update_project(project_id: str, **fields) -> Optional[Project]:
    fields = {k: v for k, v in fields.items() if k in Project.model_fields and k != "id"}
    if not fields:
        return get_project(project_id)
    client = get_service_client()
    res = client.table("projects").update(fields).eq("id", project_id).execute().data
    return Project.model_validate(res[0]) if res else None


def delete_project(project_id: str) -> bool:
    client = get_service_client()
    res = client.table("projects").delete().eq("id", project_id).execute().data
    return bool(res)
