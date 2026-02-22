import streamlit as st

def apply_custom_css():
    return st.markdown("""
        <style>
        /* Main block container padding */
        div[data-testid="stMainBlockContainer"].block-container {
            padding-top: 40px !important;
            padding-right: 20px !important;
            padding-left: 20px !important;
            padding-bottom: 40px !important;
        }

        /* Sidebar content padding */
        div[data-testid="stSidebarContent"] {
            padding-top: 16px !important;
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
        /* Streamlit header and toolbar — reduce top spacing */
        header[data-testid="stHeader"],
        header[data-testid="stHeader"] .stAppToolbar,
        div[data-testid="stToolbar"] {
            padding-top: 0px !important;
            padding-bottom: 4px !important;
            margin-top: 0px !important;
            margin-bottom: 0px !important;
        }

        /* Reduce internal toolbar/button padding */
        div[data-testid="stToolbar"] .stToolbarActions,
        header[data-testid="stHeader"] button[data-testid^="stBaseButton"] {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            min-height: 0px !important;
        }
                       
        /* Container for the nav block */
        nav[data-testid="stSidebarNav"],
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* UL that holds the nav items */
        ul[data-testid="stSidebarNavItems"] {
            display: none !important;
        }
                       
        
        /* Remove top space above user content block */
        div[data-testid="stSidebarUserContent"] {
            margin-top: 0px !important;
            padding-top: 0px !important;
        }


        </style>
        """, unsafe_allow_html=True)