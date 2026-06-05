import dash
import dash_mantine_components as dmc
from utils import page_body, page_header

dash.register_page(__name__, path="/tools/poa")

layout = page_body(
    page_header("Plan of Action"),
)