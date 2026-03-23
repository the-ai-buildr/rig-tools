# Skill: Creating Streamlit Themes

<!--
Purpose: Theming via .streamlit/config.toml — colors, fonts, borders, light/dark modes.
Source: https://github.com/the-ai-buildr/st-agent-skills (creating-streamlit-themes)
-->

## When to Use

Changing app colors, fonts, borders, or appearance. Customizing light/dark mode.

## Critical Rule

**NO custom CSS for theming.** Do NOT use `st.markdown(..., unsafe_allow_html=True)` with `<style>` blocks
or `st.html()` with style blocks for theming. Use `.streamlit/config.toml` only.
If custom CSS is explicitly requested, target elements with `key=` parameter → `.st-key-{key}` CSS class.

## config.toml Structure

All theming goes under `[theme]` in `.streamlit/config.toml`:

```toml
[theme]
base = "light"   # "light" | "dark" | path/URL to external .toml

# Core colors
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
linkColor = "#0066CC"
codeTextColor = "#333"
codeBackgroundColor = "#F0F2F6"
borderColor = "#D1D5DB"

# Semantic palette (optional)
redColor = "#FF4B4B"
greenColor = "#21C354"
blueColor = "#0066CC"
# Optional variants: redBackgroundColor, redTextColor, etc.

# Charts
chartCategoricalColors = ["#0066CC", "#FF6B6B", "#21C354", "#FFD700"]
chartSequentialColors = ["#EFF6FF", "#DBEAFE", "#BFDBFE", "#93C5FD", "#60A5FA",
                          "#3B82F6", "#2563EB", "#1D4ED8", "#1E40AF", "#1E3A8A"]  # exactly 10

# Typography
font = "sans-serif"   # "sans-serif" | "serif" | "monospace" | Google Fonts URL
headingFont = "sans-serif"
codeFont = "monospace"
baseFontSize = "16px"
baseFontWeight = "400"
headingFontSizes = ["2rem", "1.5rem", "1.25rem"]
headingFontWeights = ["700", "600", "500"]
linkUnderline = true

# Borders & radius
baseRadius = "0.5rem"
buttonRadius = "0.5rem"
showWidgetBorder = true
showSidebarBorder = true

[theme.sidebar]
backgroundColor = "#1A1A2E"
textColor = "#FFFFFF"

# Light/dark mode — BOTH must be defined for users to toggle
[theme.light]
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"

[theme.dark]
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
```

## Detect Active Theme

```python
if st.context.theme.base == "dark":
    # dark-mode specific logic
```

## Custom Fonts

Google Fonts URL syntax:
```toml
font = "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700"
```

Self-hosted fonts go in `static/` and are referenced via `[[theme.fontFaces]]`:
```toml
[[theme.fontFaces]]
family = "MyFont"
url = "app/static/my-font.woff2"
weight = "400"
```

> `fontFaces` changes require a server restart. Most other theme options hot-reload.

## Available Theme Templates

`snowflake`, `dracula`, `nord`, `stripe`, `solarized-light`, `spotify`, `github`, `minimal`
(from source repo's `templates/themes/`).
