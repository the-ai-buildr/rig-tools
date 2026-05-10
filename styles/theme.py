theme = {
    "primaryColor": "indigo",
    "primaryShade": {"light": 6, "dark": 8},
    "defaultRadius": "sm",
    "cursorType": "pointer",
    "colors": {
        "dark": [
            "#C9C9C9",
            "#b8b8b8",
            "#828282",
            "#696969",
            "#424242",
            "#3b3b3b",
            "#2e2e2e",
            "#242424",
            "#1f1f1f",
            "#141414",
        ],
        "indigo": [
            "#edf2ff",  # 0 — very light tint
            "#dbe4ff",  # 1
            "#bac8ff",  # 2
            "#91a7ff",  # 3
            "#748ffc",  # 4
            "#5c7cfa",  # 5
            "#4c6ef5",  # 6 — primary light (hover fill, active bg)
            "#4263eb",  # 7
            "#3b5bdb",  # 8 — primary dark (hover fill dark mode)
            "#364fc7",  # 9 — deep accent
        ],
    },
    "components": {
        "NavLink": {"defaultProps": {"color": "indigo", "variant": "subtle"}},
        "Button": {"defaultProps": {"fw": 400}},
        "Table": {
            "defaultProps": {
                "highlightOnHover": True,
                "withTableBorder": True,
                "verticalSpacing": "sm",
                "horizontalSpacing": "md",
            }
        },
    },
}
