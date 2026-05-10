import dash
import dash_mantine_components as dmc
from dash import Dash, dcc
from components.layouts.dashboard import nav_bar, sidebar
from callbacks.register import register_callbacks
from styles import theme

# App Setup
app = Dash(
    __name__,
    backend="fastapi",
    use_pages=True,
    assets_folder="assets",
    suppress_callback_exceptions=True,
)

# Register callbacks
register_callbacks(app)

# Layout
body = dmc.AppShellMain(dmc.Box(), id="main-content")
    
layout = dmc.AppShell(
    [
        nav_bar,
        sidebar,
        body,
    ],
    header={"height": 42},
    navbar={
        "width": {"base": 300, "md": 250, "lg": 200},
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    padding="sm",
    id="appshell",
    className="dmc",
)


app.layout = dmc.MantineProvider([
    dcc.Location(id="route-location", refresh=False),
    layout,
], id="theme-provider", theme=theme)


if __name__ == '__main__':
    app.run(debug=True)