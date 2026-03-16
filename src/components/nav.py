import streamlit as st
from .utils import horizontal_rule


def nav_menu():
    with st.popover("Goto", type="secondary", use_container_width=True, width=200):
        # st.page_link("pages/00_template.py", label="Template", icon="📝")
        st.page_link("pages/01_home.py", label="Home", icon="🏠")
        st.page_link("pages/03_projects.py", label="Projects", icon="📁")
        st.page_link("pages/02_digital_stamp.py", label="Digital Stamp", icon="📱")


def page_nav(title_text="", icon=""):
    col1, col2 = st.columns([0.80, 0.20], gap="small", vertical_alignment="bottom")
    cont = st.container()

    with cont:
        with col1:
            st.markdown(f"# {icon} {title_text}", text_alignment="left")
        with col2:
            nav_menu()
    
    return cont
