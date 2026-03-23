"""
Planner table component — editable operational schedule for a rig/well.

Produced by: frontend-agent / developing-with-streamlit skill
"""
import streamlit as st
import datetime
import numpy as np
import pandas as pd
from components.utils import horizontal_rule


@st.fragment
def planner_table(rig: str = "HP 643", well: str = "Butters 5J 210H"):
    st.subheader(f"{rig} \u2014 {well}")
    st.caption("Operational planner — edit procedures, times, and remarks inline.")

    # TODO: replace with real API data keyed on rig/well
    data = {
        "Procedure": [f"Procedure {i}" for i in range(1, 11)],
        "Est Hours": np.random.randint(1, 10, size=10).astype(float),
        "Start Time": pd.date_range("2026-03-19 08:00", periods=10, freq="2h"),
        "End Time": pd.date_range("2026-03-19 09:00", periods=10, freq="2h"),
        "Actual Hours": np.random.randint(1, 10, size=10).astype(float),
        "Remarks": [f"Remark {i}" for i in range(1, 11)],
    }
    planner = pd.DataFrame(data)

    col_conf = {
        "Procedure": st.column_config.TextColumn(
            "Procedure",
            help="Operational procedure to be performed.",
            max_chars=300,
            pinned=True,
            width="large",
        ),
        "Est Hours": st.column_config.NumberColumn(
            "Est hours",
            help="Estimated hours for the procedure.",
            default=0.0,
            format="%.1f",
            width="small",
            required=True,
        ),
        "Start Time": st.column_config.DatetimeColumn(
            "Start time",
            help="Scheduled start time.",
            default=datetime.datetime.now(),
            format="YYYY-MM-DD HH:mm",
            width="medium",
            required=True,
        ),
        "End Time": st.column_config.DatetimeColumn(
            "End time",
            help="Scheduled end time.",
            default=datetime.datetime.now() + datetime.timedelta(hours=1),
            format="YYYY-MM-DD HH:mm",
            width="medium",
            required=True,
        ),
        "Actual Hours": st.column_config.NumberColumn(
            "Actual hours",
            help="Actual hours spent.",
            default=0.0,
            format="%.1f",
            width="small",
            required=True,
        ),
        "Remarks": st.column_config.TextColumn(
            "Remarks",
            help="Additional remarks or notes.",
            max_chars=400,
            width="large",
        ),
    }

    edited_df = st.data_editor(
        planner,
        column_config=col_conf,
        num_rows="dynamic",
        use_container_width=True,
    )

    return edited_df
