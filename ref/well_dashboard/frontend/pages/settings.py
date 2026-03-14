"""
Settings Page — ⚙️ Settings Tab

Shows the current user profile and API connectivity status.
"""

import streamlit as st
from frontend.api_client import api_request, get_current_user


def settings_page() -> None:
    """Render the Settings page."""
    st.markdown(
        "<p style='font-size:1.5rem;font-weight:bold;color:#4472c4;"
        "border-bottom:2px solid #4472c4;padding-bottom:4px;'>⚙️ Settings</p>",
        unsafe_allow_html=True,
    )

    user = get_current_user()
    st.markdown("### 👤 User Profile")
    st.write(f"**Username:** {user.get('username', 'N/A')}")
    st.write(f"**Email:** {user.get('email', 'N/A')}")

    st.markdown("### 🌐 API Status")
    health = api_request("GET", "/api/health")
    if health:
        st.success(f"✅ API is healthy  ·  version {health.get('version', '?')}")
        st.caption(f"Last checked: {health.get('timestamp', '')}")
    else:
        st.error("❌ API is not responding. Check docker-compose logs.")
