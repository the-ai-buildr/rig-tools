import streamlit as st
from .nav import page_nav
from .utils import horizontal_rule


def page_header(title_text="", icon=""):
    cont = st.container()
    with cont:
        page_nav(title_text, icon)
    horizontal_rule()
    return cont


def page_content(cont=None):
    if cont is None:
        cont = st.container()
    return cont
