# Skill: Streamlit Components

<!--
Purpose: Patterns for reusable UI components, st.fragment, and st.html in Rig Tools.
Produced by: frontend-agent
-->

## Purpose

Define every rule and pattern for building reusable Streamlit UI components, including `@st.fragment` partial rerenders and embedded `st.html` blocks.

## When to Use

Activate when the task contains: **component**, **fragment**, **widget**, **reusable**, `st.fragment`, or when touching `components/`.

## Conventions

1. Every component lives in `components/{feature}/{component_name}.py` — never inline in a page.
2. Components that rerender independently (e.g., a data table, a form with submit feedback) **must** use `@st.fragment`.
3. Components that are purely static layout helpers (headers, rules) are plain functions — do **not** wrap in `@st.fragment`.
4. Components call `frontend.api_client` wrappers for data — they never call Supabase or `calcs/` directly.
5. `@st.fragment` functions call `st.rerun(scope="fragment")` for self-contained updates, `st.rerun(scope="app")` only when the full page must update (e.g., after login).
6. Component functions are named in `snake_case` matching their file name.
7. All component files go in `__all__` and are re-exported from `components/layout.py` when appropriate.
8. HTMX-powered components embed the `<script>` tag once and use `st.html()` to render fragments.
9. Components receive only primitives or simple dicts as arguments — never mutable objects from another layer.

## Patterns

### Static layout component (no fragment)

```python
# components/utils.py
"""
Lightweight layout helpers — static, no rerender needed.
Produced by: frontend-agent / streamlit-components skill
"""
import streamlit as st


def horizontal_rule() -> None:
    """Renders a thin horizontal divider."""
    st.markdown("<hr style='margin: 0.5rem 0; border-color: #e0e0e0;'>", unsafe_allow_html=True)


def empty_state(message: str, icon: str = ":material/inbox:") -> None:
    """Renders a centered empty-state message."""
    st.markdown(
        f"<div style='text-align:center;padding:2rem;color:#888'>{icon} {message}</div>",
        unsafe_allow_html=True,
    )
```

### Data table with fragment rerender

```python
# components/items/items_table.py
"""
Items table component — renders a list of items with delete actions.
Rerenders independently via @st.fragment.
Produced by: frontend-agent / streamlit-components skill
"""
import streamlit as st

from frontend.api_client import api_request


@st.fragment
def items_table() -> None:
    """Displays items in a table; delete buttons rerender only this fragment."""
    token = st.session_state.get("auth_token")
    response = api_request("GET", "/items", token=token)

    if response is None:
        st.error("Failed to load items.")
        return

    items: list[dict] = response.get("items", [])

    if not items:
        st.info("No items yet. Use the form to create one.")
        return

    st.markdown(f"**{len(items)} item(s)**")

    for item in items:
        col_name, col_qty, col_action = st.columns([3, 1, 1])
        col_name.write(item["name"])
        col_qty.write(str(item.get("quantity", "—")))
        if col_action.button("Delete", key=f"del_{item['id']}"):
            result = api_request("DELETE", f"/items/{item['id']}", token=token)
            if result is not None:
                st.success("Deleted.")
                # Rerender only this fragment, not the full page
                st.rerun(scope="fragment")
            else:
                st.error("Delete failed.")
```

### Create form with fragment rerender

```python
# components/items/create_item_form.py
"""
Item creation form component — independent submit/feedback cycle.
Produced by: frontend-agent / streamlit-components skill
"""
import streamlit as st

from frontend.api_client import api_request


@st.fragment
def create_item_form() -> None:
    """Form for creating a new item; rerenders only this fragment on submit."""
    with st.form("create_item_form", clear_on_submit=True):
        st.subheader("New Item")
        name = st.text_input("Name", max_chars=120)
        quantity = st.number_input("Quantity", min_value=0, step=1, value=1)
        submitted = st.form_submit_button("Create")

    if submitted:
        if not name.strip():
            st.warning("Name is required.")
            return
        token = st.session_state.get("auth_token")
        result = api_request("POST", "/items", json={"name": name, "quantity": quantity}, token=token)
        if result is not None:
            st.success(f"Created: {result.get('name')}")
            st.rerun(scope="fragment")
        else:
            st.error("Failed to create item.")
```

### HTMX-enhanced component (Streamlit + st.html)

```python
# components/items/items_htmx.py
"""
HTMX-powered items list — uses FastAPI partials for live updates without full Streamlit rerun.
Produced by: frontend-agent / streamlit-components skill
"""
import streamlit as st

from api.config import settings  # Only to build the API URL — no business logic


def items_htmx_list(api_base_url: str) -> None:
    """
    Renders an HTMX-powered items table that polls FastAPI /api/partials/items.

    The HTMX script is embedded once. Targets /api/partials/items for the initial
    load and delete operations. Auth token is injected via hx-headers.
    """
    token = st.session_state.get("auth_token", "")

    html = f"""
    <script src="https://unpkg.com/htmx.org@1.9.10"
            integrity="sha384-D1Kt99CQMDuVetoL1lrYwg5t+9QdHe7NLX/SoJYkXDFfX37iInKRy5ViYgSibmK"
            crossorigin="anonymous"></script>

    <div id="items-htmx-root">
      <table style="width:100%;border-collapse:collapse;">
        <thead>
          <tr>
            <th style="text-align:left;padding:6px;">Name</th>
            <th style="text-align:left;padding:6px;">Qty</th>
            <th></th>
          </tr>
        </thead>
        <tbody
          hx-get="{api_base_url}/api/partials/items"
          hx-trigger="load"
          hx-swap="innerHTML"
          hx-headers='{{"Authorization": "Bearer {token}"}}'
        >
          <tr><td colspan="3" style="color:#888;padding:8px;">Loading…</td></tr>
        </tbody>
      </table>
    </div>
    """
    st.html(html)
```

### Login form component

```python
# components/auth/login_form.py
"""
Login form component — handles credential submission and session state update.
Produced by: frontend-agent / streamlit-components skill
"""
import streamlit as st

from frontend.api_client import api_request


@st.fragment
def login_form() -> None:
    """Renders login form; on success writes auth_token/auth_user to session_state."""
    with st.form("login_form"):
        st.subheader("Sign In")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")

    if submitted:
        if not email or not password:
            st.warning("Email and password are required.")
            return
        result = api_request("POST", "/auth/login", json={"email": email, "password": password})
        if result is None:
            st.error("Login failed. Check your credentials.")
            return
        st.session_state["auth_token"] = result["access_token"]
        st.session_state["auth_user"] = {"id": result["user_id"], "email": result["email"]}
        # Full page rerun to apply auth-guard logic on the current page
        st.rerun(scope="app")
```

## Anti-Patterns

- **`@st.fragment` on a static helper** (e.g., `horizontal_rule`) — adds overhead with no benefit.
- **`st.rerun(scope="app")` inside a fragment loop** — causes full-page reload for every iteration.
- **Passing mutable objects (lists, dicts from a DB call) as component arguments** — cache or fetch inside the component.
- **Accessing `st.session_state` mutably inside a loop** — read once before the loop.
- **Embedding `<script src="htmx…">` multiple times** — include it once per page, not per component call.
- **Using `st.experimental_rerun()`** — deprecated since 1.27; use `st.rerun()`.
- **Mixing Streamlit rendering and HTMX for the same element** — pick one update strategy per element.

## Checklist

- [ ] Component is in `components/{feature}/{name}.py`
- [ ] Component that rerenders independently uses `@st.fragment`
- [ ] Static helpers do NOT use `@st.fragment`
- [ ] `st.rerun(scope="fragment")` used for self-contained updates
- [ ] `st.rerun(scope="app")` used only when full-page state must update
- [ ] No direct Supabase or `calcs/` imports
- [ ] Auth token read from `st.session_state.get("auth_token")`
- [ ] HTMX `<script>` tag included at most once per rendered HTML block
- [ ] Component exported from `components/layout.py` if broadly reused

## User Preferences

<!-- This section is updated during use. Start with defaults below. -->
- preferred_pattern: @st.fragment with api_request
- style_overrides: {}
- avoid: []
- learned_corrections: []
- notes: []

### Self-Update Rules

1. When the user corrects output from this skill, append the correction to `learned_corrections` with date and context.
2. When the user expresses a preference, add it to `style_overrides`.
3. When a pattern causes an error traceable to a doc change, add the old pattern to `avoid` and update Patterns above.
4. Before generating any output, read the full User Preferences section and apply every entry.
5. After every 5 iterations, summarize `learned_corrections` into consolidated rules and prune resolved entries.
