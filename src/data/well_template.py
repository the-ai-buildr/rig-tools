"""
Default well template — pre-populates a new Well with standard structure.
Pure Python, no framework imports.

Produced by: backend-agent / data-layer
"""
from data.models import Well, WellHeader, Wellbore, CasingLiner


def apply_template(well: Well) -> Well:
    """Fill a Well with default template structure. Modifies and returns the well."""
    well.header = WellHeader()

    well.wellbores = [
        Wellbore(name="Main Bore", wellbore_type="Vertical", measured_depth=0.0, true_vertical_depth=0.0),
    ]

    well.casings = [
        CasingLiner(name="Surface Casing",      casing_type="Casing", grade="J-55"),
        CasingLiner(name="Intermediate Casing", casing_type="Casing", grade="N-80"),
        CasingLiner(name="Production Liner",    casing_type="Liner",  grade="P-110"),
    ]

    well.mud_entries = []

    return well
