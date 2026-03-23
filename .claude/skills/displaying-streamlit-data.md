# Skill: Displaying Streamlit Data

<!--
Purpose: Tables, dataframes, charts, and column configuration patterns.
Source: https://github.com/the-ai-buildr/st-agent-skills (displaying-streamlit-data)
-->

## When to Use

Displaying tabular data, charts, KPI numbers, or structured data in Streamlit.

## Decision Table

| Need | Widget |
|---|---|
| Interactive, sortable, filterable table | `st.dataframe` |
| User-editable table | `st.data_editor` |
| Static display table | `st.table` |
| KPI numbers with delta / sparkline | `st.metric` |
| Raw JSON inspection | `st.json` |
| Simple trend charts | `st.line_chart`, `st.bar_chart`, `st.area_chart` |
| Complex / custom charts | Altair (bundled) |

## Rules

1. Prefer `st.dataframe` over `st.table` unless output must be completely static.
2. Start with native charting (`st.line_chart`, `st.bar_chart`); use Altair for customization.
3. Use `column_config` only when it genuinely helps — don't add it just for labels/tooltips.
4. **Critical — sensitive data:** Setting a column to `None` in `column_config` hides it from the UI
   but the data is **still sent to the frontend**. Pre-filter the DataFrame before display for sensitive data.
5. `st.data_editor` with `num_rows="dynamic"` enables add/delete row UX.
6. Altair is bundled with Streamlit — no extra install. Plotly requires `plotly` in requirements.txt.
7. Native chart params: `color`, `stack`, `horizontal` — use these before reaching for Altair.

## Patterns

```python
import streamlit as st
import altair as alt

# Formatted dataframe
st.dataframe(
    df,
    column_config={
        "depth_ft":       st.column_config.NumberColumn("Depth (ft)", format="%.1f"),
        "mud_weight":     st.column_config.NumberColumn("Mud Wt (ppg)", format="%.2f"),
        "pressure_psi":   st.column_config.ProgressColumn(
                              "Pressure", min_value=0, max_value=10000, format="%d psi"),
        "report_url":     st.column_config.LinkColumn("Report"),
        "well_id":        st.column_config.TextColumn("Well", pinned=True),
    },
    hide_index=True,
    use_container_width=True,
)

# Editable table
edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Altair chart
chart = (
    alt.Chart(df)
    .mark_line()
    .encode(x="depth_ft:Q", y="pressure_psi:Q", color="well_id:N")
    .properties(height=300)
)
st.altair_chart(chart, use_container_width=True)

# CORRECT — pre-filter before display (don't rely on column_config=None for security)
public_cols = ["well_id", "depth_ft", "mud_weight"]
st.dataframe(df[public_cols])
```
