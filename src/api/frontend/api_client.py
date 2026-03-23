"""
HTTP client for Streamlit → FastAPI communication.

Usage:
    from api.frontend.api_client import api_request, get_api_base_url

    result = api_request("POST", "/calcs/hydrostatic-pressure", json={
        "mud_weight": 10.5,
        "depth": 5000,
        "unit_system": "us",
    })
"""

import os
import httpx
import streamlit as st
from typing import Any


def get_api_base_url() -> str:
    """
    Reads API_BASE_URL from environment.
    - Single-process mode (default): Streamlit + FastAPI share port 8501 via asgi.py
    - Docker: same container, defaults to http://localhost:8501
    - Override: set API_BASE_URL env var for external API access
    """
    return os.getenv("API_BASE_URL", "http://localhost:8501").rstrip("/")


def api_request(
    method: str,
    endpoint: str,
    **kwargs: Any,
) -> dict | list | None:
    """
    Make a request to the FastAPI backend.

    Args:
        method:   HTTP method ("GET", "POST", "PUT", "DELETE")
        endpoint: Path starting with "/" (e.g. "/calcs/hydrostatic-pressure")
        **kwargs: Passed directly to httpx.request (json=, params=, etc.)

    Returns:
        Parsed JSON response, or None on network failure.

    Raises:
        httpx.HTTPStatusError for non-2xx responses (caller handles).
    """
    url = f"{get_api_base_url()}/api{endpoint}"
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.request(method.upper(), url, **kwargs)
            response.raise_for_status()
            return response.json()
    except httpx.ConnectError:
        st.error(
            f"Cannot connect to the Rig Tools API at `{get_api_base_url()}`. "
            "Make sure the API service is running."
        )
        return None
    except httpx.HTTPStatusError as e:
        st.error(f"API error {e.response.status_code}: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"Unexpected error calling API: {e}")
        return None


# --- Convenience wrappers ---

def calc_hydrostatic_pressure(mud_weight: float, depth: float, unit_system: str = "us") -> dict | None:
    return api_request("POST", "/calcs/hydrostatic-pressure", json={
        "mud_weight": mud_weight,
        "depth": depth,
        "unit_system": unit_system,
    })


# ---------------------------------------------------------------------------
# Project wrappers — mirrors session-state store in data/project_store.py
# Migrate pages to these when Supabase DB is wired.
# ---------------------------------------------------------------------------

@st.cache_data(ttl=60)
def list_projects() -> list | None:
    return api_request("GET", "/projects")


def create_project_api(name: str, project_type: str = "single") -> dict | None:
    result = api_request("POST", "/projects", json={"project_name": name, "project_type": project_type})
    if result:
        list_projects.clear()
    return result


@st.cache_data(ttl=60)
def get_project_api(project_id: str) -> dict | None:
    return api_request("GET", f"/projects/{project_id}")


def update_project_api(project_id: str, name: str | None = None, project_type: str | None = None) -> dict | None:
    payload = {k: v for k, v in {"project_name": name, "project_type": project_type}.items() if v is not None}
    result = api_request("PUT", f"/projects/{project_id}", json=payload)
    if result:
        list_projects.clear()
        get_project_api.clear()
    return result


def delete_project_api(project_id: str) -> bool:
    result = api_request("DELETE", f"/projects/{project_id}")
    if result is not None:
        list_projects.clear()
        get_project_api.clear()
    return result is not None


def add_well_api(project_id: str, well_name: str) -> dict | None:
    result = api_request("POST", f"/projects/{project_id}/wells", json={"well_name": well_name})
    if result:
        get_project_api.clear()
    return result


def update_well_api(project_id: str, well_id: str, data: dict) -> dict | None:
    result = api_request("PUT", f"/projects/{project_id}/wells/{well_id}", json=data)
    if result:
        get_project_api.clear()
    return result


def delete_well_api(project_id: str, well_id: str) -> bool:
    result = api_request("DELETE", f"/projects/{project_id}/wells/{well_id}")
    if result is not None:
        get_project_api.clear()
    return result is not None


def calc_emw(pressure: float, depth: float, unit_system: str = "us") -> dict | None:
    return api_request("POST", "/calcs/equivalent-mud-weight", json={
        "pressure": pressure,
        "depth": depth,
        "unit_system": unit_system,
    })


def calc_kill_sheet(
    sidpp: float,
    current_mud_weight: float,
    depth: float,
    unit_system: str = "us",
) -> dict | None:
    return api_request("POST", "/calcs/kill-sheet", json={
        "shut_in_drillpipe_pressure": sidpp,
        "current_mud_weight": current_mud_weight,
        "depth": depth,
        "unit_system": unit_system,
    })


def calc_annular_velocity(
    flow_rate: float,
    hole_diameter: float,
    pipe_od: float,
    unit_system: str = "us",
) -> dict | None:
    return api_request("POST", "/calcs/annular-velocity", json={
        "flow_rate": flow_rate,
        "hole_diameter": hole_diameter,
        "pipe_od": pipe_od,
        "unit_system": unit_system,
    })


def api_health() -> bool:
    """Returns True if the API is reachable and healthy."""
    result = api_request("GET", "/health")
    return result is not None and result.get("status") == "ok"
