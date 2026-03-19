import streamlit as st
import time
import datetime, dateutil
import numpy as np
import pandas as pd
from components.utils import horizontal_rule

def planner_table():
    st.subheader("HP 643 - Butters 5J 210H")
    st.caption("This is where the planner table will be displayed.")

    # Create fake data
    data = {
        'Procedure': [f'Procedure {i}' for i in range(1, 11)],
        'Est Hours': np.random.randint(1, 10, size=10),
        'Start Time': pd.date_range('2026-03-19 08:00', periods=10, freq='2h'),
        'End Time': pd.date_range('2026-03-19 09:00', periods=10, freq='2h'),
        'Actual Hours': np.random.randint(1, 10, size=10),
        'Remarks': [f'Remark {i}' for i in range(1, 11)]
    }

    planner = pd.DataFrame(data)

    col_conf = {
        "Procedure": st.column_config.TextColumn(
            "Procedure",
            help="Operational procedure to be performed.",
            max_chars=300,
            pinned=True,
            disabled=True,
            width="large"
        ),
        "Est Hours": st.column_config.NumberColumn(
            "Est Hours",
            help="Estimated hours for the procedure.",
            default=0.0,
            format="%.1f",
            pinned=False,
            disabled=False,
            width="125",
            required=True
        ),
        "Start Time": st.column_config.DatetimeColumn(
            "Start Time",
            help="Scheduled start time for the procedure.",
            default=datetime.datetime.now(),
            format="YYYY-MM-DD HH:mm",
            pinned=False,
            disabled=False,
            width="medium",
            required=True
        ),
        "End Time": st.column_config.DatetimeColumn(
            "End Time",
            help="Scheduled end time for the procedure.",
            default=datetime.datetime.now() + datetime.timedelta(hours=1),
            format="YYYY-MM-DD HH:mm",
            pinned=False,
            disabled=False,
            width="medium",
            required=True
        ),
        "Actual Hours": st.column_config.NumberColumn(
            "Actual Hours",
            help="Actual hours spent on the procedure.",
            default=0.0,
            format="%.1f",
            pinned=False,
            disabled=False,
            width="125",
            required=True
        ),
        "Remarks": st.column_config.TextColumn(
            "Remarks",
            help="Additional remarks or notes.",
            max_chars=400,
            pinned=False,
            disabled=False,
            width="large"
        )
    }

    edited_df = st.data_editor(
        planner, 
        column_config=col_conf,
        num_rows="dynamic", 
        height="content",
        width="content",
        disabled=[0,2]

    )

    return edited_df