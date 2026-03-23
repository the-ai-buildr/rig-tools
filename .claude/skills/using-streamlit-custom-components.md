# Skill: Using Streamlit Custom Components

<!--
Purpose: Third-party community Streamlit components — when and how to use them.
Source: https://github.com/the-ai-buildr/st-agent-skills (using-streamlit-custom-components)
-->

## When to Use

Extending Streamlit with community packages when core Streamlit doesn't cover the need.

## Before Adopting a Third-Party Component

Check in order:
1. Does a core Streamlit feature already do this? (prefer built-in)
2. Is the package actively maintained?
3. Is it compatible with the current Streamlit version?
4. Is it popular enough to trust?

Always install via PyPI package name (may differ from import name).

## Popular Components

| Package | Import | Use Case |
|---|---|---|
| `streamlit-keyup` | `st_keyup` | Keystroke-level text input for live search |
| `streamlit-bokeh` | `streamlit_bokeh` | Official replacement for removed `st.bokeh_chart` |
| `streamlit-aggrid` | `st_aggrid` | Advanced interactive dataframes (grouping, pivoting, complex filtering) |
| `streamlit-folium` | `st_folium` | Interactive Folium maps |
| `pygwalker` | `pygwalker` | Tableau-like drag-and-drop data exploration |
| `streamlit-extras` | various | Collection of community utilities |

## Usage Pattern

```python
# Install: pip install streamlit-aggrid
from st_aggrid import AgGrid, GridOptionsBuilder

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_side_bar()
gb.configure_selection("multiple", use_checkbox=True)
grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode="MODEL_CHANGED",
)
selected = grid_response["selected_rows"]
```
