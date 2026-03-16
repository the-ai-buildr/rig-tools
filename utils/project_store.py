"""Project store — CRUD helpers and JSON import/export using st.session_state."""

from __future__ import annotations

import json
import getpass
from dataclasses import dataclass, asdict
from datetime import datetime

import streamlit as st

from data.models import (
    Project, Well, WellHeader, Wellbore, CasingLiner, MudEntry,
    _now, _current_user,
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _touch(obj) -> None:
    """Update modified_at and modified_by on a Project or Well."""
    obj.modified_at = _now()
    obj.modified_by = _current_user()


def _projects() -> dict:
    return st.session_state.setdefault("projects", {})


# ---------------------------------------------------------------------------
# Project CRUD
# ---------------------------------------------------------------------------

def get_projects() -> dict:
    return _projects()


def create_project(name: str, project_type: str = "single") -> Project:
    p = Project(project_name=name, project_type=project_type)
    _projects()[p.project_id] = p
    return p


def get_project(project_id: str) -> Project | None:
    return _projects().get(project_id)


def update_project(project: Project) -> None:
    _touch(project)
    _projects()[project.project_id] = project


def delete_project(project_id: str) -> None:
    _projects().pop(project_id, None)


# ---------------------------------------------------------------------------
# Well CRUD
# ---------------------------------------------------------------------------

def create_well(project_id: str, well_name: str) -> Well | None:
    project = get_project(project_id)
    if project is None:
        return None
    well = Well(well_name=well_name)
    project.wells.append(well)
    _touch(project)
    return well


def get_well(project_id: str, well_id: str) -> Well | None:
    project = get_project(project_id)
    if project is None:
        return None
    for w in project.wells:
        if w.well_id == well_id:
            return w
    return None


def update_well(project_id: str, well: Well) -> None:
    project = get_project(project_id)
    if project is None:
        return
    for i, w in enumerate(project.wells):
        if w.well_id == well.well_id:
            _touch(well)
            project.wells[i] = well
            _touch(project)
            return


def delete_well(project_id: str, well_id: str) -> None:
    project = get_project(project_id)
    if project is None:
        return
    project.wells = [w for w in project.wells if w.well_id != well_id]
    _touch(project)


# ---------------------------------------------------------------------------
# JSON serialization helpers
# ---------------------------------------------------------------------------

def _serialize(obj) -> dict:
    return asdict(obj)


def _deserialize_well(d: dict) -> Well:
    header = WellHeader(**d.get("header", {}))
    wellbores = [Wellbore(**wb) for wb in d.get("wellbores", [])]
    casings = [CasingLiner(**c) for c in d.get("casings", [])]
    mud_entries = [MudEntry(**m) for m in d.get("mud_entries", [])]
    return Well(
        well_id=d["well_id"],
        well_name=d["well_name"],
        header=header,
        wellbores=wellbores,
        casings=casings,
        mud_entries=mud_entries,
        user_id=d.get("user_id", ""),
        created_at=d.get("created_at", ""),
        created_by=d.get("created_by", ""),
        modified_at=d.get("modified_at", ""),
        modified_by=d.get("modified_by", ""),
    )


def _deserialize_project(d: dict) -> Project:
    wells = [_deserialize_well(w) for w in d.get("wells", [])]
    return Project(
        project_id=d["project_id"],
        project_name=d["project_name"],
        project_type=d.get("project_type", "single"),
        wells=wells,
        user_id=d.get("user_id", ""),
        created_at=d.get("created_at", ""),
        created_by=d.get("created_by", ""),
        modified_at=d.get("modified_at", ""),
        modified_by=d.get("modified_by", ""),
    )


# ---------------------------------------------------------------------------
# Export / Import
# ---------------------------------------------------------------------------

def export_project_json(project_id: str) -> str | None:
    project = get_project(project_id)
    if project is None:
        return None
    return json.dumps(_serialize(project), indent=2, default=str)


def import_project_json(json_str: str) -> Project:
    d = json.loads(json_str)
    project = _deserialize_project(d)
    # Reassign a new ID to avoid collisions if imported multiple times
    existing = _projects()
    if project.project_id in existing:
        from data.models import _new_id
        project.project_id = _new_id()
    existing[project.project_id] = project
    return project
