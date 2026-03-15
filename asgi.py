"""
Root-level shim — preserves `uvicorn asgi:app` for local dev convenience.
Real ASGI entry point lives at src/api/asgi.py.

In Docker and CI, run directly:
    uvicorn api.asgi:app --host 0.0.0.0 --port 8501
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from api.asgi import app  # noqa: F401
