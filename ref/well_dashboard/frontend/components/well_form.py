"""
Well Form Component

The create-well form is used in two places (Projects page and Well Data page),
so it lives here as a reusable component rather than being duplicated.

Usage:
    from frontend.components.well_form import show_create_well_form

    show_create_well_form(project_id=3)
"""

import streamlit as st
from frontend.api_client import api_request


def show_create_well_form(project_id: int) -> None:
    """
    Render the full create-well form and POST to the API on submission.

    On success, stores the new well's ID in ``st.session_state['current_well']``
    and triggers a rerun so the well-detail view opens immediately.

    Args:
        project_id: ID of the project this well will belong to.
    """
    st.markdown("### ➕ Create New Well")

    # ── Template picker ───────────────────────────────────────────────────────
    templates = api_request("GET", "/api/templates") or []
    template_options = [(None, "No Template")] + [(t["id"], t["template_name"]) for t in templates]
    selected_template = st.selectbox(
        "Apply Template (Optional)",
        options=template_options,
        format_func=lambda x: x[1],
    )

    # ── Form ──────────────────────────────────────────────────────────────────
    with st.form("create_well_form", clear_on_submit=True):
        st.markdown("#### Well Header")

        col1, col2 = st.columns(2)
        with col1:
            well_name  = st.text_input("Well Name *")
            well_num   = st.text_input("Well Number")
            api_number = st.text_input("API Number")
            well_type  = st.selectbox(
                "Well Type",
                ["Oil Producer", "Gas Producer", "Water Injector",
                 "Gas Injector", "Exploration", "Appraisal", "Other"],
            )

        with col2:
            surface_lat = st.number_input("Surface Latitude",  value=0.0, format="%.6f")
            surface_lon = st.number_input("Surface Longitude", value=0.0, format="%.6f")
            rig_name    = st.text_input("Rig Name")
            contractor  = st.text_input("Contractor")

        st.markdown("#### Planned Depths")
        d1, d2, d3 = st.columns(3)
        with d1:
            td_planned  = st.number_input("Total Depth (ft)",    value=0.0, step=100.0)
            md_planned  = st.number_input("Measured Depth (ft)", value=0.0, step=100.0)
        with d2:
            tvd_planned = st.number_input("TVD (ft)",            value=0.0, step=100.0)
            kop         = st.number_input("Kick-Off Point (ft)", value=0.0, step=100.0)
        with d3:
            spud_date = st.date_input("Planned Spud Date", value=None)

        description = st.text_area("Description")

        submitted = st.form_submit_button("Create Well", use_container_width=True)

    # ── Submission ────────────────────────────────────────────────────────────
    if submitted:
        if not well_name:
            st.error("Well name is required.")
            return

        payload = {
            "project_id":               project_id,
            "well_name":                well_name,
            "well_number":              well_num or None,
            "api_number":               api_number or None,
            "well_type":                well_type,
            "surface_lat":              surface_lat or None,
            "surface_lon":              surface_lon or None,
            "rig_name":                 rig_name or None,
            "contractor":               contractor or None,
            "total_depth_planned":      td_planned  or None,
            "measured_depth_planned":   md_planned  or None,
            "true_vertical_depth_planned": tvd_planned or None,
            "kick_off_point":           kop or None,
            "spud_date":                spud_date.isoformat() if spud_date else None,
            "description":              description or None,
            "template_id":              selected_template[0],
        }

        result = api_request("POST", "/api/wells", json=payload)
        if result:
            st.success(f"Well '{well_name}' created!")
            st.session_state["current_well"] = result["id"]
            st.rerun()
