# Skill: HTMX Integration

<!--
Purpose: Patterns for HTMX requests hitting FastAPI HTML-fragment endpoints from Streamlit pages.
Produced by: frontend-agent + backend-agent
-->

## Purpose

Define every rule and pattern for wiring HTMX in Streamlit pages: embedding the HTMX script, writing FastAPI endpoints that return HTML fragments, passing auth tokens through HTMX headers, and handling HTMX responses.

## When to Use

Activate when the task contains: **htmx**, **partial**, **swap**, **hx-get**, **hx-post**, **hx-target**, **fragment endpoint**, or when touching `api/routes/partials.py` or any `components/` file that uses `st.html()`.

## Conventions

1. HTMX partial endpoints live in `api/routes/partials.py` and are prefixed `/api/partials`.
2. Every partial endpoint returns `HTMLResponse` — never JSON, never a full HTML page.
3. The HTMX `<script>` tag is embedded once per `st.html()` block — not once per component call.
4. Auth tokens are passed via `hx-headers='{"Authorization": "Bearer <token>"}'` — never in query strings.
5. HTMX targets use `id` attributes — never class selectors for swap targets.
6. HTMX partial endpoints must check the `HX-Request: true` header to confirm the caller is HTMX.
7. Partial endpoints require `Depends(get_current_user)` — no public HTMX partials for authenticated resources.
8. HTML fragments returned by FastAPI must be self-contained (no `<html>`, `<head>`, `<body>` tags).
9. Use `hx-indicator` to show a loading state during requests.
10. HTMX error responses (non-2xx) should return an HTML error fragment, not plain text; include the `HX-Reswap: none` header to prevent swapping on error if desired.

> **⚠️ HTMX version note:** Patterns use HTMX 1.9.x attributes. HTMX 2.0 changes the default
> swap strategy and removes some deprecated attributes. Pin the CDN version explicitly.
> Integrity hash shown is for 1.9.10 — verify at https://cdn.jsdelivr.net/npm/htmx.org if upgrading.

## Patterns

### HTMX partials router (`api/routes/partials.py`)

```python
# api/routes/partials.py
"""
FastAPI endpoints returning HTML fragments for HTMX consumption.
All endpoints require authentication. Return HTMLResponse only — no full pages.
Produced by: frontend-agent + backend-agent / htmx-integration skill
"""
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from supabase import Client

from api.db import items as items_db
from api.deps import get_current_user, get_user_db

router = APIRouter(prefix="/partials", tags=["HTMX Partials"])


def _require_htmx(hx_request: str | None = Header(default=None, alias="HX-Request")) -> None:
    """Dependency: Reject non-HTMX calls to partial endpoints."""
    if hx_request != "true":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This endpoint only accepts HTMX requests.",
        )


@router.get(
    "/items",
    response_class=HTMLResponse,
    dependencies=[Depends(_require_htmx)],
)
async def items_partial(
    db: Client = Depends(get_user_db),
    _user: dict = Depends(get_current_user),
) -> str:
    """
    Returns the items table rows as an HTML fragment.
    Swapped into <tbody id="items-tbody"> by the Streamlit component.
    """
    items, error = items_db.read_items(db)
    if error:
        return f'<tr><td colspan="3" class="htmx-error">Error: {error}</td></tr>'

    if not items:
        return '<tr><td colspan="3" style="color:#888;padding:8px;">No items found.</td></tr>'

    rows = []
    for item in items:
        item_id = item["id"]
        name = item["name"]
        qty = item.get("quantity", "—")
        rows.append(
            f'<tr id="item-row-{item_id}">'
            f'  <td style="padding:6px">{name}</td>'
            f'  <td style="padding:6px">{qty}</td>'
            f'  <td style="padding:6px">'
            f'    <button'
            f'      hx-delete="/api/partials/items/{item_id}"'
            f'      hx-target="#item-row-{item_id}"'
            f'      hx-swap="outerHTML"'
            f'      hx-confirm="Delete {name}?"'
            f'      style="color:red;cursor:pointer;background:none;border:none;"'
            f'    >✕</button>'
            f'  </td>'
            f'</tr>'
        )
    return "\n".join(rows)


@router.delete(
    "/items/{item_id}",
    response_class=HTMLResponse,
    dependencies=[Depends(_require_htmx)],
)
async def delete_item_partial(
    item_id: str,
    db: Client = Depends(get_user_db),
    _user: dict = Depends(get_current_user),
) -> str:
    """
    Deletes an item and returns an empty string.
    HTMX swaps the target row with outerHTML → empty = row removed.
    """
    success, error = items_db.delete_item(db, item_id)
    if not success:
        # Return error fragment in-place; do not remove the row
        return (
            f'<tr id="item-row-{item_id}">'
            f'  <td colspan="3" style="color:red">Delete failed: {error}</td>'
            f'</tr>'
        )
    return ""  # outerHTML swap with empty string removes the row


@router.post(
    "/items",
    response_class=HTMLResponse,
    dependencies=[Depends(_require_htmx)],
)
async def create_item_partial(
    request: Request,
    db: Client = Depends(get_user_db),
    current_user: dict = Depends(get_current_user),
) -> str:
    """
    Creates an item from HTMX form submission (application/x-www-form-urlencoded).
    Returns a new <tr> fragment to be prepended into the table body.
    """
    form = await request.form()
    name = str(form.get("name", "")).strip()
    quantity = int(form.get("quantity", 1))

    if not name:
        return '<tr><td colspan="3" style="color:red">Name is required.</td></tr>'

    data = {"name": name, "quantity": quantity, "user_id": str(current_user["user"].id)}
    item, error = items_db.create_item(db, data)
    if error or item is None:
        return f'<tr><td colspan="3" style="color:red">Error: {error}</td></tr>'

    item_id = item["id"]
    return (
        f'<tr id="item-row-{item_id}">'
        f'  <td style="padding:6px">{item["name"]}</td>'
        f'  <td style="padding:6px">{item.get("quantity", "—")}</td>'
        f'  <td style="padding:6px">'
        f'    <button'
        f'      hx-delete="/api/partials/items/{item_id}"'
        f'      hx-target="#item-row-{item_id}"'
        f'      hx-swap="outerHTML"'
        f'      hx-confirm="Delete {item["name"]}?"'
        f'      style="color:red;cursor:pointer;background:none;border:none;"'
        f'    >✕</button>'
        f'  </td>'
        f'</tr>'
    )
```

### Register partials router

```python
# api/routes/__init__.py — add this line inside register_routers()
from api.routes.partials import router as partials_router

# inside register_routers(app):
app.include_router(partials_router, prefix="/api", tags=["HTMX Partials"])
```

### Streamlit component using HTMX (`components/items/items_htmx_table.py`)

```python
# components/items/items_htmx_table.py
"""
HTMX-powered items table component.
Loads rows from /api/partials/items on mount; delete buttons fire in-place without Streamlit rerun.
Produced by: frontend-agent / htmx-integration skill
"""
import os

import streamlit as st


def items_htmx_table() -> None:
    """
    Render an HTMX-powered items table inside a Streamlit page.

    - Initial load: hx-get fires on 'load' trigger → populates tbody
    - Delete: hx-delete fires per row → swaps row with outerHTML (removes it)
    - Auth: Bearer token injected via hx-headers from session_state

    The HTMX script is included inline. Call this function at most once per page
    to avoid duplicate <script> tags.
    """
    token = st.session_state.get("auth_token", "")
    api_base = os.environ.get("API_BASE_URL", "http://localhost:8000")

    html = f"""
    <script
      src="https://unpkg.com/htmx.org@1.9.10"
      integrity="sha384-D1Kt99CQMDuVetoL1lrYwg5t+9QdHe7NLX/SoJYkXDFfX37iInKRy5ViYgSibmK"
      crossorigin="anonymous"
    ></script>

    <div id="htmx-items-wrapper" style="font-family:sans-serif;">
      <!-- Loading indicator -->
      <div id="items-loading" style="display:none;color:#888;" class="htmx-indicator">
        Loading items…
      </div>

      <table style="width:100%;border-collapse:collapse;font-size:0.9rem;">
        <thead>
          <tr style="border-bottom:2px solid #ddd;">
            <th style="text-align:left;padding:8px;">Name</th>
            <th style="text-align:left;padding:8px;">Qty</th>
            <th style="width:40px;"></th>
          </tr>
        </thead>
        <tbody
          id="items-tbody"
          hx-get="{api_base}/api/partials/items"
          hx-trigger="load, itemCreated from:body"
          hx-swap="innerHTML"
          hx-indicator="#items-loading"
          hx-headers='{{"Authorization": "Bearer {token}"}}'
        >
          <tr><td colspan="3" style="padding:8px;color:#aaa;">Loading…</td></tr>
        </tbody>
      </table>
    </div>
    """
    st.html(html)


def create_item_htmx_form() -> None:
    """
    HTMX form that submits to /api/partials/items (POST).
    On success, fires the 'itemCreated' event on <body> to trigger the table reload.
    """
    token = st.session_state.get("auth_token", "")
    api_base = os.environ.get("API_BASE_URL", "http://localhost:8000")

    html = f"""
    <form
      hx-post="{api_base}/api/partials/items"
      hx-target="#items-tbody"
      hx-swap="afterbegin"
      hx-headers='{{"Authorization": "Bearer {token}"}}'
      style="display:flex;gap:8px;margin-bottom:12px;align-items:flex-end;"
    >
      <div>
        <label style="font-size:0.8rem;display:block;">Name</label>
        <input name="name" type="text" required maxlength="120"
               style="padding:6px;border:1px solid #ccc;border-radius:4px;" />
      </div>
      <div>
        <label style="font-size:0.8rem;display:block;">Qty</label>
        <input name="quantity" type="number" value="1" min="0"
               style="padding:6px;width:70px;border:1px solid #ccc;border-radius:4px;" />
      </div>
      <button type="submit"
              style="padding:6px 14px;background:#2563eb;color:#fff;border:none;border-radius:4px;cursor:pointer;">
        Add
      </button>
    </form>
    """
    st.html(html)
```

### HTMX response headers helpers (`api/routes/partials.py` utilities)

```python
# Utility to add HTMX response headers in FastAPI

from fastapi.responses import HTMLResponse


def htmx_response(content: str, status_code: int = 200, **htmx_headers: str) -> HTMLResponse:
    """
    Return an HTMLResponse with optional HTMX response headers.

    Common htmx_headers:
      HX_Trigger="itemCreated"     — fire a client-side event
      HX_Reswap="none"             — cancel the swap (e.g., on soft error)
      HX_Redirect="/page"          — redirect via HTMX
      HX_Refresh="true"            — full page refresh
    """
    headers = {k.replace("_", "-"): v for k, v in htmx_headers.items()}
    return HTMLResponse(content=content, status_code=status_code, headers=headers)


# Usage example in a partial endpoint:
# return htmx_response("<tr>…</tr>", HX_Trigger="itemCreated")
```

## Anti-Patterns

- **Returning a full `<html>` page from a partial endpoint** — HTMX swaps the response into an existing element; a full page breaks layout.
- **Using class selectors as `hx-target`** — use `id` selectors to guarantee uniqueness.
- **Passing the auth token in query params** — tokens in URLs appear in logs; use `hx-headers`.
- **Embedding `<script src="htmx…">` once per loop iteration** — include it once per page render.
- **No `_require_htmx` dependency on partial endpoints** — without it, browser navigation hits the endpoint and renders orphaned HTML.
- **Returning JSON from a partial endpoint** — HTMX swaps raw response text; JSON will render as literal text.
- **Using `hx-swap="innerHTML"` on a `<tr>`** — `<tr>` requires `outerHTML` for replacement; `innerHTML` targets container elements like `<tbody>`, `<div>`.

## Checklist

- [ ] Partial endpoints in `api/routes/partials.py` under `/api/partials` prefix
- [ ] Every partial endpoint uses `response_class=HTMLResponse`
- [ ] `_require_htmx` dependency applied to all partial endpoints
- [ ] Protected partials use `Depends(get_current_user)` and `Depends(get_user_db)`
- [ ] Auth token passed via `hx-headers`, not query string
- [ ] HTMX `<script>` tag included once per `st.html()` block, not per component call
- [ ] `hx-target` uses `id` selectors
- [ ] Error responses return HTML error fragments (not plain text, not JSON)
- [ ] Partials router registered in `register_routers()` in `api/routes/__init__.py`
- [ ] CDN version pinned in `<script>` tag

## User Preferences

<!-- This section is updated during use. Start with defaults below. -->
- preferred_pattern: hx-get on load, hx-delete per row with outerHTML swap
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
