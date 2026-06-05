import dash
from dash import html
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from utils import page_header
from components.ui.metric_card import metric_card
from utils import page_header

dash.register_page(__name__, path="/settings")


layout = dmc.Box([
        page_header(
            "Settings",
            action=dmc.Button(
                "Create",
                id="create-settings-btn",
                leftSection=DashIconify(icon="tabler:plus", width=16),
                variant="subtle",
            ),
        ),
    ],
    p="sm",
)