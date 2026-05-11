# rig-tools Agent Instructions

## Project Overview

A multi-page oilfield operations dashboard built with **Plotly Dash 4 + FastAPI** backend and **Dash Mantine Components (DMC) v2** for all UI. Deployed on Plotly Cloud.

## Architecture

```
app.py              # Entry point — Dash app with FastAPI backend, use_pages=True
pages/              # One file per route, each calls dash.register_page(__name__, path="...")
components/
  layouts/          # App shell structure (nav_bar, sidebar)
  ui/               # Reusable UI widgets (metric_card, settings_popover, theme_toggle)
callbacks/
  register.py       # Central callback registration — import and call register_*_callbacks(app) here
  theme.py          # Theme/color-scheme callbacks
styles/theme.py     # Mantine theme dict (primaryColor=indigo, dark palette, component defaults)
api/routes/         # FastAPI route handlers added to app.server
data/               # Pad/well data directories
```

## Build and Run

```bash
# Activate venv
source .venv/bin/activate

# Run dev server
python app.py
```

## Conventions

### UI — always use DMC
- All layout and UI components come from `dash_mantine_components` (imported as `dmc`).
- Icons use `dash_iconify.DashIconify` with the **tabler** icon set. Browse: https://icon-sets.iconify.design/tabler/
- Never use plain `dash.html` elements where a DMC equivalent exists.

### Adding a new page
1. Create `pages/<name>.py` and call `dash.register_page(__name__, path="/<name>")`.
2. Export a `layout` variable (DMC component tree).
3. Add a `dmc.NavLink` entry in `components/layouts/dashboard.py`.

### Adding callbacks
- Define `register_<feature>_callbacks(app)` in `callbacks/<feature>.py`.
- Import and call it inside `register_callbacks()` in `callbacks/register.py`.

### Theme
- Primary color is `indigo`. Use `color="indigo"` on DMC components.
- The full theme dict lives in `styles/theme.py` — edit component `defaultProps` there rather than setting props on every instance.
- Dark mode custom palette is defined under `theme["colors"]["dark"]`.

### API endpoints
- Add FastAPI routes via `app.server` (the underlying FastAPI instance).
- Place route handlers in `api/routes/` and register them in `api/__init__.py`.

## Design System

Dark-first, electric-blue accent, high-density data layout. Source of truth: `styles/flowtides_theme.py`.

Import from it:
```python
from styles.flowtides_theme import (
    dmc_theme,
    PLOTLY_TEMPLATE_DARK, PLOTLY_TEMPLATE_LIGHT,
    SPAN_FULL, SPAN_HALF, SPAN_THIRD, SPAN_QUARTER,
    SPAN_SIDEBAR, SPAN_MAIN, GRID_GUTTER, APPSHELL_CONFIG,
    style_kpi_value, style_label_upper, style_card_featured_dark,
)
```

### Colors

| Role | Token | Value |
|------|-------|-------|
| Brand primary (dark) | `blue.6` | `#2579FF` |
| Brand primary (light) | `blue.7` | `#1762DE` |
| Page canvas (dark) | `slate.10` | `#070C16` |
| Card surface (dark) | `slate.9` | `#0C1525` |
| Card surface (light) | white | `#FFFFFF` |
| Default border (dark) | `slate.7` | `#1E3554` |

- `primaryColor = "blue"` — use `color="blue"` on all DMC components (replaces old `"indigo"`).
- Semantic: `green.5` success · `yellow.5` warning · `red.5` error.

### Typography

| Role | Font | Usage |
|------|------|-------|
| Display / headings | `Barlow Condensed` | KPI headers, section titles, chart titles |
| Body / labels | `DM Sans` | Prose, nav labels, descriptions |
| Mono / data | `JetBrains Mono` | KPI values, table cells, numeric data |

Load fonts via Google Fonts link in `assets/styles.css` or `external_stylesheets`.

### Component Defaults (defined in `dmc_theme["components"]`)

All defaults live in `styles/flowtides_theme.py` — set them there, not per-instance.

| Component | Key defaults |
|-----------|-------------|
| `Button` | `radius="sm"` (4 px, tactical) |
| `Card` | `radius="md"`, `padding="lg"`, `withBorder=True` |
| `Badge` | `radius="sm"`, `size="sm"` |
| `Table` | `highlightOnHover`, `withBorder`, no column borders |
| `NavLink` | `radius="sm"` — active fill = `blue.6` |
| `Input` | mono font for data entry |
| `Tooltip` | `withArrow=True`, `radius="sm"` |

### KPI / Stat Display Pattern

```python
dmc.Stack([
    dmc.Text("LABEL", style=style_label_upper, c="dimmed"),   # uppercase, tracked
    dmc.Text("4,280 bbl", style=style_kpi_value),             # mono, bold, 1.75 rem
    dmc.Badge("↑ 3.2%", color="green", variant="light"),      # trend delta
], gap=4)
```

### Plotly Figures

- Apply `PLOTLY_TEMPLATE_DARK` or `PLOTLY_TEMPLATE_LIGHT` via `fig.update_layout(**template["layout"])`.
- Switch template in the theme-toggle callback alongside `forceColorScheme`.
- Colorway: `blue.6 → green.5 → yellow.5 → red.5 → purple.5 → cyan.5`.

### Layout Helpers

```python
# Responsive GridCol spans — pass as span=SPAN_THIRD etc.
SPAN_FULL    = {"base": 12}
SPAN_HALF    = {"base": 12, "sm": 6}
SPAN_THIRD   = {"base": 12, "sm": 6, "md": 4}
SPAN_QUARTER = {"base": 12, "sm": 6, "md": 3}
SPAN_SIDEBAR = {"base": 12, "md": 3}
SPAN_MAIN    = {"base": 12, "md": 9}

GRID_GUTTER  = {"base": "sm", "sm": "md", "lg": "lg"}
```

### Inline Style Helpers

| Helper | Use on |
|--------|--------|
| `style_card_featured_dark/light` | Accent-glow hero cards |
| `style_kpi_value` | Stat/metric primary value |
| `style_label_upper` | Uppercase metric label above value |
| `style_data_cell` | Mono table cell text |
| `style_section_header` | Blue left-border section divider |

### Iconography

Library: `dash_iconify.DashIconify` — `icon="tabler:*"` preferred.

| Size | Context |
|------|---------|
| 16 px | Inline, nav labels |
| 20 px | Nav items |
| 24 px | Card headers |
| 32 px | Feature / hero |

Recommended icons: `tabler:bolt` · `tabler:chart-line` · `tabler:shield-check` · `tabler:activity` · `tabler:database` · `tabler:api`

### AppShell Config

```python
APPSHELL_CONFIG = {
    "header":  {"height": 42},   # slim profile — do not change
    "navbar":  {"width": 225, "breakpoint": "sm", "collapsed": {"mobile": True, "desktop": False}},
    "padding": "md",
}
```

### Sidebar Toggle Pattern

The `dmc.Burger` (id=`"burger"`) in the header is visible at **all** screen sizes — no `hiddenFrom`. It drives both desktop and mobile collapse via a single callback:

```python
# collapsed logic — burger.opened=False is the "rest" state
# desktop: sidebar open  | mobile: sidebar closed
# desktop: sidebar closed | mobile: sidebar open  (after clicking)
navbar["collapsed"] = {"mobile": not opened, "desktop": opened}
```

- Default (hamburger icon, `opened=False`): sidebar **open** on desktop, **closed** on mobile.
- Toggled (X icon, `opened=True`): sidebar **closed** on desktop, **open** on mobile.
- Callback lives in `callbacks/theme.py` → `update_layout_for_route`.

### Motion

- Hover cards: `translateY(-2px)` + border-color shift, `200ms ease`.
- Buttons: color + shadow only, `100ms` — no translate.
- Drawer/modal open: `300ms`. Nav fill: instant (0 ms).
- Always provide `prefers-reduced-motion` fallback; disable Plotly transitions there.

---

## Deployment (Plotly Cloud)

- Cloud may expect an entry file named after the app (e.g., `rig-tools.py`). Add a root shim that imports from `app.py` if needed.
- `requirements.txt` at root must list all dependencies — Plotly Cloud installs from it directly.
- See `/memories/repo/deploy-notes.md` for additional deployment gotchas.
