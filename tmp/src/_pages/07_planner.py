"""Template page scaffold — copy this for new pages. Produced by: frontend-agent."""
import streamlit as st
from old.src.components.page import page_content
from old.src.utils.global_init import global_init
from old.src.components.layout import page_header, sidebar_header
from old.src.components.planner.table import planner_table 

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
    