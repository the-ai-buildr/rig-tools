"""
Well editor page — 4 tabs for header, wellbores, casings, and mud entries.

Works for both single-well and pad projects:
  - Back button → 04_project.py for pad, 03_projects.py for single
  - Guard redirects appropriately if no active well

Each tab is decorated with @st.fragment to prevent full-page reruns on save.

Produced by: frontend-agent
"""
import streamlit as st
import pandas as pd
from utils.global_init import global_init
from components.layout import page_header, sidebar_header, horizontal_rule
from data.project_store import get_project, get_well, update_well
from data.models import WellHeader, Wellbore, CasingLiner, MudEntry, _new_id

global_init()

# ---------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------
project_id = st.session_state.get("active_project_id")
well_id = st.session_state.get("active_well_id")

project = get_project(project_id) if project_id else None
well = get_well(project_id, well_id) if (project_id and well_id) else None

if project is None:
    st.warning("No project selected.")
    if st.button(":material/folder: Go to Projects"):
        st.switch_page("src/pages/03_projects.py")
    st.stop()

if well is None:
    st.warning("No well selected.")
    back_page = "src/pages/04_project.py" if project.project_type == "pad" else "src/pages/03_projects.py"
    if st.button(":material/arrow_back: Go Back"):
        st.switch_page(back_page)
    st.stop()

_back_page = "src/pages/04_project.py" if project.project_type == "pad" else "src/pages/03_projects.py"
_back_label = "Back to Pad" if project.project_type == "pad" else "Back to Projects"

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Rig Tools", icon=":material/handyman:")
    st.markdown(f"**{project.project_name}** / **{well.well_name}**")
    st.caption(f":material/person: {well.created_by}")
    st.caption(f":material/schedule: modified {well.modified_at[:10]}")
    horizontal_rule()
    if st.button(f":material/arrow_back: {_back_label}", use_container_width=True):
        st.switch_page(_back_page)

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
page_header(well.well_name, ":material/oil_barrel:")

col_back, col_spacer = st.columns([0.18, 0.82])
with col_back:
    if st.button(f":material/arrow_back: {_back_label}", use_container_width=True):
        st.switch_page(_back_page)

horizontal_rule()

tab_header, tab_wellbores, tab_casings, tab_mud = st.tabs([
    ":material/info: Well Header",
    ":material/water: Wellbores",
    ":material/settings: Casing & Liners",
    ":material/opacity: Mud Tables",
])


# ===========================================================================
# Tab 1 — Well Header
# ===========================================================================
@st.fragment
def _tab_well_header():
    well_local = get_well(project_id, well_id)
    if well_local is None:
        st.error("Well not found.")
        return
    h = well_local.header

    with st.form("form_well_header"):
        c1, c2 = st.columns(2)
        with c1:
            operator   = st.text_input("Operator",   value=h.operator)
            w_name     = st.text_input("Well Name",   value=h.well_name)
            api_number = st.text_input("API Number",  value=h.api_number)
            field      = st.text_input("Field",       value=h.field)
            county     = st.text_input("County",      value=h.county)
        with c2:
            state      = st.text_input("State",       value=h.state)
            country    = st.text_input("Country",     value=h.country)
            spud_date  = st.text_input("Spud Date (YYYY-MM-DD)", value=h.spud_date)
            rig_name   = st.text_input("Rig Name",    value=h.rig_name)
            c_lat, c_lon = st.columns(2)
            with c_lat:
                latitude  = st.number_input("Latitude",  value=h.latitude  or 0.0, format="%.6f")
            with c_lon:
                longitude = st.number_input("Longitude", value=h.longitude or 0.0, format="%.6f")

        if st.form_submit_button(":material/save: Save Header", type="primary"):
            well_local.header = WellHeader(
                operator=operator,
                well_name=w_name,
                api_number=api_number,
                field=field,
                county=county,
                state=state,
                country=country,
                spud_date=spud_date,
                rig_name=rig_name,
                latitude=latitude if latitude != 0.0 else None,
                longitude=longitude if longitude != 0.0 else None,
            )
            update_well(project_id, well_local)
            st.success("Well header saved.")


# ===========================================================================
# Tab 2 — Wellbores
# ===========================================================================
@st.fragment
def _tab_wellbores():
    well_local = get_well(project_id, well_id)
    if well_local is None:
        st.error("Well not found.")
        return

    wb_data = [
        {"Name": wb.name, "Type": wb.wellbore_type,
         "MD (ft)": wb.measured_depth, "TVD (ft)": wb.true_vertical_depth}
        for wb in well_local.wellbores
    ]
    df = pd.DataFrame(wb_data) if wb_data else pd.DataFrame(columns=["Name", "Type", "MD (ft)", "TVD (ft)"])

    edited = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Type": st.column_config.SelectboxColumn("Type", options=["Vertical", "Horizontal", "Deviated"]),
            "MD (ft)":  st.column_config.NumberColumn("MD (ft)",  min_value=0.0, format="%.1f"),
            "TVD (ft)": st.column_config.NumberColumn("TVD (ft)", min_value=0.0, format="%.1f"),
        },
        key="editor_wellbores",
    )

    if st.button(":material/save: Save Wellbores", type="primary"):
        well_local.wellbores = [
            Wellbore(
                wellbore_id=_new_id(),
                name=str(row.get("Name", "")),
                wellbore_type=str(row.get("Type", "Vertical")),
                measured_depth=float(row.get("MD (ft)", 0.0) or 0.0),
                true_vertical_depth=float(row.get("TVD (ft)", 0.0) or 0.0),
            )
            for _, row in edited.iterrows()
            if str(row.get("Name", "")).strip()
        ]
        update_well(project_id, well_local)
        st.success("Wellbores saved.")


# ===========================================================================
# Tab 3 — Casing & Liners
# ===========================================================================
@st.fragment
def _tab_casings():
    well_local = get_well(project_id, well_id)
    if well_local is None:
        st.error("Well not found.")
        return

    csg_data = [
        {"Name": c.name, "Type": c.casing_type,
         "OD (in)": c.od, "ID (in)": c.id_, "Weight (lb/ft)": c.weight,
         "Grade": c.grade, "Top (ft)": c.top_depth, "Bottom (ft)": c.bottom_depth,
         "Cement Top (ft)": c.cement_top}
        for c in well_local.casings
    ]
    df = pd.DataFrame(csg_data) if csg_data else pd.DataFrame(
        columns=["Name", "Type", "OD (in)", "ID (in)", "Weight (lb/ft)",
                 "Grade", "Top (ft)", "Bottom (ft)", "Cement Top (ft)"]
    )

    edited = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Type": st.column_config.SelectboxColumn("Type", options=["Casing", "Liner"]),
            "OD (in)":         st.column_config.NumberColumn("OD (in)",         format="%.3f"),
            "ID (in)":         st.column_config.NumberColumn("ID (in)",          format="%.3f"),
            "Weight (lb/ft)":  st.column_config.NumberColumn("Weight (lb/ft)",   format="%.2f"),
            "Top (ft)":        st.column_config.NumberColumn("Top (ft)",         format="%.1f"),
            "Bottom (ft)":     st.column_config.NumberColumn("Bottom (ft)",      format="%.1f"),
            "Cement Top (ft)": st.column_config.NumberColumn("Cement Top (ft)",  format="%.1f"),
        },
        key="editor_casings",
    )

    if st.button(":material/save: Save Casings & Liners", type="primary"):
        well_local.casings = [
            CasingLiner(
                id=_new_id(),
                name=str(row.get("Name", "")),
                casing_type=str(row.get("Type", "Casing")),
                od=float(row.get("OD (in)", 0.0) or 0.0),
                id_=float(row.get("ID (in)", 0.0) or 0.0),
                weight=float(row.get("Weight (lb/ft)", 0.0) or 0.0),
                grade=str(row.get("Grade", "")),
                top_depth=float(row.get("Top (ft)", 0.0) or 0.0),
                bottom_depth=float(row.get("Bottom (ft)", 0.0) or 0.0),
                cement_top=float(row.get("Cement Top (ft)", 0.0) or 0.0),
            )
            for _, row in edited.iterrows()
            if str(row.get("Name", "")).strip()
        ]
        update_well(project_id, well_local)
        st.success("Casings & Liners saved.")


# ===========================================================================
# Tab 4 — Mud Tables
# ===========================================================================
@st.fragment
def _tab_mud():
    well_local = get_well(project_id, well_id)
    if well_local is None:
        st.error("Well not found.")
        return

    mud_data = [
        {"Date": m.date, "Depth (ft)": m.depth, "Mud Type": m.mud_type,
         "MW (ppg)": m.mud_weight, "Viscosity (cP)": m.viscosity,
         "pH": m.ph, "Chlorides (mg/L)": m.chlorides}
        for m in well_local.mud_entries
    ]
    df = pd.DataFrame(mud_data) if mud_data else pd.DataFrame(
        columns=["Date", "Depth (ft)", "Mud Type", "MW (ppg)", "Viscosity (cP)", "pH", "Chlorides (mg/L)"]
    )

    edited = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Date":              st.column_config.TextColumn("Date (YYYY-MM-DD)"),
            "Depth (ft)":        st.column_config.NumberColumn("Depth (ft)",        format="%.1f"),
            "MW (ppg)":          st.column_config.NumberColumn("MW (ppg)",           format="%.2f"),
            "Viscosity (cP)":    st.column_config.NumberColumn("Viscosity (cP)",     format="%.1f"),
            "pH":                st.column_config.NumberColumn("pH",                 format="%.1f"),
            "Chlorides (mg/L)":  st.column_config.NumberColumn("Chlorides (mg/L)",  format="%.0f"),
        },
        key="editor_mud",
    )

    if st.button(":material/save: Save Mud Table", type="primary"):
        well_local.mud_entries = [
            MudEntry(
                id=_new_id(),
                date=str(row.get("Date", "")),
                depth=float(row.get("Depth (ft)", 0.0) or 0.0),
                mud_type=str(row.get("Mud Type", "")),
                mud_weight=float(row.get("MW (ppg)", 0.0) or 0.0),
                viscosity=float(row.get("Viscosity (cP)", 0.0) or 0.0),
                ph=float(row.get("pH", 0.0) or 0.0),
                chlorides=float(row.get("Chlorides (mg/L)", 0.0) or 0.0),
            )
            for _, row in edited.iterrows()
            if str(row.get("Mud Type", "")).strip() or float(row.get("Depth (ft)", 0.0) or 0.0) > 0
        ]
        update_well(project_id, well_local)
        st.success("Mud table saved.")


# ---------------------------------------------------------------------------
# Render tabs
# ---------------------------------------------------------------------------
with tab_header:
    _tab_well_header()

with tab_wellbores:
    _tab_wellbores()

with tab_casings:
    _tab_casings()

with tab_mud:
    _tab_mud()
