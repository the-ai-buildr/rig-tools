"""
Template page — copy this file to build new calculator pages.

Rename the file (e.g., 02_mud_weight.py), update the title,
inputs, and calculation logic. Add the new page to app.py and
to the NAV_PAGES list below.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st
import numpy as np
from styles.style import nav_bar

# ---------------------------------------------------------------------------
# Navigation — keep in sync with app.py and other pages
# ---------------------------------------------------------------------------
NAV_PAGES = [
    ("🏠 Home", "page/01_home.py"),
    ("📐 Template", "page/00_template.py"),
]
nav_bar(NAV_PAGES)

# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
st.title("Template Calculator")
st.caption("Copy this page as a starting point for new calculators.")

st.divider()

# ── Sidebar — inputs ────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Inputs")

    unit_system = st.radio("Unit System", ["Oilfield", "SI"], horizontal=True)

    st.subheader("Parameters")
    value_a = st.number_input(
        "Value A",
        min_value=0.0,
        value=10.0,
        step=0.1,
        help="Description of Value A.",
    )
    value_b = st.number_input(
        "Value B",
        min_value=0.0,
        value=5.0,
        step=0.1,
        help="Description of Value B.",
    )

    calculate = st.button("Calculate", type="primary", use_container_width=True)

# ── Main area — results ─────────────────────────────────────────────────────
if calculate:
    result = value_a * value_b

    st.subheader("Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Result", f"{result:.2f}", help="Value A × Value B")
    with col2:
        st.metric("Value A", f"{value_a:.2f}")
    with col3:
        st.metric("Value B", f"{value_b:.2f}")

    st.divider()

    st.subheader("Chart")
    x = np.linspace(0, value_a, 100)
    y = x * value_b
    st.line_chart({"x": x, "y": y}, x="x", y="y")

    with st.expander("Formula Reference"):
        st.markdown(
            """
            **Formula used:**
            ```
            result = value_a × value_b
            ```
            Replace this with the actual formula and references.
            """
        )
else:
    st.info("Enter values in the sidebar and press **Calculate**.")
