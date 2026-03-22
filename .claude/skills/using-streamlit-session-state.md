# Skill: Using Streamlit Session State

<!--
Purpose: st.session_state patterns — initialization, callbacks, cross-page state, common pitfalls.
Source: https://github.com/the-ai-buildr/st-agent-skills (using-streamlit-session-state)
-->

## When to Use

Managing state across reruns, sharing data across pages, or using widget callbacks.

## Rules

1. `st.session_state.setdefault("key", default)` — preferred initialization; never overwrites existing value.
2. Widget `key=` parameter auto-syncs to `st.session_state[key]` — no manual assignment needed.
3. Callbacks (`on_change`, `on_click`) execute **before** the rerun — read widget values from
   `st.session_state` inside callbacks, not from widget return values.
4. **Widgets are NOT stateful across pages** — use session state variables (not widget keys) to share
   data across pages. Put shared widgets in the entry point (before `nav.run()`).
5. Use namespaced keys for page-specific state: `"kill_sheet_depth"`, not `"depth"`.
6. Never mix `value=` and `key=` targeting the same widget — pick one pattern.
7. Session state is per-user and per-tab — ephemeral; lost when tab closes or server restarts.
   Persist to Supabase for durable data.

## Common Mistakes

```python
# WRONG — module-level mutable state is shared across ALL users
user_data = {}  # This is global! Every user modifies the same dict.

# RIGHT — store per-user data in session state
st.session_state.setdefault("user_data", {})

# WRONG — reading widget value after setting state in callback
def on_change():
    process(new_value)  # new_value is from outer scope — may be stale

# RIGHT — read from session state inside callback
def on_change():
    process(st.session_state["my_widget"])

# WRONG — widget key does NOT persist across page navigation
st.selectbox("Well", options=wells, key="well_select")
# If user navigates away and comes back, well_select resets to default

# RIGHT — store the value explicitly before page change
st.session_state["selected_well"] = st.session_state.get("well_select")
```

## Patterns

```python
# Safe initialization (entry point / global_init)
st.session_state.setdefault("unit_system", "us")
st.session_state.setdefault("kill_sheet_results", None)
st.session_state.setdefault("auth_user", None)

# Callback — read from state
def on_unit_change():
    convert_cached_results(st.session_state["unit_system"])

st.selectbox("Unit system", ["us", "metric"],
             key="unit_system", on_change=on_unit_change)

# Safe read with fallback
results = st.session_state.get("kill_sheet_results")
if results:
    render_results(results)

# Namespaced page-specific keys
st.session_state.setdefault("kill_sheet_depth", 0.0)
st.session_state.setdefault("kill_sheet_mw", 8.6)
st.session_state.setdefault("hydrostatic_tvd", 0.0)
```
