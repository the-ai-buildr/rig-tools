import streamlit as st
import pandas as pd
from textwrap import dedent
from components.comp_page_layout import (
    page_header, nav_menu,
    sidebar_header, horizontal_rule
)
from utils.project_store import (
    get_projects, create_project, delete_project,
    import_project_json,
)
from data.well_template import apply_template
from utils.project_store import create_well

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Home",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Session state — creation wizard step
# ---------------------------------------------------------------------------
if "create_step" not in st.session_state:
    st.session_state.create_step = 0     # 0=hidden, 1=name+type, 2=template choice
if "create_name" not in st.session_state:
    st.session_state.create_name = ""
if "create_type" not in st.session_state:
    st.session_state.create_type = "single"

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Rig Tools", icon=":material/handyman:")

    st.markdown(
        dedent("""
            Rig Tools is a collection of calculators and data tools for Operations
            Supervisors, Rig Managers, and Engineers.

            **GitHub:** [rig-tools](https://github.com/the-ai-buildr/rig-tools)
        """)
    )

    horizontal_rule()

    current_user = st.session_state.get("current_user", "unknown")
    st.caption(f":material/person: **{current_user}**", help="OS user (DB auth coming soon)")
    st.caption("Made with ❤️ by [The Ai Buildr](https://github.com/the-ai-buildr)", text_alignment="center")


# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
page_header("Projects", ":material/folder:")

projects = get_projects()

# ---- Action bar -----------------------------------------------------------
col_create, col_import, col_spacer = st.columns([0.15, 0.15, 0.70])

with col_create:
    if st.button(":material/add: New Project", use_container_width=True, type="primary"):
        st.session_state.create_step = 1

with col_import:
    if st.button(":material/upload: Import", use_container_width=True):
        st.session_state.create_step = 99  # special: show uploader


# ---- Creation wizard ------------------------------------------------------
if st.session_state.create_step == 1:
    with st.container(border=True):
        st.markdown("**New Project — Step 1 of 2**")
        c1, c2 = st.columns(2)
        with c1:
            name_input = st.text_input("Project Name", value=st.session_state.create_name, key="_proj_name")
        with c2:
            type_input = st.selectbox(
                "Project Type",
                options=["single", "pad"],
                format_func=lambda x: "Single Well" if x == "single" else "Pad (Multiple Wells)",
                index=0 if st.session_state.create_type == "single" else 1,
                key="_proj_type",
            )
        col_next, col_cancel = st.columns([0.15, 0.85])
        with col_next:
            if st.button("Next →", type="primary", use_container_width=True):
                if name_input.strip():
                    st.session_state.create_name = name_input.strip()
                    st.session_state.create_type = type_input
                    st.session_state.create_step = 2
                else:
                    st.warning("Please enter a project name.")
        with col_cancel:
            if st.button("Cancel", use_container_width=True):
                st.session_state.create_step = 0

elif st.session_state.create_step == 2:
    with st.container(border=True):
        st.markdown(f"**New Project — Step 2 of 2** — *{st.session_state.create_name}*")
        st.markdown("Start with a blank project or use the default well template?")

        col_blank, col_template, col_cancel = st.columns([0.2, 0.2, 0.60])

        with col_blank:
            if st.button(":material/note_add: Start Blank", type="secondary", use_container_width=True):
                create_project(st.session_state.create_name, st.session_state.create_type)
                st.session_state.create_step = 0
                st.session_state.create_name = ""
                st.rerun()

        with col_template:
            if st.button(":material/auto_fix_high: Use Template", type="primary", use_container_width=True):
                project = create_project(st.session_state.create_name, st.session_state.create_type)
                well_name = f"{st.session_state.create_name} Well 1"
                well = create_well(project.project_id, well_name)
                if well:
                    apply_template(well)
                    # persist template changes back into project store
                    from utils.project_store import update_well
                    update_well(project.project_id, well)
                st.session_state.create_step = 0
                st.session_state.create_name = ""
                st.rerun()

        with col_cancel:
            if st.button("← Back", use_container_width=True):
                st.session_state.create_step = 1

elif st.session_state.create_step == 99:
    with st.container(border=True):
        st.markdown("**Import Project from JSON**")
        uploaded = st.file_uploader("Select a .json project file", type=["json"], label_visibility="collapsed")
        if uploaded is not None:
            try:
                json_str = uploaded.read().decode("utf-8")
                imported = import_project_json(json_str)
                st.success(f"Imported: **{imported.project_name}**")
                st.session_state.create_step = 0
                st.rerun()
            except Exception as e:
                st.error(f"Failed to import: {e}")
        if st.button("Cancel"):
            st.session_state.create_step = 0


# ---- Project list ---------------------------------------------------------
horizontal_rule()

if not projects:
    st.info("No projects yet. Click **New Project** to get started.")
else:
    for pid, project in projects.items():
        type_label = "Single Well" if project.project_type == "single" else "Pad"
        well_count = len(project.wells)
        modified = project.modified_at[:10] if project.modified_at else "—"

        with st.container(border=True):
            cols = st.columns([0.40, 0.15, 0.10, 0.15, 0.10, 0.10])
            with cols[0]:
                st.markdown(f"**{project.project_name}**")
                st.caption(f"by {project.created_by} · modified {modified}")
            with cols[1]:
                st.caption(f":material/category: {type_label}")
            with cols[2]:
                st.caption(f":material/oil_barrel: {well_count} well{'s' if well_count != 1 else ''}")
            with cols[3]:
                if st.button("Open", key=f"open_{pid}", use_container_width=True, type="primary"):
                    st.session_state.active_project_id = pid
                    st.switch_page("pages/03_project.py")
            with cols[4]:
                from utils.project_store import export_project_json
                json_data = export_project_json(pid)
                if json_data:
                    file_name = f"{project.project_name.replace(' ', '_')}.json"
                    st.download_button(
                        label="↓",
                        data=json_data,
                        file_name=file_name,
                        mime="application/json",
                        key=f"dl_{pid}",
                        use_container_width=True,
                        help="Download project as JSON",
                    )
            with cols[5]:
                if st.button(":material/delete:", key=f"del_{pid}", use_container_width=True, help="Delete project"):
                    delete_project(pid)
                    st.rerun()
