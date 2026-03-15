import streamlit as st
from utils.global_init import global_init, init_session_state

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
        page_title="Rig Tools",
        layout="wide",
        initial_sidebar_state="expanded",
    )

# ---------------------------------------------------------------------------
# Global init
# ---------------------------------------------------------------------------
is_global_loaded = global_init()
is_session_state_loaded = init_session_state()

# ---------------------------------------------------------------------------
# Redirect to Home page
# ---------------------------------------------------------------------------
if is_global_loaded and is_session_state_loaded:
    st.switch_page("pages/01_home.py")
