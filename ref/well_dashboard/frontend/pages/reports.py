"""
Reports Page — 📊 Reports Tab

Provides one-click Excel export for individual wells or entire projects.
"""

import streamlit as st
from frontend.api_client import api_request


def reports_page() -> None:
    """Render the Reports & Exports page."""
    st.markdown(
        "<p style='font-size:1.5rem;font-weight:bold;color:#4472c4;"
        "border-bottom:2px solid #4472c4;padding-bottom:4px;'>📊 Reports & Exports</p>",
        unsafe_allow_html=True,
    )

    projects = api_request("GET", "/api/projects") or []

    if not projects:
        st.info("No projects found. Create a project first.")
        return

    col1, col2 = st.columns(2)

    # ── Project export ────────────────────────────────────────────────────────
    with col1:
        st.markdown("### Export Project")
        proj = st.selectbox(
            "Select Project",
            options=projects,
            format_func=lambda x: x["project_name"],
            key="export_project_picker",
        )
        if proj and st.button("📥 Export Project", use_container_width=True):
            result = api_request("POST", f"/api/export/project/{proj['id']}")
            if result:
                st.success(f"Exported: **{result['filename']}**")
                st.markdown(
                    f"[⬇️ Download]({result['download_url']})",
                    unsafe_allow_html=True,
                )

    # ── Well export ───────────────────────────────────────────────────────────
    with col2:
        st.markdown("### Export Well")
        proj_for_well = st.selectbox(
            "Project",
            options=projects,
            format_func=lambda x: x["project_name"],
            key="export_well_project",
        )
        if proj_for_well:
            wells = api_request("GET", f"/api/projects/{proj_for_well['id']}/wells") or []
            if wells:
                well = st.selectbox(
                    "Select Well",
                    options=wells,
                    format_func=lambda x: x["well_name"],
                )
                if well and st.button("📥 Export Well", use_container_width=True):
                    result = api_request("POST", f"/api/export/well/{well['id']}")
                    if result:
                        st.success(f"Exported: **{result['filename']}**")
                        st.markdown(
                            f"[⬇️ Download]({result['download_url']})",
                            unsafe_allow_html=True,
                        )
            else:
                st.info("No wells in this project yet.")
