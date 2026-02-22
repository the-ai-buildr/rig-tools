import streamlit as st
from styles.style import apply_custom_css
from components.comp_page_header import page_header

# Set page config
st.set_page_config(
    page_title="Rig Tools",
    page_icon="assets/eng_man.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_css()
page_header("Rig Tools", ":material/handyman:")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Mud Weight & Pressure**\nHydrostatic pressure, ECD, ESD, surge & swab.")

with col2:
    st.info("**Hydraulics**\nPump output, annular velocity, pressure drop.")

with col3:
    st.info("**More tools coming soon...**\nDrill string, hole geometry, cementing.")
