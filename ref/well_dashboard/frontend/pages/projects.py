"""
Projects Page — 📋 Projects Tab

Displays all projects for the current user and provides a form to create
new ones. Clicking "Open" on a project sets ``st.session_state['current_project']``
so the Well Data tab can scope its content to that project.
"""

import streamlit as st
from frontend.api_client import api_request
from frontend.components.well_form import show_create_well_form


def projects_page() -> None:
    """Render the full Projects page."""
    st.markdown(
        "<p style='font-size:1.5rem;font-weight:bold;color:#4472c4;"
        "border-bottom:2px solid #4472c4;padding-bottom:4px;'>📋 Project Management</p>",
        unsafe_allow_html=True,
    )

    col_list, col_form = st.columns([2, 1])

    # ── Project List ──────────────────────────────────────────────────────────
    with col_list:
        st.markdown("### Your Projects")
        projects = api_request("GET", "/api/projects") or []

        if not projects:
            st.info("No projects yet. Use the form on the right to create your first project.")
        else:
            for project in projects:
                _render_project_card(project)

    # ── Create Project Form ───────────────────────────────────────────────────
    with col_form:
        _show_create_project_form()


def _render_project_card(project: dict) -> None:
    """Render a single project card with Open and Delete controls."""
    with st.container():
        st.markdown("<div style='background:#f8f9fa;padding:1rem;border-radius:8px;border:1px solid #dee2e6;margin-bottom:0.75rem;'>", unsafe_allow_html=True)

        icon = "🛢️" if project["project_type"] == "single_well" else "🏭"
        col_info, col_count, col_actions = st.columns([3, 1, 1])

        with col_info:
            st.markdown(f"**{icon} {project['project_name']}**")
            st.caption(f"Type: {project['project_type'].replace('_', ' ').title()}")
            if project.get("pad_name"):
                st.caption(f"Pad: {project['pad_name']}")
            if project.get("field"):
                st.caption(f"Field: {project['field']}")

        with col_count:
            st.metric("Wells", project.get("well_count", 0))

        with col_actions:
            if st.button("📂 Open", key=f"open_proj_{project['id']}"):
                st.session_state["current_project"] = project["id"]
                st.session_state["current_well"] = None
                st.rerun()

            if st.button("🗑️", key=f"del_proj_{project['id']}", help="Delete project"):
                if st.checkbox("Confirm?", key=f"confirm_del_{project['id']}"):
                    api_request("DELETE", f"/api/projects/{project['id']}")
                    st.success("Project deleted.")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


def _show_create_project_form() -> None:
    """Render the new-project creation form."""
    st.markdown("### Create New Project")

    with st.form("new_project_form", clear_on_submit=True):
        project_name = st.text_input("Project Name *")
        project_type = st.selectbox(
            "Project Type *",
            options=["single_well", "pad"],
            format_func=lambda x: "Single Well" if x == "single_well" else "Pad of Wells",
        )
        pad_name = st.text_input("Pad Name (pad projects only)")

        c1, c2 = st.columns(2)
        surface_lat = c1.number_input("Surface Latitude",  value=0.0, format="%.6f")
        surface_lon = c2.number_input("Surface Longitude", value=0.0, format="%.6f")

        field       = st.text_input("Field")
        operator    = st.text_input("Operator")
        description = st.text_area("Description")

        submitted = st.form_submit_button("Create Project", use_container_width=True)

    if submitted:
        if not project_name:
            st.error("Project name is required.")
            return

        payload = {
            "project_name":         project_name,
            "project_type":         project_type,
            "pad_name":             pad_name or None,
            "surface_location_lat": surface_lat or None,
            "surface_location_lon": surface_lon or None,
            "field":                field or None,
            "operator":             operator or None,
            "description":          description or None,
        }
        result = api_request("POST", "/api/projects", json=payload)
        if result:
            st.success(f"Project '{project_name}' created!")
            st.session_state["current_project"] = result["id"]
            st.rerun()
