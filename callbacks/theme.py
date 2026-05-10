
import dash

from dash import Input, Output, State

from utils import landing_content


BASE_NAVBAR = {
    "width": {"base": 225, "md": 225, "lg": 200},
    "breakpoint": "sm",
    "collapsed": {"mobile": True},
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
        Output("main-content", "children"),
        Input("route-location", "pathname"),
        Input("burger", "opened"),
    )
    def update_layout_for_route(pathname, opened):
        if pathname in (None, "", "/"):
            return LANDING_NAVBAR, landing_content("/home")

        navbar = dict(BASE_NAVBAR)
        navbar["collapsed"] = {"mobile": not bool(opened)}
        return navbar, dash.page_container