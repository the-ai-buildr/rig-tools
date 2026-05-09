import dash
from dash import ( 
    Dash, html, dcc, 
    Input, Output, State,
    callback
)
import dash_mantine_components as dmc
from dash_iconify import DashIconify as dc

app = Dash(
    __name__,
    backend="fastapi",
    use_pages=True
)

# app.layout = html.Div([
#     html.H1('Rig Tools'),
#     html.Div([
#         html.Div(
#             dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
#         ) for page in dash.page_registry.values()
#     ]),
#     dash.page_container
# ])

# logo = html.Div(dc(icon="material:tools", width=30))

nav_bar = dmc.AppShellHeader(
            dmc.Group([
                    dmc.Burger(
                        id="burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    # dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="90%",
                px="md",
            )
        )

sidebar = dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=True) for _ in range(15)],
            ],
            p="md",
        )

body = dmc.AppShellMain("Main")
    
layout = dmc.AppShell([
        nav_bar,
        sidebar,
        body,
        dash.page_container
    ],
    header={
        "height": {"base": 42, "md": 42, "lg": 42},
    },
    navbar={
        "width": {"base": 225, "md": 225, "lg": 225},
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar

if __name__ == '__main__':
    app.run(debug=True)