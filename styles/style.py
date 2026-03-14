import streamlit as st

def apply_custom_css():
    return st.markdown("""
        <style>

        /* Main block container */
        div[data-testid="stMainBlockContainer"],
        div[data-testid="stMainBlockContainer"].block-container,
        section[data-testid="stMain"] .block-container {
            padding-top: 10px !important;
            padding-right: 20px !important;
            padding-left: 20px !important;
            padding-bottom: 40px !important;
        }

        /* Strip default margins from headings in main + sidebar */
        div[data-testid="stMainBlockContainer"] h1,
        div[data-testid="stSidebarUserContent"] h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
            margin-bottom: 0.25rem !important;
        }

        /* Sidebar content padding */
        div[data-testid="stSidebarContent"] {
            padding-top: 0px !important;
            padding-right: 10px !important;
            padding-left: 10px !important;
            padding-bottom: 10px !important;
        }

        /* Collapse header to zero height but let children overflow */
        header[data-testid="stHeader"] {
            height: 0 !important;
            min-height: 0 !important;
            padding: 0 !important;
            overflow: visible !important;
            background: transparent !important;
            border: none !important;
        }

        /* Hide toolbar contents but keep in flow so children can opt back in */
        div[data-testid="stToolbar"] {
            visibility: hidden !important;
        }

        /* Keep the expand-sidebar button visible and fixed in top-left */
        button[data-testid="stExpandSidebarButton"] {
            visibility: visible !important;
            position: fixed !important;
            top: 8px !important;
            left: 8px !important;
            z-index: 99999 !important;
        }

        /* Sidebar header region (collapse button area) */
        div[data-testid="stSidebarHeader"] {
            height: 40px !important;
            min-height: 40px !important;
            max-height: 40px !important;
            padding: 0 !important;
            margin-bottom: 0 !important;
            overflow: visible !important;
        }

        /* Remove top space above user content block */
        div[data-testid="stSidebarUserContent"] {
            margin-top: 0px !important;
            padding-top: 8px !important;
        }

        </style>
        """, unsafe_allow_html=True)
    
def render_top_bar():
    st.markdown(f"""
        <style>
        /* Offset main content below the fixed bar */
        div[data-testid="stMainBlockContainer"] {
            padding-top: 0px !important;
            
        }
        
        h1#approval-digital-stamp {
            padding-bottom: 8px !important;
        }

        button[data-testid="stPopoverButton"] {
            min-width: 200px !important;
            max-width: 200px !important;
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
