"""Login view — rendered into main-content when the user is unauthenticated."""
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def login_view():
    return dmc.Center(
        dmc.Card(
            dmc.Stack(
                [
                    dmc.Group(
                        [
                            DashIconify(
                                icon="tabler:shield-chevron",
                                width=32,
                                color="var(--brand)",
                            ),
                            dmc.Title("Rig Tools", order=2, c="var(--brand)", lh=1),
                        ],
                        gap=8,
                        justify="center",
                        align="center",
                    ),
                    dmc.Text(
                        "Sign in to continue",
                        c="dimmed",
                        size="sm",
                        ta="center",
                        mb="xs",
                    ),
                    dmc.TextInput(
                        id="login-email",
                        label="Email",
                        placeholder="you@example.com",
                        leftSection=DashIconify(icon="tabler:mail", width=16),
                    ),
                    dmc.PasswordInput(
                        id="login-password",
                        label="Password",
                        placeholder="Your password",
                        leftSection=DashIconify(icon="tabler:lock", width=16),
                    ),
                    html.Div(id="login-alert"),
                    dmc.Button(
                        "Sign in",
                        id="login-btn",
                        fullWidth=True,
                        leftSection=DashIconify(icon="tabler:login-2", width=18),
                    ),
                ],
                gap="sm",
            ),
            withBorder=True,
            shadow="md",
            radius="md",
            p="xl",
            style={"width": 360, "maxWidth": "92vw"},
        ),
        style={"height": "100vh", "width": "100%"},
    )
