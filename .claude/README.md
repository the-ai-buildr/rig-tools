# Rig Tools — Claude Orchestrator Guide

This directory (`.claude/`) contains the agent system for AI-assisted development of Rig Tools. It gives Claude a structured way to generate, review, and extend code while enforcing project conventions automatically.

---

## Directory Layout

```
.claude/
├── CLAUDE.md                  # Master context — read this to understand the whole system
├── README.md                  # This file
├── skills/
│   ├── SKILLS_INDEX.md        # Compact cheat-sheet — orchestrator's fast routing reference
│   ├── streamlit-pages.md     # How to create/edit pages
│   ├── streamlit-components.md# @st.fragment, st.html, component patterns
│   ├── fastapi-routes.md      # Endpoints, Pydantic models, dependency injection
│   ├── fastapi-streamlit-mount.md # Service wiring, Docker, api_client bridge
│   ├── supabase-crud.md       # api/db/ layer, (data, error) tuples, client singleton
│   ├── supabase-auth.md       # Signup/login/logout/refresh, RLS, JWT dep
│   ├── htmx-integration.md    # HTMX partials via FastAPI, st.html embedding
│   └── streamlit.md           # Legacy Rig Tools conventions (existing code)
└── agents/
    ├── orchestrator.md        # Routes tasks, decomposes work, resolves conflicts
    ├── frontend-agent.md      # Owns pages/, components/, nav
    ├── backend-agent.md       # Owns api/, services/, api_client.py
    └── reviewer-agent.md      # 30-point audit checklist; signs off all generated code
```

---

## How It Works

```
User request
     │
     ▼
orchestrator          reads CLAUDE.md + SKILLS_INDEX.md
     │                classifies task → assigns agents
     ├──► frontend-agent    reads skill files → writes pages + components
     ├──► backend-agent     reads skill files → writes routes + db + models
     └──► reviewer-agent    audits output → returns CRITICALs for fix
```

- **The orchestrator** never writes code. It reads only two files (CLAUDE.md + SKILLS_INDEX.md) to route the task.
- **Sub-agents** read the full skill files relevant to their task before generating anything.
- **The reviewer** runs after every non-trivial generation and blocks output on CRITICAL findings.
- **Skill files self-update** — corrections, preferences, and learned mistakes accumulate in the `User Preferences` section of each file over time.

---

## Invoking the Orchestrator

### In VS Code with GitHub Copilot

Reference the orchestrator agent in chat:

```
@orchestrator add a 'rig profiles' CRUD page with Supabase auth
```

Or describe the task naturally — the orchestrator will classify it:

```
I need a page where logged-in users can create and manage rig profiles stored in Supabase.
```

### Invoking a specific agent directly

Skip orchestration for scoped tasks:

```
@backend-agent add a FastAPI endpoint for GET /api/rigs
@frontend-agent create the rigs table component using the existing api_client wrapper
@reviewer-agent audit all files changed in the last task
```

### Triggering a skill explicitly

Tell any agent which skill to apply:

```
@backend-agent using the supabase-crud skill, add CRUD for the 'wells' table
@frontend-agent using the htmx-integration skill, add an HTMX-powered delete button to the rigs table
```

---

## Common Task Recipes

### Add a new CRUD resource end-to-end

```
@orchestrator add a 'wells' resource — users can create, list, update, and delete wells.
Each well has: name (string), depth_ft (int), rig_id (foreign key to rigs).
Use Supabase with RLS. Include a Streamlit page with @st.fragment table + create form.
```

The orchestrator will decompose this into:
1. `api/models/well_models.py`
2. `api/db/wells.py`
3. `api/routes/wells.py` + `__init__.py` registration
4. `frontend/api_client.py` wrappers
5. `components/wells/wells_table.py` + `create_well_form.py`
6. `pages/NN_wells.py`
7. `components/nav.py` update
8. Reviewer audit

### Add authentication to an existing page

```
@backend-agent the wells page needs to be auth-gated.
Add signup/login/logout endpoints and the Streamlit login page.
```

### Add an HTMX live-updating table

```
@orchestrator add an HTMX-powered wells table that deletes rows in-place without a Streamlit rerun.
```

### Review all recent changes

```
@reviewer-agent audit the wells feature — check RLS, service-role usage, layer separation, and missing response_model decorators.
```

---

## How Skills Self-Update

Each skill and agent file has a **User Preferences** section at the bottom:

```markdown
## User Preferences
- learned_corrections: []
- style_overrides: {}
- avoid: []
- notes: []
```

When Claude makes a mistake and you correct it, tell Claude to record it:

```
That's wrong — you used response.error but supabase-py v2 raises exceptions instead.
Record this in the supabase-crud skill's learned_corrections.
```

On the next task using that skill, Claude reads the corrections and avoids them automatically.

**After 5 corrections**, Claude consolidates them into permanent rules in the skill file.

---

## Adding a New Skill

1. Copy the template from any existing skill file.
2. Save it as `.claude/skills/{skill-name}.md`.
3. Add a row to the table in `.claude/skills/SKILLS_INDEX.md`.
4. Add the skill to the relevant agent's **Skills** section in `agents/{agent}.md`.
5. Reference it in `CLAUDE.md`'s Skill Index table.

---

## Architecture Quick-Reference

```
User browser (:8501)
  └─► Streamlit page       (pages/*.py)
        └─► Component      (components/{feature}/*.py)  ← @st.fragment
              └─► api_client.py  → HTTP → FastAPI (:8000)
                                           └─► api/routes/{feature}.py
                                                 └─► api/db/{table}.py
                                                       └─► Supabase (PostgreSQL + Auth)

HTMX path:
  └─► st.html() with hx-get/post → FastAPI /api/partials/*.py → HTMLResponse fragment
```

**Layer rules (never cross):**

| Layer | Folder | May NOT import |
|---|---|---|
| UI | `pages/`, `components/` | `supabase`, `fastapi`, `calcs/` |
| API Bridge | `frontend/api_client.py` | `supabase`, business logic |
| API Routes | `api/routes/` | `streamlit` |
| DB | `api/db/` | `fastapi`, `streamlit` |
| Services | `services/` | framework layers |
| Calculations | `calcs/` | everything except stdlib/numpy/scipy |

---

## Troubleshooting

| Symptom | Check |
|---|---|
| Agent ignores project conventions | Verify it reads `CLAUDE.md` first; remind it with `@agent read CLAUDE.md before proceeding` |
| Repeated mistakes after correction | Add to skill's `learned_corrections`; check the agent reads User Preferences |
| Orchestrator writes code instead of delegating | Remind: "orchestrator routes only, delegate to frontend-agent/backend-agent" |
| Reviewer keeps flagging the same thing | The underlying skill's Patterns section may be wrong — update the skill |
| HTMX partial returns 400 | Check `_require_htmx` dep and `HX-Request: true` header in the request |
| Supabase query ignores RLS | Route is using `get_db` (service-role) instead of `get_user_db` |
| Auth token not reaching API | Verify `api_client.py` passes `Authorization: Bearer <token>` header |
