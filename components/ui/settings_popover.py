import dash_mantine_components as dmc
from dash_iconify import DashIconify

from components.ui.theme_toggle import theme_toggle
from styles.flowtides_theme import ACCENT_SWATCHES

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

settings_dropdown = dmc.PopoverDropdown(
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
            dmc.Group(
                [
                    dmc.Group(
                        [
                            DashIconify(icon="tabler:sun-moon", width=16),
                            dmc.Text("Theme", size="sm", c="dimmed"),
                        ],
                        gap="xs",
                    ),
                    theme_toggle,
                ],
                justify="space-between",
                align="center",
                px="xs",
                py=6,
            ),
            accent_picker,
            dmc.Divider(),
            dmc.NavLink(
                label="Settings",
                leftSection=DashIconify(icon="tabler:settings", width=16),
                variant="subtle",
                href="/settings",
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
)


def build_settings_popover(target, *, position="top", popover_id=None):
    """Wrap a target element in the shared settings popover.

    The dropdown content (profile, theme, accent, settings, sign-out) is the
    same regardless of where it is triggered from.
    """
    kwargs = {}
    if popover_id is not None:
        kwargs["id"] = popover_id
    return dmc.Popover(
        [
            dmc.PopoverTarget(target),
            settings_dropdown,
        ],
        position=position,
        withArrow=False,
        trapFocus=True,
        shadow="sm",
        width=240,
        keepMounted=True,
        withinPortal=True,
        **kwargs,
    )