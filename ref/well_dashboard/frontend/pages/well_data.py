"""
Well Data Page — 🔧 Well Data Tab

Displays a well picker for the current project and then renders the full
well-detail view broken into sub-tabs:

    📋 Header    Basic info and depth table
    🕳️ Wellbore  Hole sections (plan / actual)
    🔧 Casing    Casing strings (plan / actual)
    ⚙️ Tubulars  Drill string components (plan / actual)
    🧭 Survey    Directional stations + Plotly visualisation

Each sub-tab section is a private function below, keeping this file
self-contained yet clearly segmented.
"""

import streamlit as st
import pandas as pd

from frontend.api_client import api_request
from frontend.components.data_table import render_data_table
from frontend.components.status_badge import status_badge, show_status_selector
from frontend.components.survey_chart import render_survey_charts
from frontend.components.well_form import show_create_well_form


def well_data_page() -> None:
    """Render the full Well Data page."""
    st.markdown(
        "<p style='font-size:1.5rem;font-weight:bold;color:#4472c4;"
        "border-bottom:2px solid #4472c4;padding-bottom:4px;'>🔧 Well Data Management</p>",
        unsafe_allow_html=True,
    )

    if not st.session_state.get("current_project"):
        st.warning("Please open a project from the 📋 Projects tab first.")
        return

    project = api_request("GET", f"/api/projects/{st.session_state['current_project']}")
    if not project:
        st.error("Project not found.")
        return

    st.write(f"**Project:** {project['project_name']}")
    wells = api_request("GET", f"/api/projects/{project['id']}/wells") or []

    if not wells:
        st.info("No wells yet.")
        show_create_well_form(project["id"])
        return

    # ── Well selector ─────────────────────────────────────────────────────────
    col_picker, col_add = st.columns([4, 1])
    with col_picker:
        well_options = [(w["id"], f"{w['well_name']} ({w['current_status']})") for w in wells]
        selected = st.selectbox("Select Well", options=well_options, format_func=lambda x: x[1])
        if selected:
            st.session_state["current_well"] = selected[0]

    with col_add:
        st.write("")  # vertical spacer
        if st.button("➕ New Well", use_container_width=True):
            st.session_state["current_well"] = None
            st.rerun()

    if not st.session_state.get("current_well"):
        show_create_well_form(project["id"])
        return

    # ── Well detail view ──────────────────────────────────────────────────────
    _show_well_detail(st.session_state["current_well"])


# ── Well detail ────────────────────────────────────────────────────────────────

def _show_well_detail(well_id: int) -> None:
    well = api_request("GET", f"/api/wells/{well_id}")
    if not well:
        st.error("Well not found.")
        return

    # Header metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"**Well:** {well['well_name']}")
    c2.markdown(f"**Status:** {status_badge(well['current_status'])}", unsafe_allow_html=True)
    if well.get("measured_depth_planned"):
        c3.metric("Planned MD", f"{well['measured_depth_planned']:,.0f} ft")
    if well.get("measured_depth_actual"):
        c4.metric("Actual MD", f"{well['measured_depth_actual']:,.0f} ft")

    # Action bar
    _action_bar(well)

    # Sub-tabs
    tabs = st.tabs(["📋 Header", "🕳️ Wellbore", "🔧 Casing", "⚙️ Tubulars", "🧭 Survey"])
    with tabs[0]: _header_tab(well)
    with tabs[1]: _wellbore_tab(well_id, well)
    with tabs[2]: _casing_tab(well_id, well)
    with tabs[3]: _tubular_tab(well_id, well)
    with tabs[4]: _survey_tab(well_id, well)


def _action_bar(well: dict) -> None:
    """Export, status update, and delete controls."""
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("📥 Export Well", use_container_width=True):
            result = api_request("POST", f"/api/export/well/{well['id']}")
            if result:
                st.success(f"Exported: {result['filename']}")

    with c2:
        new_status = show_status_selector(well["current_status"], key=f"status_{well['id']}")
        if new_status != well["current_status"]:
            if st.button("Update Status", use_container_width=True):
                api_request("POST", f"/api/wells/{well['id']}/status",
                            json={"new_status": new_status})
                st.success(f"Status → {new_status}")
                st.rerun()

    with c3:
        if st.button("🗑️ Delete Well", use_container_width=True):
            if st.checkbox("Confirm delete?", key=f"confirm_del_well_{well['id']}"):
                api_request("DELETE", f"/api/wells/{well['id']}")
                st.success("Well deleted.")
                st.session_state["current_well"] = None
                st.rerun()


# ── Sub-tab helpers ────────────────────────────────────────────────────────────

def _header_tab(well: dict) -> None:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Basic Information")
        render_data_table([{
            "Field":      k,
            "Value":      well.get(v) or "N/A",
        } for k, v in [
            ("Well Name",  "well_name"),
            ("Well Number","well_number"),
            ("API Number", "api_number"),
            ("Well Type",  "well_type"),
            ("Rig Name",   "rig_name"),
            ("Contractor", "contractor"),
        ]])

    with c2:
        st.markdown("##### Depth Information")
        render_data_table([{
            "Type":    t,
            "Planned": _fmt_depth(well.get(pk)),
            "Actual":  _fmt_depth(well.get(ak)),
        } for t, pk, ak in [
            ("Total Depth", "total_depth_planned", "total_depth_actual"),
            ("Meas. Depth", "measured_depth_planned", "measured_depth_actual"),
            ("TVD",         "true_vertical_depth_planned", "true_vertical_depth_actual"),
        ]])


def _fmt_depth(v) -> str:
    return f"{v:,.0f} ft" if v else "N/A"


def _wellbore_tab(well_id: int, well: dict) -> None:
    st.markdown("#### Wellbore Sections")
    plan_tab, actual_tab = st.tabs(["📋 Plan", "✅ Actual"])

    with plan_tab:
        render_data_table(well.get("wellbore_plan", []), empty_msg="No planned wellbore sections.")
        with st.expander("➕ Add Planned Section"):
            _wellbore_form(well_id, is_plan=True)

    with actual_tab:
        render_data_table(well.get("wellbore_actual", []), empty_msg="No actual wellbore sections.")
        with st.expander("➕ Add Actual Section"):
            _wellbore_form(well_id, is_plan=False)


def _wellbore_form(well_id: int, is_plan: bool) -> None:
    key = "plan" if is_plan else "actual"
    with st.form(f"wellbore_{key}_{well_id}"):
        c1, c2 = st.columns(2)
        section_name = c1.text_input("Section Name")
        section_type = c2.selectbox("Type", ["surface", "intermediate", "production", "other"])
        top_md    = c1.number_input("Top MD (ft)",    value=0.0, step=10.0)
        bottom_md = c2.number_input("Bottom MD (ft)", value=0.0, step=10.0)
        hole_size = c1.number_input("Hole Size (in)", value=0.0, step=0.5)
        mud_weight = c2.number_input("Mud Weight (ppg)", value=0.0, step=0.1)
        mud_type  = st.text_input("Mud Type")

        if st.form_submit_button("Add Section"):
            api_request("POST", f"/api/wells/{well_id}/wellbore", json={
                "section_name": section_name, "section_type": section_type,
                "top_md": top_md, "bottom_md": bottom_md,
                "hole_size": hole_size, "mud_weight": mud_weight,
                "mud_type": mud_type, "is_plan": is_plan,
            })
            st.success("Section added.")
            st.rerun()


def _casing_tab(well_id: int, well: dict) -> None:
    st.markdown("#### Casing Strings")
    plan_tab, actual_tab = st.tabs(["📋 Plan", "✅ Actual"])

    with plan_tab:
        render_data_table(well.get("casing_plan", []), empty_msg="No planned casing.")
        with st.expander("➕ Add Planned Casing"):
            _casing_form(well_id, is_plan=True)

    with actual_tab:
        render_data_table(well.get("casing_actual", []), empty_msg="No actual casing.")
        with st.expander("➕ Add Actual Casing"):
            _casing_form(well_id, is_plan=False)


def _casing_form(well_id: int, is_plan: bool) -> None:
    key = "plan" if is_plan else "actual"
    with st.form(f"casing_{key}_{well_id}"):
        c1, c2 = st.columns(2)
        string_name = c1.text_input("String Name")
        string_type = c2.selectbox("Type", ["conductor", "surface", "intermediate", "production", "liner"])
        top_md    = c1.number_input("Top MD (ft)",    value=0.0)
        bottom_md = c2.number_input("Bottom MD (ft)", value=0.0)
        casing_od = c1.number_input("OD (in)",  value=0.0)
        casing_id = c2.number_input("ID (in)",  value=0.0)
        weight = c1.number_input("Weight (lb/ft)", value=0.0)
        grade  = c2.text_input("Grade")

        if st.form_submit_button("Add Casing"):
            api_request("POST", f"/api/wells/{well_id}/casing", json={
                "string_name": string_name, "string_type": string_type,
                "top_md": top_md, "bottom_md": bottom_md,
                "casing_od": casing_od, "casing_id": casing_id,
                "weight": weight, "grade": grade, "is_plan": is_plan,
            })
            st.success("Casing added.")
            st.rerun()


def _tubular_tab(well_id: int, well: dict) -> None:
    st.markdown("#### Tubular Strings")
    plan_tab, actual_tab = st.tabs(["📋 Plan", "✅ Actual"])
    with plan_tab:
        render_data_table(well.get("tubular_plan", []), empty_msg="No planned tubulars.")
    with actual_tab:
        render_data_table(well.get("tubular_actual", []), empty_msg="No actual tubulars.")


def _survey_tab(well_id: int, well: dict) -> None:
    st.markdown("#### Directional Survey")
    plan_tab, actual_tab, viz_tab = st.tabs(["📋 Plan", "✅ Actual", "📊 Visualisation"])

    with plan_tab:
        render_data_table(well.get("survey_plan", []), empty_msg="No planned survey stations.")
    with actual_tab:
        render_data_table(well.get("survey_actual", []), empty_msg="No actual survey stations.")
    with viz_tab:
        render_survey_charts(well.get("survey_plan", []), well.get("survey_actual", []))
