import streamlit as st
from utils.global_init import global_init
from components.comp_page_header import page_header

st.set_page_config(
        page_title="Rig Tools",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

# Global init
global_init()

# Page Setup
page_header("Welcome to the Rig Tools App! 🛠️")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Mud Weight & Pressure**\nHydrostatic pressure, ECD, ESD, surge & swab.")

with col2:
    st.info("**Hydraulics**\nPump output, annular velocity, pressure drop.")

with col3:
    st.info("**More tools coming soon...**\nDrill string, hole geometry, cementing.")
