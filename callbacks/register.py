# Callbacks Registration function

def register_callbacks(app):
    from .theme import register_theme_callbacks

    register_theme_callbacks(app)