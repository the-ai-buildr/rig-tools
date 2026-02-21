import streamlit as st


def apply_custom_css():
    st.markdown("""
        <style>
        /* ── Main content padding ── */
        div[data-testid="stMainBlockContainer"].block-container {
            padding-top: 0px !important;
            padding-right: 20px !important;
            padding-left: 20px !important;
            padding-bottom: 40px !important;
        }
        div[data-testid="stMainBlockContainer"] {
            padding: 20px !important;
            padding-top: 0px !important;
        }
        section[data-testid="stMain"] .block-container {
            padding: 30px !important;
            padding-top: 0px !important;
        }

        /* ── Sidebar header tweaks ── */
        div[data-testid="stSidebarHeader"] {
            height: 20px !important;
            min-height: 20px !important;
            padding: 8px !important;
        }
        div[data-testid="stSidebarHeader"] > div,
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

        /* ── Hide default Streamlit sidebar nav list ── */
        section[data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* ── Top nav bar container ── */
        .rig-nav {
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 8px 0 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            margin-bottom: 20px;
        }
        .rig-nav-title {
            font-size: 1.1rem;
            font-weight: 700;
            margin-right: 12px;
            white-space: nowrap;
            color: inherit;
        }

        /* ── Style st.page_link buttons inside the nav ── */
        .rig-nav a[data-testid="stPageLink-NavLink"],
        .rig-nav a[data-testid="stPageLink"] {
            border-radius: 6px;
            padding: 4px 14px !important;
            font-size: 0.875rem !important;
            font-weight: 500;
            text-decoration: none !important;
            transition: background 0.15s;
        }
        .rig-nav a[data-testid="stPageLink-NavLink"]:hover,
        .rig-nav a[data-testid="stPageLink"]:hover {
            background: rgba(255,255,255,0.08);
        }
        .rig-nav a[aria-current="page"],
        .rig-nav a[data-testid="stPageLink-NavLink"][aria-current="page"] {
            background: rgba(255, 75, 75, 0.18) !important;
            color: #ff4b4b !important;
        }

        .stFileUploader {
            margin-top: -10px !important;
        }
        </style>
        """, unsafe_allow_html=True)


def nav_bar(pages: list[tuple[str, str]]) -> None:
    """Render a horizontal top navigation bar.

    Args:
        pages: List of (label, path) tuples where path is the page file path
               relative to the project root, e.g. [("Home", "app.py"), ("Template", "pages/00_template.py")]
    """
    apply_custom_css()

    cols_needed = 1 + len(pages)  # title col + one per page
    # Use small fixed width for title, equal widths for page links
    col_widths = [2] + [1] * len(pages)
    cols = st.columns(col_widths)

    with cols[0]:
        st.markdown('<span class="rig-nav-title">🛢️ Rig Tools</span>', unsafe_allow_html=True)

    for i, (label, path) in enumerate(pages):
        with cols[i + 1]:
            st.page_link(path, label=label)

    st.markdown('<div style="border-bottom:1px solid rgba(255,255,255,0.12);margin-bottom:16px;"></div>', unsafe_allow_html=True)