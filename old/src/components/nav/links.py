"""Top-level navigation definition using st.navigation with position='top'.

All pages that must be reachable (even via st.switch_page) are registered here.
Produced by: orchestrator.
"""
import streamlit as st


def nav_links():
    pages = {
        "Main": [
            st.Page("src/_pages/01_home.py", title="Home", icon=":material/home:", default=True),
        ],
        "Projects": [
            st.Page("src/_pages/03_projects.py", title="My Projects", icon=":material/folder:"),
            st.Page("src/_pages/04_project.py", title="Project", icon=":material/construction:"),
            st.Page("src/_pages/05_well.py", title="Well", icon=":material/water_drop:"),
        ],
        "Tools": [
            st.Page("src/_pages/02_digital_stamp.py", title="Digital Stamp", icon=":material/approval:"),
            st.Page("src/_pages/07_planner.py", title="Planner", icon=":material/event:"),
        ],
        "Account": [
            st.Page("src/_pages/06_settings.py", title="Settings", icon=":material/settings:"),
        ],
    }

    nav = st.navigation(pages, position="top")
    return nav
