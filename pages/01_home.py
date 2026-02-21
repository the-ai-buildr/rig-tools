import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st
from styles.style import nav_bar

# ---------------------------------------------------------------------------
# Navigation — keep in sync with app.py and other pages
# ---------------------------------------------------------------------------
NAV_PAGES = [
    ("🏠 Home", "pages/01_home.py"),
    ("📐 Template", "pages/00_template.py"),
]
nav_bar(NAV_PAGES)

# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
st.title("Rig Tools")
st.markdown("Oilfield drilling calculators — select a tool from the nav bar above.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Mud Weight & Pressure**\nHydrostatic pressure, ECD, ESD, surge & swab.")

with col2:
    st.info("**Hydraulics**\nPump output, annular velocity, pressure drop.")

with col3:
    st.info("**More tools coming soon...**\nDrill string, hole geometry, cementing.")
