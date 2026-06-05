import dash
import dash_mantine_components as dmc
from utils import page_body, page_header

dash.register_page(__name__, path="/tools/planner")

layout = page_body(
    page_header("Planner"),
)