import streamlit as st
import sys
import getpass
from pathlib import Path

def init_global():
    st.session_state.setdefault("unit_system", "us")
    st.session_state.setdefault(
        "parameters", {
            "value_a": 10.0,
            "value_b": 5.0
        }
    )

    st.session_state.setdefault("project_root", Path(__file__).resolve().parent.parent)
    if str(st.session_state.project_root) not in sys.path:
        sys.path.insert(0, str(st.session_state.project_root))

    try:
        current_user = getpass.getuser()
    except Exception:
        current_user = "unknown"

    st.session_state.setdefault("current_user", current_user)
    st.session_state.setdefault("projects", {})
    st.session_state.setdefault("active_project_id", None)
    st.session_state.setdefault("active_well_id", None)
