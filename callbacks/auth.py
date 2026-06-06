"""
    Authentication callbacks: login, logout, and profile display.

    Auth is validated server-side against the SQLite users table via the
    repository layer (same data layer the REST API uses). The signed-in user
    is held in a session-scoped ``dcc.Store`` (``auth-store``); route gating
    lives in ``callbacks/theme.py``.
"""
import dash_mantine_components as dmc
from dash import Input, Output, State, no_update
from dash_iconify import DashIconify
from sqlmodel import Session

from data.db import engine
from data.repositories import users as user_repo


def _error_alert(message: str):
    return dmc.Alert(
        message,
        color="red",
        variant="light",
        icon=DashIconify(icon="tabler:alert-triangle", width=18),
        withCloseButton=False,
    )


def register_auth_callbacks(app):
    @app.callback(
        Output("auth-store", "data"),
        Output("login-alert", "children"),
        Output("route-location", "pathname"),
        Input("login-btn", "n_clicks"),
        State("login-email", "value"),
        State("login-password", "value"),
        prevent_initial_call=True,
    )
    def do_login(_clicks, email, password):
        if not email or not password:
            return no_update, _error_alert("Enter both email and password."), no_update
        with Session(engine) as session:
            user = user_repo.authenticate(session, email.strip().lower(), password)
            if user is None:
                return no_update, _error_alert("Invalid email or password."), no_update
            data = {
                "user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
            }
        return data, None, "/home"

    @app.callback(
        Output("auth-store", "data", allow_duplicate=True),
        Input("sign-out-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def do_logout(n_clicks):
        if not n_clicks:
            return no_update
        return None

    @app.callback(
        Output("profile-link", "label"),
        Output("profile-link", "description"),
        Input("auth-store", "data"),
    )
    def show_profile(auth):
        if not auth:
            return "Profile", None
        return auth.get("full_name") or auth.get("email"), auth.get("role")

    @app.callback(
        Output("footer-user-avatar", "children"),
        Output("footer-user-name", "children"),
        Input("auth-store", "data"),
    )
    def show_footer_user(auth):
        if not auth:
            return "··", "Guest"
        name = auth.get("full_name") or auth.get("email") or "User"
        parts = [p for p in name.replace(".", " ").replace("@", " ").split() if p]
        initials = "".join(p[0] for p in parts[:2]).upper() or name[0].upper()
        return initials, name

    @app.callback(
        Output("admin-nav-link", "display"),
        Input("auth-store", "data"),
    )
    def toggle_admin_link(auth):
        is_admin = bool(auth) and auth.get("role") == "admin"
        return "block" if is_admin else "none"
