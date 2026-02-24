import streamlit as st
import pandas as pd
import numpy as np
from components.comp_page_header import page_header

st.set_page_config(
        page_title="Home",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

# Page Setup
page_header("Home", ":material/home:")

# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
st.write("This is the home page. Use the sidebar to navigate to different tools and features. More content coming soon!")


# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------
