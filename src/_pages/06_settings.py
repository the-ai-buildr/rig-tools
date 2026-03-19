"""Settings page — user account and app preferences. Produced by: frontend-agent."""
import streamlit as st
from utils.global_init import global_init
from components.layout import page_header, sidebar_header, horizontal_rule

global_init()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Rig Tools", icon=":material/handyman:")
    horizontal_rule()
    st.caption("Made with ❤️ by [The Ai Buildr](https://github.com/the-ai-buildr)", text_alignment="center")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
page_header("Settings", ":material/settings:")

st.info("Settings coming soon.", icon=":material/info:")
