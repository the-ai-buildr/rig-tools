# Skill: Choosing Streamlit Selection Widgets

<!--
Purpose: Widget selection guide — which input widget to use for which scenario.
Source: https://github.com/the-ai-buildr/st-agent-skills (choosing-streamlit-selection-widgets)
-->

## When to Use

Deciding which selection widget to use for a given input scenario.

## Decision Table

| Scenario | Widget |
|---|---|
| 2–5 options, single-select, all visible | `st.segmented_control` |
| 2–5 options, multi-select, all visible | `st.pills` |
| Many options, single-select, dropdown | `st.selectbox` |
| Many options, multi-select, dropdown | `st.multiselect` |
| Boolean on/off setting | `st.toggle` |
| Boolean inside a form | `st.checkbox` |

## Rules

- Replace `st.radio(..., horizontal=True)` with `st.segmented_control` — same semantics, modern look.
- `st.pills` with `label_visibility="collapsed"` for suggestion chips or prompt examples.
- `accept_new_options=True` on `st.selectbox` / `st.multiselect` allows user-defined entries.
- `st.toggle` for app settings (unit system, dark mode); `st.checkbox` for form opt-ins.

## Patterns

```python
# Unit system — replace radio
unit = st.segmented_control(
    "Unit system",
    options=["US", "Metric"],
    default="US",
    key="unit_system_ctrl",
)

# Multi-select visible chips
selected = st.pills(
    "Quick calculations",
    options=["Hydrostatic", "Kill sheet", "Annular velocity", "EMW"],
    selection_mode="multi",
)

# Selectbox with user-defined entries
formation = st.selectbox(
    "Formation",
    options=["Shale", "Sandstone", "Carbonate"],
    accept_new_options=True,
)

# App setting toggle
metric_mode = st.toggle("Metric units", key="metric_mode")
```
