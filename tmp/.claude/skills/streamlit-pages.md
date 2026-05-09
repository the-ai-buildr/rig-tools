# Skill: Streamlit Pages

<!--
Purpose: Conventions and patterns for creating and editing Streamlit multipage pages in Rig Tools.
Produced by: frontend-agent
-->

## Purpose

Define every rule and pattern for creating, editing, and structuring Streamlit pages in this project.

## When to Use

Activate when the task contains: **page**, **view**, **layout**, **UI**, or when touching any file in `pages/`.

## Conventions

1. Every page file is named `{NN}_{snake_case_name}.py` with a two-digit prefix.
2. `st.set_page_config` is **never called inside individual page files** — it is set once in `app.py`.
3. Every page calls `global_init()` as the first statement before any `st.*` calls.
4. Pages are **UI shells only** — they call components and `api_client` wrappers, never raw HTTP, never `calcs/`, never Supabase.
5. Heavy or independently-rerenable sections are extracted into `@st.fragment` components in `components/`.
6. A new page must be added to `nav_menu()` in `components/nav.py`.
7. All pages use `page_header(title, icon)` from `components/layout.py` — never roll a custom header.
8. Session state reads/writes use `st.session_state` with the project-namespaced keys from CLAUDE.md.
9. Auth-gated pages check `st.session_state.get("auth_token")` and redirect to login if absent.

## Patterns

### New page scaffold

```python
# pages/NN_{name}.py
"""
{Page title} page — {one-line description}.
Produced by: frontend-agent / streamlit-pages skill
"""
import streamlit as st

from components.layout import page_header, page_content, sidebar_header, sidebar_content
from utils.global_init import global_init

global_init()

# ── Auth guard (remove if page is public) ──────────────────────────────────
if not st.session_state.get("auth_token"):
    st.switch_page("pages/01_home.py")

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    sidebar_header("{Page Title}", ":material/settings:")
    with sidebar_content():
        pass  # Sidebar inputs go here

# ── Main ───────────────────────────────────────────────────────────────────
page_header("{Page Title}", ":material/article:")
with page_content():
    pass  # Page body goes here
```

### Auth-gated page with data loading

```python
# pages/05_items.py
"""
Items management page — lists, creates, and deletes items.
Produced by: frontend-agent / streamlit-pages skill
"""
import streamlit as st

from components.layout import page_header, page_content, sidebar_header
from components.items.items_table import items_table
from components.items.create_item_form import create_item_form
from utils.global_init import global_init

global_init()

if not st.session_state.get("auth_token"):
    st.warning("Please log in to continue.")
    st.switch_page("pages/03_login.py")

with st.sidebar:
    sidebar_header("Items", ":material/list:")
    with st.container():
        st.markdown("Manage your items below.")

page_header("Items", ":material/inventory:")
with page_content():
    col_form, col_table = st.columns([1, 2])
    with col_form:
        create_item_form()   # @st.fragment — rerenders independently
    with col_table:
        items_table()        # @st.fragment — rerenders independently
```

### Adding the page to nav

```python
# components/nav.py  — add inside nav_menu() popover
st.page_link("pages/05_items.py", label="Items", icon=":material/inventory:")
```

## Anti-Patterns

- **`import supabase` in a page file** — pages must not touch the DB layer.
- **Calling `api_request` directly in a page** — extract into a component or helper.
- **`st.set_page_config` in a page file** — it lives in `app.py` only.
- **Inline CSS or `st.markdown('<style>…</style>')` in a page** — CSS lives in `styles/style.py`.
- **Business logic in a page** — all logic belongs in `calcs/` (math) or `api/db/` (data).
- **Skipping `global_init()`** — CSS won't load and `sys.path` will be incomplete.

## Checklist

- [ ] File named `{NN}_{name}.py` with correct sequential prefix
- [ ] `global_init()` is the first call in the file
- [ ] `st.set_page_config` is NOT in this file
- [ ] Page has no direct Supabase imports
- [ ] Page has no direct `calcs/` imports
- [ ] Page uses `page_header()` and `page_content()` from `components/layout.py`
- [ ] Auth-gated pages redirect to login when `auth_token` is missing
- [ ] Page is registered in `nav_menu()` in `components/nav.py`
- [ ] Any independently-rerenable section is in an `@st.fragment` component

## User Preferences

<!-- This section is updated during use. Start with defaults below. -->
- preferred_pattern: scaffold from `pages/00_template.py`
- style_overrides: {}
- avoid: []
- learned_corrections: []
- notes: []

### Self-Update Rules

1. When the user corrects output from this skill, append the correction to `learned_corrections` with date and context.
2. When the user expresses a preference (e.g., "always use X instead of Y"), add it to `style_overrides`.
3. When a pattern causes an error traceable to a doc change, add the old pattern to `avoid` and update Patterns above.
4. Before generating any output, read the full User Preferences section and apply every entry. Never repeat a mistake listed in `learned_corrections`.
5. After every 5 iterations using this skill, summarize `learned_corrections` into consolidated rules and prune resolved entries.
