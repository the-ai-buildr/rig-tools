import dash
from dash import html
import dash_mantine_components as dmc
from components.ui.metric_card import metric_card
from utils import page_body, page_header

dash.register_page(__name__, path="/home")


layout = page_body(
    page_header("Overview"),
    dmc.SimpleGrid(
        [
            metric_card("Active Wells", "12", "tabler:antenna", color="blue"),
            metric_card("Daily Footage", "4,280'", "tabler:chart-bar", color="blue"),
            metric_card("Rig Hours", "186 hrs", "tabler:clock", color="blue"),
            metric_card("Incidents", "0", "tabler:shield-check", color="blue"),
        ],
        cols={"base": 1, "sm": 2, "md": 4},
        spacing="sm",
    ),
)
