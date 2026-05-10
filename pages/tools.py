import dash
from dash import html

dash.register_page(__name__, path="/tools")

layout = html.Div([
    html.H1('This is our Tools page'),
    html.Div('This is our Tools page content.'),
    ],
    className="dmc",
)