import streamlit as st

st.set_page_config(
    page_title="Rig Tools",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🛢️ Rig Tools")
st.markdown("Oilfield drilling calculators — select a tool from the sidebar.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Mud Weight & Pressure**\nHydrostatic pressure, ECD, ESD, surge & swab.")

with col2:
    st.info("**Hydraulics**\nPump output, annular velocity, pressure drop.")

with col3:
    st.info("**More tools coming soon...**\nDrill string, hole geometry, cementing.")
