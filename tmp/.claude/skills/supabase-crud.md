# Skill: Supabase CRUD

<!--
Purpose: Patterns for the api/db/ service layer — Supabase table CRUD consumed by FastAPI routes.
Produced by: backend-agent
-->

## Purpose

Define every rule and pattern for building the Supabase query layer in `api/db/`, the client singleton in `services/supabase.py`, and how routes consume them.

## When to Use

Activate when the task contains: **crud**, **database**, **table**, **query**, **supabase**, **row**, or when touching `api/db/`, `services/supabase.py`, or adding a new Supabase table.

## Conventions

1. One file per Supabase table: `api/db/{table_name}.py`. Exports exactly: `create_`, `read_s`, `read_`, `update_`, `delete_`.
2. All functions take `client: Client` as their first argument — never create clients internally.
3. All functions return `(data, error)` tuples — never raise exceptions out of `api/db/`.
4. Every function has a full type signature and docstring.
5. The service-role client (`get_supabase_client()`) bypasses RLS — must be accompanied by comment: `# SERVICE ROLE: bypasses RLS — [reason]`.
6. The user-scoped client (`get_user_supabase_client(jwt)`) respects RLS — use for all user-facing data operations.
7. `services/supabase.py` contains the one and only client instantiation logic.
8. The singleton is `@lru_cache(maxsize=1)` — one service-role client per process lifetime.
9. User-scoped clients are created per request (cheap — just sets the auth header on an existing connection pool).
10. Filter dicts use equality matching by default; complex filters (range, ilike) use explicit chaining.

> **⚠️ supabase-py v2 note:** `response.data` is always a `list[dict]`. Single-row operations
> return a one-element list — always guard with `response.data[0] if response.data else None`.
> `response.error` was removed in v2; errors raise exceptions instead.

## Patterns

### Supabase client singleton (`services/supabase.py`)

```python
# services/supabase.py
"""
Supabase client factory — single source of truth for all client instances.
Produced by: backend-agent / supabase-crud skill
"""
from functools import lru_cache

from supabase import Client, create_client

from api.config import settings


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Returns the cached service-role Supabase client.
    # SERVICE ROLE: bypasses RLS — for use by auth validation and admin operations only.
    Never pass this client to user-facing query functions.
    """
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment."
        )
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def get_user_supabase_client(jwt: str) -> Client:
    """
    Returns a Supabase client scoped to the authenticated user's JWT.
    All PostgREST queries through this client respect Row-Level Security policies.
    A new client object is created per request (lightweight — shares connection pool).
    """
    client = create_client(settings.supabase_url, settings.supabase_anon_key)
    client.postgrest.auth(jwt)
    return client
```

### DB layer for a table (`api/db/{table_name}.py`)

```python
# api/db/items.py
"""
Supabase CRUD operations for the 'items' table.
All functions assume RLS is active unless the client is the service-role client.
Produced by: backend-agent / supabase-crud skill
"""
from supabase import Client


def create_item(client: Client, data: dict) -> tuple[dict | None, str | None]:
    """
    Insert a new row into the items table.

    Args:
        client: Supabase client (user-scoped for RLS enforcement).
        data: Dict of column values. Must include 'name' and 'user_id'.

    Returns:
        (created_row, None) on success; (None, error_message) on failure.
    """
    try:
        response = client.table("items").insert(data).execute()
        return response.data[0] if response.data else None, None
    except Exception as exc:
        return None, str(exc)


def read_items(
    client: Client,
    filters: dict | None = None,
    order_by: str = "created_at",
    ascending: bool = False,
) -> tuple[list[dict], str | None]:
    """
    Fetch all items matching optional equality filters.

    Args:
        client: Supabase client.
        filters: Dict of {column: value} equality filters; None returns all rows visible to user.
        order_by: Column to sort by. Defaults to 'created_at'.
        ascending: Sort direction.

    Returns:
        (list_of_rows, None) on success; ([], error_message) on failure.
    """
    try:
        query = client.table("items").select("*").order(order_by, desc=not ascending)
        if filters:
            for column, value in filters.items():
                query = query.eq(column, value)
        response = query.execute()
        return response.data, None
    except Exception as exc:
        return [], str(exc)


def read_item(client: Client, item_id: str) -> tuple[dict | None, str | None]:
    """
    Fetch a single item by primary key.

    Returns:
        (row_dict, None) if found; (None, None) if not found; (None, error) on failure.
    """
    try:
        response = client.table("items").select("*").eq("id", item_id).execute()
        return response.data[0] if response.data else None, None
    except Exception as exc:
        return None, str(exc)


def update_item(
    client: Client, item_id: str, data: dict
) -> tuple[dict | None, str | None]:
    """
    Update an existing item. Only columns present in `data` are changed.

    Returns:
        (updated_row, None) on success; (None, error) on failure.
    """
    try:
        response = client.table("items").update(data).eq("id", item_id).execute()
        return response.data[0] if response.data else None, None
    except Exception as exc:
        return None, str(exc)


def delete_item(client: Client, item_id: str) -> tuple[bool, str | None]:
    """
    Delete an item by primary key.

    Returns:
        (True, None) on success; (False, error) on failure.
    """
    try:
        client.table("items").delete().eq("id", item_id).execute()
        return True, None
    except Exception as exc:
        return False, str(exc)
```

### Complex filters (range, pattern match)

```python
# api/db/items.py — additional query helpers

def search_items(
    client: Client,
    name_query: str,
    min_qty: int = 0,
) -> tuple[list[dict], str | None]:
    """
    Search items by name (case-insensitive) and minimum quantity.

    Uses .ilike() for pattern match and .gte() for range filter.
    Returns (rows, None) on success; ([], error) on failure.
    """
    try:
        response = (
            client.table("items")
            .select("*")
            .ilike("name", f"%{name_query}%")   # case-insensitive pattern match
            .gte("quantity", min_qty)            # greater-than-or-equal filter
            .order("name")
            .execute()
        )
        return response.data, None
    except Exception as exc:
        return [], str(exc)
```

### Service-role admin query (explicit bypass comment required)

```python
# api/db/admin_items.py
"""
Admin-level item queries using service-role client — bypasses RLS.
Produced by: backend-agent / supabase-crud skill
"""
from supabase import Client


def admin_count_all_items(client: Client) -> tuple[int, str | None]:
    """
    Count all items across all users.
    # SERVICE ROLE: bypasses RLS — used only in admin dashboard, requires role check at route level.

    Returns:
        (count, None) on success; (0, error) on failure.
    """
    try:
        response = client.table("items").select("id", count="exact").execute()
        return response.count or 0, None
    except Exception as exc:
        return 0, str(exc)
```

## Anti-Patterns

- **`create_client()` inside an `api/db/` function** — always receive `client` as a parameter.
- **Raising exceptions from `api/db/` functions** — always catch and return `(None, str(exc))`.
- **`response.data[0]` without guard** — `response.data` may be an empty list; always check.
- **Using `response.error` (supabase-py v1 API)** — removed in v2; errors raise exceptions.
- **Accessing service-role client from user-facing routes without comment** — must document intent.
- **Storing `jwt` in a global variable** — user clients must be request-scoped.
- **Directly calling `client.auth.*` from `api/db/` modules** — auth operations belong in `api/db/auth_users.py` or `api/routes/auth.py`.

## Checklist

- [ ] One file per table in `api/db/{table_name}.py`
- [ ] All five CRUD functions present: `create_`, `read_s`, `read_`, `update_`, `delete_`
- [ ] Every function annotated with full type hints
- [ ] Every function has a docstring
- [ ] All functions return `(data, error)` tuples, never raise
- [ ] `response.data[0] if response.data else None` pattern used for single-row returns
- [ ] Service-role usage has explicit `# SERVICE ROLE:` comment
- [ ] `services/supabase.py` is the only place `create_client()` is called
- [ ] Module-level docstring present

## User Preferences

<!-- This section is updated during use. Start with defaults below. -->
- preferred_pattern: (data, error) tuple with try/except
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
