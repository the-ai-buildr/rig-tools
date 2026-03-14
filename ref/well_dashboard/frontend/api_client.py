"""
API Client — Frontend Utility

Provides a single ``api_request()`` function used by every page and component.
All HTTP communication with the FastAPI backend goes through this module.

Usage:
    from frontend.api_client import api_request

    projects = api_request("GET", "/api/projects")
    result   = api_request("POST", "/api/projects", json={"project_name": "P1"})
"""

import os
import streamlit as st
import httpx

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def api_request(method: str, endpoint: str, **kwargs) -> dict | list | None:
    """
    Make an authenticated HTTP request to the FastAPI backend.

    Args:
        method:    HTTP verb ("GET", "POST", "PUT", "DELETE").
        endpoint:  Path starting with "/" (e.g. "/api/projects").
        **kwargs:  Passed directly to httpx (e.g. ``json=``, ``params=``).

    Returns:
        Parsed JSON response, or ``None`` on failure (error shown via st.error).

    Side effects:
        - Shows an ``st.error`` banner on network or HTTP errors.
        - Triggers logout and page rerun on 401 Unauthorized.
    """
    url = f"{API_BASE_URL}{endpoint}"
    headers = kwargs.pop("headers", {})

    if "token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state['token']}"

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.request(method, url, headers=headers, **kwargs)

            if response.status_code == 401:
                st.error("Session expired — please log in again.")
                _logout()
                st.rerun()
                return None

            response.raise_for_status()
            return response.json() if response.content else None

    except httpx.HTTPStatusError as e:
        st.error(f"API error {e.response.status_code}: {e.response.text}")
        return None
    except httpx.RequestError as e:
        st.error(f"Could not reach the API: {e}")
        return None


def login(username: str, password: str) -> bool:
    """Exchange credentials for a JWT token. Returns True on success."""
    resp = api_request("POST", "/api/auth/login",
                       json={"username": username, "password": password})
    if resp and "access_token" in resp:
        st.session_state["token"] = resp["access_token"]
        st.session_state["user"] = resp["user"]
        return True
    return False


def _logout() -> None:
    for key in ("token", "user", "current_project", "current_well"):
        st.session_state.pop(key, None)


def logout() -> None:
    """Clear session state and force re-render to login screen."""
    _logout()


def is_authenticated() -> bool:
    return "token" in st.session_state


def get_current_user() -> dict:
    return st.session_state.get("user", {})
