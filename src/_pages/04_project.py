"""
Pad project overview page — well list and management for multi-well pad projects.

Guards:
  - active_project_id is None → redirect to 03_projects.py
  - project.project_type == "single" → redirect to 05_well.py (single projects skip this page)

Add-well wizard (inline, 2-step):
  Step 1 — well name input
  Step 2 — blank or template choice

Produced by: frontend-agent
"""
import streamlit as st
from utils.global_init import global_init
from components.layout import page_header, sidebar_header, horizontal_rule
from data.project_store import (
    get_project,
    update_well,
    create_well,
    delete_well,
    export_project_json,
)
from data.well_template import apply_template

global_init()

# ---------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------
project_id = st.session_state.get("active_project_id")
project = get_project(project_id) if project_id else None

if project is None:
    st.warning("No project selected.")
    if st.button(":material/folder: Go to Projects"):
        st.switch_page("src/pages/03_projects.py")
    st.stop()

if project.project_type == "single":
    # Single-well projects never land here
    if project.wells:
        st.session_state["active_well_id"] = project.wells[0].well_id
    st.switch_page("src/pages/05_well.py")

# ---------------------------------------------------------------------------
# Add-well wizard session keys (pad-specific)
# ---------------------------------------------------------------------------
st.session_state.setdefault("pad_add_well_step", 0)
st.session_state.setdefault("pad_add_well_name", "")
st.session_state.setdefault("pad_confirm_delete_well", None)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Rig Tools", icon=":material/handyman:")
    st.markdown(f"**{project.project_name}**")
    st.caption(":material/category: Pad")
    st.caption(f":material/person: {project.created_by}")
    st.caption(f":material/schedule: modified {project.modified_at[:10]}")
    horizontal_rule()
    if st.button(":material/arrow_back: All Projects", use_container_width=True):
        st.switch_page("src/pages/03_projects.py")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
page_header(project.project_name, ":material/folder_open:")

col_back, col_dl, col_spacer = st.columns([0.14, 0.18, 0.68])
with col_back:
    if st.button(":material/arrow_back: Projects", use_container_width=True):
        st.switch_page("src/pages/03_projects.py")
with col_dl:
    json_data = export_project_json(project_id)
    if json_data:
        fname = f"{project.project_name.replace(' ', '_')}.json"
        st.download_button(
            label=":material/download: Export JSON",
            data=json_data,
            file_name=fname,
            mime="application/json",
            use_container_width=True,
        )

horizontal_rule()

# ---- Wells header + Add button -------------------------------------------
col_hdr, col_add = st.columns([0.80, 0.20])
with col_hdr:
    st.markdown("### Wells")
with col_add:
    if st.button(":material/add: Add Well", type="primary", use_container_width=True):
        st.session_state["pad_add_well_step"] = 1
        st.session_state["pad_add_well_name"] = ""
        st.rerun()

# ---- Add-well wizard -------------------------------------------------------
add_step = st.session_state["pad_add_well_step"]

if add_step == 1:
    with st.container(border=True):
        st.markdown("**Add Well — Step 1 of 2**")
        well_name_input = st.text_input("Well Name", value=st.session_state["pad_add_well_name"], key="_pad_well_name")
        col_next, col_cancel = st.columns([0.15, 0.85])
        with col_next:
            if st.button("Next →", type="primary", use_container_width=True):
                if well_name_input.strip():
                    st.session_state["pad_add_well_name"] = well_name_input.strip()
                    st.session_state["pad_add_well_step"] = 2
                    st.rerun()
                else:
                    st.warning("Well name is required.")
        with col_cancel:
            if st.button("Cancel", use_container_width=True):
                st.session_state["pad_add_well_step"] = 0
                st.rerun()

elif add_step == 2:
    with st.container(border=True):
        st.markdown(f"**Add Well — Step 2 of 2** — *{st.session_state['pad_add_well_name']}*")
        st.markdown("Start blank or apply the default template?")
        col_blank, col_tmpl, col_back_btn = st.columns([0.18, 0.18, 0.64])
        with col_blank:
            if st.button(":material/note_add: Blank", type="secondary", use_container_width=True):
                create_well(project_id, st.session_state["pad_add_well_name"])
                st.session_state["pad_add_well_step"] = 0
                st.rerun()
        with col_tmpl:
            if st.button(":material/auto_fix_high: Template", type="primary", use_container_width=True):
                well = create_well(project_id, st.session_state["pad_add_well_name"])
                if well:
                    apply_template(well)
                    update_well(project_id, well)
                st.session_state["pad_add_well_step"] = 0
                st.rerun()
        with col_back_btn:
            if st.button("← Back", use_container_width=True):
                st.session_state["pad_add_well_step"] = 1
                st.rerun()

# ---- Re-fetch project after mutations -------------------------------------
project = get_project(project_id)

# ---- Well list ------------------------------------------------------------
if not project.wells:
    st.info("No wells yet. Click **Add Well** to get started.")
else:
    for well in project.wells:
        modified = well.modified_at[:10] if well.modified_at else "—"

        with st.container(border=True):
            cols = st.columns([0.38, 0.12, 0.12, 0.12, 0.16, 0.10])
            with cols[0]:
                st.markdown(f"**{well.well_name}**")
                st.caption(f"modified {modified}")
            with cols[1]:
                wbc = len(well.wellbores)
                st.caption(f":material/water: {wbc} bore{'s' if wbc != 1 else ''}")
            with cols[2]:
                cc = len(well.casings)
                st.caption(f":material/settings: {cc} casing{'s' if cc != 1 else ''}")
            with cols[3]:
                mc = len(well.mud_entries)
                st.caption(f":material/opacity: {mc} mud")
            with cols[4]:
                if st.button("Open", key=f"open_well_{well.well_id}", use_container_width=True, type="primary"):
                    st.session_state["active_well_id"] = well.well_id
                    st.switch_page("src/pages/05_well.py")
            with cols[5]:
                if st.session_state.get("pad_confirm_delete_well") == well.well_id:
                    if st.button(":material/check:", key=f"confirm_del_{well.well_id}", use_container_width=True, help="Confirm delete"):
                        delete_well(project_id, well.well_id)
                        st.session_state["pad_confirm_delete_well"] = None
                        st.rerun()
                else:
                    if st.button(":material/delete:", key=f"del_{well.well_id}", use_container_width=True, help="Delete well"):
                        st.session_state["pad_confirm_delete_well"] = well.well_id
                        st.rerun()
