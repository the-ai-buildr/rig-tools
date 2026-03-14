"""
HTTP client for Streamlit → FastAPI communication.

Usage:
    from frontend.api_client import api_request, get_api_base_url

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
    - Docker: set to http://api:8000 via docker-compose
    - Local dev: defaults to http://localhost:8000
    """
    return os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


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
