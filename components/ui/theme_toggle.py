import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify


theme_toggle = dmc.Switch(
    offLabel=DashIconify(icon="tabler:sun", width=15, color="var(--mantine-color-yellow-6)"),
    onLabel=DashIconify(icon="tabler:moon", width=15, color="var(--mantine-color-blue-6)"),
    id="color-scheme-switch",
    persistence=True,
    color="gray",
    size="md",
)
