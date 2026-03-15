import pandas as pd
import numpy as np

def calc_capacity(depth: pd.Series, hole_diameter: pd.Series) -> pd.Series:
    """Calculate the capacity of the wellbore at each depth."""
    try:
        radius = hole_diameter / 2
        capacity = np.pi * radius**2 * depth
    except Exception:
        # Return NaN series if error occurs
        capacity = pd.Series([np.nan] * len(depth))
    return capacity

def calc_segment_capacity(depth_top: pd.Series, depth_btm: pd.Series, hole_diameter: pd.Series) -> pd.Series:
    """Calculate the capacity of the wellbore segment between two depths."""
    length = depth_btm - depth_top
    try:
        radius = hole_diameter / 2
        capacity = np.pi * radius**2 * length
    except Exception:
        # Return NaN series if error occurs
        capacity = pd.Series([np.nan] * len(length))
    return capacity

def calc_displacement(depth: pd.Series, hole_diameter: pd.Series) -> pd.Series:
    """Calculate the displacement of the wellbore at each depth."""
    try:
        radius = hole_diameter / 2
        displacement = np.pi * radius**2 * depth
    except Exception as e:
        # Return NaN series if error occurs
        displacement = pd.Series([np.nan] * len(depth))
    return displacement

def calc_segment_displacement(depth_top: pd.Series, depth_btm: pd.Series, hole_diameter: pd.Series) -> pd.Series:
    """Calculate the displacement of the wellbore segment between two depths."""
    length = depth_btm - depth_top
    try:
        radius = hole_diameter / 2
        displacement = np.pi * radius**2 * length
    except Exception:
        # Return NaN series if error occurs
        displacement = pd.Series([np.nan] * len(length))
    return displacement

def calc_volume(depth: pd.Series, hole_diameter: pd.Series) -> pd.Series:
    """Calculate the volume of the wellbore at each depth."""
    try:
        radius = hole_diameter / 2
        volume = np.pi * radius**2 * depth
    except Exception as e:
        # Return NaN series if error occurs
        volume = pd.Series([np.nan] * len(depth))
    return volume

def calc_segment_volume(depth_top: pd.Series, depth_btm: pd.Series, hole_diameter: pd.Series) -> pd.Series:
    """Calculate the volume of the wellbore segment between two depths."""
    length = depth_btm - depth_top
    try:
        radius = hole_diameter / 2
        volume = np.pi * radius**2 * length
    except Exception:
        # Return NaN series if error occurs
        volume = pd.Series([np.nan] * len(length))
    return volume