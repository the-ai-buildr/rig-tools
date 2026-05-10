import dash_mantine_components as dmc

from components.ui.theme_toggle import theme_toggle

NAVBAR_CONTENT_ID = "navbar-content"


def default_sidebar_content():
    return [
        dmc.Text("Sidebar", fw=600),
        dmc.Text("Add sidebar content in page register_page(..., sidebar=[...])", c="dimmed", size="sm"),
    ]


nav_bar = dmc.AppShellHeader(
    dmc.Group(
        [
            dmc.Burger(
                id="burger",
                size="sm",
                hiddenFrom="sm",
                opened=False,
            ),
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
    children=dmc.Stack(default_sidebar_content(), id=NAVBAR_CONTENT_ID, gap="sm"),
    p="sm",
)