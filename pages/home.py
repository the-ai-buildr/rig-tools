import dash
import dash_mantine_components as dmc
from components.ui.metric_card import metric_card

dash.register_page(__name__, path="/home")

layout = dmc.Box(
    [
        dmc.Title("Overview", order=1, mb="5px"),
        dmc.Divider(mb="sm"),

        dmc.Flex(
            [
                metric_card("Active Wells", "12", "tabler:antenna"),
                metric_card("Daily Output", "4,280 bbl", "tabler:chart-bar"),
                metric_card("Rig Hours", "186 hrs", "tabler:clock", color="orange"),
                metric_card("Incidents", "0", "tabler:shield-check", color="green"),
                metric_card("Efficiency", "94.2%", "tabler:trending-up", color="teal"),
            ],
            gap="md",
            wrap="wrap",
        ),
    ],
    p="sm", pt="0px",
)
