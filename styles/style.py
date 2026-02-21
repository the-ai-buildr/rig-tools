import streamlit as st

def apply_custom_css():
    return st.markdown("""
        <style>
        /* Main block container padding */
        div[data-testid="stMainBlockContainer"].block-container {
            padding-top: 20px !important;
            padding-right: 20px !important;
            padding-left: 20px !important;
            padding-bottom: 40px !important;
        }

        /* Sidebar content padding */
        div[data-testid="stSidebarContent"] {
            padding-top: 0px !important;
            padding-right: 10px !important;
            padding-left: 10px !important;
            padding-bottom: 10px !important;
        }

        /* Sidebar header padding */
        div[data-testid="stSidebarHeader"] {
            height: 20px !important;
            min-height: 20px !important;
            padding-top: 10px !important;
            padding-right: 10px !important;
            padding-left: 10px !important;
            padding-bottom: 10px !important;
        }

        /* Main block container */
        div[data-testid="stMainBlockContainer"] {
            padding: 20px !important;
        }

        /* Main section block container */
        section[data-testid="stMain"] .block-container {
            padding: 30px !important;
        }
        </style>
        """, unsafe_allow_html=True)