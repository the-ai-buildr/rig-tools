import dash
from dash import dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from utils import page_body, page_header

dash.register_page(__name__, path="/projects")


project_modal = dmc.Modal(
    id="project-modal",
    title="Create Project",
    centered=True,
    children=dmc.Stack(
        [
            dmc.TextInput(
                id="project-name-input",
                label="Project name",
                placeholder="e.g. Benedum Pad",
                leftSection=DashIconify(icon="tabler:list-details", width=16),
            ),
            dmc.Select(
                id="project-type-input",
                label="Type",
                value="single",
                data=[
                    {"value": "single", "label": "Single well"},
                    {"value": "pad", "label": "Pad"},
                ],
            ),
            dmc.Textarea(
                id="project-desc-input",
                label="Description",
                placeholder="Optional",
                autosize=True,
                minRows=2,
            ),
            dmc.Box(id="project-modal-alert"),
            dmc.Group(
                [
                    dmc.Button(
                        "Cancel",
                        id="project-cancel-btn",
                        variant="subtle",
                        color="gray",
                    ),
                    dmc.Button(
                        "Create",
                        id="project-create-confirm",
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


layout = page_body(
    page_header(
        "Projects",
        action=dmc.Button(
            "Create",
            id="create-project-btn",
            leftSection=DashIconify(icon="tabler:plus", width=16),
            variant="subtle",
            styles={"root": {"border": "1px solid var(--mantine-color-default-border)"}},
        ),
    ),
    project_modal,
    dcc.Store(id="projects-refresh", data=0),
    dmc.Box(id="projects-list", mt="sm"),
)