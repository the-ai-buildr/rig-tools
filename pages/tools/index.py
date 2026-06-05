import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from styles.flowtides_theme import SPAN_THIRD
from utils import page_body, page_header

dash.register_page(__name__, path="/tools")


TOOLS = [
    {
        "label": "Digital Stamp",
        "description": "Generate and apply digital stamps to well documents.",
        "icon": "tabler:mail-code",
        "href": "/tools/digital-stamp",
    },
    {
        "label": "Templater",
        "description": "Build and manage reusable well templates.",
        "icon": "tabler:template",
        "href": "/tools/templater",
    },
    {
        "label": "Scheduler",
        "description": "Sync team schedules.",
        "icon": "tabler:calendar-month",
        "href": "/tools/scheduler",
    },{
        "label": "Planner",
        "description": "Plan and schedule rig operations and activities.",
        "icon": "tabler:calendar-month",
        "href": "/tools/planner",
    },{
        "label": "Plan of Action",
        "description": "Define and track the plan of action for rig operations.",
        "icon": "tabler:clipboard-list",
        "href": "/tools/poa",
    },{
        "label": "Safety",
        "description": "PSMS and Observational Safety tools.",
        "icon": "tabler:shield-check",
        "href": "/tools/safety",
    },
]


def _tool_card(tool: dict) -> dmc.Anchor:
    return dmc.Anchor(
        dmc.Card(
            [
                dmc.Group(
                    [
                        dmc.ThemeIcon(
                            DashIconify(icon=tool["icon"], width=20),
                            size="lg",
                            radius="md",
                            variant="light",
                            color="blue",
                        ),
                        dmc.Text(tool["label"], fw=600, size="sm"),
                    ],
                    gap="xs",
                    align="center",
                ),
                dmc.Text(tool["description"], size="xs", c="dimmed", mt="xs"),
            ],
            className="metric-card",
            radius="md",
            withBorder=True,
            p="sm",
            h="100%",
        ),
        href=tool["href"],
        underline="never",
        style={"display": "block", "height": "100%"},
    )


layout = page_body(
    page_header("Tools",),
    dmc.Grid(
        [
            dmc.GridCol(_tool_card(tool), span=SPAN_THIRD)
            for tool in TOOLS
        ],
        gutter="sm",
    ),
)