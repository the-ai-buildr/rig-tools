"""Operational planner page — rig/well selection in sidebar, editable schedule table.

Produced by: frontend-agent / developing-with-streamlit skill
"""
import streamlit as st
from utils.global_init import global_init
from components.layout import page_header, sidebar_header
from components.planner.table import planner_table

global_init()

# ---------------------------------------------------------------------------
# Sidebar — filters
# ---------------------------------------------------------------------------
_RIGS = ["HP 643", "HP 604", "HP 637", "HP 390", "Ensign 142", "Ensign 125"]

with st.sidebar:
    sidebar_header("Planner")
    st.session_state.setdefault("planner_rig", _RIGS[0])
    st.session_state.setdefault("planner_well", "Butters 5J 210H")

    selected_rig = st.selectbox(
        "Rig",
        options=_RIGS,
        key="planner_rig",
    )
    selected_well = st.text_input(
        "Well",
        key="planner_well",
    )

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
page_header("Planner", ":material/event_note:")

planner_table(rig=selected_rig, well=selected_well)
