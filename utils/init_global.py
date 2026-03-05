import streamlit as st
import sys
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
