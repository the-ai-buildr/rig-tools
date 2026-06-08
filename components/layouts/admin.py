import dash_mantine_components as dmc
from dash_iconify import DashIconify

from components.ui.settings_popover import build_settings_popover
from components.ui.nav_links import nav_links

# Nav items are configured in components/ui/nav_links.py

settings_link = dmc.NavLink(
    label="Settings",
    leftSection=DashIconify(icon="tabler:adjustments-horizontal", width=20),
    variant="subtle",
    active="exact",
    href="/settings",
)

nav_bar = dmc.AppShellHeader(
    dmc.Group(
        [
            dmc.Burger(
                id="burger",
                size="sm",
                opened=False,
            ),
            dmc.Group([
                    DashIconify(icon="tabler:shield-checkered", width=24),
                    dmc.Title("Rig Tools - Admin", order=3, lh=1),
                ],
                gap=6,
                ml="7px",
                align="center",
            ),
            dmc.Space(style={"flex": 1}),
            build_settings_popover(
                dmc.ActionIcon(
                    DashIconify(icon="tabler:settings", width=18),
                    variant="subtle",
                    size="lg",
                    mr=10,
                ),
                position="left",
            ),
        ],
        h="100%",
        px="md",
        justify="space-between",
        align="center",
    ),
    id="app-header",
)

sidebar = dmc.AppShellNavbar(
    id="navbar",
    children=dmc.Flex([
            nav_links,
            # Todo: Add back to dashboard sidebar link and make dynamic based on user role
            # only admin allowed to view this page.
            dmc.Divider(),
            settings_link,
        ],
        direction="column",
        style={"height": "100%"},
    ),
    p=0, 
)