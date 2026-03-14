import streamlit as st


def horizontal_rule():
    st.markdown("<hr style='border:0.15px solid #ccc; margin-top:4px; margin-bottom:12px; padding:0;'>", unsafe_allow_html=True)

# Page navigation menu
def nav_menu():
    with st.popover("Goto", type="secondary", use_container_width=True, width=200):
        st.page_link("pages/01_home.py", label="Home", icon="🏠")
        # st.page_link("pages/00_template.py", label="Template", icon="📝")
        st.page_link("pages/02_digital_stamp.py", label="Digital Stamp", icon="📱")

# Page navigation menu
def page_nav(title_text="", icon=""):
    col1, col2 = st.columns([0.80, 0.20], gap="small", vertical_alignment="center")
    cont = st.container()

    with cont:
        with col1:
            st.markdown(f"# {icon} {title_text}", text_alignment="left")
        with col2:
            nav_menu()

    return cont

# Sidebar header with title and horizontal rule
def sidebar_header(title_text="", icon=""):
    cont = st.container()
    cont.markdown(f"# {icon} {title_text}", text_alignment="center")
    horizontal_rule()
    return cont


# Sidebar content container
def sidebar_content(cont=None):
    if cont is None:
        cont = st.container()
    return cont

# Page header with navigation menu and horizontal rule
def page_header(title_text="", icon=""):
    cont = st.container()
    with cont:
        page_nav(title_text, icon)
    horizontal_rule()
    return cont

# Page content container
def page_content(cont=None):
    if cont is None:
        cont = st.container()
    return cont
