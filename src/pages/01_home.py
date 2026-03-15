"""Home page — landing page with rig stat cards. Produced by: frontend-agent."""
import streamlit as st
from textwrap import dedent
from utils.global_init import global_init
from components.layout import (
    page_header,
    page_content,
    sidebar_header,
    horizontal_rule,
    rig_stats,
)

# Initialize global state (must be first executable call)
global_init()
# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
with st.sidebar:

    sidebar_header("Rig Tools", icon=":material/handyman:")

    with st.container():
        st.markdown(
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
            """)
        )

    horizontal_rule()

    st.caption("Made with ❤️ by [The Ai Buildr](https://github.com/the-ai-buildr)", text_alignment="center")

# ---------------------------------------------------------------------------
# Main area — results
# ---------------------------------------------------------------------------
page_header("Home", ":material/home:")

rig_stat_cards = rig_stats()

page_content(rig_stat_cards)




