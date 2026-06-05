"""Digital Stamp page callbacks.

Builds the well-delivery stamp as an inline SVG from the form inputs, renders
a live preview (data-URI image), and stashes the raw SVG markup in a Store so
a clientside callback can rasterize it and copy a PNG to the clipboard.

No DB data yet — the page seeds the inputs with placeholder values.
"""
from __future__ import annotations

import base64
from html import escape

from dash import Input, Output, State, ClientsideFunction

# Palette tuned to the reference stamp (navy frame, blue values).
_NAVY = "#16335F"
_BLUE = "#2B5BA8"
_BOX_BG = "#F5F6F8"    # light gray fill for signature/date boxes
_BOX_LINE = "#C7CCD4"  # thin gray border

# Modern sans-serif stack matching the app body font.
_FONT = "'DM Sans', 'Segoe UI', system-ui, sans-serif"

# Canvas geometry.
_W, _H = 720, 272

# Preview/export heights (px) per size option.
_SIZE_HEIGHTS = {"lg": 400, "md": 300, "sm": 200}


def _row(label_x, value_x, value_end, y, label, value):
    """One label/value pair: bold navy label + blue underlined value."""
    label = escape(label)
    value = escape(value or "")
    return (
        f'<text x="{label_x}" y="{y}" text-anchor="end" '
        f'font-weight="600" font-size="14" fill="{_NAVY}">{label}</text>'
        f'<line x1="{value_x}" y1="{y + 5}" x2="{value_end}" y2="{y + 5}" '
        f'stroke="{_BOX_LINE}" stroke-width="1"/>'
        f'<text x="{(value_x + value_end) / 2:.0f}" y="{y}" text-anchor="middle" '
        f'font-size="13.5" fill="{_BLUE}">{value}</text>'
    )


def _build_svg(title, well, afe, rig, gfcm, name, cost, date) -> str:
    title = escape(title or "")

    # Two columns. The right (AFE / GFCM / Cost) column is wider to fit long
    # reference numbers; each tuple is (label_x, value_start, value_end).
    left = (108, 116, 300)    # width 184
    right = (392, 400, 700)   # width 300 — wide for long AFE values
    full_v0, full_v1 = left[1], right[2]  # signature/date span both columns

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_W}" height="{_H}" '
        f'viewBox="0 0 {_W} {_H}" font-family="{_FONT}">',
        f'<rect x="4" y="4" width="{_W - 8}" height="{_H - 8}" rx="14" ry="14" '
        f'fill="#ffffff" stroke="{_NAVY}" stroke-width="1"/>',
        # Title.
        f'<text x="{_W / 2:.0f}" y="44" text-anchor="middle" '
        f'font-weight="700" font-size="23" letter-spacing="0.3" fill="{_NAVY}">{title}</text>',
        # Row 1.
        _row(*left, 86, "Well Name:", well),
        _row(*right, 86, "AFE #:", afe),
        # Row 2.
        _row(*left, 118, "Rig Name:", rig),
        _row(*right, 118, "GFCM #:", gfcm),
        # Row 3.
        _row(*left, 150, "Print Name:", name),
        _row(*right, 150, "Cost Est:", cost),
        # Signature label + empty box (full width).
        f'<text x="{left[0]}" y="196" text-anchor="end" font-weight="600" '
        f'font-size="14" fill="{_NAVY}">Signature:</text>',
        f'<rect x="{full_v0}" y="180" width="{full_v1 - full_v0}" height="44" rx="6" ry="6" '
        f'fill="{_BOX_BG}" stroke="{_BOX_LINE}" stroke-width="0.5"/>',
        # Date label + value box (full width).
        f'<text x="{left[0]}" y="248" text-anchor="end" font-weight="600" '
        f'font-size="14" fill="{_NAVY}">Date:</text>',
        f'<rect x="{full_v0}" y="232" width="{full_v1 - full_v0}" height="26" rx="6" ry="6" '
        f'fill="{_BOX_BG}" stroke="{_BOX_LINE}" stroke-width="0.5"/>',
        f'<text x="{(full_v0 + full_v1) / 2:.0f}" y="249" text-anchor="middle" '
        f'font-size="13.5" fill="{_BLUE}">{escape(date or "")}</text>',
        "</svg>",
    ]
    return "".join(parts)


def register_digital_stamp_callbacks(app):
    @app.callback(
        Output("stamp-svg-store", "data"),
        Output("stamp-preview", "src"),
        Input("stamp-title", "value"),
        Input("stamp-well", "value"),
        Input("stamp-afe", "value"),
        Input("stamp-rig", "value"),
        Input("stamp-gfcm", "value"),
        Input("stamp-name", "value"),
        Input("stamp-cost", "value"),
        Input("stamp-date", "value"),
    )
    def _render(title, well, afe, rig, gfcm, name, cost, date):
        svg = _build_svg(title, well, afe, rig, gfcm, name, cost, date)
        b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        return svg, f"data:image/svg+xml;base64,{b64}"

    @app.callback(
        Output("stamp-preview", "h"),
        Input("stamp-size", "value"),
    )
    def _resize(size):
        return _SIZE_HEIGHTS.get(size, 400)

    app.clientside_callback(
        ClientsideFunction(namespace="digital_stamp", function_name="copy"),
        Output("stamp-copy-status", "children"),
        Input("stamp-copy-btn", "n_clicks"),
        State("stamp-svg-store", "data"),
        State("stamp-size", "value"),
        prevent_initial_call=True,
    )

    @app.callback(
        Output("stamp-title", "value"),
        Output("stamp-well", "value"),
        Output("stamp-afe", "value"),
        Output("stamp-rig", "value"),
        Output("stamp-gfcm", "value"),
        Output("stamp-name", "value"),
        Output("stamp-cost", "value"),
        Output("stamp-date", "value"),
        Input("stamp-clear-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def _clear(_n_clicks):
        return "", "", "", "", "", "", "", ""
