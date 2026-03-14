import streamlit as st
from textwrap import dedent
from utils.global_init import global_init
from components.comp_page_layout import (
<<<<<<< HEAD
    page_header, page_content, nav_menu,
    sidebar_header, sidebar_content,
    horizontal_rule 
    )
from sections.home.cards import home_page_cards
=======
    page_header,
    sidebar_header,
    horizontal_rule,
)
>>>>>>> origin/main

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
<<<<<<< HEAD
        page_title="Home",
        layout="wide"
    )
=======
    page_title="Home",
    layout="wide",
    import streamlit as st
    from textwrap import dedent
    from utils.global_init import global_init
    from components.comp_page_layout import (
        page_header,
        sidebar_header,
        horizontal_rule,
    )

    # ---------------------------------------------------------------------------
    # Page config
    # ---------------------------------------------------------------------------
    st.set_page_config(
        page_title="Home",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize global state
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
