import dash_mantine_components as dmc
from dash import html


def sidebar_section(title, description=None, children=None):
    items = [dmc.Text(title, fw=600)]

    if description:
        items.append(dmc.Text(description, c="dimmed", size="sm"))

    if children:
        items.extend(children)

    return items


def sidebar_links(labels, active_label=None):
    return [
        dmc.NavLink(label=label, active=label == active_label)
        for label in labels
    ]


def landing_content(home_path="/home"):
    return dmc.Container(
        dmc.Stack(
            [
                dmc.Title("Rig-Tools", order=1),
                dmc.Text("Welcome. Start from the Home page.", c="dimmed"),
                html.A(
                    dmc.Button("Go to Home"),
                    href=home_path,
                    style={"textDecoration": "none"},
                ),
            ],
            gap="md",
            align="center",
        ),
        pt="xl",
    )