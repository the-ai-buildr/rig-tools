import streamlit as st
import numpy as np
from styles.style import apply_custom_css
from components.comp_page_header import page_header
from components.comp_sidebar_header import sidebar_header 

# Set page config
st.set_page_config(
    page_title="Digital Stamp",
    page_icon="material/approval",
    layout="wide",
    # initial_sidebar_state="collapsed",
)

apply_custom_css()
page_header("Digital Stamp", ":material/approval:")

# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Input Fields")

    rigs = ["HP 643","HP 637","HP 604"]
    wells = ["Example Well 1", "Example Well 2", "Example Well 3"]

    rig_name = st.selectbox("Rig", rigs)
    well_name = st.selectbox("Well Name", wells)

# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------

    # Example chart — replace with something meaningful
   