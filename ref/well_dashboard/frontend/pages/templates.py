"""
Templates Page — 📐 Templates Tab

Displays all available templates (prebuilt + user's custom) and allows
deletion of custom templates.
"""

import streamlit as st
from frontend.api_client import api_request


def templates_page() -> None:
    """Render the Templates page."""
    st.markdown(
        "<p style='font-size:1.5rem;font-weight:bold;color:#4472c4;"
        "border-bottom:2px solid #4472c4;padding-bottom:4px;'>📐 Well Templates</p>",
        unsafe_allow_html=True,
    )

    templates = api_request("GET", "/api/templates") or []

    if not templates:
        st.info("No templates available.")
        return

    # Group into prebuilt vs custom
    prebuilt = [t for t in templates if t["template_type"] == "prebuilt"]
    custom   = [t for t in templates if t["template_type"] != "prebuilt"]

    st.markdown("### 🏭 Pre-built Templates")
    for t in prebuilt:
        with st.expander(f"{t['template_name']}  ·  {t.get('category', '')}"):
            st.caption(t.get("description", "No description."))

    if custom:
        st.markdown("### 🛠️ Custom Templates")
        for t in custom:
            with st.expander(f"{t['template_name']}"):
                st.caption(t.get("description", "No description."))
                if st.button("🗑️ Delete", key=f"del_tmpl_{t['id']}"):
                    api_request("DELETE", f"/api/templates/{t['id']}")
                    st.success("Template deleted.")
                    st.rerun()
