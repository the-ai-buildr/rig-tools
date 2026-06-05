import dash
from dash import dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils import page_body, page_header

dash.register_page(__name__, path="/tools/digital-stamp")


# --- Placeholder defaults (no DB yet) ---------------------------------------
_DEFAULTS = {
    "title": "Permian Basin - Well Delivery",
    "well": "Benedum 3K 11H",
    "afe": "DD.2025.30892.CAP.DRL",
    "rig": "H&P 643",
    "gfcm": "46001103",
    "name": "Matt Williams",
    "cost": "$ 31,066.08",
    "date": "5/21/2026 6:00 AM",
}


# Widest default value drives the field width: "Permian Basin - Well Delivery"
# (29 chars) + 15% ≈ 33 ch, plus ~3 ch for the left icon padding.
_FIELD_WIDTH = "36ch"


def _field(label, field_id, default, icon, placeholder=""):
    return dmc.TextInput(
        id=field_id,
        label=label,
        value=default,
        placeholder=placeholder,
        leftSection=DashIconify(icon=icon, width=16),
        size="sm",
        w=_FIELD_WIDTH,
        maw="100%",
    )


# --- Left column: input form ------------------------------------------------
_inputs = dmc.Card(
    dmc.Stack(
        [
            dmc.Group(
                [
                    dmc.Text("Stamp Details", fw=600, size="lg"),
                    dmc.Button(
                        "Clear All",
                        id="stamp-clear-btn",
                        leftSection=DashIconify(icon="tabler:eraser", width=16),
                        size="xs",
                        variant="subtle",
                        color="gray",
                    ),
                ],
                justify="space-between",
                align="center",
            ),
            dmc.Divider(),
            _field("Stamp Title", "stamp-title", _DEFAULTS["title"], "tabler:heading"),
            _field("Well Name", "stamp-well", _DEFAULTS["well"], "tabler:antenna"),
            _field("AFE #", "stamp-afe", _DEFAULTS["afe"], "tabler:file-invoice"),
            _field("Rig Name", "stamp-rig", _DEFAULTS["rig"], "tabler:tower"),
            _field("GFCM #", "stamp-gfcm", _DEFAULTS["gfcm"], "tabler:hash"),
            _field("Print Name", "stamp-name", _DEFAULTS["name"], "tabler:user"),
            _field("Cost Est", "stamp-cost", _DEFAULTS["cost"], "tabler:currency-dollar"),
            _field("Date", "stamp-date", _DEFAULTS["date"], "tabler:calendar"),
        ],
        gap="sm",
    ),
    # Shrink the card to its content width rather than filling the grid column.
    w="fit-content",
    maw="100%",
)


# --- Right column: live preview + copy --------------------------------------
_preview = dmc.Card(
    dmc.Stack(
        [
            dmc.Group(
                [
                    dmc.Text("Preview", fw=600, size="lg"),
                    dmc.SegmentedControl(
                        id="stamp-size",
                        value="md",
                        data=[
                            {"label": "Large", "value": "lg"},
                            {"label": "Medium", "value": "md"},
                            {"label": "Small", "value": "sm"},
                        ],
                        size="xs",
                        color="blue",
                    ),
                    dmc.Button(
                        "Copy Image",
                        id="stamp-copy-btn",
                        leftSection=DashIconify(icon="tabler:clipboard", width=16),
                        size="xs",
                        variant="light",
                        color="blue",
                    ),
                ],
                justify="space-between",
                align="center",
            ),
            dmc.Divider(),
            dmc.Box(
                dmc.Image(
                    id="stamp-preview",
                    src="",
                    fit="contain",
                    h=300,
                    style={"maxWidth": "100%", "width": "auto"},
                ),
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "padding": "8px",
                    "width": "100%",
                    "backgroundColor": "var(--mantine-color-body)",
                    "borderRadius": "8px",
                },
            ),
            # Status row — fixed height so the copy message never shifts the image.
            dmc.Grid(
                [
                    dmc.GridCol(span=4),
                    dmc.GridCol(
                        dmc.Text(
                            "",
                            id="stamp-copy-status",
                            size="xs",
                            c="gray.5",
                            ta="center",
                        ),
                        span=4,
                    ),
                    dmc.GridCol(span=4),
                ],
                style={"minHeight": "18px"},
            ),
        ],
        gap="sm",
    ),
)


layout = page_body(
    page_header("Digital Stamp"),
    dmc.Grid(
        [
            dmc.GridCol(_inputs, span="content"),
            dmc.GridCol(_preview, span="auto"),
        ],
        gutter="sm",
    ),
    # Holds the raw SVG markup used by the clientside copy-to-clipboard callback.
    dcc.Store(id="stamp-svg-store"),
)
