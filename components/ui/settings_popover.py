import dash_mantine_components as dmc
from dash_iconify import DashIconify

from components.ui.theme_toggle import theme_toggle

settings_popover = dmc.Popover(
    [
        dmc.PopoverTarget(
            dmc.ActionIcon(
                DashIconify(icon="tabler:settings", width=18),
                variant="subtle",
                size="lg",
                id="settings-popover-btn",
            ),
        ),
        dmc.PopoverDropdown(
            dmc.Stack(
                [
                    dmc.NavLink(
                        label="Profile",
                        leftSection=DashIconify(icon="tabler:user-square-rounded", width=16),
                        color="indigo",
                        variant="subtle",
                    ),
                    dmc.NavLink(
                        label="Docs",
                        leftSection=DashIconify(icon="tabler:book-2", width=16),
                        color="indigo",
                        variant="subtle",
                        href="https://dash.plotly.com",
                        target="_blank",
                    ),
                    dmc.NavLink(
                        label="Theme",
                        leftSection=DashIconify(icon="tabler:sun-moon", width=16),
                        rightSection=theme_toggle,
                        color="indigo",
                        variant="subtle",
                    ),
                    dmc.Divider(),
                    dmc.NavLink(
                        label="Sign out",
                        leftSection=DashIconify(icon="tabler:logout", width=16),
                        color="red",
                        variant="subtle",
                    ),
                ],
                gap=2,
            ),
            p="xs",
        ),
    ],
    position="bottom-end",
    withArrow=True,
    shadow="md",
    width=220,
    keepMounted=True,
)