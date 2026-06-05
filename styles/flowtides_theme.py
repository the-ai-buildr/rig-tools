"""
flowtides_theme.py

Dash Mantine Components (DMC v2 / Mantine v7) theme configuration.
Derived from FlowTides "Full Performance Stack" visual language.
Dark-first, electric-blue accent, high-density data layout.

Usage:
    from styles.flowtides_theme import (
        dmc_theme,
        PLOTLY_TEMPLATE_DARK, PLOTLY_TEMPLATE_LIGHT,
        SPAN_FULL, SPAN_HALF, SPAN_THIRD, SPAN_QUARTER,
        SPAN_SIDEBAR, SPAN_MAIN, GRID_GUTTER, APPSHELL_CONFIG,
        style_kpi_value, style_label_upper, style_card_featured_dark,
    )
"""

# ─────────────────────────────────────────────────────────────────
# 1. COLOR PALETTE
# ─────────────────────────────────────────────────────────────────

# Electric / Tactical Blue — shadcn/Tailwind blue scale (matches --brand #3b82f6)
BLUE = {
    1: "#EFF6FF",   # blue-50
    2: "#DBEAFE",   # blue-100
    3: "#BFDBFE",   # blue-200
    4: "#93C5FD",   # blue-300
    5: "#60A5FA",   # blue-400
    6: "#3B82F6",   # blue-500 — brand primary (matches --brand)
    7: "#2563EB",   # blue-600 — filled buttons / active
    8: "#1D4ED8",   # blue-700 — focus rings, pressed
    9: "#1E40AF",   # blue-800 — darkest
}

# Neutral / Navy
SLATE = {
    1:  "#F4F8FC",
    2:  "#E2ECF6",
    3:  "#C5D8EC",
    4:  "#8AAFC8",
    5:  "#5C7A96",
    6:  "#3A5068",
    7:  "#2B2D30",   # Border — bg-per-channel +30 ≈ 30% lighter than body bg
    8:  "#181C26",   # Card / Paper surface — clearly lighter than body bg
    9:  "#0D0F12",   # Body background — near-black, very slightly cool
    10: "#000000",   # Pure black — deepest pressed states
}

# Semantic
GREEN  = {4: "#4ADE80", 5: "#22C55E", 6: "#16A34A", 7: "#15803D"}
YELLOW = {4: "#FCD34D", 5: "#F59E0B", 6: "#D97706", 7: "#B45309"}
RED    = {4: "#F87171", 5: "#EF4444", 6: "#DC2626", 7: "#B91C1C"}
PURPLE = {4: "#C084FC", 5: "#A855F7", 6: "#9333EA", 7: "#7C3AED"}
CYAN   = {4: "#22D3EE", 5: "#06B6D4", 6: "#0891B2", 7: "#0E7490"}

# ─────────────────────────────────────────────────────────────────
# 2. TYPOGRAPHY
# ─────────────────────────────────────────────────────────────────

# shadcn/ui uses a single clean sans stack everywhere; mono reserved for numeric data.
FONT_DISPLAY = "Inter, 'Geist', ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
FONT_BODY    = "Inter, 'Geist', ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
FONT_MONO    = "'Geist Mono', ui-monospace, 'JetBrains Mono', 'SFMono-Regular', Menlo, monospace"

# ─────────────────────────────────────────────────────────────────
# 3. DMC THEME OBJECT
# Compatible with dash_mantine_components >= 2.0 (Mantine v7 API)
# ─────────────────────────────────────────────────────────────────

dmc_theme = {
    # Font families
    "fontFamily":          FONT_BODY,
    "fontFamilyMonospace": FONT_MONO,

    # Font sizes
    "fontSizes": {
        "xs": "0.6875rem",   # 11px — labels / metadata
        "sm": "0.75rem",     # 12px — secondary text
        "md": "0.875rem",    # 14px — body default
        "lg": "1.0rem",      # 16px — body large
        "xl": "1.125rem",    # 18px — heading sm
    },

    # Line heights
    "lineHeights": {
        "xs": "1.4",
        "sm": "1.5",
        "md": "1.6",
        "lg": "1.6",
        "xl": "1.5",
    },

    # Heading scale — Barlow Condensed
    "headings": {
        "fontFamily": FONT_DISPLAY,
        "fontWeight": "700",
        "sizes": {
            "h1": {"fontSize": "2.25rem",  "lineHeight": "1.05", "fontWeight": "800"},
            "h2": {"fontSize": "1.75rem",  "lineHeight": "1.15", "fontWeight": "700"},
            "h3": {"fontSize": "1.375rem", "lineHeight": "1.2",  "fontWeight": "600"},
            "h4": {"fontSize": "1.125rem", "lineHeight": "1.25", "fontWeight": "600"},
            "h5": {"fontSize": "0.875rem", "lineHeight": "1.3",  "fontWeight": "600"},
            "h6": {"fontSize": "0.75rem",  "lineHeight": "1.4",  "fontWeight": "600"},
        },
    },

    # Spacing — base-4 scale (xs–xl only; use raw CSS for larger gaps)
    "spacing": {
        "xs": "0.25rem",   #  4px
        "sm": "0.5rem",    #  8px
        "md": "1.0rem",    # 16px
        "lg": "1.5rem",    # 24px
        "xl": "2.0rem",    # 32px
    },

    # Breakpoints — Mantine v7 em-based
    "breakpoints": {
        "xs": "36em",    # 576px  — phones landscape
        "sm": "48em",    # 768px  — tablets portrait
        "md": "62em",    # 992px  — tablets landscape / small laptop
        "lg": "75em",    # 1200px — desktop
        "xl": "88em",    # 1408px — wide desktop
    },

    # Border radius — shadcn scale (derived from --radius: 0.5rem)
    "radius": {
        "xs":   "2px",
        "sm":   "4px",     # rounded-sm  (--radius - 4px)
        "md":   "6px",     # rounded-md  (--radius - 2px) — buttons, inputs
        "lg":   "8px",     # rounded-lg  (--radius)        — cards, popovers
        "xl":   "12px",    # larger surfaces / modals
        "full": "9999px",  # circular avatars
    },

    # Shadows — Tailwind-equivalent subtle set (no accent glow)
    "shadows": {
        "xs": "0 1px 2px 0 rgba(0,0,0,0.05)",
        "sm": "0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)",
        "md": "0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)",
        "lg": "0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)",
        "xl": "0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1)",
    },

    # Color overrides — Mantine v7 requires 10-shade arrays
    "colors": {
        # shadcn "neutral" dark palette — pure grayscale, no blue cast.
        # dark[7] = body bg (3.9%), dark[6] = card surface, dark[5] = border/muted (14.9%)
        "dark": [
            "#fafafa",  # dark[0] — foreground / lightest text on dark bg
            "#e5e5e5",  # dark[1]
            "#a3a3a3",  # dark[2] — muted-foreground (63.9%)
            "#737373",  # dark[3]
            "#404040",  # dark[4]
            "#262626",  # dark[5] — border / muted (14.9%)
            "#1c1c1c",  # dark[6] — card / Paper surface (slightly raised)
            "#0a0a0a",  # dark[7] — body background (3.9%)
            "#050505",  # dark[8]
            "#000000",  # dark[9] — pure black
        ],
        "blue": [
            BLUE[1], BLUE[2], BLUE[3], BLUE[4], BLUE[5],
            BLUE[6], BLUE[7], BLUE[8], BLUE[9],
            "#1E3A8A",  # shade 9 (index 9) — blue-900, deepest
        ],
        "slate": [
            SLATE[1], SLATE[2], SLATE[3], SLATE[4], SLATE[5],
            SLATE[6], SLATE[7], SLATE[8], SLATE[9], SLATE[10],
        ],
        "green": [
            "#F0FDF4", "#DCFCE7", "#BBF7D0", GREEN[4], GREEN[5],
            GREEN[6],  GREEN[7], "#166534", "#14532D", "#052E16",
        ],
        "yellow": [
            "#FFFBEB", "#FEF3C7", "#FDE68A", YELLOW[4], YELLOW[5],
            YELLOW[6], YELLOW[7], "#92400E", "#78350F", "#451A03",
        ],
        "red": [
            "#FFF1F2", "#FFE4E6", "#FECDD3", RED[4], RED[5],
            RED[6],   RED[7],   "#991B1B",  "#7F1D1D", "#450A0A",
        ],
    },

    # Primary — monochrome by default (near-black light / near-white dark).
    # The live accent color is injected via the --brand CSS var (see assets/styles.css
    # + the accent color picker), so primary surfaces follow the user's chosen accent.
    "primaryColor": "dark",
    "primaryShade": {"light": 9, "dark": 0},

    # Focus ring — visible for keyboard, hidden for mouse
    "focusRing": "auto",

    # Cursor
    "cursorType": "pointer",

    # Default radius for all components
    "defaultRadius": "sm",

    # Component-level overrides
    "components": {

        "AppShell": {
            "styles": {
                "main": {
                    "backgroundColor": "var(--mantine-color-body)",
                },
            },
        },

        # Card — hover handled in assets/styles.css via .mantine-Card-root:hover
        "Card": {
            "defaultProps": {
                "radius":     "lg",
                "padding":    "lg",
                "withBorder": True,
            },
        },

        "Button": {
            "defaultProps": {
                "radius": "md",
                "size":   "md",
            },
        },

        "Badge": {
            "defaultProps": {
                "radius": "sm",
                "size":   "sm",
            },
        },

        # Input / TextInput / Select — clean sans, shadcn radius + border
        "Input": {
            "defaultProps": {
                "radius": "md",
            },
            "styles": {
                "input": {
                    "fontFamily": FONT_BODY,
                    "fontSize":   "0.875rem",
                },
            },
        },

        "Table": {
            "defaultProps": {
                "striped":           False,
                "highlightOnHover":  True,
                "withTableBorder":   True,
                "withColumnBorders": False,
                "verticalSpacing":   "sm",
                "horizontalSpacing": "md",
            },
        },

        "Tooltip": {
            "defaultProps": {
                "radius":    "sm",
                "withArrow": True,
            },
        },

        "NavLink": {
            "defaultProps": {
                "radius":  "md",
                "variant": "subtle",
            },
        },

        "Tabs": {
            "defaultProps": {
                "radius": "sm",
            },
        },

        "Paper": {
            "defaultProps": {
                "radius":     "lg",
                "withBorder": True,
            },
        },

        "Notification": {
            "defaultProps": {
                "radius": "sm",
            },
        },

        "Progress": {
            "defaultProps": {
                "radius": "sm",
                "size":   "sm",
            },
        },

        "Loader": {
            "defaultProps": {
                "size":  "sm",
            },
        },
    },
}

# ─────────────────────────────────────────────────────────────────
# 4. CSS VARIABLE REFERENCE DICTS
# For documentation / manual injection — use double-hyphens (--).
# ─────────────────────────────────────────────────────────────────

DARK_CSS_VARS = {
    "--color-bg-base":       SLATE[10],     # #070C16
    "--color-bg-surface":    SLATE[9],      # #0C1525
    "--color-bg-elevated":   SLATE[8],      # #111E33
    "--color-bg-overlay":    "#1A2D4A",     # spec: not SLATE[7] (#1E3554)
    "--color-border":        SLATE[7],      # #1E3554
    "--color-border-subtle": "#162840",
    "--text-primary":        "#FFFFFF",
    "--text-secondary":      "#A8BDCF",
    "--text-muted":          SLATE[5],      # #5C7A96
    "--text-accent":         BLUE[5],       # #4A9EFF
    "--text-inverse":        SLATE[10],     # #070C16
    "--glow-blue":           "0 0 0 1px rgba(37,121,255,0.45), 0 0 30px rgba(37,121,255,0.18) inset",
    "--gradient-card":       f"linear-gradient(135deg, {SLATE[9]} 0%, {SLATE[8]} 100%)",
}

LIGHT_CSS_VARS = {
    "--color-bg-base":       "#EEF3F9",
    "--color-bg-surface":    "#FFFFFF",
    "--color-bg-elevated":   SLATE[1],      # #F4F8FC
    "--color-bg-overlay":    SLATE[2],      # #E2ECF6
    "--color-border":        SLATE[3],      # #C5D8EC
    "--color-border-subtle": SLATE[2],      # #E2ECF6
    "--text-primary":        SLATE[10],     # #070C16
    "--text-secondary":      SLATE[6],      # #3A5068
    "--text-muted":          SLATE[4],      # #8AAFC8
    "--text-accent":         BLUE[7],       # #1762DE
    "--text-inverse":        "#FFFFFF",
    "--glow-blue":           "0 0 0 1px rgba(19,85,204,0.35), 0 0 20px rgba(19,85,204,0.1) inset",
    "--gradient-card":       f"linear-gradient(135deg, #FFFFFF 0%, {SLATE[1]} 100%)",
}

# ─────────────────────────────────────────────────────────────────
# 5. PLOTLY FIGURE TEMPLATES
# Apply: fig.update_layout(**PLOTLY_TEMPLATE_DARK["layout"])
# ─────────────────────────────────────────────────────────────────

PLOTLY_TEMPLATE_DARK = {
    "layout": {
        "paper_bgcolor": SLATE[9],
        "plot_bgcolor":  SLATE[9],
        "font": {
            "family": FONT_BODY,
            "color":  "#A8BDCF",
            "size":   13,
        },
        "title": {
            "font": {
                "family": FONT_DISPLAY,
                "size":   20,
                "color":  "#FFFFFF",
            },
            "pad": {"l": 0, "t": 0},
        },
        "colorway": [
            BLUE[6],    # #2579FF — primary series
            GREEN[5],   # #22C55E
            YELLOW[5],  # #F59E0B
            RED[5],     # #EF4444
            PURPLE[5],  # #A855F7
            CYAN[5],    # #06B6D4
        ],
        "xaxis": {
            "gridcolor":     SLATE[7],
            "linecolor":     SLATE[7],
            "tickfont":      {"color": SLATE[5], "size": 11},
            "titlefont":     {"color": "#A8BDCF", "size": 12},
            "zerolinecolor": SLATE[7],
            "showgrid":      True,
            "gridwidth":     1,
        },
        "yaxis": {
            "gridcolor":     SLATE[7],
            "linecolor":     SLATE[7],
            "tickfont":      {"color": SLATE[5], "size": 11},
            "titlefont":     {"color": "#A8BDCF", "size": 12},
            "zerolinecolor": SLATE[7],
            "showgrid":      True,
            "gridwidth":     1,
        },
        "legend": {
            "bgcolor":       "rgba(7,12,22,0.75)",
            "bordercolor":   SLATE[7],
            "borderwidth":   1,
            "font":          {"color": "#A8BDCF", "size": 12},
            "itemsizing":    "constant",
            "tracegroupgap": 4,
        },
        "hoverlabel": {
            "bgcolor":    SLATE[8],
            "bordercolor": BLUE[6],
            "font":       {"family": FONT_BODY, "color": "#FFFFFF", "size": 12},
        },
        "margin": {"l": 48, "r": 16, "t": 40, "b": 40},
        "colorscale": {
            "sequential": [[0, SLATE[9]], [1, BLUE[6]]],
            "diverging":  [[0, RED[5]], [0.5, SLATE[8]], [1, BLUE[6]]],
        },
        "geo": {
            "bgcolor":      SLATE[9],
            "lakecolor":    SLATE[8],
            "landcolor":    SLATE[8],
            "subunitcolor": SLATE[7],
        },
    },
}

PLOTLY_TEMPLATE_LIGHT = {
    "layout": {
        "paper_bgcolor": "#FFFFFF",
        "plot_bgcolor":  SLATE[1],
        "font": {
            "family": FONT_BODY,
            "color":  SLATE[6],
            "size":   13,
        },
        "title": {
            "font": {
                "family": FONT_DISPLAY,
                "size":   20,
                "color":  SLATE[10],
            },
            "pad": {"l": 0, "t": 0},
        },
        "colorway": [
            BLUE[7],    # #1762DE — darker for light bg
            GREEN[6],   # #16A34A
            YELLOW[6],  # #D97706
            RED[6],     # #DC2626
            PURPLE[6],  # #9333EA
            CYAN[6],    # #0891B2
        ],
        "xaxis": {
            "gridcolor":     SLATE[2],
            "linecolor":     SLATE[3],
            "tickfont":      {"color": SLATE[4], "size": 11},
            "titlefont":     {"color": SLATE[6], "size": 12},
            "zerolinecolor": SLATE[3],
            "showgrid":      True,
            "gridwidth":     1,
        },
        "yaxis": {
            "gridcolor":     SLATE[2],
            "linecolor":     SLATE[3],
            "tickfont":      {"color": SLATE[4], "size": 11},
            "titlefont":     {"color": SLATE[6], "size": 12},
            "zerolinecolor": SLATE[3],
            "showgrid":      True,
            "gridwidth":     1,
        },
        "legend": {
            "bgcolor":       "rgba(255,255,255,0.9)",
            "bordercolor":   SLATE[3],
            "borderwidth":   1,
            "font":          {"color": SLATE[6], "size": 12},
            "itemsizing":    "constant",
            "tracegroupgap": 4,
        },
        "hoverlabel": {
            "bgcolor":     "#FFFFFF",
            "bordercolor": BLUE[7],
            "font":        {"family": FONT_BODY, "color": SLATE[10], "size": 12},
        },
        "margin": {"l": 48, "r": 16, "t": 40, "b": 40},
        "colorscale": {
            "sequential": [[0, SLATE[1]], [1, BLUE[7]]],
            "diverging":  [[0, RED[6]], [0.5, SLATE[2]], [1, BLUE[7]]],
        },
        "geo": {
            "bgcolor":      "#FFFFFF",
            "lakecolor":    SLATE[1],
            "landcolor":    SLATE[1],
            "subunitcolor": SLATE[3],
        },
    },
}

# ─────────────────────────────────────────────────────────────────
# 6. APPSHELL LAYOUT DEFAULTS
# ─────────────────────────────────────────────────────────────────

APPSHELL_CONFIG = {
    "header":  {"height": 42},   # slim profile — do not change
    "navbar":  {"width": 225, 
                "breakpoint": "sm", 
                "collapsed": {"mobile": True, "desktop": False},
                "font": {"family": FONT_BODY, "color": [1, BLUE[6]], "size": 16},
                },
    "padding": "md",
}

# Responsive GridCol spans — pass as span=SPAN_THIRD etc.
GRID_GUTTER  = {"base": "sm", "sm": "md", "lg": "lg"}

SPAN_FULL      = {"base": 12}
SPAN_HALF      = {"base": 12, "sm": 6}
SPAN_THIRD     = {"base": 12, "sm": 6, "md": 4}
SPAN_QUARTER   = {"base": 12, "sm": 6, "md": 3}
SPAN_SIDEBAR   = {"base": 12, "md": 3}
SPAN_MAIN      = {"base": 12, "md": 9}
SPAN_WIDE_MAIN = {"base": 12, "md": 8}
SPAN_NARROW    = {"base": 12, "md": 4}

# ─────────────────────────────────────────────────────────────────
# 7. INLINE STYLE HELPERS
# Pre-built dicts — spread into dmc component style={}
# ─────────────────────────────────────────────────────────────────

# Featured / accent card — flat surface with a subtle brand-accent border
style_card_featured_dark = {
    "background":  "hsl(var(--card))",
    "border":     "1px solid var(--brand)",
    "boxShadow":  "0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)",
}

style_card_featured_light = {
    "background":  "hsl(var(--card))",
    "border":     "1px solid var(--brand)",
    "boxShadow":  "0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)",
}

# KPI value text — mono, bold, large
style_kpi_value = {
    "fontFamily":    FONT_MONO,
    "fontWeight":    "700",
    "fontSize":      "1.75rem",
    "lineHeight":    "1.1",
    "letterSpacing": "-0.01em",
}

# Uppercase metric label above KPI value
style_label_upper = {
    "fontFamily":    FONT_BODY,
    "fontWeight":    "600",
    "fontSize":      "0.6875rem",
    "letterSpacing": "0.08em",
    "textTransform": "uppercase",
}

# Mono data cell — for table cells and numeric data
style_data_cell = {
    "fontFamily": FONT_MONO,
    "fontSize":   "0.8125rem",
}

# Section header with brand-accent left-border
style_section_header = {
    "borderLeft":   "3px solid var(--brand)",
    "paddingLeft":  "0.75rem",
    "marginBottom": "1.0rem",
}

# Divider line colors
style_divider_dark  = {"borderColor": SLATE[7]}
style_divider_light = {"borderColor": SLATE[3]}

# ─────────────────────────────────────────────────────────────────
# 8. EXPORTS
# ─────────────────────────────────────────────────────────────────

__all__ = [
    "dmc_theme",
    "DARK_CSS_VARS",
    "LIGHT_CSS_VARS",
    "PLOTLY_TEMPLATE_DARK",
    "PLOTLY_TEMPLATE_LIGHT",
    "APPSHELL_CONFIG",
    "GRID_GUTTER",
    "SPAN_FULL", "SPAN_HALF", "SPAN_THIRD", "SPAN_QUARTER",
    "SPAN_SIDEBAR", "SPAN_MAIN", "SPAN_WIDE_MAIN", "SPAN_NARROW",
    "style_card_featured_dark",
    "style_card_featured_light",
    "style_kpi_value",
    "style_label_upper",
    "style_data_cell",
    "style_section_header",
    "style_divider_dark",
    "style_divider_light",
    "BLUE", "SLATE", "GREEN", "YELLOW", "RED", "PURPLE", "CYAN",
    "FONT_DISPLAY", "FONT_BODY", "FONT_MONO",
]
