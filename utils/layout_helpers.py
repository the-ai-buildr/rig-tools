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
    title_node = dmc.Title(title, order=order, ta="center")

    if action is None:
        header = dmc.Flex(
            [title_node],
            justify="center",
            align="center",
            px="5px",
            mb="0px",
        )
    else:
        header = dmc.Flex(
            [
                title_node,
                action,
            ],
            direction={"base": "column", "xs": "row"},
            justify="space-between",
            align={"base": "stretch", "xs": "center"},
            gap={"base": "xs", "xs": "sm"},
            px="5px",
            mb="0px",
        )
    if divider:
        return dmc.Box([header, dmc.Divider(mb="md")])
    return header


def page_body(*children, p="sm", **kwargs):
    """Standard page body wrapper.

    Provides the default padding/structure for a page's content, mirroring the
    way ``page_header`` standardizes the title bar. Compose a page as::

        layout = page_body(
            page_header("Projects", action=...),
            ...,
        )

    Args:
        *children: page content components.
        p:         outer padding (defaults to "sm").
        **kwargs:  forwarded to the underlying ``dmc.Box``.
    """
    return dmc.Box(list(children), p=p, **kwargs)


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