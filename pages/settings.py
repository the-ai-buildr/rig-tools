import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from components.ui.settings_popover import ACCENT_SWATCHES
from utils import page_body, page_header

dash.register_page(__name__, path="/settings")

SCHEME_OPTIONS = [
    {"label": "Dark", "value": "dark"},
    {"label": "Light", "value": "light"},
]

UNITS_OPTIONS = [
    {"label": "Imperial", "value": "imperial"},
    {"label": "Metric", "value": "metric"},
]

ACCENT_OPTIONS = [
    {"label": key.capitalize(), "value": key} for key, _ in ACCENT_SWATCHES
]


def _section(title, description, *children):
    return dmc.Card(
        dmc.Stack(
            [
                dmc.Box(
                    [
                        dmc.Text(title, fw=700, size="lg"),
                        dmc.Text(description, c="dimmed", size="sm"),
                    ]
                ),
                dmc.Divider(),
                *children,
            ],
            gap="md",
        ),
    )


account_section = _section(
    "Account",
    "Your signed-in profile details.",
    dmc.SimpleGrid(
        cols={"base": 1, "sm": 3},
        children=[
            dmc.Box(
                [
                    dmc.Text("Name", size="xs", c="dimmed", tt="uppercase", fw=600),
                    dmc.Text("—", id="account-name", fw=500),
                ]
            ),
            dmc.Box(
                [
                    dmc.Text("Email", size="xs", c="dimmed", tt="uppercase", fw=600),
                    dmc.Text("—", id="account-email", fw=500),
                ]
            ),
            dmc.Box(
                [
                    dmc.Text("Role", size="xs", c="dimmed", tt="uppercase", fw=600),
                    dmc.Text("—", id="account-role", fw=500),
                ]
            ),
        ],
    ),
)


app_settings_section = _section(
    "App Settings",
    "Organization-wide defaults. Editable by administrators only.",
    dmc.Box(id="app-settings-role-note"),
    dmc.Group(
        [
            dmc.Text("Default color scheme", w=200, fw=500),
            dmc.SegmentedControl(
                id="app-setting-default-scheme",
                data=SCHEME_OPTIONS,
                value="dark",
            ),
        ],
        justify="space-between",
    ),
    dmc.Group(
        [
            dmc.Text("Default accent color", w=200, fw=500),
            dmc.Select(
                id="app-setting-default-accent",
                data=ACCENT_OPTIONS,
                value="blue",
                w=180,
                allowDeselect=False,
            ),
        ],
        justify="space-between",
    ),
    dmc.Group(
        [
            dmc.Text("Default measurement units", w=200, fw=500),
            dmc.SegmentedControl(
                id="app-setting-default-units",
                data=UNITS_OPTIONS,
                value="imperial",
            ),
        ],
        justify="space-between",
    ),
    dmc.Group(
        [
            dmc.Box(id="app-settings-save-status"),
            dmc.Button(
                "Save app settings",
                id="save-app-settings-btn",
                variant="default",
                leftSection=DashIconify(icon="tabler:device-floppy", width=16),
                disabled=True,
            ),
        ],
        justify="flex-end",
    ),
)


layout = page_body(
    page_header("Settings"),
    dmc.Stack(
        [
            account_section,
            app_settings_section,
        ],
        gap="md",
        maw=820,
    ),
)