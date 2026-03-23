# Skill: Organizing Streamlit Code

<!--
Purpose: Code organization patterns for maintainable Streamlit apps.
Source: https://github.com/the-ai-buildr/st-agent-skills (organizing-streamlit-code)
-->

## When to Use

Deciding how to structure files, when to split code, and how to organize modules.

## Rules

- Keep everything in one file for apps under ~1000 lines.
- Split when: data processing is complex (50+ lines of non-UI code), multiple pages share logic,
  or you need to test business logic separately.
- **Do NOT use `if __name__ == "__main__":` in Streamlit files** (fine in utility modules).
- Name the main Streamlit file `streamlit_app.py` (Streamlit's default) in new projects.
  Rig Tools uses `app.py` — respect existing convention.
- Module-level mutable state is **shared across all users** — never store user data at module level.

## Rig Tools Structure (existing)

```
app.py                    # Streamlit entry point (called by asgi.py)
pages/{NN}_{name}.py      # Page UI — calls components only
components/{feature}/     # @st.fragment components — call api_client only
frontend/api_client.py    # HTTP bridge to FastAPI
calcs/{module}.py         # Pure math — no framework imports
utils/global_init.py      # global_init(), init_session_state()
```

## General Structure (new projects)

```
streamlit_app.py          # Entry point
app_pages/                # Page UI modules (not pages/ — avoids auto-discovery conflicts)
utils/                    # Business logic, helpers
```

## Import Rules

- Import from root directory perspective, not relative imports.
- `from components.feature.widget import my_widget` ✓
- `from .widget import my_widget` ✗ (relative imports break Streamlit's module system)
