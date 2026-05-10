import dash
from components.ui.theme_toggle import theme_toggle
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# app.layout = html.Div([
#     html.H1('Rig Tools'),
#     html.Div([
#         html.Div(
#             dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
#         ) for page in dash.page_registry.values()
#     ]),
#     dash.page_container
# ])

# logo = html.Div(DashIconify(icon="material:tools", width=30))

nav_bar = dmc.AppShellHeader(
            dmc.Group([
                    dmc.Burger(
                        id="burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    # dmc.Image(src=logo, h=40, flex=0),
                    dmc.Text("Rig-Tools", c="blue", fz="xl", fw=700, fs=22),
                    dmc.Space(style={"flex": 1}),
                    theme_toggle,
                ],
                h="70%",
                px="md",
                justify="space-between",
            )
        )

sidebar = dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=22, mt="sm", animate=True) for _ in range(15)],
            ],
            p="sm",
        )