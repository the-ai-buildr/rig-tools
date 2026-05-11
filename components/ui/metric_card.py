import dash_mantine_components as dmc
from dash_iconify import DashIconify


def metric_card(title, value, icon, color="blue"):
    return dmc.Paper(
        dmc.Flex(
            [
                dmc.Stack(
                    [
                        dmc.Text(title, size="xs", c="dimmed", tt="uppercase", fw=600),
                        dmc.Text(value, size="xl", fw=700),
                    ],
                    gap=2,
                    style={"flex": 1},
                ),
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=32),
                    size="lg",
                    radius="md",
                    p=4,
                    color=color,
                    variant="light",
                ),
            ],
            align="center",
            justify="space-between",
            
            h="100%",
            px="md",
            py="xs",
        ),
        h=75,
        mt=2,
        radius="md",
        withBorder=True,
        className="metric-card",
        style={"flex": "1 1 160px"},
    )
