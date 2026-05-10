import dash
from dash import html

from utils import sidebar_links, sidebar_section

dash.register_page(
    __name__,
    path="/home",
    sidebar=sidebar_section(
        "Home",
        "Quick Actions",
        sidebar_links(["Overview", "Recent Jobs"], active_label="Overview"),
    ),
)

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
    ],
    className="dmc" 
)