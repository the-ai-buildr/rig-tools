"""Login route.

The unauthenticated view is injected into ``main-content`` by the route-gating
callback in ``callbacks/theme.py``, so this page's own layout is only shown if a
user is already authenticated and navigates here directly. Registering the path
makes ``/login`` a first-class route (no SPA-catch-all reliance / 404).
"""
import dash
from components.ui.login import login_view

dash.register_page(__name__, path="/login", name="Login")

layout = login_view()
