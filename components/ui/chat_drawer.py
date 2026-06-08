"""Right-side chat panel.

Renders a placeholder chat shell that can appear in two modes:

* **overlay** — a ``dmc.Drawer`` that floats over the page content (unpinned).
* **pinned** — a ``dmc.AppShellAside`` that docks to the right and pushes the
  body. On screens below the ``md`` breakpoint the aside collapses into a
  slide-over overlay automatically and the pin control is hidden, so pinning is
  a desktop-only affordance.

The open/closed/pinned state machine lives in ``callbacks/chat.py`` and is
persisted through the ``chat-state-store`` local store (see ``app.py``).
"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify

# Shared width for both the docked aside and the floating drawer.
CHAT_WIDTH = 340

# Static placeholder conversation so the shell looks alive without any
# messaging logic wired up yet.
_PLACEHOLDER_MESSAGES = [
    ("assistant", "Hi! I'm your Rig Tools assistant. Ask me about wells, rigs, or reports."),
    ("user", "What's the status of the Benedum pad?"),
    ("assistant", "All three wells are drilling on schedule. Want a breakdown by section?"),
]


def _message_bubble(role: str, text: str):
    is_user = role == "user"
    return dmc.Group(
        dmc.Paper(
            dmc.Text(text, size="sm"),
            p="sm",
            radius="md",
            withBorder=not is_user,
            style={
                "maxWidth": "85%",
                "backgroundColor": "var(--mantine-color-blue-light)" if is_user else None,
            },
        ),
        justify="flex-end" if is_user else "flex-start",
        w="100%",
    )


def build_chat_panel(pinned: bool = False):
    """Return the chat panel content tree.

    ``pinned`` toggles the pin icon between its filled (pinned) and outline
    (unpinned) states. The panel is rendered into exactly one container at a
    time, so the inner component ids are never duplicated.
    """
    pin_icon = "tabler:pinned-filled" if pinned else "tabler:pin"

    header = dmc.Group(
        [
            dmc.Group(
                [
                    DashIconify(icon="tabler:message-circle", width=20),
                    dmc.Title("Chat", order=4, lh=1),
                ],
                gap=8,
                align="center",
            ),
            dmc.Group(
                [
                    dmc.Tooltip(
                        label="Pin to dashboard",
                        withArrow=True,
                        children=dmc.ActionIcon(
                            DashIconify(icon=pin_icon, width=18),
                            id="chat-pin-toggle",
                            variant="subtle",
                            color="gray",
                            visibleFrom="md",
                        ),
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon="tabler:x", width=18),
                        id="chat-close",
                        variant="subtle",
                        color="gray",
                    ),
                ],
                gap=4,
                align="center",
            ),
        ],
        justify="space-between",
        align="center",
        px="md",
        py="xs",
        wrap="nowrap",
    )

    messages = dmc.ScrollArea(
        dmc.Stack(
            [_message_bubble(role, text) for role, text in _PLACEHOLDER_MESSAGES],
            gap="sm",
            p="md",
        ),
        id="chat-messages",
        style={"flex": 1, "minHeight": 0},
        type="hover",
    )

    footer = dmc.Group(
        [
            dmc.TextInput(
                id="chat-input",
                placeholder="Type a message…",
                style={"flex": 1},
            ),
            dmc.ActionIcon(
                DashIconify(icon="tabler:send", width=18),
                id="chat-send",
                variant="filled",
                color="blue",
                size="lg",
            ),
        ],
        gap="xs",
        align="center",
        wrap="nowrap",
        px="md",
        py="sm",
    )

    return dmc.Flex(
        [
            header,
            dmc.Divider(),
            messages,
            dmc.Divider(),
            footer,
        ],
        direction="column",
        style={"height": "100%"},
    )


# Docked container — populated by the render callback when pinned.
chat_aside = dmc.AppShellAside(id="chat-aside", children=[], p=0)

# Floating container — populated by the render callback when in overlay mode.
# Fully controlled by the chat state store (see callbacks/chat.py): closing is
# done via the in-panel X button or the header toggle, so we disable the
# drawer's own outside-click close to keep its `opened` prop one-directional.
chat_drawer = dmc.Drawer(
    id="chat-drawer",
    position="right",
    size=CHAT_WIDTH,
    padding=0,
    withOverlay=False,
    withCloseButton=False,
    closeOnClickOutside=False,
    closeOnEscape=False,
    lockScroll=False,
    zIndex=200,
)

# Header toggle — opens the chat from anywhere via the app header.
chat_toggle = dmc.Tooltip(
    label="Chat",
    withArrow=True,
    children=dmc.ActionIcon(
        DashIconify(
            icon="tabler:brand-twitch",
            width=24,
            color="hsl(var(--foreground))",
            flip="horizontal",
        ),
        id="chat-toggle",
        variant="subtle",
        color="gray",
    ),
)
