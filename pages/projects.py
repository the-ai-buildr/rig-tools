import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from components.ui.metric_card import metric_card
from utils import page_header

dash.register_page(__name__, path="/projects")

layout = dmc.Box([
        page_header(
            "Projects",
            action=dmc.Button(
                "Create",
                id="create-project-btn",
                leftSection=DashIconify(icon="tabler:plus", width=16),
                variant="subtle",
            ),
        ),
    ],
    p="sm",
)