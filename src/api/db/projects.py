"""
File-based database layer for Projects.

Each project is stored as {DATA_PATH}/projects/{project_id}.json.
All functions follow the (data, error) tuple contract — never raise.

This module is the only thing that changes when swapping to Supabase:
  1. Replace file I/O with supabase.Client calls
  2. Keep all function signatures identical
  3. Drop the `client` parameter or replace with Client type

Produced by: backend-agent / supabase-crud skill
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from data.models import (
    Project, Well,
    project_to_dict, project_from_dict,
    _new_id, _now, _current_user,
)

_DATA_PATH = Path(os.getenv("DATA_PATH", "/app/data"))
_PROJECTS_DIR = _DATA_PATH / "projects"


def _ensure_dir() -> None:
    _PROJECTS_DIR.mkdir(parents=True, exist_ok=True)


def _project_path(project_id: str) -> Path:
    return _PROJECTS_DIR / f"{project_id}.json"


def _load_project(project_id: str) -> dict | None:
    path = _project_path(project_id)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def _save_project(data: dict) -> None:
    _ensure_dir()
    path = _project_path(data["project_id"])
    path.write_text(json.dumps(data, indent=2))


# ---------------------------------------------------------------------------
# Project CRUD
# ---------------------------------------------------------------------------

def create_project(client, data: dict) -> tuple[dict | None, str | None]:
    try:
        project = Project(
            project_name=data.get("project_name", ""),
            project_type=data.get("project_type", "single"),
        )
        d = project_to_dict(project)
        _save_project(d)
        return d, None
    except Exception as e:
        return None, str(e)


def read_projects(client, filters: dict | None = None) -> tuple[list, str | None]:
    try:
        _ensure_dir()
        results = []
        for f in sorted(_PROJECTS_DIR.glob("*.json")):
            try:
                results.append(json.loads(f.read_text()))
            except Exception:
                continue
        results.sort(key=lambda p: p.get("modified_at", ""), reverse=True)
        return results, None
    except Exception as e:
        return [], str(e)


def read_project(client, project_id: str) -> tuple[dict | None, str | None]:
    d = _load_project(project_id)
    if d is None:
        return None, f"Project {project_id} not found"
    return d, None


def update_project(client, project_id: str, data: dict) -> tuple[dict | None, str | None]:
    try:
        existing = _load_project(project_id)
        if existing is None:
            return None, f"Project {project_id} not found"
        existing.update({k: v for k, v in data.items() if v is not None})
        existing["modified_at"] = _now()
        existing["modified_by"] = _current_user()
        _save_project(existing)
        return existing, None
    except Exception as e:
        return None, str(e)


def delete_project(client, project_id: str) -> tuple[bool, str | None]:
    path = _project_path(project_id)
    if not path.exists():
        return False, f"Project {project_id} not found"
    try:
        path.unlink()
        return True, None
    except Exception as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# Well CRUD (nested inside project file)
# ---------------------------------------------------------------------------

def create_well(client, project_id: str, data: dict) -> tuple[dict | None, str | None]:
    try:
        project_dict = _load_project(project_id)
        if project_dict is None:
            return None, f"Project {project_id} not found"
        import dataclasses
        well = Well(well_name=data.get("well_name", ""))
        well_dict = dataclasses.asdict(well)
        project_dict["wells"].append(well_dict)
        project_dict["modified_at"] = _now()
        _save_project(project_dict)
        return well_dict, None
    except Exception as e:
        return None, str(e)


def read_well(client, project_id: str, well_id: str) -> tuple[dict | None, str | None]:
    project_dict = _load_project(project_id)
    if project_dict is None:
        return None, f"Project {project_id} not found"
    for w in project_dict.get("wells", []):
        if w.get("well_id") == well_id:
            return w, None
    return None, f"Well {well_id} not found"


def update_well(client, project_id: str, well_id: str, data: dict) -> tuple[dict | None, str | None]:
    try:
        project_dict = _load_project(project_id)
        if project_dict is None:
            return None, f"Project {project_id} not found"
        wells = project_dict.get("wells", [])
        for i, w in enumerate(wells):
            if w.get("well_id") == well_id:
                wells[i].update({k: v for k, v in data.items() if v is not None})
                wells[i]["modified_at"] = _now()
                wells[i]["modified_by"] = _current_user()
                project_dict["modified_at"] = _now()
                _save_project(project_dict)
                return wells[i], None
        return None, f"Well {well_id} not found"
    except Exception as e:
        return None, str(e)


def delete_well(client, project_id: str, well_id: str) -> tuple[bool, str | None]:
    try:
        project_dict = _load_project(project_id)
        if project_dict is None:
            return False, f"Project {project_id} not found"
        before = len(project_dict["wells"])
        project_dict["wells"] = [w for w in project_dict["wells"] if w.get("well_id") != well_id]
        if len(project_dict["wells"]) == before:
            return False, f"Well {well_id} not found"
        project_dict["modified_at"] = _now()
        _save_project(project_dict)
        return True, None
    except Exception as e:
        return False, str(e)
