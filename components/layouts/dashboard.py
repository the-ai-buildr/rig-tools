import dash_mantine_components as dmc
from dash_iconify import DashIconify

from components.ui.settings_popover import build_settings_popover
from components.ui.nav_links import nav_links
from components.ui.chat_drawer import chat_toggle

# Nav items are configured in components/ui/nav_links.py

nav_bar = dmc.AppShellHeader(
    dmc.Group(
        [
            dmc.Burger(
                id="burger",
                size="sm",
                opened=False,
            ),
            dmc.Group([
                    DashIconify(icon="tabler:cpu-2", width=24, color="hsl(var(--foreground))"),
                    dmc.Title("Rig Tools", c="hsl(var(--foreground))", order=3, lh=1),
                ],
                gap=6,
                ml="7px",
                align="center",
            ),
            dmc.Space(style={"flex": 1}),
            dmc.Group([
                    DashIconify(icon="tabler:brand-twitch", width=24, color="hsl(var(--foreground))", flip="horizontal"),
                    chat_toggle,
                ],
                gap=6,
                ml="7px",
                align="center",
            ),
        ],
        h="100%",
        px="md",
        justify="space-between",
        align="center",
    ),
    id="app-header",
)

# Sidebar footer — user avatar + name open the settings popover; the
# preferences icon on the right navigates to the Settings page.
footer_profile = dmc.Group(
    [
        dmc.Avatar(
            "··",
            id="footer-user-avatar",
            radius="md",
            size="sm",
            color="blue",
        ),
        dmc.Text(
            "User",
            id="footer-user-name",
            fw=500,
            size="sm",
            ml="8px",
            truncate=True,
        ),
    ],
    gap="xs",
    align="center",
    wrap="nowrap",
    style={"flex": 1, "cursor": "pointer", "minWidth": 0},
)

sidebar_footer = dmc.Group(
    [
        build_settings_popover(footer_profile, position="top"),
        dmc.Tooltip(
            label="Preferences",
            withArrow=True,
            children=dmc.Anchor(
                dmc.ActionIcon(
                    DashIconify(icon="tabler:settings", width=18),
                    id="footer-settings-link",
                    variant="subtle",
                    color="gray",
                    size="lg",
                ),
                href="/settings",
            ),
        ),
    ],
    justify="space-between",
    align="center",
    wrap="nowrap",
    px="sm",
    py="xs",
    className="rail-hide",
)

# Admin entry — gated to admin users via callback (callbacks/theme.py);
# hidden by default and shown just above the settings footer.
admin_link = dmc.Box(
    dmc.NavLink(
        label="Admin",
        leftSection=DashIconify(icon="tabler:shield-check", width=20),
        variant="subtle",
        active="exact",
        href="/admin",
    ),
    id="admin-nav-link",
    px="sm",
    pb="sm",
    display="none",
)

sidebar = dmc.AppShellNavbar(
    id="navbar",
    children=dmc.Flex([
            nav_links,
            admin_link,
            dmc.Divider(),
            sidebar_footer,
        ],
        direction="column",
        style={"height": "100%"},
    ),
    p=0, 
)