import dash
import dash_mantine_components as dmc

from utils import page_body, page_header
from components.ui.schematic_card import schematic_card


dash.register_page(__name__, path="/test/schematic")


layout = page_body(
    schematic_card("Benedum 3J 10H", "Active", "tabler:device-laptop", color="blue"),
    p=0,
    style={"height": "calc(100dvh - 42px - 2rem)"},
)
