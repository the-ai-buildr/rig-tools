import streamlit as st
from utils.global_init import global_init


# Page config
st.set_page_config(
        page_title="Rig Tools",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

# Global init
is_loaded = global_init()

# Redirect to Home page after global init
if is_loaded:
    st.switch_page("pages/01_home.py")
