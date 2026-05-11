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
                mr=10,
            ),
        ),
        dmc.PopoverDropdown(
            dmc.Stack(
                [
                    dmc.NavLink(
                        label="Profile",
                        leftSection=DashIconify(icon="tabler:user-square-rounded", width=16),
                        color="blue",
                        variant="subtle",
                        c='dimmed',
                    ),
                    dmc.NavLink(
                        label="Docs",
                        leftSection=DashIconify(icon="tabler:book-2", width=16),
                        color="blue",
                        variant="subtle",
                        href="#",
                        c='dimmed',
                        target="_blank",
                    ),
                    dmc.NavLink(
                        label="Theme",
                        leftSection=DashIconify(icon="tabler:sun-moon", width=16),
                        rightSection=theme_toggle,
                        color="blue",
                        c='dimmed',
                        variant="subtle",
                    ),
                    dmc.Divider(),
                    dmc.NavLink(
                        label="Settings",
                        leftSection=DashIconify(icon="tabler:settings", width=16),
                        variant="subtle",
                        c='dimmed',
                    ),
                    dmc.Divider(),
                    dmc.NavLink(
                        label="Sign out",
                        leftSection=DashIconify(icon="tabler:logout", width=16),
                        color="red",
                        variant="subtle",
                        c='dimmed',
                    ),
                ],
                gap=1,
            ),
            p="xs",
        ),
    ],
    position="left",
    withArrow=False,
    trapFocus=True,
    shadow="sm",
    width=220,
    keepMounted=True,
    withinPortal=True,
    # offset=4,
)