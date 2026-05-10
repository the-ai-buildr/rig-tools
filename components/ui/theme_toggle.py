import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify


theme_toggle = dmc.Switch(
    offLabel=DashIconify(icon="radix-icons:sun", width=15, color="var(--mantine-color-yellow-8)"),
    onLabel=DashIconify(icon="radix-icons:moon", width=15, color="var(--mantine-color-blue-6)"),
    id="color-scheme-switch",
    persistence=True,
    # color="grey",
    styles={
        "track": {
            "backgroundColor": "var(--mantine-color-dark-6)",
        }
    }
)