import dash
from dash import html
import dash_mantine_components as dmc
from components.ui.metric_card import metric_card
from components.ui.user_table import user_table
from utils import page_body, page_header

dash.register_page(__name__, path="/admin")

layout = page_body(
    page_header("Admin"),
    # Todo: add user and team metric cards from db
    dmc.Card(user_table, withBorder=True, radius="md", p="md", pt="10px"),
    # Todo: add team config table
)
