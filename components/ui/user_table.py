"""
Reusable User CRUD table component.

Renders a table of users (no passwords). An **Edit** button switches the whole
table into inline-edit mode where username / full name / email / role / active
are editable per row, plus a per-row delete action. **Save** commits all edits;
**Cancel** discards them. **Add user** opens a modal to create a new user
(password is collected here, never shown in the table).

Usage
-----
    from components.ui.user_table import user_table, register_user_table_callbacks

    layout = page_body(user_table)              # drop into a page
    register_user_table_callbacks(app)          # once at startup

Data access goes straight through the repository layer (same layer the
``/api/users`` endpoints use), mirroring callbacks/projects.py.
"""
from datetime import datetime

import dash_mantine_components as dmc
from dash import ALL, Input, Output, State, ctx, dcc, no_update
from dash_iconify import DashIconify
from sqlmodel import Session

from data.db import engine
from data.repositories import users as user_repo

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ROLES = ["admin", "engineer", "supervisor", "geologist", "viewer"]
ROLE_OPTIONS = [{"value": r, "label": r.capitalize()} for r in ROLES]
ROLE_COLORS = {
    "admin": "red",
    "engineer": "blue",
    "supervisor": "violet",
    "geologist": "green",
    "viewer": "gray",
}
ACTIVE_OPTIONS = [
    {"value": "active", "label": "Active"},
    {"value": "inactive", "label": "Inactive"},
]

_VIEW_COLS = ["Username", "Full name", "Email", "Role", "Status", "Created"]
_EDIT_COLS = ["Username", "Full name", "Email", "Role", "Status", ""]


def _fmt_date(value) -> str:
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return str(value or "")[:10]


def _cell_id(field: str, index: str) -> dict:
    return {"type": "user-cell", "field": field, "index": index}


def _alert(message: str, color: str = "red"):
    icon = "tabler:alert-triangle" if color == "red" else "tabler:check"
    return dmc.Alert(
        message,
        color=color,
        variant="light",
        icon=DashIconify(icon=icon, width=18),
        withCloseButton=True,
    )


# ---------------------------------------------------------------------------
# Row renderers
# ---------------------------------------------------------------------------
def _view_row(u) -> dmc.TableTr:
    return dmc.TableTr(
        [
            dmc.TableTd(u.username),
            dmc.TableTd(u.full_name or "—"),
            dmc.TableTd(u.email),
            dmc.TableTd(
                dmc.Badge(
                    u.role.capitalize(),
                    color=ROLE_COLORS.get(u.role, "gray"),
                    variant="light",
                )
            ),
            dmc.TableTd(
                dmc.Badge(
                    "Active" if u.is_active else "Inactive",
                    color="green" if u.is_active else "gray",
                    variant="light",
                )
            ),
            dmc.TableTd(_fmt_date(u.created_at)),
        ]
    )


def _edit_row(u, *, deletable: bool) -> dmc.TableTr:
    return dmc.TableTr(
        [
            dmc.TableTd(
                dmc.TextInput(value=u.username, id=_cell_id("username", u.id), size="xs")
            ),
            dmc.TableTd(
                dmc.TextInput(value=u.full_name, id=_cell_id("full_name", u.id), size="xs")
            ),
            dmc.TableTd(
                dmc.TextInput(value=u.email, id=_cell_id("email", u.id), size="xs")
            ),
            dmc.TableTd(
                dmc.Select(
                    value=u.role,
                    data=ROLE_OPTIONS,
                    id=_cell_id("role", u.id),
                    size="xs",
                    allowDeselect=False,
                    comboboxProps={"withinPortal": True},
                )
            ),
            dmc.TableTd(
                dmc.Select(
                    value="active" if u.is_active else "inactive",
                    data=ACTIVE_OPTIONS,
                    id=_cell_id("is_active", u.id),
                    size="xs",
                    allowDeselect=False,
                    comboboxProps={"withinPortal": True},
                )
            ),
            dmc.TableTd(
                dmc.Tooltip(
                    label="Delete user" if deletable else "Can't delete the signed-in user",
                    withArrow=True,
                    children=dmc.ActionIcon(
                        DashIconify(icon="tabler:trash", width=16),
                        id={"type": "user-delete", "index": u.id},
                        color="gray",
                        variant="subtle",
                        className="card-delete",
                        disabled=not deletable,
                        n_clicks=0,
                    ),
                )
            ),
        ]
    )


def _render_table(edit: bool, current_user_id: str | None):
    with Session(engine) as session:
        users = user_repo.list_users(session)
    users.sort(key=lambda u: (u.role != "admin", u.username.lower()))

    if not users:
        return dmc.Stack(
            [
                DashIconify(
                    icon="tabler:users-off",
                    width=40,
                    color="var(--mantine-color-dimmed)",
                ),
                dmc.Text("No users yet. Click Add user to create one.", c="dimmed"),
            ],
            align="center",
            gap="xs",
            py="xl",
        )

    cols = _EDIT_COLS if edit else _VIEW_COLS
    head = dmc.TableThead(dmc.TableTr([dmc.TableTh(c) for c in cols]))
    if edit:
        rows = [_edit_row(u, deletable=(u.id != current_user_id)) for u in users]
    else:
        rows = [_view_row(u) for u in users]
    body = dmc.TableTbody(rows)
    return dmc.Table(
        [head, body],
        highlightOnHover=True,
        withTableBorder=True,
        verticalSpacing="sm",
        horizontalSpacing="md",
        striped=True,
    )


# ---------------------------------------------------------------------------
# Add-user modal
# ---------------------------------------------------------------------------
_add_modal = dmc.Modal(
    id="user-add-modal",
    title="Add User",
    centered=True,
    children=dmc.Stack(
        [
            dmc.TextInput(
                id="user-add-username",
                label="Username",
                placeholder="e.g. jdoe",
                leftSection=DashIconify(icon="tabler:user", width=16),
            ),
            dmc.TextInput(
                id="user-add-fullname",
                label="Full name",
                placeholder="e.g. Jane Doe",
            ),
            dmc.TextInput(
                id="user-add-email",
                label="Email",
                placeholder="e.g. jane@rigtools.local",
                leftSection=DashIconify(icon="tabler:mail", width=16),
            ),
            dmc.Select(
                id="user-add-role",
                label="Role",
                data=ROLE_OPTIONS,
                value="viewer",
                allowDeselect=False,
            ),
            dmc.PasswordInput(
                id="user-add-password",
                label="Password",
                placeholder="Temporary password",
                leftSection=DashIconify(icon="tabler:lock", width=16),
            ),
            dmc.Box(id="user-add-alert"),
            dmc.Group(
                [
                    dmc.Button(
                        "Cancel",
                        id="user-add-cancel",
                        variant="subtle",
                        color="gray",
                    ),
                    dmc.Button(
                        "Create",
                        id="user-add-confirm",
                        leftSection=DashIconify(icon="tabler:plus", width=16),
                        variant="subtle",
                        styles={"root": {"border": "1px solid var(--mantine-color-default-border)"}},
                    ),
                ],
                justify="flex-end",
            ),
        ],
        gap="sm",
    ),
)


# ---------------------------------------------------------------------------
# Toolbar + component layout
# ---------------------------------------------------------------------------
def _toolbar_button(label, btn_id, icon, **kwargs):
    return dmc.Button(
        label,
        id=btn_id,
        leftSection=DashIconify(icon=icon, width=16),
        variant="subtle",
        styles={"root": {"border": "1px solid var(--mantine-color-default-border)"}},
        **kwargs,
    )


_toolbar = dmc.Group(
    [
        dmc.Text("Users", fw=600, size="lg"),
        dmc.Group(
            [
                # View-mode action
                dmc.Box(
                    _toolbar_button("Edit", "user-edit-btn", "tabler:edit"),
                    id="user-view-actions",
                ),
                # Edit-mode actions
                dmc.Group(
                    [
                        _toolbar_button("Add user", "user-add-open-btn", "tabler:user-plus"),
                        _toolbar_button(
                            "Cancel", "user-cancel-btn", "tabler:x", color="gray"
                        ),
                        _toolbar_button("Save", "user-save-btn", "tabler:device-floppy"),
                    ],
                    id="user-edit-actions-wrap",
                    gap="xs",
                ),
            ],
            gap="xs",
        ),
    ],
    justify="space-between",
    align="center",
)


user_table = dmc.Stack(
    [
        dcc.Store(id="users-refresh", data=0),
        dcc.Store(id="users-edit-mode", data=False),
        _add_modal,
        _toolbar,
        dmc.Box(id="user-table-alert"),
        dmc.Box(id="users-table-container"),
    ],
    gap="sm",
)


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------
def register_user_table_callbacks(app):
    # ── Render table (view or edit mode) ─────────────────────────
    @app.callback(
        Output("users-table-container", "children"),
        Input("users-refresh", "data"),
        Input("users-edit-mode", "data"),
        State("auth-store", "data"),
    )
    def render_users(_refresh, edit_mode, auth):
        current_id = auth.get("user_id") if auth else None
        return _render_table(bool(edit_mode), current_id)

    # ── Toggle toolbar buttons for the active mode ───────────────
    @app.callback(
        Output("user-view-actions", "display"),
        Output("user-edit-actions-wrap", "display"),
        Input("users-edit-mode", "data"),
    )
    def toggle_toolbar(edit_mode):
        if edit_mode:
            return "none", "flex"
        return "flex", "none"

    # ── Enter / cancel edit mode ─────────────────────────────────
    @app.callback(
        Output("users-edit-mode", "data"),
        Output("users-refresh", "data", allow_duplicate=True),
        Input("user-edit-btn", "n_clicks"),
        Input("user-cancel-btn", "n_clicks"),
        State("users-refresh", "data"),
        prevent_initial_call=True,
    )
    def toggle_edit_mode(_edit, _cancel, refresh):
        if ctx.triggered_id == "user-edit-btn":
            return True, no_update
        # Cancel → leave edit mode and re-render fresh from DB.
        return False, (refresh or 0) + 1

    # ── Save inline edits ────────────────────────────────────────
    @app.callback(
        Output("users-edit-mode", "data", allow_duplicate=True),
        Output("users-refresh", "data", allow_duplicate=True),
        Output("user-table-alert", "children"),
        Input("user-save-btn", "n_clicks"),
        State({"type": "user-cell", "field": ALL, "index": ALL}, "value"),
        State({"type": "user-cell", "field": ALL, "index": ALL}, "id"),
        State("users-refresh", "data"),
        prevent_initial_call=True,
    )
    def save_edits(_clicks, values, ids, refresh):
        # Regroup the flat pattern-matched cells into per-user dicts.
        edited: dict[str, dict] = {}
        for value, cid in zip(values, ids):
            edited.setdefault(cid["index"], {})[cid["field"]] = value

        # Validate required fields before touching the DB.
        for fields in edited.values():
            if not (fields.get("username") or "").strip():
                return no_update, no_update, _alert("Username is required for every row.")
            if not (fields.get("email") or "").strip():
                return no_update, no_update, _alert("Email is required for every row.")

        with Session(engine) as session:
            for user_id, fields in edited.items():
                user_repo.update_user(
                    session,
                    user_id,
                    username=fields["username"].strip(),
                    full_name=(fields.get("full_name") or "").strip(),
                    email=fields["email"].strip().lower(),
                    role=fields.get("role"),
                    is_active=(fields.get("is_active") == "active"),
                )
        return False, (refresh or 0) + 1, None

    # ── Add-user modal open / close ──────────────────────────────
    @app.callback(
        Output("user-add-modal", "opened"),
        Input("user-add-open-btn", "n_clicks"),
        Input("user-add-cancel", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_add_modal(_open, _cancel):
        return ctx.triggered_id == "user-add-open-btn"

    # ── Create user ──────────────────────────────────────────────
    @app.callback(
        Output("user-add-modal", "opened", allow_duplicate=True),
        Output("users-refresh", "data", allow_duplicate=True),
        Output("user-add-alert", "children"),
        Output("user-add-username", "value"),
        Output("user-add-fullname", "value"),
        Output("user-add-email", "value"),
        Output("user-add-password", "value"),
        Input("user-add-confirm", "n_clicks"),
        State("user-add-username", "value"),
        State("user-add-fullname", "value"),
        State("user-add-email", "value"),
        State("user-add-role", "value"),
        State("user-add-password", "value"),
        State("users-refresh", "data"),
        prevent_initial_call=True,
    )
    def create_user(_clicks, username, full_name, email, role, password, refresh):
        username = (username or "").strip()
        email = (email or "").strip().lower()
        if not username or not email or not password:
            return (
                no_update, no_update,
                _alert("Username, email, and password are required."),
                no_update, no_update, no_update, no_update,
            )
        with Session(engine) as session:
            if user_repo.get_user_by_email(session, email):
                return (
                    no_update, no_update,
                    _alert("Email already registered."),
                    no_update, no_update, no_update, no_update,
                )
            if user_repo.get_user_by_username(session, username):
                return (
                    no_update, no_update,
                    _alert("Username already taken."),
                    no_update, no_update, no_update, no_update,
                )
            user_repo.create_user(
                session,
                username=username,
                full_name=(full_name or "").strip(),
                email=email,
                role=role or "viewer",
                password=password,
            )
        return False, (refresh or 0) + 1, None, "", "", "", ""

    # ── Delete user ──────────────────────────────────────────────
    @app.callback(
        Output("users-refresh", "data", allow_duplicate=True),
        Input({"type": "user-delete", "index": ALL}, "n_clicks"),
        State("users-refresh", "data"),
        State("auth-store", "data"),
        prevent_initial_call=True,
    )
    def delete_user(clicks, refresh, auth):
        if not clicks or not any(clicks):
            return no_update
        target = ctx.triggered_id
        if not target:
            return no_update
        current_id = auth.get("user_id") if auth else None
        if target["index"] == current_id:
            return no_update
        with Session(engine) as session:
            user_repo.delete_user(session, target["index"])
        return (refresh or 0) + 1
