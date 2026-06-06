# Callbacks Registration function

def register_callbacks(app):
    from .theme import register_theme_callbacks
    from .auth import register_auth_callbacks
    from .projects import register_project_callbacks
    from .digital_stamp import register_digital_stamp_callbacks
    from .settings import register_settings_callbacks
    from components.ui.stepper import register_stepper_callbacks

    register_theme_callbacks(app)
    register_auth_callbacks(app)
    register_project_callbacks(app)
    register_digital_stamp_callbacks(app)
    register_settings_callbacks(app)
    register_stepper_callbacks(app)