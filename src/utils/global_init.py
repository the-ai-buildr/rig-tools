"""Global initialisation helpers — session state and CSS setup. Produced by: frontend-agent."""
import streamlit as st
from styles.style import apply_custom_css
from pathlib import Path
import sys


# Initialize session state
def init_session_state():
    # Ensure project root is on sys.path first (needed before importing feature modules)
    _project_root = Path(__file__).resolve().parent.parent
    st.session_state.setdefault("project_root", _project_root)
    if str(_project_root) not in sys.path:
        sys.path.insert(0, str(_project_root))

    # Core app keys
    st.session_state.setdefault("unit_system", "us")
    st.session_state.setdefault(
        "parameters", {
            "value_a": 10.0,
            "value_b": 5.0
        }
    )

    # Auth keys — required by CLAUDE.md session state contract
    st.session_state.setdefault("auth_token", None)
    st.session_state.setdefault("auth_refresh_token", None)
    st.session_state.setdefault("auth_user", None)
    st.session_state.setdefault("auth_expires_at", None)

    # Feature modules register their own keys — this is the registry, not the definition site
    from data.project_store import init_project_state
    init_project_state()

    return True


# Initialize global state
def global_init():
    # Initialise session state first so auth keys are always present
    init_session_state()

    # Apply custom CSS globally
    apply_custom_css()

    # Add project root so styles can be imported (needed for Streamlit multipage / Pyodide)
    _project_root = Path(__file__).resolve().parent.parent
    if str(_project_root) not in sys.path:
        sys.path.insert(0, str(_project_root))

    return True
