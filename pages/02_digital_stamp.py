import streamlit as st
from utils.global_init import global_init
from components.comp_page_layout import page_header, sidebar_header

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Digital Stamp",
    page_icon="material/approval",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Initialize global
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
