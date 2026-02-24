import streamlit as st
from styles.style import apply_custom_css
from pathlib import Path
import sys



def global_init():
    # Apply custom CSS globally
    apply_custom_css()

    # Add project root so styles can be imported (needed for Streamlit multipage / Pyodide)
    _project_root = Path(__file__).resolve().parent.parent
    if str(_project_root) not in sys.path:
        sys.path.insert(0, str(_project_root))
    
    return True
