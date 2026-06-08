import dash
import dash_mantine_components as dmc

from utils import page_body, page_header


dash.register_page(__name__, path="/test/schematic")


layout = page_body(
    page_header("Test Components"),
    dmc.Alert(
        "Use this page to prototype and validate UI components before moving them into production pages.",
        title="Test Lab",
        color="blue",
        variant="light",
    ),
    dmc.Card(
        [
            dmc.Text("Starter Canvas", fw=600),
            dmc.Text(
                "Add temporary component experiments here. Keep this route focused on quick UI iteration.",
                size="sm",
                c="dimmed",
                mt="xs",
            ),
        ],
        className="metric-card",
        radius="md",
        withBorder=True,
        p="sm",
        mt="sm",
    ),
)
