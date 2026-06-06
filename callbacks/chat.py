"""Chat panel state machine.

A single persisted store (``chat-state-store``) holds one of three values:

* ``"closed"``  — panel hidden.
* ``"overlay"`` — floating ``dmc.Drawer`` over the content (unpinned).
* ``"pinned"``  — docked ``dmc.AppShellAside`` that pushes the body.

State is driven by two *input* callbacks and rendered by one *output* callback:

1. ``toggle_chat`` — the always-present header button opens / closes the panel.
2. ``panel_controls`` — the pin and close buttons that live *inside* the
   rendered panel. They are split into their own callback so the header toggle
   never references ids that are absent while the panel is closed (which would
   raise "nonexistent object" errors).
3. ``render_chat`` — maps the current state onto the aside/drawer props. It is
   the *sole* writer of ``chat-drawer.opened``; nothing reads that prop back
   into the store, which avoids a dependency cycle.
"""

import dash
from dash import Input, Output, State, no_update

from components.ui.chat_drawer import build_chat_panel, CHAT_WIDTH

ASIDE_HIDDEN = {"width": CHAT_WIDTH, "breakpoint": "md", "collapsed": {"mobile": True, "desktop": True}}
ASIDE_SHOWN = {"width": CHAT_WIDTH, "breakpoint": "md", "collapsed": {"mobile": False, "desktop": False}}


def register_chat_callbacks(app):
    # Header toggle — always present in the layout, so it is safe for this
    # callback to fire whether or not the panel is currently rendered.
    @app.callback(
        Output("chat-state-store", "data"),
        Input("chat-toggle", "n_clicks"),
        State("chat-state-store", "data"),
        prevent_initial_call=True,
    )
    def toggle_chat(_clicks, state):
        return "closed" if (state or "closed") != "closed" else "overlay"

    # Pin / close live inside the rendered panel. Keeping them in a separate
    # callback means they are only ever evaluated when the panel (and thus
    # these ids) exists.
    @app.callback(
        Output("chat-state-store", "data", allow_duplicate=True),
        Input("chat-pin-toggle", "n_clicks"),
        Input("chat-close", "n_clicks"),
        State("chat-state-store", "data"),
        prevent_initial_call=True,
    )
    def panel_controls(_pin, _close, state):
        state = state or "closed"
        if dash.ctx.triggered_id == "chat-close":
            return "closed"
        # Pin toggles between docked and floating.
        return "overlay" if state == "pinned" else "pinned"

    # Sole writer of chat-drawer.opened — one-directional, so no cycle.
    @app.callback(
        Output("appshell", "aside"),
        Output("chat-drawer", "opened"),
        Output("chat-aside", "children"),
        Output("chat-drawer", "children"),
        Input("chat-state-store", "data"),
    )
    def render_chat(state):
        state = state or "closed"

        if state == "pinned":
            return ASIDE_SHOWN, False, build_chat_panel(pinned=True), None
        if state == "overlay":
            return ASIDE_HIDDEN, True, None, build_chat_panel(pinned=False)
        return ASIDE_HIDDEN, False, None, None
