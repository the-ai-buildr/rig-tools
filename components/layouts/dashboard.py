import dash_mantine_components as dmc
from dash_iconify import DashIconify

from components.ui.settings_popover import settings_popover

# Icon packages:
# https://icon-sets.iconify.design/tabler/page-32.html?icon-filter=t&keyword=table

nav_links = dmc.Stack(
    [
        dmc.NavLink(
            label="Dashboard",
            leftSection=DashIconify(icon="tabler:layout-dashboard", width=16),
            color="indigo",
            variant="subtle",
            active="exact",
            href="/home",
        ),
        dmc.NavLink(
            label="Tools",
            leftSection=DashIconify(icon="tabler:tools", width=16),
            color="indigo",
            variant="subtle",
            active="exact",
            href="/tools",
        ),
        dmc.NavLink(
            label="Scheduler",
            leftSection=DashIconify(icon="tabler:calendar-month", width=16),
            color="indigo",
            variant="subtle",
            active="exact",
            href="/scheduler",
        ),
    ],
    gap=0,
    p="sm",
    style={"flex": 1},
)

settings_link = dmc.NavLink(
    label="Settings",
    leftSection=DashIconify(icon="tabler:settings", width=16),
    color="indigo",
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
                    DashIconify(icon="tabler:shield-chevron", width=30, color="var(--mantine-color-indigo-6)"),
                    dmc.Text(" Rig Apps", c="var(--mantine-color-indigo-6)", fz="xl", fw=900, lh=1),
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