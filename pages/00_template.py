import streamlit as st
from utils.global_init import global_init
from components.layout import page_header, sidebar_header


# Set page config
st.set_page_config(
    page_title="Template",
    page_icon="material/draft",
    layout="wide",
    initial_sidebar_state="expanded",
)
global_init()

# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Input Fields")

# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------
page_header("Page Template", ":material/draft:")
