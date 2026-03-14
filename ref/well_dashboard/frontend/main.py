"""
Well Dashboard — Streamlit Entry Point

This file is the only file Streamlit needs to know about:
    streamlit run frontend/main.py

Responsibilities:
    1. Configure the Streamlit page
    2. Gate on authentication (show login if not authenticated)
    3. Render navigation (top tabs + sidebar)
    4. Delegate each tab to its page module

To add a new top-level tab:
    1. Create frontend/pages/my_page.py with a my_page() function
    2. Add the tab label in frontend/components/navigation.py > TABS
    3. Add a ``with tabs[N]:`` block below calling your page function
"""

import streamlit as st

from frontend.api_client import is_authenticated
from frontend.components.auth import show_login_page, show_logout_button
from frontend.components.navigation import show_top_nav, show_sidebar

from frontend.pages.projects  import projects_page
from frontend.pages.well_data import well_data_page
from frontend.pages.templates import templates_page
from frontend.pages.reports   import reports_page
from frontend.pages.settings  import settings_page


# ── Page configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Well Dashboard",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Minimal global CSS — component-level styling lives inside each component
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    div[data-testid="metric-container"] { background: #f8f9fa; border-radius: 6px; padding: 0.5rem; }
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ─────────────────────────────────────────────────────
st.session_state.setdefault("current_project", None)
st.session_state.setdefault("current_well", None)


# ── Authentication gate ────────────────────────────────────────────────────────
if not is_authenticated():
    show_login_page()
    st.stop()


# ── Sidebar ────────────────────────────────────────────────────────────────────
show_sidebar()
show_logout_button()


# ── Main content ───────────────────────────────────────────────────────────────
tabs = show_top_nav()

with tabs[0]:
    projects_page()

with tabs[1]:
    well_data_page()

with tabs[2]:
    templates_page()

with tabs[3]:
    reports_page()

with tabs[4]:
    settings_page()
