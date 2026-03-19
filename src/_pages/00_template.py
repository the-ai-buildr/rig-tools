"""Template page scaffold — copy this for new pages. Produced by: frontend-agent."""
import streamlit as st
from utils.global_init import global_init
from components.layout import page_header, sidebar_header

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
