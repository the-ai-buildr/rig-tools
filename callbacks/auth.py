"""Authentication callbacks: login, logout, and profile display.

Auth is validated against Supabase Auth (GoTrue) via ``sign_in_with_password``;
the app-specific role/flags come from the ``profiles`` table (loaded through the
user repository). The signed-in user — plus the Supabase access/refresh tokens —
is held in a session-scoped ``dcc.Store`` (``auth-store``); route gating lives in
``callbacks/theme.py``.
"""
import dash_mantine_components as dmc
from dash import Input, Output, State, no_update
from dash_iconify import DashIconify

from data.repositories import users as user_repo
from data.supabase_client import get_auth_client


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

        email = email.strip().lower()
        try:
            res = get_auth_client().auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception:
            return no_update, _error_alert("Invalid email or password."), no_update

        session = getattr(res, "session", None)
        user = getattr(res, "user", None)
        if not session or not user:
            return no_update, _error_alert("Invalid email or password."), no_update

        profile = user_repo.get_user(user.id)
        if profile is None or not profile.is_active:
            return (
                no_update,
                _error_alert("This account is inactive. Contact an administrator."),
                no_update,
            )

        data = {
            "user_id": user.id,
            "email": user.email or email,
            "username": profile.username,
            "full_name": profile.full_name,
            "role": profile.role,
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
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
        Output("auth-store", "data", allow_duplicate=True),
        Input("route-location", "pathname"),
        State("auth-store", "data"),
        prevent_initial_call=True,
    )
    def sync_auth_from_profile(_pathname, auth):
        """Refresh name/role from Supabase profiles so UI stays in sync with DB changes."""
        if not auth:
            return no_update

        user_id = auth.get("user_id")
        if not user_id:
            return no_update

        profile = user_repo.get_user(user_id)
        if profile is None or not profile.is_active:
            # User removed/deactivated in DB: clear session.
            return None

        merged = {
            **auth,
            "email": profile.email or auth.get("email"),
            "username": profile.username,
            "full_name": profile.full_name,
            "role": profile.role,
        }

        # Avoid unnecessary store writes.
        if (
            merged.get("email") == auth.get("email")
            and merged.get("username") == auth.get("username")
            and merged.get("full_name") == auth.get("full_name")
            and merged.get("role") == auth.get("role")
        ):
            return no_update

        return merged

    @app.callback(
        Output("profile-link", "label"),
        Output("profile-link", "description"),
        Input("auth-store", "data"),
    )
    def show_profile(auth):
        if not auth:
            return "Profile", None
        return (
            auth.get("full_name") or auth.get("username") or auth.get("email"),
            auth.get("role"),
        )
