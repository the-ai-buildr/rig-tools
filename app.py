import streamlit as st
from page import *

st.set_page_config(
    page_title="Rig Tools",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define all pages — position="hidden" suppresses the default sidebar nav list.
# Each st.Page maps a label to a file in pages/.
home_page = st.Page("page/01_home.py", title="Home", icon="🏠", default=True)
template_page = st.Page("page/00_template.py", title="Template", icon="📐")

pg = st.navigation(
    [home_page, template_page],
    position="hidden",
)

pg.run()
