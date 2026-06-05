import dash_mantine_components as dmc
from dash_iconify import DashIconify

from components.ui.settings_popover import settings_popover
from components.ui.nav_links import nav_links

# Nav items are configured in components/ui/nav_links.py

settings_link = dmc.NavLink(
    label="Settings",
    leftSection=DashIconify(icon="tabler:settings", width=20),
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
                    DashIconify(icon="tabler:shield-chevron", width=26, color="var(--brand)"),
                    dmc.Title("Rig Tools", c="var(--brand)", order=2, lh=1),
                ],
                gap=6,
                ml="7px",
                align="center",
            ),
            dmc.Space(style={"flex": 1}),
            settings_popover,
        ],
        h="100%",
        px="md",
        justify="space-between",
        align="center",
    )
)

sidebar = dmc.AppShellNavbar(
    id="navbar",
    children=dmc.Flex([
            nav_links,
            dmc.Divider(),
            settings_link,
        ],
        direction="column",
        style={"height": "100%"},
    ),
    p=0, 
)