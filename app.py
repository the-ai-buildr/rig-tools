import dash
import dash_mantine_components as dmc
from dash import Dash, dcc
from components.layouts.dashboard import nav_bar, sidebar
from callbacks.register import register_callbacks
from api import register_api
from styles.flowtides_theme import dmc_theme

# App Setup
app = Dash(
    __name__,
    backend="fastapi",
    use_pages=True,
    assets_folder="assets",
    suppress_callback_exceptions=True,
)

# Register callbacks & init db
register_callbacks(app)
register_api(app)

# Layout
body = dmc.AppShellMain(dmc.Box(), id="main-content")
    
layout = dmc.AppShell([
        nav_bar,
        sidebar,
        body,
    ],
    header={"height": 42},
    navbar={
        "width": {"base": 225, "md": 225, "lg": 225},
        "breakpoint": "sm",
        "collapsed": {"mobile": True, "desktop": False},
    },
    padding="sm",
    id="appshell",
    className="dmc",
)

app.layout = dmc.MantineProvider([
    dcc.Location(id="route-location", refresh=False),
    dcc.Store(id="auth-store", storage_type="session"),
    dcc.Store(id="accent-store", storage_type="local", data="blue"),
    dcc.Store(id="accent-dummy"),
    layout,
], id="theme-provider", theme=dmc_theme, forceColorScheme="light")


if __name__ == '__main__':
    import os

    # Local runs default to the dev environment (seeds the dev login user).
    # Plotly Cloud imports this module rather than executing __main__, so it
    # stays in production unless APP_ENV is set explicitly.
    os.environ.setdefault("APP_ENV", "dev")

    # Re-seed now that APP_ENV is set so the dev login user is provisioned
    # (seeding is idempotent).
    from data.seed import seed_default_users
    seed_default_users()

    app.run(debug=True)