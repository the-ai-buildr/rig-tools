
import json

import dash

from dash import Input, Output, State, ALL, ctx, no_update

from styles.flowtides_theme import ACCENT_HEX_BY_KEY, DEFAULT_ACCENT_KEY
from utils import landing_content


BASE_NAVBAR = {
    "width": {"base": 225, "md": 225, "lg": 225},
    "breakpoint": "sm",
    "collapsed": {"mobile": True, "desktop": False},
}

# Collapsed desktop state = narrow icon-only rail (labels hidden via .rail CSS).
# On mobile the same toggle opens the full-width overlay instead.
RAIL_NAVBAR = {
    "width": {"base": 225, "md": 64, "lg": 64},
    "breakpoint": "sm",
    "collapsed": {"mobile": False, "desktop": False},
}

LANDING_NAVBAR = {
    "width": 0,
    "breakpoint": "sm",
    "collapsed": {"mobile": True, "desktop": True},
}

ACCENT_COLOR_MAP_JSON = json.dumps(ACCENT_HEX_BY_KEY, separators=(",", ":"))
ACCENT_CLIENT_CALLBACK = """
        function(accent) {
            var map = __MAP__;
            var root = document.documentElement;
            if (!accent || accent === "neutral") {
                root.style.setProperty("--brand", "hsl(var(--foreground))");
                root.style.setProperty("--brand-foreground", "hsl(var(--background))");
                root.style.setProperty("--brand-contrast", "hsl(var(--background))");
            } else {
                var c = map[accent] || map["__DEFAULT__"];
                root.style.setProperty("--brand", c);
                root.style.setProperty("--brand-foreground", "#ffffff");
                root.style.setProperty("--brand-contrast", "#ffffff");
            }
            return "";
        }
        """.replace("__MAP__", ACCENT_COLOR_MAP_JSON).replace("__DEFAULT__", DEFAULT_ACCENT_KEY)


def register_theme_callbacks(app):
    @app.callback(
        Output("theme-provider", "forceColorScheme"),
        Input("color-scheme-switch", "checked"),
    )
    def set_theme_color_scheme(switch_on):
        return "dark" if switch_on else "light"

    @app.callback(
        Output("appshell", "navbar"),
        Output("navbar", "className"),
        Output("main-content", "children"),
        Output("app-header", "style"),
        Output("route-location", "pathname", allow_duplicate=True),
        Input("route-location", "pathname"),
        Input("burger", "opened"),
        Input("auth-store", "data"),
        prevent_initial_call="initial_duplicate",
    )
    def update_layout_for_route(pathname, opened, auth):
        # Unauthenticated: hide app chrome and route to the /login page.
        # The login UI is served by pages/login.py through page_container
        # (a first-class route), not injected as a one-off view.
        if not auth:
            redirect = no_update if pathname == "/login" else "/login"
            return LANDING_NAVBAR, "", dash.page_container, {"display": "none"}, redirect

        # Authenticated user landing on /login → send them to the dashboard.
        if pathname == "/login":
            return BASE_NAVBAR, "", dash.page_container, None, "/home"

        # Admin pages are restricted to users with the admin role.
        if pathname and pathname.startswith("/admin") and auth.get("role") != "admin":
            return BASE_NAVBAR, "", dash.page_container, None, "/home"

        if pathname in (None, "", "/"):
            return LANDING_NAVBAR, "", landing_content("/home"), None, no_update

        # Burger "opened" toggles the desktop mini rail.
        if opened:
            return RAIL_NAVBAR, "rail", dash.page_container, None, no_update
        return BASE_NAVBAR, "", dash.page_container, None, no_update

    # ── Accent color picker ──────────────────────────────────────
    @app.callback(
        Output("accent-store", "data"),
        Input({"type": "accent-swatch", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def choose_accent(_clicks):
        triggered = ctx.triggered_id
        if not triggered:
            return no_update
        return triggered["index"]

    # Apply the chosen accent to --brand on :root (runs on load with the
    # persisted value, and on every swatch click).
    app.clientside_callback(
        ACCENT_CLIENT_CALLBACK,
        Output("accent-dummy", "data"),
        Input("accent-store", "data"),
    )