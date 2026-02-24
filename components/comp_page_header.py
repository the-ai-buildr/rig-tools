import streamlit as st
from styles.style import apply_custom_css

def horizontal_rule():
    # reduced vertical spacing (small top/bottom margins and no padding)
    st.markdown("<hr style='border:0.15px solid #ccc; margin-top:0px; margin-bottom:0px; padding:0;'>", unsafe_allow_html=True)


def page_header(title_text, icon=""):
    # Custom Page CSS
    apply_custom_css()

    # Page header cols
    col1, col2 = st.columns([0.80, 0.2], vertical_alignment="center")
    cont = st.container()
    
    with cont:
        with col1:
            st.markdown(f"# {icon} {title_text}", text_alignment="left")

        with col2:
            with st.popover("Goto", type="secondary", use_container_width=True, width=200):
                st.page_link("pages/01_home.py", label="Home", icon="🏠")
                st.page_link("pages/00_template.py", label="Template", icon="📝")
                st.page_link("pages/02_digital_stamp.py", label="Digital Stamp", icon="📱")

    horizontal_rule()

    return cont





