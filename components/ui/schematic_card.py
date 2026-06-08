import dash_mantine_components as dmc
from dash import dcc
from dash_iconify import DashIconify
from components.visuals.shematic import get_schematic_figure

def schematic_card(title, value, icon, color="gray"):
    return dmc.Paper(
        dmc.Stack(
            [
                dmc.Flex(
                    [
                        dmc.Stack(
                            [
                                dmc.Text(title, size="sm", c="dimmed", tt="uppercase", fw=600),
                                dmc.Text(value, size="xs", fw=700),
                            ],
                            gap=2,
                            style={"flex": 1},
                        ),
                        dmc.ThemeIcon(
                            DashIconify(icon=icon, width=20),
                            size="lg",
                            radius="md",
                            color=color,
                            variant="light",
                        ),
                    ],
                    align="center",
                    justify="space-between",
                ),
                dcc.Graph(
                    figure=get_schematic_figure(),
                    config={"displayModeBar": False, "responsive": True},
                    style={"height": "100%", "width": "100%", "flex": 1, "minHeight": 0},
                ),
            ],
            gap="xs",
            h="100%",
            style={"flex": 1, "minHeight": 0},
            px="md",
            py="sm",
        ),
        h="100%",
        w="25%",
        mt=0,
        radius="md",
        withBorder=True,
        className="schematic-card",
        style={"flex": "1 1 160px", "display": "flex", "minHeight": 0, "height": "100%"},
    )
