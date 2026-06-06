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


def register_settings_callbacks(app):
    # ── Populate the settings form when the page opens ───────────────
    @app.callback(
        Output("account-name", "children"),
        Output("account-email", "children"),
        Output("account-role", "children"),
        Output("app-setting-default-scheme", "value"),
        Output("app-setting-default-accent", "value"),
        Output("app-setting-default-units", "value"),
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
            return [no_update] * 11

        with Session(engine) as session:
            app_settings = app_settings_repo.get_app_settings(session)

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
            auth.get("full_name") or "—",
            auth.get("email") or "—",
            (auth.get("role") or "—").capitalize(),
            app_settings.default_color_scheme,
            app_settings.default_accent,
            app_settings.default_units,
            not is_admin,
            not is_admin,
            not is_admin,
            not is_admin,
            role_note,
        )

    # ── Save global app settings (admin only) ────────────────────────
    @app.callback(
        Output("app-settings-save-status", "children"),
        Input("save-app-settings-btn", "n_clicks"),
        State("app-setting-default-scheme", "value"),
        State("app-setting-default-accent", "value"),
        State("app-setting-default-units", "value"),
        State("auth-store", "data"),
        prevent_initial_call=True,
    )
    def save_app_settings(_clicks, default_scheme, default_accent, default_units, auth):
        if not auth or (auth.get("role") or "").lower() != "admin":
            return _status("Administrator access required.", ok=False)

        with Session(engine) as session:
            app_settings_repo.update_app_settings(
                session,
                default_color_scheme=default_scheme,
                default_accent=default_accent,
                default_units=default_units,
            )
        return _status("App settings saved.")
