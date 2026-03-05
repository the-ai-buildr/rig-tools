import streamlit as st
import pandas as pd
import numpy as np
from textwrap import dedent 
from components.comp_page_layout import (
    page_header, page_content, 
    sidebar_header, sidebar_content )


# Set page config
st.set_page_config(
    page_title="Template",
    page_icon="material/draft",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Input Fields")
# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------

page_header("Page Template", ":material/draft:")
