"""
Status Badge Component

Renders a coloured HTML <span> for a well's operational status.

Usage:
    from frontend.components.status_badge import status_badge, STATUS_OPTIONS

    st.markdown(status_badge("Drilling"), unsafe_allow_html=True)
"""

import streamlit as st

# Colour mapping for each status value
_COLOURS: dict[str, str] = {
    "Planned":   "#6c757d",
    "Spudded":   "#ffc107",
    "Drilling":  "#17a2b8",
    "Completed": "#28a745",
    "Suspended": "#fd7e14",
    "Abandoned": "#dc3545",
}

STATUS_OPTIONS = list(_COLOURS.keys())


def status_badge(status: str) -> str:
    """
    Return an HTML string rendering *status* as a coloured badge.

    Args:
        status: One of the keys in STATUS_OPTIONS.

    Returns:
        HTML ``<span>`` string; pass to ``st.markdown(..., unsafe_allow_html=True)``.
    """
    colour = _COLOURS.get(status, "#6c757d")
    return (
        f"<span style='color:{colour};font-weight:bold;"
        f"background:{colour}22;padding:2px 8px;border-radius:4px;'>"
        f"{status}</span>"
    )


def show_status_selector(current_status: str, key: str) -> str:
    """
    Render a selectbox pre-selected to *current_status*.

    Returns:
        The chosen status string.
    """
    idx = STATUS_OPTIONS.index(current_status) if current_status in STATUS_OPTIONS else 0
    return st.selectbox("Status", STATUS_OPTIONS, index=idx, key=key)
