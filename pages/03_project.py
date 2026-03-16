import streamlit as st
from components.comp_page_layout import (
    page_header, sidebar_header, horizontal_rule
)
from utils.project_store import (
    get_project, create_well, delete_well, update_well,
    export_project_json,
)
from data.well_template import apply_template

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Project",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Guard — must have an active project
# ---------------------------------------------------------------------------
project_id = st.session_state.get("active_project_id")
project = get_project(project_id) if project_id else None

if project is None:
    st.warning("No project selected. Please open a project from the Home page.")
    if st.button(":material/home: Go to Projects"):
        st.switch_page("pages/01_home.py")
    st.stop()

# ---------------------------------------------------------------------------
# Session state — add-well wizard
# ---------------------------------------------------------------------------
if "add_well_step" not in st.session_state:
    st.session_state.add_well_step = 0
if "add_well_name" not in st.session_state:
    st.session_state.add_well_name = ""
if "confirm_delete_well" not in st.session_state:
    st.session_state.confirm_delete_well = None

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Rig Tools", icon=":material/handyman:")
    type_label = "Single Well" if project.project_type == "single" else "Pad"
    st.markdown(f"**{project.project_name}**")
    st.caption(f":material/category: {type_label}")
    st.caption(f":material/person: Created by {project.created_by}")
    st.caption(f":material/schedule: Modified {project.modified_at[:10]}")
    horizontal_rule()
    st.caption(f":material/person: {st.session_state.get('current_user', 'unknown')}")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
page_header(project.project_name, ":material/folder_open:")

# Back + download bar
col_back, col_dl, col_spacer = st.columns([0.12, 0.15, 0.73])
with col_back:
    if st.button(":material/arrow_back: Projects", use_container_width=True):
        st.switch_page("pages/01_home.py")
with col_dl:
    json_data = export_project_json(project_id)
    if json_data:
        file_name = f"{project.project_name.replace(' ', '_')}.json"
        st.download_button(
            label=":material/download: Export JSON",
            data=json_data,
            file_name=file_name,
            mime="application/json",
            use_container_width=True,
        )

horizontal_rule()

# ---- Add Well button ------------------------------------------------------
col_wells_hdr, col_add_btn = st.columns([0.80, 0.20])
with col_wells_hdr:
    st.markdown("### Wells")
with col_add_btn:
    if st.button(":material/add: Add Well", type="primary", use_container_width=True):
        st.session_state.add_well_step = 1

# ---- Add-well wizard -------------------------------------------------------
if st.session_state.add_well_step == 1:
    with st.container(border=True):
        st.markdown("**Add Well — Step 1 of 2**")
        well_name_input = st.text_input("Well Name", value=st.session_state.add_well_name, key="_new_well_name")
        col_next, col_cancel = st.columns([0.15, 0.85])
        with col_next:
            if st.button("Next →", type="primary", use_container_width=True, key="aw_next"):
                if well_name_input.strip():
                    st.session_state.add_well_name = well_name_input.strip()
                    st.session_state.add_well_step = 2
                else:
                    st.warning("Please enter a well name.")
        with col_cancel:
            if st.button("Cancel", use_container_width=True, key="aw_cancel"):
                st.session_state.add_well_step = 0

elif st.session_state.add_well_step == 2:
    with st.container(border=True):
        st.markdown(f"**Add Well — Step 2 of 2** — *{st.session_state.add_well_name}*")
        st.markdown("Start blank or use the default template?")

        col_blank, col_template, col_back_btn = st.columns([0.2, 0.2, 0.60])
        with col_blank:
            if st.button(":material/note_add: Blank", type="secondary", use_container_width=True, key="aw_blank"):
                create_well(project_id, st.session_state.add_well_name)
                st.session_state.add_well_step = 0
                st.session_state.add_well_name = ""
                st.rerun()
        with col_template:
            if st.button(":material/auto_fix_high: Template", type="primary", use_container_width=True, key="aw_template"):
                well = create_well(project_id, st.session_state.add_well_name)
                if well:
                    apply_template(well)
                    update_well(project_id, well)
                st.session_state.add_well_step = 0
                st.session_state.add_well_name = ""
                st.rerun()
        with col_back_btn:
            if st.button("← Back", use_container_width=True, key="aw_back"):
                st.session_state.add_well_step = 1

# ---- Well list ------------------------------------------------------------
project = get_project(project_id)  # re-fetch after any mutations

if not project.wells:
    st.info("No wells yet. Click **Add Well** to get started.")
else:
    for well in project.wells:
        modified = well.modified_at[:10] if well.modified_at else "—"
        wb_count = len(well.wellbores)
        casing_count = len(well.casings)
        mud_count = len(well.mud_entries)

        with st.container(border=True):
            cols = st.columns([0.40, 0.12, 0.12, 0.12, 0.14, 0.10])
            with cols[0]:
                st.markdown(f"**{well.well_name}**")
                st.caption(f"modified {modified}")
            with cols[1]:
                st.caption(f":material/water: {wb_count} wellbore{'s' if wb_count != 1 else ''}")
            with cols[2]:
                st.caption(f":material/settings: {casing_count} casing/liner")
            with cols[3]:
                st.caption(f":material/opacity: {mud_count} mud entry/entries")
            with cols[4]:
                if st.button("Open", key=f"open_well_{well.well_id}", use_container_width=True, type="primary"):
                    st.session_state.active_well_id = well.well_id
                    st.switch_page("pages/04_well.py")
            with cols[5]:
                if st.session_state.confirm_delete_well == well.well_id:
                    if st.button("Confirm", key=f"confirm_del_{well.well_id}", use_container_width=True):
                        delete_well(project_id, well.well_id)
                        st.session_state.confirm_delete_well = None
                        st.rerun()
                else:
                    if st.button(":material/delete:", key=f"del_well_{well.well_id}", use_container_width=True, help="Delete well"):
                        st.session_state.confirm_delete_well = well.well_id
                        st.rerun()
