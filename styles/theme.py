# Re-export dmc_theme as `theme` for backward compatibility with app.py.
# Source of truth: styles/flowtides_theme.py
from .flowtides_theme import dmc_theme as theme

__all__ = ["theme"]
