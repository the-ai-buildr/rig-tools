import dash
import dash_mantine_components as dmc
from components.ui.metric_card import metric_card

dash.register_page(__name__, path="/home")

layout = dmc.Box(
    [
        dmc.Title("Overview", order=3, mb="5px"),
        dmc.Divider(mb="sm"),
        dmc.Flex(
            [
                metric_card("Active Wells", "12", "tabler:antenna", color="red"),
                metric_card("Daily Footage", "4,280'", "tabler:chart-bar", color="blue"),
                metric_card("Rig Hours", "186 hrs", "tabler:clock", color="orange"),
                metric_card("Incidents", "0", "tabler:shield-check", color="green"),
                metric_card("Efficiency", "94.2%", "tabler:trending-up", color="purple"),
            ],
            gap="md",
            wrap="wrap",
        ),
    ],
    p="sm",
)
