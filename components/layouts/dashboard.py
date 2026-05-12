import dash_mantine_components as dmc
from dash_iconify import DashIconify

from components.ui.settings_popover import settings_popover

# Icon packages:
# https://icon-sets.iconify.design/tabler/page-32.html?icon-filter=t&keyword=table

nav_links = dmc.Stack([
        dmc.NavLink(
            label="Dashboard",
            leftSection=DashIconify(icon="tabler:layout-dashboard", width=20),
            color="blue",
            variant="subtle",
            active="exact",
            href="/home",
        ),
        dmc.NavLink(
            label="Setup",
            leftSection=DashIconify(icon="tabler:building", width=20),
            color="blue",
            variant="subtle",
            active="exact",
            href="/setup",
        ),
        dmc.NavLink(
            label="Tools",
            leftSection=DashIconify(icon="tabler:tools", width=20),
            color="blue",
            variant="subtle",
            childrenOffset=28,
            children=[
                dmc.NavLink(
                    label="Digital Stamp",
                    leftSection=DashIconify(icon="tabler:mail-code", width=16),
                    color="blue",
                    variant="subtle",
                    active="exact",
                    href="/tools/digital-stamp",
                ),
                dmc.NavLink(
                    label="Templater",
                    leftSection=DashIconify(icon="tabler:template", width=16),
                    color="blue",
                    variant="subtle",
                    active="exact",
                    href="/tools/templater",
                ),
                dmc.NavLink(
                    label="Scheduler",
                    leftSection=DashIconify(icon="tabler:calendar-month", width=20),
                    color="blue",
                    variant="subtle",
                    active="exact",
                    href="/scheduler",
                ),
            ],
        ),
   
    ],
    gap=0,
    p="sm",
    style={"flex": 1},
)

settings_link = dmc.NavLink(
    label="Settings",
    leftSection=DashIconify(icon="tabler:settings", width=20),
    color="blue",
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
            dmc.Group(
                [
                    DashIconify(icon="tabler:shield-chevron", width=26, color="var(--mantine-color-blue-6)"),
                    dmc.Title("Rig Apps", c="var(--mantine-color-blue-6)", order=2, lh=1),
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
    children=dmc.Flex(
        [
            nav_links,
            dmc.Divider(),
            settings_link,
        ],
        direction="column",
        style={"height": "100%"},
    ),
    p=0, 
)