"""
Data Table Component

Thin wrapper around ``st.dataframe`` that applies consistent formatting
and handles the empty-state gracefully.

Usage:
    from frontend.components.data_table import render_data_table

    render_data_table(well["casing_plan"], empty_msg="No planned casing strings yet.")
"""

from typing import Optional
import pandas as pd
import streamlit as st


def render_data_table(
    data: list[dict],
    columns: Optional[list[str]] = None,
    column_labels: Optional[dict[str, str]] = None,
    empty_msg: str = "No data available.",
    height: Optional[int] = None,
) -> None:
    """
    Render a list of dicts as a styled dataframe.

    Args:
        data:          List of row dicts (from the API).
        columns:       Subset of keys to display (preserves order).
                       Defaults to all keys.
        column_labels: Mapping from raw key → display header.
                       Example: {"casing_od": "OD (in)", "casing_id": "ID (in)"}
        empty_msg:     Message shown when *data* is empty.
        height:        Optional pixel height for the table widget.
    """
    if not data:
        st.info(empty_msg)
        return

    df = pd.DataFrame(data)

    if columns:
        # Only keep columns that actually exist in the data
        existing = [c for c in columns if c in df.columns]
        df = df[existing]

    if column_labels:
        df = df.rename(columns=column_labels)

    # Drop internal DB fields the user doesn't need to see
    for hidden in ("id", "well_id", "is_plan"):
        if hidden in df.columns:
            df = df.drop(columns=[hidden])

    kwargs: dict = {"hide_index": True, "use_container_width": True}
    if height:
        kwargs["height"] = height

    st.dataframe(df, **kwargs)
