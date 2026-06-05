import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from styles.flowtides_theme import SPAN_THIRD, GRID_GUTTER
from utils import page_body, page_header

dash.register_page(__name__, path="/calculators")


CALCULATORS = [
    {
        "label": "FIT / LOT ",
        "description": "Calculate FIT / LOT values.",
        "icon": "tabler:wave-sine",
        "href": "/calculators/#",
    },
   
]


def _calculator_card(calculator: dict) -> dmc.Anchor:
    return dmc.Anchor(
        dmc.Card(
            [
                dmc.Group(
                    [
                        dmc.ThemeIcon(
                            DashIconify(icon=calculator["icon"], width=20),
                            size="lg",
                            radius="md",
                            variant="light",
                            color="blue",
                        ),
                        dmc.Text(calculator["label"], fw=600, size="sm"),
                    ],
                    gap="xs",
                    align="center",
                ),
                dmc.Text(calculator["description"], size="xs", c="dimmed", mt="xs"),
            ],
            className="metric-card",
            radius="md",
            withBorder=True,
            p="sm",
            h="100%",
        ),
        href=calculator["href"],
        underline="never",
        style={"display": "block", "height": "100%"},
    )


layout = page_body(
    page_header("Calculators",),
    dmc.Grid(
        [
            dmc.GridCol(_calculator_card(calculator), span=SPAN_THIRD)
            for calculator in CALCULATORS
        ],
        gutter=GRID_GUTTER,
    ),
)