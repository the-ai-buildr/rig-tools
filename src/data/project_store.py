""" Session-state store for Projects and Wells.

    Manages runtime state in st.session_state["projects"] as a dict of
    {project_id: dict} — serialized on write, deserialized on read.

    Exports init_project_state() which is called by utils/global_init.py.
    No other module should define project-related session state keys.

    Produced by: frontend-agent / data-layer
"""
import json
import streamlit as st

from data.models import (
    Project, Well,
    project_to_dict, project_from_dict,
    project_to_json, project_from_json,
    _now, _current_user,
)


# ---------------------------------------------------------------------------
# Session state initialisation — called once by global_init
# ---------------------------------------------------------------------------

def init_project_state() -> None:
    """Register all project + wizard session state keys. Called by global_init."""
    st.session_state.setdefault("projects", {})
    st.session_state.setdefault("active_project_id", None)
    st.session_state.setdefault("active_well_id", None)
    # Wizard keys
    st.session_state.setdefault("project_wizard_step", 0)
    st.session_state.setdefault("project_wizard_mode", None)        # "create" | "upload"
    st.session_state.setdefault("project_wizard_name", "")
    st.session_state.setdefault("project_wizard_type", "single")    # "single" | "pad"
    st.session_state.setdefault("project_wizard_import_data", None) # dict from parsed JSON


def _reset_wizard() -> None:
    st.session_state["project_wizard_step"] = 0
    st.session_state["project_wizard_mode"] = None
    st.session_state["project_wizard_name"] = ""
    st.session_state["project_wizard_type"] = "single"
    st.session_state["project_wizard_import_data"] = None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _store() -> dict:
    """Return the raw projects dict from session state."""
    return st.session_state["projects"]


def _read(project_id: str) -> dict | None:
    return _store().get(project_id)


def _write(project: Project) -> None:
    _store()[project.project_id] = project_to_dict(project)


# ---------------------------------------------------------------------------
# Project CRUD
# ---------------------------------------------------------------------------

def get_all_projects() -> list[Project]:
    """Return all projects sorted by modified_at descending."""
    projects = [project_from_dict(d) for d in _store().values()]
    return sorted(projects, key=lambda p: p.modified_at, reverse=True)


def get_project(project_id: str) -> Project | None:
    raw = _read(project_id)
    return project_from_dict(raw) if raw else None


def create_project(name: str, project_type: str = "single") -> Project:
    project = Project(project_name=name, project_type=project_type)
    _write(project)
    return project


def update_project(project: Project) -> None:
    project.modified_at = _now()
    project.modified_by = _current_user()
    _write(project)


def delete_project(project_id: str) -> bool:
    if project_id in _store():
        del _store()[project_id]
        return True
    return False


# ---------------------------------------------------------------------------
# Well CRUD
# ---------------------------------------------------------------------------

def create_well(project_id: str, well_name: str) -> Well | None:
    project = get_project(project_id)
    if project is None:
        return None
    well = Well(well_name=well_name)
    project.wells.append(well)
    update_project(project)
    return well


def get_well(project_id: str, well_id: str) -> Well | None:
    project = get_project(project_id)
    if project is None:
        return None
    for well in project.wells:
        if well.well_id == well_id:
            return well
    return None


def update_well(project_id: str, well: Well) -> None:
    project = get_project(project_id)
    if project is None:
        return
    well.modified_at = _now()
    well.modified_by = _current_user()
    project.wells = [well if w.well_id == well.well_id else w for w in project.wells]
    update_project(project)


def delete_well(project_id: str, well_id: str) -> bool:
    project = get_project(project_id)
    if project is None:
        return False
    before = len(project.wells)
    project.wells = [w for w in project.wells if w.well_id != well_id]
    if len(project.wells) < before:
        update_project(project)
        return True
    return False


# ---------------------------------------------------------------------------
# Export / Import
# ---------------------------------------------------------------------------

def export_project_json(project_id: str) -> str | None:
    """Return the project as a JSON string, or None if not found."""
    project = get_project(project_id)
    if project is None:
        return None
    return project_to_json(project)


def import_project_from_json(json_str: str) -> Project | None:
    """
    Parse a JSON string and merge the project into session state.
    Merge strategy: overwrites by project_id (idempotent re-import).
    Returns the imported Project, or None on parse failure.
    """
    try:
        project = project_from_json(json_str)
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    _write(project)
    return project
