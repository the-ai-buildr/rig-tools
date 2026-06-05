
import dash

from dash import Input, Output, State, ALL, ctx, no_update

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
        Input("route-location", "pathname"),
        Input("burger", "opened"),
    )
    def update_layout_for_route(pathname, opened):
        if pathname in (None, "", "/"):
            return LANDING_NAVBAR, "", landing_content("/home")

        # Burger "opened" toggles the desktop mini rail.
        if opened:
            return RAIL_NAVBAR, "rail", dash.page_container
        return BASE_NAVBAR, "", dash.page_container

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
        """
        function(accent) {
            var map = {
                blue:   "#3b82f6", violet: "#8b5cf6", green:  "#22c55e",
                amber:  "#f59e0b", orange: "#f97316", red:    "#ef4444",
                rose:   "#f43f5e", cyan:   "#06b6d4"
            };
            var root = document.documentElement;
            if (!accent || accent === "neutral") {
                root.style.setProperty("--brand", "hsl(var(--foreground))");
                root.style.setProperty("--brand-foreground", "hsl(var(--background))");
                root.style.setProperty("--brand-contrast", "hsl(var(--background))");
            } else {
                var c = map[accent] || map.blue;
                root.style.setProperty("--brand", c);
                root.style.setProperty("--brand-foreground", "#ffffff");
                root.style.setProperty("--brand-contrast", "#ffffff");
            }
            return "";
        }
        """,
        Output("accent-dummy", "data"),
        Input("accent-store", "data"),
    )