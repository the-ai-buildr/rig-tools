import sys
from pathlib import Path
import streamlit as st
import numpy as np
from styles.style import apply_custom_css
from components.comp_page_header import page_header

# Set page config
st.set_page_config(
    page_title="Home",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add project root so styles can be imported (needed for Streamlit multipage / Pyodide)
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

apply_custom_css()
page_header("Home", ":material/home:")

# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------
if calculate:
    # Replace this block with real calculation logic
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

    # Example chart — replace with something meaningful
    st.subheader("Chart")
    x = np.linspace(0, value_a, 100)
    y = x * value_b
    chart_data = {"x": x, "y": y}
    st.line_chart(chart_data, x="x", y="y")

    # Notes / formula reference
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
