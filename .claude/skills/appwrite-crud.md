# Skill: Appwrite CRUD

<!--
Purpose: Patterns for the api/db/ service layer — Appwrite Databases document CRUD consumed by FastAPI routes.
Produced by: backend-agent
-->

## Purpose

Define every rule and pattern for building the Appwrite Databases query layer in `api/db/`, the client singleton in `services/appwrite.py`, and how routes consume them.

## When to Use

Activate when the task contains: **appwrite**, **crud**, **database**, **collection**, **document**, **query**, or when touching `api/db/`, `services/appwrite.py`, or adding a new Appwrite collection.

## Conventions

1. One file per Appwrite collection: `api/db/{collection_name}.py`. Exports exactly: `create_`, `list_`, `read_`, `update_`, `delete_`.
2. All functions take `client: Client` as their first argument — never create clients internally.
3. All functions return `(data, error)` tuples — never raise exceptions out of `api/db/`.
4. Every function has a full type signature and docstring.
5. The API key client (`get_appwrite_client()`) bypasses permissions — must be accompanied by comment: `# API KEY: bypasses permissions — [reason]`.
6. The user-scoped client (`get_user_appwrite_client(jwt)`) respects document permissions — use for all user-facing data operations.
7. `services/appwrite.py` contains the one and only client instantiation logic.
8. The singleton is `@lru_cache(maxsize=1)` — one API-key client per process lifetime.
9. User-scoped clients are created per request (lightweight — just sets the JWT header).
10. Use `Query` helpers for filtering; avoid constructing raw query strings.

> **⚠️ appwrite-py v6+ note:**
> - `databases.list_documents(database_id, collection_id, queries=[])` returns a `DocumentList` with `.documents` (list) and `.total` (int)
> - `databases.create_document(database_id, collection_id, document_id, data, permissions=[])` — use `ID.unique()` for auto-generated IDs
> - `databases.get_document(database_id, collection_id, document_id)` returns a `Document` dict-like object
> - `databases.update_document(database_id, collection_id, document_id, data, permissions=[])` — only fields present in `data` are changed
> - `databases.delete_document(database_id, collection_id, document_id)` returns an empty string on success
> - Document fields are accessed as dict keys or attributes: `doc["field"]` or `doc.field`
> - `Query.equal("field", ["value"])` — note: value must be a **list** even for single values
> - `AppwriteException` is raised on error — always catch it; never check a `.error` attribute

## Patterns

### Appwrite client singleton (`services/appwrite.py`)

```python
# services/appwrite.py
"""
Appwrite client factory — single source of truth for all client instances.
Produced by: backend-agent / appwrite-crud skill
"""
from functools import lru_cache

from appwrite.client import Client

from api.config import settings


@lru_cache(maxsize=1)
def get_appwrite_client() -> Client:
    """
    Returns the cached server-side Appwrite client using the API key.
    # API KEY: bypasses document permissions — for admin and server-side operations only.
    Never pass this client to user-facing document query functions.
    """
    if not settings.appwrite_endpoint or not settings.appwrite_project_id or not settings.appwrite_api_key:
        raise RuntimeError(
            "APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID, and APPWRITE_API_KEY must be set."
        )
    client = Client()
    (
        client
        .set_endpoint(settings.appwrite_endpoint)
        .set_project(settings.appwrite_project_id)
        .set_key(settings.appwrite_api_key)
    )
    return client


def get_user_appwrite_client(jwt: str) -> Client:
    """
    Returns an Appwrite client scoped to the authenticated user's JWT.
    All document operations respect Appwrite collection/document permissions.
    A new client object is created per request.
    """
    client = Client()
    (
        client
        .set_endpoint(settings.appwrite_endpoint)
        .set_project(settings.appwrite_project_id)
        .set_jwt(jwt)
    )
    return client
```

### DB layer for a collection (`api/db/{collection_name}.py`)

```python
# api/db/items.py
"""
Appwrite document CRUD operations for the 'items' collection.
All functions assume document permissions are active unless the client uses the API key.
Produced by: backend-agent / appwrite-crud skill
"""
from appwrite.client import Client
from appwrite.exception import AppwriteException
from appwrite.id import ID
from appwrite.query import Query
from appwrite.services.databases import Databases

from api.config import settings

_DATABASE_ID = settings.appwrite_database_id
_COLLECTION_ID = "items"


def create_item(client: Client, data: dict) -> tuple[dict | None, str | None]:
    """
    Insert a new document into the items collection.

    Args:
        client: Appwrite client (user-scoped for permission enforcement).
        data: Dict of field values.

    Returns:
        (created_document, None) on success; (None, error_message) on failure.
    """
    try:
        db = Databases(client)
        doc = db.create_document(_DATABASE_ID, _COLLECTION_ID, ID.unique(), data)
        return dict(doc), None
    except AppwriteException as exc:
        return None, exc.message


def list_items(
    client: Client,
    filters: list | None = None,
    order_by: str | None = None,
    limit: int = 25,
    offset: int = 0,
) -> tuple[list[dict], str | None]:
    """
    Fetch all documents matching optional Query filters.

    Args:
        client: Appwrite client.
        filters: List of Query objects (e.g. [Query.equal("status", ["active"])]).
        order_by: Field name to sort by (ascending). Prefix with '-' for descending.
        limit: Max documents to return (max 100 per Appwrite limit).
        offset: Pagination offset.

    Returns:
        (list_of_documents, None) on success; ([], error_message) on failure.
    """
    try:
        db = Databases(client)
        queries = list(filters) if filters else []
        queries.append(Query.limit(limit))
        queries.append(Query.offset(offset))
        if order_by:
            if order_by.startswith("-"):
                queries.append(Query.order_desc(order_by[1:]))
            else:
                queries.append(Query.order_asc(order_by))
        result = db.list_documents(_DATABASE_ID, _COLLECTION_ID, queries=queries)
        return [dict(d) for d in result.documents], None
    except AppwriteException as exc:
        return [], exc.message


def read_item(client: Client, document_id: str) -> tuple[dict | None, str | None]:
    """
    Fetch a single document by its ID.

    Returns:
        (document_dict, None) if found; (None, error) on failure or not found.
    """
    try:
        db = Databases(client)
        doc = db.get_document(_DATABASE_ID, _COLLECTION_ID, document_id)
        return dict(doc), None
    except AppwriteException as exc:
        return None, exc.message


def update_item(
    client: Client, document_id: str, data: dict
) -> tuple[dict | None, str | None]:
    """
    Update an existing document. Only fields present in `data` are changed.

    Returns:
        (updated_document, None) on success; (None, error) on failure.
    """
    try:
        db = Databases(client)
        doc = db.update_document(_DATABASE_ID, _COLLECTION_ID, document_id, data)
        return dict(doc), None
    except AppwriteException as exc:
        return None, exc.message


def delete_item(client: Client, document_id: str) -> tuple[bool, str | None]:
    """
    Delete a document by its ID.

    Returns:
        (True, None) on success; (False, error) on failure.
    """
    try:
        db = Databases(client)
        db.delete_document(_DATABASE_ID, _COLLECTION_ID, document_id)
        return True, None
    except AppwriteException as exc:
        return False, exc.message
```

### Complex queries (range, pattern, multiple filters)

```python
# api/db/items.py — additional query helpers

from appwrite.query import Query


def search_items(
    client: Client,
    name_query: str,
    min_qty: int = 0,
) -> tuple[list[dict], str | None]:
    """
    Search items by name (full-text) and minimum quantity.

    Uses Query.search() for full-text and Query.greater_than_equal() for range.
    The 'name' attribute must have full-text search enabled in the Appwrite console.

    Returns (documents, None) on success; ([], error) on failure.
    """
    try:
        db = Databases(client)
        queries = [
            Query.search("name", name_query),
            Query.greater_than_equal("quantity", min_qty),
            Query.limit(50),
        ]
        result = db.list_documents(_DATABASE_ID, _COLLECTION_ID, queries=queries)
        return [dict(d) for d in result.documents], None
    except AppwriteException as exc:
        return [], exc.message
```

### API key admin query (explicit bypass comment required)

```python
# api/db/admin_items.py
"""
Admin-level document queries using API key client — bypasses permissions.
Produced by: backend-agent / appwrite-crud skill
"""
from appwrite.client import Client
from appwrite.exception import AppwriteException
from appwrite.services.databases import Databases

from api.config import settings

_DATABASE_ID = settings.appwrite_database_id
_COLLECTION_ID = "items"


def admin_count_all_items(client: Client) -> tuple[int, str | None]:
    """
    Count all documents across all users.
    # API KEY: bypasses permissions — used only in admin dashboard, requires role check at route level.

    Returns:
        (count, None) on success; (0, error) on failure.
    """
    try:
        db = Databases(client)
        result = db.list_documents(_DATABASE_ID, _COLLECTION_ID)
        return result.total, None
    except AppwriteException as exc:
        return 0, exc.message
```

### Permissions helper (Appwrite document-level)

```python
# Appwrite permission patterns — import in api/db/ functions when explicit permissions needed
from appwrite.permission import Permission
from appwrite.role import Role

# Allow only the creating user to read/update/delete
def _owner_permissions(user_id: str) -> list[str]:
    return [
        Permission.read(Role.user(user_id)),
        Permission.update(Role.user(user_id)),
        Permission.delete(Role.user(user_id)),
    ]

# Usage in create_document:
# db.create_document(DB_ID, COL_ID, ID.unique(), data, _owner_permissions(current_user["user_id"]))
```

### FastAPI route consuming the DB layer

```python
# api/routes/items.py
"""
Items CRUD endpoints for Appwrite-backed documents.
Produced by: backend-agent / appwrite-crud skill
"""
from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_user
from api.models.item_models import ItemCreate, ItemRead, ItemUpdate
from api.db.items import create_item, delete_item, list_items, read_item, update_item
from services.appwrite import get_user_appwrite_client

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", response_model=list[ItemRead])
async def get_items(current_user: dict = Depends(get_current_user)) -> list[ItemRead]:
    client = get_user_appwrite_client(current_user["token"])
    data, error = list_items(client)
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
    return data


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item_endpoint(
    body: ItemCreate,
    current_user: dict = Depends(get_current_user),
) -> ItemRead:
    client = get_user_appwrite_client(current_user["token"])
    data, error = create_item(client, {**body.model_dump(), "user_id": current_user["user_id"]})
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return data
```

## Anti-Patterns

- **`Client()` instantiation inside an `api/db/` function** — always receive `client` as a parameter.
- **Raising exceptions from `api/db/` functions** — always catch `AppwriteException` and return `(None, exc.message)`.
- **Checking a `.error` attribute** — Appwrite Python SDK raises `AppwriteException`; there is no `.error` field.
- **`Query.equal("field", "value")` with a bare string** — the third argument must be a list: `Query.equal("field", ["value"])`.
- **Using the API key client for user-facing routes without a comment** — must document intent with `# API KEY: bypasses permissions — [reason]`.
- **Storing `jwt` in a global variable** — user clients must be request-scoped.
- **Directly calling `client.account.*` from `api/db/` modules** — auth operations belong in `api/routes/auth.py`.
- **Accessing `result.data` instead of `result.documents`** — Appwrite `list_documents` returns a `DocumentList` with `.documents`, not `.data`.

## Checklist

- [ ] One file per collection in `api/db/{collection_name}.py`
- [ ] All five CRUD functions present: `create_`, `list_`, `read_`, `update_`, `delete_`
- [ ] Every function annotated with full type hints
- [ ] Every function has a docstring
- [ ] All functions return `(data, error)` tuples, never raise
- [ ] `AppwriteException` is caught and its `.message` returned as the error string
- [ ] API key usage has explicit `# API KEY: bypasses permissions — [reason]` comment
- [ ] `services/appwrite.py` is the only place `Client()` is instantiated
- [ ] Module-level docstring present
- [ ] `Query.equal` uses list values: `Query.equal("field", ["value"])`

## User Preferences

<!-- This section is updated during use. Start with defaults below. -->
- preferred_pattern: (data, error) tuple with AppwriteException catch
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
