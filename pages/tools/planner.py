import dash
from dash import html

dash.register_page(__name__, path="/tools/planner")

layout = html.Div([
    html.H1('This is our Planner page'),
    html.Div('This is our Planner page content.'),
    ],
    className="dmc",
)