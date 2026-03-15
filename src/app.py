import streamlit as st

# Page config must be the first Streamlit call.
st.set_page_config(
    page_title="Rig Tools",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Redirect immediately — no rendering here so there is nothing for Streamlit to
# clear on switch, eliminating the CSS flash between app.py and 01_home.py.
# Session state and CSS are initialised by global_init() in each page.
st.switch_page("pages/01_home.py")

