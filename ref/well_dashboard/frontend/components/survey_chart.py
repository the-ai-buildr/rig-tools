"""
Survey Chart Component

Renders Plan vs Actual directional survey visualisations using Plotly:
    - Vertical section view  (VS on X, TVD on Y, inverted)
    - Plan view / spider plot (Easting on X, Northing on Y)

Usage:
    from frontend.components.survey_chart import render_survey_charts

    render_survey_charts(well["survey_plan"], well["survey_actual"])
"""

from typing import Optional
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def _make_trace(df: pd.DataFrame, x_col: str, y_col: str, name: str, colour: str, dash: str = "solid"):
    return go.Scatter(
        x=df.get(x_col, [0]).tolist(),
        y=df.get(y_col, [0]).tolist(),
        mode="lines+markers",
        name=name,
        line=dict(color=colour, dash=dash),
        marker=dict(size=5),
    )


def render_survey_charts(
    plan: list[dict],
    actual: list[dict],
) -> None:
    """
    Render side-by-side Vertical Section and Plan View charts.

    Args:
        plan:   List of planned survey point dicts.
        actual: List of actual survey point dicts.
    """
    if not plan and not actual:
        st.info("No survey data to visualise. Add survey stations in the Plan or Actual tab.")
        return

    plan_df   = pd.DataFrame(plan)   if plan   else pd.DataFrame()
    actual_df = pd.DataFrame(actual) if actual else pd.DataFrame()

    col1, col2 = st.columns(2)

    # ── Vertical Section ──────────────────────────────────────────────────────
    with col1:
        st.markdown("##### 📐 Vertical Section")
        fig = go.Figure()

        if not plan_df.empty:
            fig.add_trace(_make_trace(plan_df, "vertical_section", "tvd", "Plan", "#4472c4", "dash"))
        if not actual_df.empty:
            fig.add_trace(_make_trace(actual_df, "vertical_section", "tvd", "Actual", "#28a745"))

        fig.update_layout(
            xaxis_title="VS (ft)",
            yaxis_title="TVD (ft)",
            yaxis_autorange="reversed",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(l=40, r=20, t=30, b=40),
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Plan View ─────────────────────────────────────────────────────────────
    with col2:
        st.markdown("##### 🗺️ Plan View (Top-Down)")
        fig2 = go.Figure()

        if not plan_df.empty:
            fig2.add_trace(_make_trace(plan_df, "easting", "northing", "Plan", "#4472c4", "dash"))
        if not actual_df.empty:
            fig2.add_trace(_make_trace(actual_df, "easting", "northing", "Actual", "#28a745"))

        fig2.update_layout(
            xaxis_title="Easting (ft)",
            yaxis_title="Northing (ft)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(l=40, r=20, t=30, b=40),
            height=400,
        )
        st.plotly_chart(fig2, use_container_width=True)
