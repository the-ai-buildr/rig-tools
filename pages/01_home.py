import streamlit as st
import pandas as pd
import numpy as np
from textwrap import dedent 
from components.comp_page_layout import (
    page_header, page_content, nav_menu,
    sidebar_header, sidebar_content,
    horizontal_rule 
    )

# ---------------------------------------------------------------------------
# Page - config
# ---------------------------------------------------------------------------
st.set_page_config(
        page_title="Home",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_header("Rig Tools", icon=":material/handyman:")
    cont = st.container()

    with cont:
        st.markdown (
            dedent("""
                This app is a collection of tools for Operations Supervisors, 
                Rig Managers, Engineers designed to make calculations and
                data analysis easier.
                   
                This project is also fully open-source, so feel free to explore
                the code and contribute if you have ideas for new features or 
                improvements! 
                   
                Use this sidebar section to navigate to different tools and features. 
                   
                **Located here:** [GitHub Repo](https://github.com/the-ai-buildr/rig-tools)
                
                More content coming soon!
                   

                """
            )
        )

    horizontal_rule()

    st.caption("Made with ❤️ by [The Ai Buildr](https://github.com/the-ai-buildr)", text_alignment="center")

    # sidebar_content(cont) # Use if build components in another file or section


# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------
cont = st.container()


page_header("Home", ":material/home:")

# page_content(cont) # Use if build components in another file or section