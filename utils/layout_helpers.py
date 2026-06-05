import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def page_header(title, action=None, order=3, divider=True):
    """Responsive page title bar.

    Title + optional action button sit side-by-side on tablet/desktop and
    stack (title above, action below, full-width) on mobile — mirroring the
    responsive card grids in the page body.

    Args:
        title:   heading text.
        action:  optional component (e.g. a Button) shown on the right.
        order:   dmc.Title order.
        divider: append a bottom Divider when True.
    """
    header = dmc.Flex(
        [
            dmc.Title(title, order=order),
            action if action is not None else None,
        ],
        direction={"base": "column", "xs": "row"},
        justify="space-between",
        align={"base": "stretch", "xs": "center"},
        gap={"base": "xs", "xs": "sm"},
        px="5px",
        mb="5px",
    )
    if divider:
        return dmc.Box([header, dmc.Divider(mb="md")])
    return header


def sidebar_section(title, description=None, children=None):
    items = [dmc.Text(title, fw=700)]

    if description:
        items.append(dmc.Text(description, c="dimmed", size="sm"))

    if children:
        items.extend(children)

    return items


def sidebar_links(labels, active_label=None, icons=None, hrefs=None):
    icons = icons or {}
    hrefs = hrefs or {}
    links = []
    for label in labels:
        icon = icons.get(label)
        links.append(
            dmc.NavLink(
                label=label,
                active=label == active_label,
                leftSection=DashIconify(icon=icon, width=16) if icon else None,
                href=hrefs.get(label),
            )
        )
    return links


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
            gap="sm",
            align="center",
        ),
        pt="sm",
    )