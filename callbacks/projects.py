"""Projects page callbacks — create / list / delete via the data layer.

Callbacks run in the Dash/FastAPI process and call the repository layer
directly (the same layer the ``/api/projects`` endpoints use), which avoids
issuing self-HTTP requests from within a request handler.
"""
from datetime import datetime

import dash_mantine_components as dmc
from dash import ALL, Input, Output, State, ctx, no_update
from dash_iconify import DashIconify
from sqlmodel import Session

from data.db import engine
from data.repositories import projects as project_repo

_TYPE_LABELS = {"single": "Single well", "pad": "Pad"}
_STATUS_COLORS = {
    "planned": "gray",
    "active": "green",
    "on_hold": "yellow",
    "completed": "blue",
    "archived": "dark",
}


def _fmt_date(value) -> str:
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return str(value or "")[:10]


def _project_card(project) -> dmc.Card:
    return dmc.Card(
        dmc.Group(
            [
                dmc.Stack(
                    [
                        dmc.Group(
                            [
                                dmc.Text(project.name, fw=600),
                                dmc.Badge(
                                    _TYPE_LABELS.get(
                                        project.project_type, project.project_type
                                    ),
                                    variant="light",
                                    size="sm",
                                ),
                                dmc.Badge(
                                    project.status,
                                    color=_STATUS_COLORS.get(project.status, "gray"),
                                    variant="light",
                                    size="sm",
                                ),
                            ],
                            gap="xs",
                            align="center",
                        ),
                        dmc.Text(
                            project.description or "No description",
                            c="dimmed",
                            size="sm",
                        ),
                        dmc.Text(
                            f"Created {_fmt_date(project.created_at)}",
                            c="dimmed",
                            size="xs",
                        ),
                    ],
                    gap=4,
                ),
                dmc.Tooltip(
                    label="Delete project",
                    children=dmc.ActionIcon(
                        DashIconify(icon="tabler:trash", width=18),
                        id={"type": "project-delete", "index": project.id},
                        color="red",
                        variant="subtle",
                        n_clicks=0,
                    ),
                ),
            ],
            justify="space-between",
            align="flex-start",
            wrap="nowrap",
        ),
        withBorder=True,
        radius="md",
        p="md",
    )


def _empty_state() -> dmc.Stack:
    return dmc.Stack(
        [
            DashIconify(icon="tabler:folder-off", width=40, color="var(--mantine-color-dimmed)"),
            dmc.Text("No projects yet. Click Create to add one.", c="dimmed"),
        ],
        align="center",
        gap="xs",
        py="xl",
    )


def register_project_callbacks(app):
    @app.callback(
        Output("project-modal", "opened"),
        Input("create-project-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def open_modal(_clicks):
        return True

    @app.callback(
        Output("project-modal", "opened", allow_duplicate=True),
        Input("project-cancel-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def close_modal(_clicks):
        return False

    @app.callback(
        Output("projects-refresh", "data"),
        Output("project-modal", "opened", allow_duplicate=True),
        Output("project-modal-alert", "children"),
        Output("project-name-input", "value"),
        Output("project-desc-input", "value"),
        Input("project-create-confirm", "n_clicks"),
        State("project-name-input", "value"),
        State("project-type-input", "value"),
        State("project-desc-input", "value"),
        State("projects-refresh", "data"),
        State("auth-store", "data"),
        prevent_initial_call=True,
    )
    def create_project(_clicks, name, ptype, description, refresh, auth):
        if not name or not name.strip():
            alert = dmc.Alert(
                "Project name is required.",
                color="red",
                variant="light",
                icon=DashIconify(icon="tabler:alert-triangle", width=18),
            )
            return no_update, no_update, alert, no_update, no_update
        owner_id = auth.get("user_id") if auth else None
        with Session(engine) as session:
            project_repo.create_project(
                session,
                name=name.strip(),
                project_type=ptype or "single",
                description=(description or None),
                owner_id=owner_id,
            )
        return (refresh or 0) + 1, False, None, "", ""

    @app.callback(
        Output("projects-refresh", "data", allow_duplicate=True),
        Input({"type": "project-delete", "index": ALL}, "n_clicks"),
        State("projects-refresh", "data"),
        prevent_initial_call=True,
    )
    def delete_project(clicks, refresh):
        if not clicks or not any(clicks):
            return no_update
        target = ctx.triggered_id
        if not target:
            return no_update
        with Session(engine) as session:
            project_repo.delete_project(session, target["index"])
        return (refresh or 0) + 1

    @app.callback(
        Output("projects-list", "children"),
        Input("projects-refresh", "data"),
        Input("auth-store", "data"),
    )
    def render_projects(_refresh, auth):
        owner_id = auth.get("user_id") if auth else None
        with Session(engine) as session:
            projects = project_repo.list_projects(session, owner_id=owner_id)
        if not projects:
            return _empty_state()
        projects.sort(key=lambda p: p.created_at, reverse=True)
        return dmc.Stack([_project_card(p) for p in projects], gap="sm")
