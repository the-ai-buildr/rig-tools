# Skill: Setting Up Streamlit Environment

<!--
Purpose: Environment setup, dependency management, and project initialization.
Source: https://github.com/the-ai-buildr/st-agent-skills (setting-up-streamlit-environment)
-->

## When to Use

Setting up a new Streamlit project or configuring the development environment.

## Rules

- Always specify `streamlit>=1.53.0` (or latest) — needed for Material icons, `st.pills()`,
  `st.segmented_control()`, modern caching, and navigation APIs.
- Use `uv` as the default dependency manager (fast, isolated, automatic). Ask before installing if not present.
- `uv init` generates `pyproject.toml`, `uv.lock`, `.venv/` for reproducible builds.
- Main file convention: `streamlit_app.py` (Streamlit's default for new projects).

## Rig Tools Note

Rig Tools uses Docker Compose + `requirements.txt`. Do not introduce `pyproject.toml` or `uv`
unless explicitly requested. Run locally via:
```bash
uvicorn asgi:app --reload --port 8501
```

## New Project Setup

```bash
# Initialize with uv
uv init my-app
cd my-app
uv add streamlit>=1.53.0

# Run
uv run streamlit run streamlit_app.py
```

## Minimal Structure

```
.venv/
streamlit_app.py
.streamlit/
    config.toml
requirements.txt   # or pyproject.toml with uv
```

## `.streamlit/config.toml` Baseline

```toml
[server]
headless = true
port = 8501

[theme]
base = "light"
```
