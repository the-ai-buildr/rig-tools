# Skill: Building Streamlit Multipage Apps

<!--
Purpose: Multi-page app structure, navigation, and page-level state management.
Source: https://github.com/the-ai-buildr/st-agent-skills (building-streamlit-multipage-apps)
-->

## When to Use

Structuring multi-page Streamlit apps, navigation, and sharing state across pages.

## Rig Tools Note

Rig Tools uses the legacy `pages/` directory auto-discovery (not `st.navigation()` / `app_pages/`).
The patterns below apply to both approaches — respect the existing convention.

## Key Patterns

- **Directory:** use `app_pages/` (not `pages/`) in new apps to avoid auto-discovery conflicts; Rig Tools uses `pages/` — do not change.
- Entry point initializes global state and defines navigation **before** running pages.
- Few pages (3-7) → top navigation; many pages or nested sections → sidebar navigation.
- Group pages into sections; empty string key `""` for ungrouped pages appearing first.
- Programmatic navigation: `st.switch_page()`; individual links: `st.page_link()`.
- Use relative imports from the **root directory perspective**, not relative imports.
- Shared UI placed in the entry point (before `page.run()`) appears on all pages.

## State Across Pages

```python
# Initialize in entry point / global_init()
st.session_state.setdefault("unit_system", "us")
st.session_state.setdefault("auth_user", None)

# Page-specific state — use namespaced keys
st.session_state.setdefault("kill_sheet_depth", None)
st.session_state.setdefault("kill_sheet_results", None)

# Widgets are NOT stateful across pages — store the value, not the widget key
# WRONG: rely on widget key persisting
# RIGHT: store computed value in session state before page change
```

## Navigation Patterns

```python
# Programmatic navigation
if st.button("Go to Kill Sheet"):
    st.switch_page("pages/02_kill_sheet.py")

# Page link in sidebar
st.page_link("pages/02_kill_sheet.py", label="Kill Sheet", icon=":material/calculate:")
```
