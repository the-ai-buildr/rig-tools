# Skill: Using Streamlit Layouts

<!--
Purpose: Layout primitives — columns, containers, sidebar, dialogs, tabs, expanders.
Source: https://github.com/the-ai-buildr/st-agent-skills (using-streamlit-layouts)
-->

## When to Use

Placing content in sidebars, columns, containers, dialogs, tabs, or expanders.

## Rules

1. **Sidebar:** navigation and app-level filters only — no primary content, no charts, no tables.
2. **Max 4 columns** to prevent cramped layouts. Use width ratios (`[1, 3]`) for emphasis.
3. Prefer `st.container(horizontal=True)` over `st.columns` for button groups and action bars.
4. `horizontal_alignment` on containers: `"left"` | `"center"` | `"right"` | `"distribute"`.
5. `border=True` on containers for visual card grouping.
6. `st.tabs` always renders **all tab content** even when hidden — conditionally render expensive content.
7. `@st.dialog` for focused confirmations and short forms that rerun independently.
8. `st.popover` for contextual info; `st.expander` for secondary/optional content.
9. `st.empty()` for updateable single-element placeholders (status messages, spinners).
10. `gap` parameter on containers; `st.space()` for explicit vertical spacing.
11. Element sizing: `"stretch"`, `"content"`, or fixed pixel dimensions.

## Patterns

```python
# Ratio columns — label narrow, input wide
label_col, input_col = st.columns([1, 3])
with label_col:
    st.write("Mud weight")
with input_col:
    mw = st.number_input("Mud weight", label_visibility="collapsed")

# Horizontal button group
with st.container(horizontal=True):
    st.button(":material/calculate: Calculate", type="primary")
    st.button(":material/restart_alt: Reset")

# Centered container
with st.container(horizontal_alignment="center"):
    st.metric("Kill mud weight", "12.8 ppg")

# Dialog for confirmation
@st.dialog("Confirm reset")
def confirm_reset():
    st.write("This will clear all inputs. Continue?")
    if st.button("Yes, reset"):
        st.session_state.clear()
        st.rerun()

# Sidebar filters
with st.sidebar:
    st.selectbox("Well", options=well_list)
    st.date_input("Date range", value=(start, end))

# Updateable placeholder
status = st.empty()
status.info("Calculating...")
# ... do work ...
status.success("Done!")
```
