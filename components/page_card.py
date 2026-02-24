import streamlit as st

def card(content=None, footer=None, border=True):
    """Render a simple card with a main area and footer.

        content may be:
        - None: render an empty main area
        - str: render markdown text centered
        - callable: a function that accepts a single container argument and
        renders its content into that container (preferred)
        - a Streamlit DeltaGenerator: best-effort (if callable, it's called)
        """
    
    max_height = 250
    main_height = 160
    footer_height = max_height - main_height

    # Card - outer container
    cont_outer = st.container(border=border, height=max_height)

    with cont_outer:
        cont_main = st.container(vertical_alignment="top", horizontal_alignment="center", height=main_height, border=False)

        # Render content according to its type into cont_main
        if content is None:
            # keep empty main area
            pass
        elif isinstance(content, str):
            cont_main.markdown(content, text_alignment="center")
        elif callable(content):
            # Prefer callables that accept the container, otherwise run inside the container
            try:
                content(cont_main)
            except TypeError:
                with cont_main:
                    try:
                        content()
                    except Exception:
                        st.markdown(str(content), text_alignment="center")
        else:
            # Best-effort rendering for non-callable objects
            try:
                cont_main.markdown(str(content), text_alignment="center")
            except Exception:
                cont_main.markdown(str(content), text_alignment="center")

        # Footer area inside the outer container, fixed height to align bottom
        cont_footer = st.container(vertical_alignment="bottom", horizontal_alignment="center", height=footer_height, border=False)
        if isinstance(footer, str):
            cont_footer.markdown(footer, text_alignment="center")
        elif callable(footer):
            try:
                footer(cont_footer)
            except TypeError:
                with cont_footer:
                    try:
                        footer()
                    except Exception:
                        st.markdown(str(footer), text_alignment="center")

    # Return the inner main container so callers always receive a container
    return cont_main
