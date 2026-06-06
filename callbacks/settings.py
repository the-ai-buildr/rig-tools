"""Settings callbacks — load/save per-user preferences and global app settings.

Mirrors the data access style of ``callbacks/auth.py``: the signed-in user is
read from the ``auth-store`` and persistence goes straight through the
repository layer (same SQLite engine the REST API uses).
"""
from __future__ import annotations

import dash_mantine_components as dmc
from dash import Input, Output, State, no_update
from dash_iconify import DashIconify
from sqlmodel import Session

from data.db import engine
from data.repositories import app_settings as app_settings_repo
from data.repositories import users as user_repo


def _status(message: str, *, ok: bool = True):
    return dmc.Group(
        [
            DashIconify(
                icon="tabler:circle-check" if ok else "tabler:alert-triangle",
                width=18,
                color="var(--mantine-color-green-6)" if ok else "var(--mantine-color-red-6)",
            ),
            dmc.Text(message, size="sm", c="green" if ok else "red"),
        ],
        gap=6,
        align="center",
    )


def _effective(prefs: dict, app_settings) -> dict:
    """Resolve a user's effective settings, falling back to app defaults."""
    prefs = prefs or {}
    return {
        "color_scheme": prefs.get("color_scheme") or app_settings.default_color_scheme,
        "accent": prefs.get("accent") or app_settings.default_accent,
        "sidebar_collapsed": bool(prefs.get("sidebar_collapsed", False)),
        "units": prefs.get("units") or app_settings.default_units,
    }


def register_settings_callbacks(app):
    # ── Populate the settings form when the page opens ───────────────
    @app.callback(
        Output("prefs-color-scheme", "value"),
        Output("prefs-accent", "value"),
        Output("prefs-sidebar-collapsed", "checked"),
        Output("prefs-units", "value"),
        Output("account-name", "children"),
        Output("account-email", "children"),
        Output("account-role", "children"),
        Output("app-setting-name", "value"),
        Output("app-setting-default-scheme", "value"),
        Output("app-setting-default-accent", "value"),
        Output("app-setting-default-units", "value"),
        Output("app-setting-name", "disabled"),
        Output("app-setting-default-scheme", "disabled"),
        Output("app-setting-default-accent", "disabled"),
        Output("app-setting-default-units", "disabled"),
        Output("save-app-settings-btn", "disabled"),
        Output("app-settings-role-note", "children"),
        Input("route-location", "pathname"),
        Input("auth-store", "data"),
    )
    def populate_settings_form(pathname, auth):
        if pathname != "/settings" or not auth:
            return [no_update] * 17

        with Session(engine) as session:
            app_settings = app_settings_repo.get_app_settings(session)

        eff = _effective(auth.get("preferences"), app_settings)
        is_admin = (auth.get("role") or "").lower() == "admin"
        role_note = (
            None
            if is_admin
            else dmc.Alert(
                "Read-only — administrator access is required to edit app settings.",
                color="gray",
                variant="light",
                icon=DashIconify(icon="tabler:lock", width=18),
            )
        )

        return (
            eff["color_scheme"],
            eff["accent"],
            eff["sidebar_collapsed"],
            eff["units"],
            auth.get("full_name") or "—",
            auth.get("email") or "—",
            (auth.get("role") or "—").capitalize(),
            app_settings.app_name,
            app_settings.default_color_scheme,
            app_settings.default_accent,
            app_settings.default_units,
            not is_admin,
            not is_admin,
            not is_admin,
            not is_admin,
            not is_admin,
            role_note,
        )

    # ── Save per-user preferences ────────────────────────────────────
    @app.callback(
        Output("prefs-save-status", "children"),
        Output("auth-store", "data", allow_duplicate=True),
        Output("color-scheme-switch", "checked", allow_duplicate=True),
        Output("accent-store", "data", allow_duplicate=True),
        Input("save-prefs-btn", "n_clicks"),
        State("prefs-color-scheme", "value"),
        State("prefs-accent", "value"),
        State("prefs-sidebar-collapsed", "checked"),
        State("prefs-units", "value"),
        State("auth-store", "data"),
        prevent_initial_call=True,
    )
    def save_preferences(_clicks, color_scheme, accent, sidebar_collapsed, units, auth):
        if not auth or not auth.get("user_id"):
            return _status("You must be signed in to save.", ok=False), no_update, no_update, no_update

        prefs = {
            "color_scheme": color_scheme,
            "accent": accent,
            "sidebar_collapsed": bool(sidebar_collapsed),
            "units": units,
        }
        with Session(engine) as session:
            user = user_repo.update_user_preferences(session, auth["user_id"], prefs)
            if user is None:
                return _status("Could not save — user not found.", ok=False), no_update, no_update, no_update
            stored = dict(user.preferences or {})

        new_auth = dict(auth)
        new_auth["preferences"] = stored
        return (
            _status("Preferences saved."),
            new_auth,
            color_scheme == "dark",
            accent,
        )

    # ── Save global app settings (admin only) ────────────────────────
    @app.callback(
        Output("app-settings-save-status", "children"),
        Input("save-app-settings-btn", "n_clicks"),
        State("app-setting-name", "value"),
        State("app-setting-default-scheme", "value"),
        State("app-setting-default-accent", "value"),
        State("app-setting-default-units", "value"),
        State("auth-store", "data"),
        prevent_initial_call=True,
    )
    def save_app_settings(_clicks, app_name, default_scheme, default_accent, default_units, auth):
        if not auth or (auth.get("role") or "").lower() != "admin":
            return _status("Administrator access required.", ok=False)

        with Session(engine) as session:
            app_settings_repo.update_app_settings(
                session,
                app_name=app_name,
                default_color_scheme=default_scheme,
                default_accent=default_accent,
                default_units=default_units,
            )
        return _status("App settings saved.")
