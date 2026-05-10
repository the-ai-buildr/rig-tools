import dash_mantine_components as dmc
from dash_iconify import DashIconify


def metric_card(title, value, icon, color="indigo"):
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
                    DashIconify(icon=icon, width=20),
                    size="lg",
                    radius="md",
                    color=color,
                    variant="light",
                ),
            ],
            align="center",
            justify="space-between",
            h="100%",
            px="md",
            py="sm",
        ),
        h=100,
        radius="md",
        withBorder=True,
        style={"flex": "1 1 160px"},
    )
