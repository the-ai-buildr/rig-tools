import streamlit as st
from components.nav.links import nav_links

# Page config must be the first Streamlit call.
st.set_page_config(
    page_title="Rig Tools",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Init top nav — st.navigation handles default routing (Home is default=True)
pages_nav = nav_links()
pages_nav.run()

