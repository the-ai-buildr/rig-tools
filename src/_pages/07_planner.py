"""Template page scaffold — copy this for new pages. Produced by: frontend-agent."""
import streamlit as st
from components.page import page_content
from utils.global_init import global_init
from components.layout import page_header, sidebar_header
from components.planner.table import planner_table 

global_init()

# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Planner")


# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------
page_header("Planner", ":material/event_note:")


pt = planner_table()
page_content(pt)
    