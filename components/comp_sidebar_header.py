import streamlit as st

def horizontal_rule():
    # reduced vertical spacing (small top/bottom margins and no padding)
    st.markdown("<hr style='border:0.15px solid #ccc; margin-top:0px; margin-bottom:0px; padding:0;'>", unsafe_allow_html=True)

def sidebar_header(title_text,icon=""):
    cont = st.container()

    cont.markdown(f"# {icon} {title_text}", text_alignment="left")

    horizontal_rule()

    return cont





