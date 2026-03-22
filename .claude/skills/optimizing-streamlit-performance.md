# Skill: Optimizing Streamlit Performance

<!--
Purpose: Caching, fragments, forms, and rerun optimization patterns.
Source: https://github.com/the-ai-buildr/st-agent-skills (optimizing-streamlit-performance)
-->

## When to Use

Improving app speed, reducing reruns, caching data or resources, or optimizing rendering.

## Rules

1. `@st.cache_data` — for data, computation results, DataFrames, serializable objects.
   Always add `ttl=` to prevent stale data from accumulating indefinitely.
2. `@st.cache_resource` — for connections, models, non-serializable objects.
   **Shared across ALL users and sessions.** Never mutate the returned object — mutations affect everyone.
3. `@st.fragment` — isolates reruns to the decorated function's scope.
   **Project rule:** all independently-rerendering components use `@st.fragment` (see CLAUDE.md rule #4).
4. `st.form` — batches multiple widget inputs into one rerun on submit.
   Use `border=False` for inline forms; keep border for longer standalone forms.
5. Avoid loading full datasets — prefer filtered DB queries.
6. `st.tabs` always renders **all tab content** even when hidden — use conditional rendering
   for expensive computations inside tabs.
7. Caches without `ttl` or `max_entries` can grow indefinitely — always set one.
8. For datasets >~100M rows, `@st.cache_resource` avoids serialization overhead vs `@st.cache_data`.

## Patterns

```python
# Cached API call with TTL
@st.cache_data(ttl=300)
def fetch_well_data(well_id: str) -> dict:
    data, err = api_request("GET", f"/api/wells/{well_id}")
    return data or {}

# Cached DB connection (shared resource — never mutate)
@st.cache_resource
def get_db_client():
    return create_supabase_client()

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
    run_kill_sheet(depth, mw)  # process outside the form

# Conditional tab content (avoid rendering all tabs every time)
tabs = st.tabs(["Kill Sheet", "Annular Velocity"])
with tabs[0]:
    if st.session_state.get("active_tab") == "kill":
        render_kill_sheet()
```
