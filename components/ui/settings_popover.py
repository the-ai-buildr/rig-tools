import dash_mantine_components as dmc
from dash_iconify import DashIconify

from components.ui.theme_toggle import theme_toggle

# Curated accent swatches — value drives the live --brand CSS var (clientside).
ACCENT_SWATCHES = [
    ("neutral", "#71717a"),
    ("blue",    "#3b82f6"),
    ("violet",  "#8b5cf6"),
    ("green",   "#22c55e"),
    ("amber",   "#f59e0b"),
    ("orange",  "#f97316"),
    ("red",     "#ef4444"),
    ("rose",    "#f43f5e"),
    ("cyan",    "#06b6d4"),
]


def _accent_swatch(key: str, color: str) -> dmc.Tooltip:
    return dmc.Tooltip(
        label=key.capitalize(),
        children=dmc.ActionIcon(
            id={"type": "accent-swatch", "index": key},
            variant="filled",
            radius="xl",
            size="md",
            className="accent-swatch",
            style={"backgroundColor": color},
            n_clicks=0,
        ),
    )


accent_picker = dmc.Stack(
    [
        dmc.Text("Accent", size="xs", c="dimmed", fw=600, tt="uppercase"),
        dmc.Group(
            [_accent_swatch(key, color) for key, color in ACCENT_SWATCHES],
            gap="xs",
        ),
    ],
    gap=6,
    px="xs",
    py=4,
)

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
                        id="profile-link",
                        leftSection=DashIconify(icon="tabler:user-square-rounded", width=16),
                        variant="subtle",
                        c='dimmed',
                    ),
                    dmc.NavLink(
                        label="Docs",
                        leftSection=DashIconify(icon="tabler:book-2", width=16),
                        variant="subtle",
                        href="#",
                        c='dimmed',
                        target="_blank",
                    ),
                    dmc.NavLink(
                        label="Theme",
                        leftSection=DashIconify(icon="tabler:sun-moon", width=16),
                        rightSection=theme_toggle,
                        c='dimmed',
                        variant="subtle",
                    ),
                    accent_picker,
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
                        id="sign-out-btn",
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
    # TODO: opooer glitches out on small screens
    position="left",
    withArrow=False,
    trapFocus=True,
    shadow="sm",
    width=240,
    keepMounted=True,
    withinPortal=True,
    # offset=4,
)