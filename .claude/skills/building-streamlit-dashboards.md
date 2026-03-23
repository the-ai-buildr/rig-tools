# Skill: Building Streamlit Dashboards

<!--
Purpose: Dashboard layout patterns — KPI cards, metric rows, sparklines, filters.
Source: https://github.com/the-ai-buildr/st-agent-skills (building-streamlit-dashboards)
-->

## When to Use

Building KPI displays, metric cards, or data-heavy dashboard layouts.

## Key Patterns

- `border=True` on `st.container`, `st.metric`, `st.columns`, `st.form` for visual card grouping.
- `st.container(horizontal=True)` for responsive metric rows — wraps on small screens; prefer over `st.columns` for KPI rows.
- `st.metric(..., chart_data=weekly_values, chart_type="line")` for inline sparklines (evenly-spaced series only).
- Sidebar holds filters; main area holds all content.

## Patterns

```python
# Responsive KPI card row
with st.container(horizontal=True):
    with st.container(border=True):
        st.metric("Mud Weight", "12.5 ppg", delta="+0.2 ppg",
                  chart_data=[12.1, 12.2, 12.3, 12.5], chart_type="line")
    with st.container(border=True):
        st.metric("Annular Velocity", "142 ft/min")
    with st.container(border=True):
        st.metric("Hydrostatic Pressure", "6,240 psi")

# Sidebar filters
with st.sidebar:
    well = st.selectbox("Well", options=well_list)
    date_range = st.date_input("Date range", value=(start, end))
```

## Templates Available

`dashboard-metrics`, `dashboard-companies`, `dashboard-compute`, `dashboard-feature-usage`,
`dashboard-seattle-weather`, `dashboard-stock-peers` in the source repo's `templates/apps/`.
