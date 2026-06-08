import dash
import dash_mantine_components as dmc

from utils import page_body, page_header
from components.ui.schematic_card import schematic_card


dash.register_page(__name__, path="/test/schematic")


layout = page_body(
    page_header("Test Components"),
    schematic_card("Schematic Title", "Value", "tabler:device-laptop", color="gray")
)
