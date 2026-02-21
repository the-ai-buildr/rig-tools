import streamlit as st

def apply_custom_css():
    return st.markdown("""
        <style>
        div[data-testid="stMainBlockContainer"].block-container {
            padding-top: 40px !important;
            padding-right: 20px !important;
            padding-left: 20px !important;
            padding-bottom: 40px !important;
        }
        div[data-testid="stSidebarHeader"] {
            height: 20px !important;
            min-height: 20px !important;
            padding-top: 8px !important;
            padding-right: 8px !important;
            padding-left: 8px !important;
            padding-bottom: 8px !important;
        }
        div[data-testid="stSidebarHeader"] > div {
            transform: translateY(10px) !important;
        }
        div[data-testid="stSidebarHeader"] span[data-testid="stIconMaterial"] {
            transform: translateY(10px) !important;
        }
        div[data-testid="stSidebarCollapseButton"] {
            transform: translateY(10px) !important;
            margin-top: 5px !important;
            margin-right: 10px !important;
        }
        div[data-testid="stSidebarCollapseButton"] button,
        div[data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"] {
            transform: translateY(-10px) !important;
        }
        div[data-testid="stMainBlockContainer"] {
            padding: 20px !important;
        }
        section[data-testid="stMain"] .block-container {
            padding: 30px !important;
        }
        .stFileUploader {
            margin-top: -10px !important;
        }
        </style>
        """, unsafe_allow_html=True)