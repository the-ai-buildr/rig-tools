import dash
from dash import html

dash.register_page(__name__, path="/tools/scheduler")

layout = html.Div([
    html.H1('This is our Scheduler page'),
    html.Div('This is our Scheduler page content.'),
    ],
    className="dmc",
)