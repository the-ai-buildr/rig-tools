"""
Navigation link config.

To add a top-level page:
    Append an entry to NAV_ITEMS.

To add a sub-item under an existing parent:
    Add to its "children" list.

Entry shape:
    {
        "label": str,
        "icon":  str,          # tabler icon name, e.g. "tabler:home"
        "href":  str | None,   # None for parent-only accordion items
        "children": [...],     # optional — triggers accordion dropdown
    }
"""
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# ---------------------------------------------------------------------------
# Config — edit here to add / remove / reorder nav items
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    # Main sections
    {"label": "Dashboard", "icon": "tabler:layout-dashboard", "href": "/home",},
    {"label": "Setup", "icon": "tabler:building", "href": "/setup",},
    
    # Tools with sub-items
    {"label": "Tools","icon": "tabler:tools", "href": "/tools", "opened": True,
     "children": [
            {"label": "Digital Stamp", "icon": "tabler:mail-code",  "href": "/tools/digital-stamp"},
            {"label": "Templater",     "icon": "tabler:template",   "href": "/tools/templater"},
            {"label": "Scheduler",     "icon": "tabler:calendar-month",   "href": "/tools/scheduler"},
        ],
    },
]

# ---------------------------------------------------------------------------
# Builder — no need to touch this
# ---------------------------------------------------------------------------

def _build_link(item: dict, child: bool = False) -> dmc.NavLink:
    size = 16 if child else 20
    children = [_build_link(c, child=True) for c in item.get("children", [])]
    return dmc.NavLink(
        label=item["label"],
        leftSection=DashIconify(icon=item["icon"], width=size),
        variant="subtle",
        href=item.get("href"),
        active="exact" if item.get("href") else None,
        opened=item.get("opened"),
        childrenOffset=12 if children else None,
        children=children or None,
    )


nav_links = dmc.Stack(
    [_build_link(item) for item in NAV_ITEMS],
    gap=0,
    p="sm",
    style={"flex": 1},
)
