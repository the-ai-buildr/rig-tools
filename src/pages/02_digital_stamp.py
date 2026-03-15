"""Digital Stamp page — per-rig approval form. Produced by: frontend-agent."""
import streamlit as st
from utils.global_init import global_init
from components.layout import page_header, sidebar_header

# Initialize global (must be first executable call)
global_init()

# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Rig Tools", icon=":material/handyman:")

    rigs = ["HP 390", "HP 604", "HP 637", "HP 643", "Ensign 125", "Ensign 142"]
    wells = ["Example Well 1", "Example Well 2", "Example Well 3"]

    rig_name = st.selectbox("Rig", rigs)
    well_name = st.selectbox("Well Name", wells)

# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------
page_header("Digital Stamp", ":material/approval:")
