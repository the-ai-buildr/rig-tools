""" Projects list page — create/upload wizard + project cards.

    Wizard flow (project_wizard_step):
    0 — idle: project cards + action buttons
    1 — mode select: Create New | Upload Existing
    2 — data entry: name/type form (create) | file upload + preview (upload)
    3 — review & confirm: read-only summary → navigate

    After confirm:
    single → auto-create first well → pages/05_well.py
    pad    → pages/04_project.py

    Produced by: frontend-agent
"""
import streamlit as st
from utils.global_init import global_init
from components.layout import page_header, sidebar_header, horizontal_rule
from data.project_store import (
    get_all_projects,
    create_project,
    delete_project,
    create_well,
    export_project_json,
    import_project_from_json,
    _reset_wizard,
)

global_init()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Rig Tools", icon=":material/handyman:")
    horizontal_rule()
    st.caption("Made with ❤️ by [The Ai Buildr](https://github.com/the-ai-buildr)", text_alignment="center")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _type_label(pt: str) -> str:
    return "Single Well" if pt == "single" else "Pad"


def _navigate_after_confirm(project_id: str, project_type: str):
    """Post-confirm routing based on project type."""
    st.session_state["active_project_id"] = project_id
    st.session_state["active_well_id"] = None
    _reset_wizard()
    if project_type == "single":
        well = create_well(project_id, "Well 1")
        if well:
            st.session_state["active_well_id"] = well.well_id
        st.switch_page("src/pages/05_well.py")
    else:
        st.switch_page("src/pages/04_project.py")


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
page_header("Projects", ":material/folder:")

# ---------------------------------------------------------------------------
# Wizard — steps 1-3 rendered above the project list
# ---------------------------------------------------------------------------
step = st.session_state["project_wizard_step"]

if step == 0:
    col_new, col_upload, col_spacer = st.columns([0.20, 0.20, 0.60])
    with col_new:
        if st.button(":material/add: New Project", type="primary", use_container_width=True):
            st.session_state["project_wizard_step"] = 1
            st.session_state["project_wizard_mode"] = "create"
            st.rerun()
    with col_upload:
        if st.button(":material/upload: Upload Project", use_container_width=True):
            st.session_state["project_wizard_step"] = 1
            st.session_state["project_wizard_mode"] = "upload"
            st.rerun()

elif step == 1:
    with st.container(border=True):
        st.markdown("**Step 1 of 3 — Choose action**")
        col_create, col_upload, col_cancel = st.columns([0.2, 0.2, 0.6])
        with col_create:
            if st.button(":material/note_add: Create New", type="primary", use_container_width=True):
                st.session_state["project_wizard_mode"] = "create"
                st.session_state["project_wizard_step"] = 2
                st.rerun()
        with col_upload:
            if st.button(":material/upload_file: Upload Existing", use_container_width=True):
                st.session_state["project_wizard_mode"] = "upload"
                st.session_state["project_wizard_step"] = 2
                st.rerun()
        with col_cancel:
            if st.button("Cancel", use_container_width=True):
                _reset_wizard()
                st.rerun()

elif step == 2:
    mode = st.session_state["project_wizard_mode"]
    with st.container(border=True):
        st.markdown(f"**Step 2 of 3 — {'Project Details' if mode == 'create' else 'Upload File'}**")

        if mode == "create":
            name_input = st.text_input("Project Name", value=st.session_state["project_wizard_name"], key="_wiz_name")
            type_input = st.selectbox(
                "Project Type",
                options=["single", "pad"],
                format_func=_type_label,
                index=0 if st.session_state["project_wizard_type"] == "single" else 1,
                key="_wiz_type",
            )
            col_next, col_back, col_cancel = st.columns([0.15, 0.15, 0.70])
            with col_next:
                if st.button("Next →", type="primary", use_container_width=True):
                    if not name_input.strip():
                        st.warning("Project name is required.")
                    else:
                        st.session_state["project_wizard_name"] = name_input.strip()
                        st.session_state["project_wizard_type"] = type_input
                        st.session_state["project_wizard_step"] = 3
                        st.rerun()
            with col_back:
                if st.button("← Back", use_container_width=True):
                    st.session_state["project_wizard_step"] = 1
                    st.rerun()
            with col_cancel:
                if st.button("Cancel", use_container_width=True):
                    _reset_wizard()
                    st.rerun()

        else:  # upload
            uploaded = st.file_uploader("Select project JSON file", type=["json"], key="_wiz_upload")
            preview_error = None
            if uploaded is not None:
                try:
                    raw = uploaded.read().decode("utf-8")
                    parsed = import_project_from_json.__wrapped__(raw) if hasattr(import_project_from_json, "__wrapped__") else None
                    # Parse without committing to store
                    import json as _json
                    from data.models import project_from_dict
                    parsed_dict = _json.loads(raw)
                    parsed_proj = project_from_dict(parsed_dict)
                    st.session_state["project_wizard_import_data"] = parsed_dict
                    st.session_state["project_wizard_name"] = parsed_proj.project_name
                    st.session_state["project_wizard_type"] = parsed_proj.project_type
                    st.info(
                        f"**{parsed_proj.project_name}** · {_type_label(parsed_proj.project_type)} · "
                        f"{len(parsed_proj.wells)} well(s)"
                    )
                except Exception as exc:
                    preview_error = str(exc)
                    st.error(f"Invalid project file: {exc}")

            col_next, col_back, col_cancel = st.columns([0.15, 0.15, 0.70])
            with col_next:
                if st.button("Next →", type="primary", use_container_width=True):
                    if st.session_state["project_wizard_import_data"] is None:
                        st.warning("Please select a valid JSON file.")
                    elif not preview_error:
                        st.session_state["project_wizard_step"] = 3
                        st.rerun()
            with col_back:
                if st.button("← Back", use_container_width=True):
                    st.session_state["project_wizard_step"] = 1
                    st.rerun()
            with col_cancel:
                if st.button("Cancel", use_container_width=True):
                    _reset_wizard()
                    st.rerun()

elif step == 3:
    mode = st.session_state["project_wizard_mode"]
    wiz_name = st.session_state["project_wizard_name"]
    wiz_type = st.session_state["project_wizard_type"]
    import_data = st.session_state["project_wizard_import_data"]
    well_count = len(import_data.get("wells", [])) if import_data else 0

    with st.container(border=True):
        st.markdown("**Step 3 of 3 — Review & Confirm**")
        st.markdown(f"**Name:** {wiz_name}")
        st.markdown(f"**Type:** {_type_label(wiz_type)}")
        if mode == "upload":
            st.markdown(f"**Wells:** {well_count}")

        col_confirm, col_back, col_cancel = st.columns([0.25, 0.15, 0.60])
        confirm_label = ":material/check: Import Project" if mode == "upload" else ":material/check: Create Project"

        with col_confirm:
            if st.button(confirm_label, type="primary", use_container_width=True):
                if mode == "create":
                    project = create_project(wiz_name, wiz_type)
                    _navigate_after_confirm(project.project_id, project.project_type)
                else:
                    import json as _json
                    from data.project_store import import_project_from_json
                    project = import_project_from_json(_json.dumps(import_data))
                    if project:
                        _navigate_after_confirm(project.project_id, project.project_type)
                    else:
                        st.error("Failed to import project.")

        with col_back:
            if st.button("← Back", use_container_width=True):
                st.session_state["project_wizard_step"] = 2
                st.rerun()
        with col_cancel:
            if st.button("Cancel", use_container_width=True):
                _reset_wizard()
                st.rerun()

horizontal_rule()

# ---------------------------------------------------------------------------
# Project list (always visible below the wizard)
# ---------------------------------------------------------------------------
projects = get_all_projects()

if not projects:
    st.info("No projects yet. Click **New Project** to get started.")
else:
    st.markdown("### Your Projects")
    for project in projects:
        modified = project.modified_at[:10] if project.modified_at else "—"
        well_count = len(project.wells)
        type_label = _type_label(project.project_type)

        with st.container(border=True):
            cols = st.columns([0.40, 0.12, 0.12, 0.16, 0.10, 0.10])
            with cols[0]:
                st.markdown(f"**{project.project_name}**")
                st.caption(f"modified {modified} · by {project.created_by}")
            with cols[1]:
                st.caption(f":material/category: {type_label}")
            with cols[2]:
                st.caption(f":material/oil_barrel: {well_count} well{'s' if well_count != 1 else ''}")
            with cols[3]:
                json_data = export_project_json(project.project_id)
                if json_data:
                    fname = f"{project.project_name.replace(' ', '_')}.json"
                    st.download_button(
                        label=":material/download:",
                        data=json_data,
                        file_name=fname,
                        mime="application/json",
                        use_container_width=True,
                        key=f"dl_{project.project_id}",
                        help="Download project as JSON",
                    )
            with cols[4]:
                if st.button("Open", key=f"open_{project.project_id}", use_container_width=True, type="primary"):
                    st.session_state["active_project_id"] = project.project_id
                    st.session_state["active_well_id"] = None
                    if project.project_type == "single":
                        # Single well — navigate to first well directly
                        if project.wells:
                            st.session_state["active_well_id"] = project.wells[0].well_id
                        st.switch_page("src/pages/05_well.py")
                    else:
                        st.switch_page("src/pages/04_project.py")
            with cols[5]:
                confirm_key = f"confirm_del_{project.project_id}"
                if st.session_state.get(confirm_key):
                    if st.button(":material/check:", key=f"do_del_{project.project_id}", use_container_width=True, help="Confirm delete"):
                        delete_project(project.project_id)
                        st.session_state[confirm_key] = False
                        st.rerun()
                else:
                    if st.button(":material/delete:", key=f"del_{project.project_id}", use_container_width=True, help="Delete project"):
                        st.session_state[confirm_key] = True
                        st.rerun()
