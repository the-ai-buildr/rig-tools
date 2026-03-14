import streamlit as st

def apply_custom_css():
    return st.markdown("""
        <style>
        
        /* Main block container — single source of truth for padding */
        div[data-testid="stMainBlockContainer"],
        div[data-testid="stMainBlockContainer"].block-container,
        section[data-testid="stMain"] .block-container {
            padding-top: 20px !important;
            padding-right: 20px !important;
            padding-left: 20px !important;
            padding-bottom: 40px !important;
        }

        /* Sidebar content padding */
        div[data-testid="stSidebarContent"] {
            padding-top: 10px !important;
            padding-right: 10px !important;
            padding-left: 10px !important;
            padding-bottom: 10px !important;
        }

        /* Hide entire Streamlit header */
        header[data-testid="stHeader"],
        header[data-testid="stHeader"] div[data-testid="stToolbar"],
        header[data-testid="stHeader"] .stAppToolbar,
        div[data-testid="stToolbar"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
            overflow: hidden !important;
        }

        /* Re-show the collapsed sidebar reopen button (lives inside the hidden header) */
        [data-testid="stSidebarCollapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            height: auto !important;
            min-height: auto !important;
            overflow: visible !important;
        }

        /* Sidebar header padding */
        div[data-testid="stSidebarHeader"] {
            height: 32px !important;
            min-height: 32px !important;
            padding-top: 12px !important;
            padding-right: 10px !important;
            padding-left: 10px !important;
            padding-bottom: 10px !important;
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
    
def render_top_bar():
    st.markdown("""
        <style>
        /* Offset main content below the fixed bar */
        div[data-testid="stMainBlockContainer"] {
            padding-top: 52px !important;
        }
        
        /* Our bar must beat Streamlit's internal z-indexes (~300-400 range) */
        #rig-top-bar {
            position: fixed;
            top: 0;
            left: 400px;
            right: 400px;
            height: 44px;
            z-index: 99999;
            background: #E5E5E5;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 16px;
            gap: 12px;
        }
        #rig-top-bar span {
            font-weight: 700;
            font-size: 1rem;
        }
        </style>

        <div id="rig-top-bar">
            <span>🛢️ Rig Tools</span>
        </div>
    """, unsafe_allow_html=True)
