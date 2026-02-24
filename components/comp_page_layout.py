import streamlit as st
from styles.style import apply_custom_css

def horizontal_rule():
    # reduced vertical spacing (small top/bottom margins and no padding)
    st.markdown("<hr style='border:0.15px solid #ccc; margin-top:0px; margin-bottom:20px; padding:0;'>", unsafe_allow_html=True)

def nav_menu():
    with st.popover("Goto", type="secondary", use_container_width=True, width=200):
        st.page_link("pages/01_home.py", label="Home", icon="🏠")
        # st.page_link("pages/00_template.py", label="Template", icon="📝")
        st.page_link("pages/02_digital_stamp.py", label="Digital Stamp", icon="📱")

def page_nav(title_text="", icon=""):
    col1, col2 = st.columns([0.80, 0.2], vertical_alignment="center")
    cont = st.container()
    
    with cont:
        with col1:
            st.markdown(f"# {icon} {title_text}", text_alignment="left")

        with col2:
            nav_menu()

    return cont

def sidebar_header(title_text="",icon= ""):
    cont = st.container()

    cont.markdown(f"# {icon} {title_text}", text_alignment="center")

    horizontal_rule()

    return cont

def sidebar_content(cont=None):
    if cont is None or isinstance(cont, str):
        cont = st.container()
    elif hasattr(cont, "container"):
        cont = cont.container()

    with cont:
        cont

    return cont

def page_header(title_text="", icon=""):
    # Custom Page CSS
    apply_custom_css()

    # Page header section
    cont = st.container()
    with cont:
        page_nav(title_text, icon)

    horizontal_rule()

    return cont

def page_content(cont = None):
    if cont is None or isinstance(cont, str):
        cont = st.container()
    elif hasattr(cont, "container"):
        cont = cont.container()

    with cont:
        cont

    return cont




