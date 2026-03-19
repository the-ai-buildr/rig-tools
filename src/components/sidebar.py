import streamlit as st
from .utils import horizontal_rule


def sidebar_header(title_text="", icon=""):
    cont = st.container()
    cont.markdown(f"# {icon} {title_text}", text_alignment="center")
    return cont


def sidebar_content(cont=None):
    if cont is None:
        cont = st.container()
    return cont
