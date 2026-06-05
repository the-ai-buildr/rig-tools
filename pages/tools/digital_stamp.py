import dash
from dash import html
import dash_mantine_components as dmc
from components.ui.metric_card import metric_card
from utils import page_body

dash.register_page(__name__, path="/tools/digital-stamp")


layout = page_body(
    dmc.Title("Digital Stamp", order=3, ml="5px", mb="5px"),
    dmc.Divider(mb="sm"),
)
