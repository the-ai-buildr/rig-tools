import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from styles.flowtides_theme import SPAN_THIRD, GRID_GUTTER
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
        "description": "Plan and schedule rig operations and activities.",
        "icon": "tabler:calendar-month",
        "href": "/tools/scheduler",
    },{
        "label": "Planner",
        "description": "Plan and schedule rig operations and activities.",
        "icon": "tabler:calendar-month",
        "href": "/tools/planner",
    },
]


def _tool_card(tool: dict) -> dmc.Anchor:
    return dmc.Anchor(
        dmc.Card(
            [
                dmc.Group(
                    [
                        dmc.ThemeIcon(
                            DashIconify(icon=tool["icon"], width=24),
                            size="xl",
                            radius="md",
                            variant="light",
                            color="blue",
                        ),
                        dmc.Text(tool["label"], fw=600, size="lg"),
                    ],
                    gap="sm",
                    align="center",
                ),
                dmc.Text(tool["description"], size="sm", c="dimmed", mt="sm"),
            ],
            className="metric-card",
            h="100%",
        ),
        href=tool["href"],
        underline="never",
        style={"display": "block", "height": "100%"},
    )


layout = page_body(
    page_header(
        "Tools",
        action=dmc.Button(
            "Create",
            id="create-tools-btn",
        ),
    ),
    dmc.Divider(mb="md"),
    dmc.Grid(
        [
            dmc.GridCol(_tool_card(tool), span=SPAN_THIRD)
            for tool in TOOLS
        ],
        gutter=GRID_GUTTER,
    ),
)