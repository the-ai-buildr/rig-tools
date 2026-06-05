# Callbacks Registration function

def register_callbacks(app):
    from .theme import register_theme_callbacks
    from components.ui.stepper import register_stepper_callbacks

    register_theme_callbacks(app)
    register_stepper_callbacks(app)