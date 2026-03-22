# Rig Tools

Oilfield drilling calculators — web app built with Streamlit + FastAPI + Supabase.

## Development

### Prerequisites
- Python 3.11+
- Docker (recommended)

### Run locally

```bash
# Single command — Streamlit + FastAPI on :8501
uvicorn asgi:app --reload --port 8501
```

### Run with Docker

```bash
cp docker/.env.example docker/.env
# Edit docker/.env — set SECRET_KEY and Supabase keys at minimum

bash start.sh            # First run — builds image and starts service
bash start.sh --build    # Rebuild after dependency changes
bash start.sh --logs     # Follow logs
bash start.sh --down     # Stop service
```

## Project Structure

```
app.py              # Streamlit entry point
asgi.py             # ASGI entry point (Streamlit + FastAPI on one port)
pages/              # Calculator pages (one file = one page)
calcs/              # Pure Python calculation modules
api/                # FastAPI backend
frontend/           # HTTP bridge (Streamlit → FastAPI)
docker/             # Dockerfile, docker-compose, .env.example
```

## Adding a New Calculator

1. Copy `pages/00_template.py` → `pages/NN_my_calc.py`
2. Add calculation logic to `calcs/<name>.py`
3. Add a FastAPI endpoint in `api/routes/calcs.py`
4. Add a wrapper in `frontend/api_client.py`
5. Register the page in `nav_menu()` in `components/nav.py`
