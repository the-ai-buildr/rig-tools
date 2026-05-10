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
                    dmc.Group(
                        [
                            DashIconify(icon="tabler:user-square-rounded", width=16),
                            dmc.Text("Profile", size="sm"),
                        ],
                        gap="sm",
                        style={"cursor": "pointer"},
                    ),
                    dmc.Divider(),
                    dmc.Group(
                        [
                            DashIconify(icon="tabler:book-2", width=16),
                            dmc.Text("Docs", size="sm"),
                        ],
                        gap="sm",
                        style={"cursor": "pointer"},
                    ),
                    dmc.Group(
                        [
                            dmc.Group(
                                [
                                    DashIconify(icon="tabler:sun-moon", width=16),
                                    dmc.Text("Theme", size="sm"),
                                ],
                                gap="sm",
                            ),
                            theme_toggle,
                        ],
                        justify="space-between",
                    ),
                    dmc.Divider(),
                    dmc.Group(
                        [
                            DashIconify(icon="tabler:logout", width=16, color="var(--mantine-color-red-6)"),
                            dmc.Text("Sign out", size="sm", c="red"),
                        ],
                        gap="sm",
                        style={"cursor": "pointer"},
                    ),
                ],
                gap="xs",
            ),
            p="sm",
        ),
    ],
    position="bottom-end",
    withArrow=True,
    shadow="md",
    width=220,
    keepMounted=True,
)