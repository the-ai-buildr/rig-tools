"""
Auth Component

Provides:
    show_login_page()   Full-screen login form
    show_logout_button() Sidebar logout widget

Usage:
    from frontend.components.auth import show_login_page, show_logout_button
"""

import streamlit as st
from frontend.api_client import login, logout, get_current_user


def show_login_page() -> None:
    """
    Render a centered login form.

    On successful authentication the token is stored in ``st.session_state``
    and the app is re-run so the main dashboard appears.
    """
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            "<h2 style='text-align:center;color:#1f4e79;'>🛢️ Well Dashboard</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center;color:#666;'>Drilling Project Management</p>",
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                if login(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Default: admin / admin123")


def show_logout_button() -> None:
    """
    Render a sidebar section with the current username and a Logout button.
    """
    user = get_current_user()
    st.sidebar.markdown(f"### 👤 {user.get('username', 'User')}")

    if st.sidebar.button("Logout", use_container_width=True):
        logout()
        st.rerun()
