import streamlit as st
import pandas as pd
import numpy as np
from textwrap import dedent 
from components.comp_page_layout import (
    page_header, page_content, nav_menu,
    sidebar_header, sidebar_content )

# ---------------------------------------------------------------------------
# Page - config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Digital Stamp",
    page_icon="material/approval",
    layout="wide",
    # initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Rig Tools", icon=":material/handyman:")

    rigs = ["HP 643","HP 637","HP 604"]
    wells = ["Example Well 1", "Example Well 2", "Example Well 3"]

    rig_name = st.selectbox("Rig", rigs)
    well_name = st.selectbox("Well Name", wells)

# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------
cont = st.container()


page_header("Digital Stamp", ":material/approval:")

# page_content(cont) # Use if build components in another file or section