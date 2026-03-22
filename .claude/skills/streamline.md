# Skill: Developing with Streamlit

<!--
Purpose: Streamlit best-practices skill set — routing hub for design, layout, performance,
         data display, session state, and widget selection guidance.
Source: https://github.com/the-ai-buildr/st-agent-skills (developing-with-streamlit)
Produced by: frontend-agent
-->

## Purpose

Provide authoritative Streamlit patterns and best practices when building or improving UI in Rig Tools.
This skill routes to the appropriate sub-area based on the task type.

## When to Use

Activate when the task contains: **design**, **layout**, **widget**, **chart**, **display**, **cache**,
**performance**, **session state**, **dashboard**, **metric**, **column**, **badge**, **icon**, **theme**,
or when the existing Streamlit-pages / Streamlit-components skills don't cover the specific guidance needed.

## Project Entry Points (Rig Tools)

- **ASGI entry:** `asgi.py` (mounts Streamlit + FastAPI — never run directly)
- **Streamlit script:** `app.py` (called by `asgi.py` — not `streamlit_app.py`)
- **Pages:** `pages/{NN}_{name}.py` (two-digit prefix, auto-discovered by Streamlit)
- **Components:** `components/{feature}/{name}.py` (fragments go here)

> Rig Tools uses Streamlit 1.55 with the legacy `pages/` directory — **not** `app_pages/` or
> `st.navigation()`. Respect the existing routing conventions in CLAUDE.md.

---

## Routing Table

| Task | Sub-area |
|---|---|
| KPI cards, metrics, dashboard layout | [Dashboards](#dashboards) |
| Visual appearance, icons, badges, spacing | [Design](#design) |
| Columns, sidebar, containers, tabs, dialogs | [Layouts](#layouts) |
| `st.session_state`, callbacks, page state | [Session State](#session-state) |
| Caching, fragments, forms, reruns | [Performance](#performance) |
| Radio, select, pills, segmented control | [Selection Widgets](#selection-widgets) |
| Tables, dataframes, charts, column config | [Data Display](#data-display) |

---

## Dashboards

### Rules

- Use `st.container(border=True)` for KPI card grouping — creates visual separation without CSS hacks.
- Use `st.container(horizontal=True)` for metric rows — more responsive than fixed-column grids.
- Sidebar holds filters; main area holds content.
- Sparklines: pass `chart_data` + `chart_type` to `st.metric` (evenly-spaced series data only).

### Patterns

```python
# KPI card row
with st.container(horizontal=True):
    with st.container(border=True):
        st.metric("Mud Weight", "12.5 ppg", delta="+0.2 ppg",
                  chart_data=[12.1, 12.2, 12.3, 12.5], chart_type="line")
    with st.container(border=True):
        st.metric("Annular Velocity", "142 ft/min")
    with st.container(border=True):
        st.metric("Hydrostatic Pressure", "6,240 psi")
```

---

## Design

### Rules

1. Use **Material icons** (`:material/icon_name:`) everywhere — never emoji for UI elements.
   Source icon names from [Google Fonts Icons](https://fonts.google.com/icons).
2. Use `st.badge()` or inline `:green-badge[Active]` for status indicators.
3. **Sentence case** for all labels, titles, and button text. Avoid Title Case ("Feels Shouty").
4. Remove `st.divider()` / `---` dividers — Streamlit's default spacing is sufficient.
   Use `st.space()` only when explicit breathing room is needed.
5. `st.caption()` for lightweight metadata; `st.info()` for important instructions;
   `st.toast()` for auto-dismissing confirmations (not `st.success()`).
6. `st.set_page_config()` is called **once** in `app.py` — never repeat in page files.

### Examples

```python
# Icons in buttons and labels
st.button(":material/calculate: Calculate", type="primary")
st.button(":material/refresh: Reset")

# Status badge
st.badge("Active", color="green")
# or inline
st.markdown(":green-badge[Active]  :red-badge[Offline]")

# Feedback patterns
st.caption("Last updated: 14:32 UTC")        # lightweight info
st.info(":material/info: Fill in all fields before submitting.")  # instruction
st.toast("Saved successfully!")              # transient confirmation
```

---

## Layouts

### Rules

1. **Sidebar:** navigation and app-level filters only — no primary content.
2. **Max 4 columns** to avoid cramped layouts; use width ratios for emphasis.
3. Prefer `st.container(horizontal=True)` over `st.columns` for button groups and action bars.
4. Container alignment options: `"left"` | `"center"` | `"right"` | `"distribute"`.
5. `st.tabs` always renders **all tab content** even when hidden — use conditional rendering
   for expensive computations.
6. `st.empty()` for updateable single-element placeholders (e.g., status messages).
7. Use `st.dialog` for confirmations and short forms; `st.popover` for contextual info.

### Patterns

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

# Conditional tab content (avoid rendering all tabs)
tab = st.tabs(["Kill Sheet", "Annular Velocity", "Hydrostatic"])
with tab[0]:
    if st.session_state.get("active_tab") == "kill":
        render_kill_sheet()

# Confirmation dialog
@st.dialog("Confirm reset")
def confirm_reset():
    st.write("This will clear all inputs. Continue?")
    if st.button("Yes, reset"):
        st.session_state.clear()
        st.rerun()
```

---

## Session State

### Rules

1. Initialize with `st.session_state.setdefault(key, default)` — never overwrite on every run.
2. Widget `key=` parameter auto-syncs to `st.session_state[key]` — no manual assignment needed.
3. Callbacks run **before** the rerun — read widget values from `st.session_state` inside callbacks,
   not from widget return values.
4. Widget values **reset on page navigation**; explicitly stored state persists across pages.
5. Use `"namespace_key"` naming for page-specific state: `"kill_sheet_depth"`, not `"depth"`.
6. Never mix `value=` and `key=` targeting the same widget state — pick one pattern.
7. Session state is per-user and ephemeral — persist to Supabase for durable data.

### Patterns

```python
# Safe initialization (never overwrites)
st.session_state.setdefault("unit_system", "us")
st.session_state.setdefault("kill_sheet_results", None)

# Callback pattern — read from state, not widget return
def on_unit_change():
    # st.session_state["unit_system"] is already updated here
    convert_cached_results(st.session_state["unit_system"])

st.selectbox("Unit system", ["us", "metric"],
             key="unit_system", on_change=on_unit_change)

# Safe read
results = st.session_state.get("kill_sheet_results")
if results:
    render_results(results)
```

---

## Performance

### Rules

1. `@st.cache_data` — for data, computation results, DataFrames, serializable objects.
   Add `ttl=` to prevent stale data.
2. `@st.cache_resource` — for connections, models, non-serializable objects (shared across users).
   **Never mutate** a `@st.cache_resource` return — changes affect all users.
3. `@st.fragment` — isolates reruns to the decorated function's scope.
   Use for any component that updates without requiring a full page rerun.
   (Project rule: **all independently-rerending components use `@st.fragment`** — see CLAUDE.md.)
4. `st.form` — batches multiple inputs into one rerun on submit.
   Use `border=False` for inline forms; keep border for longer forms.
5. Avoid loading full datasets into memory — prefer filtered DB queries.

### Patterns

```python
# Cached API call with TTL
@st.cache_data(ttl=300)
def fetch_well_data(well_id: str) -> dict:
    data, err = api_request("GET", f"/api/wells/{well_id}")
    return data or {}

# Fragment for partial rerender (project convention)
@st.fragment
def kill_sheet_results_panel():
    results = st.session_state.get("kill_sheet_results")
    if not results:
        st.info("Run a calculation to see results.")
        return
    render_kill_results(results)

# Batched form
with st.form("kill_sheet_form", border=False):
    depth = st.number_input("Depth (ft)")
    mw = st.number_input("Mud weight (ppg)")
    submitted = st.form_submit_button(":material/calculate: Calculate", type="primary")
if submitted:
    # process outside the form
    run_kill_sheet(depth, mw)
```

---

## Selection Widgets

### Decision Table

| Scenario | Widget |
|---|---|
| 2–5 options, single select, all visible | `st.segmented_control` |
| 2–5 options, multi-select, all visible | `st.pills` |
| Many options, single select, dropdown | `st.selectbox` |
| Many options, multi-select, dropdown | `st.multiselect` |
| Boolean on/off setting | `st.toggle` |
| Boolean in a form | `st.checkbox` |

### Rules

1. Replace `st.radio(..., horizontal=True)` with `st.segmented_control` — modern look, same semantics.
2. `st.pills` with `label_visibility="collapsed"` for suggestion chips / prompt examples.
3. `accept_new_options=True` on `st.selectbox` / `st.multiselect` allows user-defined entries.
4. `st.toggle` for app settings (unit system, dark mode, etc.); `st.checkbox` for form opt-ins.

### Patterns

```python
# Unit system toggle — replace radio
unit = st.segmented_control(
    "Unit system",
    options=["US", "Metric"],
    default="US",
    key="unit_system_ctrl"
)

# Multi-select with visible chips
selected_calcs = st.pills(
    "Quick calculations",
    options=["Hydrostatic", "Kill sheet", "Annular velocity", "EMW"],
    selection_mode="multi",
)

# Selectbox allowing user-defined entries
formation = st.selectbox(
    "Formation",
    options=["Shale", "Sandstone", "Carbonate"],
    accept_new_options=True,
)
```

---

## Data Display

### Decision Table

| Need | Widget |
|---|---|
| Interactive, sortable, filterable table | `st.dataframe` |
| User-editable table | `st.data_editor` |
| Static display table | `st.table` |
| KPI numbers with delta | `st.metric` |
| Raw JSON inspection | `st.json` |
| Simple trend charts | `st.line_chart`, `st.bar_chart`, `st.area_chart` |
| Complex / custom charts | Altair (bundled — no install needed) |

### Rules

1. Always use `st.dataframe` over `st.table` unless output must be completely static.
2. Use `column_config` to format currency, progress bars, links, images, datetimes.
3. `pinned=True` on `TextColumn` to keep identifier columns visible during horizontal scroll.
4. `st.data_editor` with `num_rows="dynamic"` enables add/delete row UX.
5. Altair for complex charts — already bundled with Streamlit, no extra install.
   Plotly requires a separate package (`plotly` in requirements.txt).
6. Native chart params: `color`, `stack`, `horizontal` — use these before reaching for Altair.

### Patterns

```python
import streamlit as st
import altair as alt

# Formatted dataframe
st.dataframe(
    df,
    column_config={
        "depth_ft": st.column_config.NumberColumn("Depth (ft)", format="%.1f"),
        "mud_weight": st.column_config.NumberColumn("Mud Wt (ppg)", format="%.2f"),
        "pressure_psi": st.column_config.ProgressColumn(
            "Pressure", min_value=0, max_value=10000, format="%d psi"
        ),
        "report_url": st.column_config.LinkColumn("Report"),
        "well_id": st.column_config.TextColumn("Well", pinned=True),
    },
    hide_index=True,
    use_container_width=True,
)

# Editable table with add/delete
edited = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
)

# Altair chart example
chart = (
    alt.Chart(df)
    .mark_line()
    .encode(x="depth_ft:Q", y="pressure_psi:Q", color="well_id:N")
    .properties(height=300)
)
st.altair_chart(chart, use_container_width=True)
```

---

## Rig Tools Integration Notes

- This skill complements, not replaces, **Streamlit Pages** and **Streamlit Components** skills.
- `@st.fragment` rules in this skill align with project non-negotiable rule #4 in CLAUDE.md.
- All data fetching in components goes through `frontend/api_client.py` — never direct Supabase.
- Cache keys that include user identity must use `st.session_state["auth_user"]["id"]` to avoid
  cross-user data leakage with `@st.cache_data`.
- `st.set_page_config()` is already called in `app.py` — never call it in components or pages.
