"""
Reusable Stepper component.

Build a themed dmc.Stepper from a list of step dicts, with Back / Next
navigation wired up via a single pattern-matching callback.

Usage
-----
    from components.ui.stepper import stepper

    my_stepper = stepper(
        "well-setup",                       # unique id for this stepper
        steps=[
            {"label": "First step",  "description": "Create an account",
             "content": dmc.Text("Step 1 content")},
            {"label": "Second step", "description": "Verify email",
             "content": dmc.Text("Step 2 content")},
            {"label": "Final step",  "description": "Get full access",
             "content": dmc.Text("Step 3 content")},
        ],
        completed=dmc.Text("All done!"),     # optional completed-state content
    )

Register the navigation callback once at startup (see callbacks/register.py):

    from components.ui.stepper import register_stepper_callbacks
    register_stepper_callbacks(app)

Each step dict accepts:
    label       (str)            — step title
    description (str, optional)  — sub-label under the title
    content     (component)      — body rendered when the step is active
    icon        (str, optional)  — tabler icon name for the step bullet
"""
import dash_mantine_components as dmc
from dash import Input, Output, State, ALL, ctx, MATCH
from dash_iconify import DashIconify


def _ids(stepper_id: str) -> dict:
    return {
        "stepper": {"type": "stepper", "id": stepper_id},
        "back":    {"type": "stepper-back", "id": stepper_id},
        "next":    {"type": "stepper-next", "id": stepper_id},
    }


def _build_step(step: dict) -> dmc.StepperStep:
    icon = step.get("icon")
    return dmc.StepperStep(
        label=step.get("label"),
        description=step.get("description"),
        icon=DashIconify(icon=icon, width=18) if icon else None,
        children=step.get("content"),
    )


def stepper(
    stepper_id: str,
    steps: list[dict],
    active: int = 0,
    completed=None,
    color: str = "blue",
    radius: str = "md",
    show_controls: bool = True,
    back_label: str = "Back",
    next_label: str = "Next step",
) -> dmc.Stack:
    """Return a themed Stepper with optional Back / Next controls."""
    ids = _ids(stepper_id)

    children = [_build_step(step) for step in steps]
    if completed is not None:
        children.append(dmc.StepperCompleted(children=completed))

    parts = [
        dmc.Stepper(
            id=ids["stepper"],
            active=active,
            color=color,
            radius=radius,
            children=children,
        ),
    ]

    if show_controls:
        parts.append(
            dmc.Group(
                justify="center",
                mt="xl",
                children=[
                    dmc.Button(back_label, id=ids["back"], variant="default"),
                    dmc.Button(next_label, id=ids["next"], color=color),
                ],
            )
        )

    return dmc.Stack(parts, gap="md")


def register_stepper_callbacks(app):
    """Wire Back / Next buttons to every stepper built with `stepper()`."""

    @app.callback(
        Output({"type": "stepper", "id": MATCH}, "active"),
        Input({"type": "stepper-back", "id": MATCH}, "n_clicks"),
        Input({"type": "stepper-next", "id": MATCH}, "n_clicks"),
        State({"type": "stepper", "id": MATCH}, "active"),
        State({"type": "stepper", "id": MATCH}, "children"),
        prevent_initial_call=True,
    )
    def _update(_back, _next, current, children):
        step = current or 0
        # max_step = number of StepperStep/StepperCompleted children
        max_step = len(children) if isinstance(children, list) else 0
        triggered = ctx.triggered_id or {}
        if triggered.get("type") == "stepper-back":
            return step - 1 if step > 0 else step
        return step + 1 if step < max_step else step
