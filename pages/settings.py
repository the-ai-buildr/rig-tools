import dash
from dash import html

dash.register_page(__name__, path="/settings")

layout = html.Div([
    html.H1('This is our Settings page'),
    html.Div('This is our Settings page content.'),
    ],
    className="dmc"
)