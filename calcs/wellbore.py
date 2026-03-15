import pandas as pd
import numpy as np

def calc_capacity(depth: pd.Series, hole_diameter: pd.Series) -> pd.Series:
    """Calculate the capacity of the wellbore at each depth."""
    try:
        radius = hole_diameter / 2
        capacity = np.pi * radius**2 * depth
    except Exception as e:
        # Return NaN series if error occurs
        capacity = pd.Series([np.nan] * len(depth))
    return capacity