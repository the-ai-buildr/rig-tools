import dash
from dash import html
import dash_mantine_components as dmc
from components.ui.metric_card import metric_card

dash.register_page(__name__, path="/setup")
tab_list = dmc.TabsList([
        dmc.TabsTab("Rig", value="rig", style={"fontSize": 14}),
        dmc.TabsTab("Mud Pumps", value="mud_pumps", style={"fontSize": 14}),
        dmc.TabsTab("Drawworks", value="drawworks", style={"fontSize": 14}),
    ],
    pt="md",
)

# Define the content for each tab panel
rig_info = dmc.TabsPanel("Rig Info", value="rig")
mud_pump_info = dmc.TabsPanel("Mud Pump Info", value="mud_pumps")
drawworks_info = dmc.TabsPanel("Drawworks Info", value="drawworks")

# Combine TabsList and TabsPanel into a single Tabs component
tab_secions = html.Div([
        rig_info, mud_pump_info, drawworks_info],
        style={"padding": "10px",  "borderTop": "none"})      

# Create the Tabs component
tabs = dmc.Tabs([
        tab_list,
        tab_secions,
    ],
    color="#2579FF",
    orientation="horizontal",
    variant="default", 
    value="rig"
)


layout = dmc.Box([
        dmc.Title("Setup", order=3),
        tabs
    ],
    p="sm",
)
