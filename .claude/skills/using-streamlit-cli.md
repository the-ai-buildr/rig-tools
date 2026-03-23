# Skill: Using Streamlit CLI

<!--
Purpose: Streamlit CLI commands for running apps, configuration, and diagnostics.
Source: https://github.com/the-ai-buildr/st-agent-skills (using-streamlit-cli)
-->

## When to Use

Running Streamlit apps, managing configuration via CLI, or diagnosing issues.

## Key Commands

```bash
streamlit run                        # Looks for streamlit_app.py in cwd
streamlit run app.py                 # Run specific file
streamlit run <url>                  # Run remote script
uv run streamlit run app.py          # Recommended (auto manages venv)

# Config
streamlit config show                # Show all current config values
streamlit cache clear                # Clear all cached data

# Info
streamlit version                    # Show version
streamlit help                       # CLI help
streamlit docs                       # Open docs in browser
streamlit hello                      # Demo app

# Init
streamlit init                       # Create streamlit_app.py + config.toml
```

## CLI Config Overrides

```bash
# Override config inline (after script name)
streamlit run app.py --server.port=8502 --theme.base=dark

# Prefer .streamlit/config.toml for persistence
```

## Config Precedence

CLI flags → environment variables → local `.streamlit/config.toml` → global `config.toml`

## Rig Tools

Rig Tools runs via `uvicorn` (not `streamlit run`) because FastAPI is co-mounted:

```bash
uvicorn asgi:app --reload --port 8501
```

`streamlit run` is not used in this project — it would bypass the FastAPI mount.
