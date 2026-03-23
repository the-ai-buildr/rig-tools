# Skill: Developing with Streamlit

<!--
Purpose: Routing hub for all Streamlit development tasks — routes to specialized sub-skills.
Source: https://github.com/the-ai-buildr/st-agent-skills (developing-with-streamlit)
Produced by: frontend-agent
-->

## When to Use

Use for ALL Streamlit tasks: creating, editing, debugging, beautifying, styling, theming,
optimizing, or deploying Streamlit applications. Activate when task contains:
**design**, **layout**, **widget**, **chart**, **display**, **cache**, **performance**,
**session state**, **dashboard**, **metric**, **badge**, **icon**, **theme**, **chat**,
**markdown**, **component**, or when existing Streamlit-pages / Streamlit-components skills
don't cover the specific guidance needed.

## Workflow

1. Locate the Streamlit entry point (`app.py` in Rig Tools — not `streamlit_app.py`).
2. Identify task type and route to the appropriate sub-skill below.
3. Apply the sub-skill's guidance when editing code.

## Rig Tools Entry Points

- **ASGI entry:** `asgi.py` (mounts Streamlit + FastAPI — never run directly with `streamlit run`)
- **Streamlit script:** `app.py`
- **Pages:** `pages/{NN}_{name}.py`
- **Components:** `components/{feature}/{name}.py` (`@st.fragment` decorated)

## Routing Table

| Task | Sub-skill file |
|---|---|
| Performance, caching, fragments, forms | `optimizing-streamlit-performance.md` |
| Dashboard KPIs, metric cards | `building-streamlit-dashboards.md` |
| Visual design, icons, badges, spacing | `improving-streamlit-design.md` |
| Widget selection (radio, pills, select) | `choosing-streamlit-selection-widgets.md` |
| Themes, colors, fonts, config.toml | `creating-streamlit-themes.md` |
| Layouts — columns, sidebar, containers, dialogs | `using-streamlit-layouts.md` |
| Charts, dataframes, tables, column config | `displaying-streamlit-data.md` |
| Multi-page apps, navigation, page state | `building-streamlit-multipage-apps.md` |
| Session state, callbacks, cross-page state | `using-streamlit-session-state.md` |
| Markdown, colored text, badges, LaTeX | `using-streamlit-markdown.md` |
| Chat UI, AI assistant interfaces | `building-streamlit-chat-ui.md` |
| Custom components (CCv2) | `building-streamlit-custom-components-v2.md` |
| Third-party components | `using-streamlit-custom-components.md` |
| Code organization, file structure | `organizing-streamlit-code.md` |
| Environment setup, dependencies | `setting-up-streamlit-environment.md` |
| CLI commands | `using-streamlit-cli.md` |

## Compound Tasks

- **Beautify / improve:** read `improving-streamlit-design.md` → `using-streamlit-layouts.md` → `choosing-streamlit-selection-widgets.md`
- **New dashboard:** `building-streamlit-dashboards.md` → `displaying-streamlit-data.md`
- **New page:** `building-streamlit-multipage-apps.md` → `using-streamlit-layouts.md`

## Rig Tools Integration

- All data fetching goes through `frontend/api_client.py` — never direct Supabase in components.
- Cache keys that include user identity must use `st.session_state["auth_user"]["id"]` to avoid
  cross-user data leakage with `@st.cache_data`.
- `st.set_page_config()` is already called in `app.py` — never call it in components or pages.
- `@st.fragment` is required on all independently-rerendering components (CLAUDE.md rule #4).
