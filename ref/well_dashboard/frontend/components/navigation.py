"""
Navigation Component

Provides:
    show_top_nav()  Main header + tab bar; returns (tabs, page_names)
    show_sidebar()  Left sidebar with quick-actions and filters

Usage:
    from frontend.components.navigation import show_top_nav, show_sidebar

    tabs = show_top_nav()
    show_sidebar()

    with tabs[0]:
        projects_page()
"""

import streamlit as st


# Tab definitions — (label, page_key) pairs.
# To add a new top-level tab, append an entry here and add a handler in main.py.
TABS = [
    ("📋 Projects",   "projects"),
    ("🔧 Well Data",  "well_data"),
    ("📐 Templates",  "templates"),
    ("📊 Reports",    "reports"),
    ("⚙️ Settings",   "settings"),
]


def show_top_nav():
    """
    Render the page header and the horizontal tab bar.

    Returns:
        A list of Streamlit tab context managers in the same order as TABS.
    """
    st.markdown(
        "<p style='font-size:2.2rem;font-weight:bold;color:#1f4e79;margin-bottom:0.5rem;'>"
        "🛢️ Well Dashboard</p>",
        unsafe_allow_html=True,
    )
    return st.tabs([label for label, _ in TABS])


def show_sidebar() -> None:
    """
    Render the application sidebar:

    - Quick-action buttons (New Project / New Well)
    - Project and status filter controls
    - Recent exports list (fetched live from the API)
    """
    st.sidebar.markdown("## 🔍 Filters & Actions")

    # ── Quick actions ─────────────────────────────────────────────────────────
    st.sidebar.markdown("### Quick Actions")

    if st.sidebar.button("➕ New Project", use_container_width=True):
        st.session_state["current_project"] = None
        st.session_state["current_well"] = None
        st.rerun()

    if st.session_state.get("current_project"):
        if st.sidebar.button("➕ New Well", use_container_width=True):
            st.session_state["current_well"] = None
            st.rerun()

    st.sidebar.markdown("---")

    # ── Recent exports ────────────────────────────────────────────────────────
    from frontend.api_client import api_request
    export_files = api_request("GET", "/api/export/files") or []

    if export_files:
        st.sidebar.markdown("### 📥 Recent Exports")
        for f in export_files[:5]:
            col_a, col_b = st.sidebar.columns([3, 1])
            col_a.caption(f["filename"][:28] + ("…" if len(f["filename"]) > 28 else ""))
            col_b.markdown(
                f"[⬇]({f'/api/export/download/{f[\"filename\"]}'})",
                unsafe_allow_html=True,
            )

    st.sidebar.markdown("---")
