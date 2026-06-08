"""Central application configuration.

Loads environment variables from a local ``.env`` file (via python-dotenv) once,
at import time, and exposes the Supabase credentials and app settings as module
constants. Import this module early (before anything that reads the config) so
the ``.env`` values are present in ``os.environ``.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load the repo-root .env then .env.local (if present). .env.local overrides
# .env for local-only secrets and is gitignored. Real OS environment variables
# always win over both, so this is safe in production where the platform injects
# the vars directly.
_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env", override=False)
load_dotenv(_ROOT / ".env.local", override=True)


def _require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing required environment variable {name!r}. "
            "Copy .env.example to .env and fill in the Supabase credentials."
        )
    return value


# ── Supabase ────────────────────────────────────────────────────────────────
SUPABASE_URL = _require("SUPABASE_URL")
SUPABASE_ANON_KEY = _require("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = _require("SUPABASE_SERVICE_ROLE_KEY")

# Optional — only needed by the CLI / migrations, not the app runtime.
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL", "").strip()

# ── App ─────────────────────────────────────────────────────────────────────
APP_ENV = os.getenv("APP_ENV", "").strip().lower()


def is_dev() -> bool:
    """True when running in the development environment (seeds the dev user)."""
    return APP_ENV == "dev"
