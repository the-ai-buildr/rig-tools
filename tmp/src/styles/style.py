"""
Global CSS injection helpers for the Rig Tools Streamlit app.

CSS lives in src/assets/style.css — edit that file to change styles.
Loading from a file (rather than an inline string) means the CSS is always
valid CSS syntax regardless of Python string escaping rules.

Produced by: frontend-agent / streamlit-components skill
"""
from pathlib import Path
import streamlit as st

_CSS_FILE = Path(__file__).resolve().parent.parent / "assets" / "style.css"


def apply_custom_css() -> None:
    """Inject global CSS into the current Streamlit page."""
    css = _CSS_FILE.read_text(encoding="utf-8")
    st.html(f"<style>{css}</style>")


def render_top_bar() -> None:
    """Render the fixed top navigation bar and inject its CSS."""
    st.markdown(
        """
        <div id="rig-top-bar">
            <span>🛢️ Rig Tools</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

