import streamlit as st

def horizontal_rule():
    # reduced vertical spacing (small top/bottom margins and no padding)
    st.markdown("<hr style='border:0.5px solid #ccc;margin:10px 0;padding:0;'>", unsafe_allow_html=True)

