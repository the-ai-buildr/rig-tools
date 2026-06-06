import dash
from dash import html
import dash_mantine_components as dmc
from components.ui.metric_card import metric_card
from utils import page_body, page_header

dash.register_page(__name__, path="/files")

layout = page_body(
    page_header("Files"),
)
