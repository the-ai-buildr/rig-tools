"""Default user seeding via Supabase Auth (GoTrue admin API).

Edit ``DEFAULT_USERS`` with the emails/passwords you want provisioned.
Seeding is idempotent — existing users (matched by email) are left untouched.

Set ``APP_ENV=dev`` to additionally provision the local development login user.
"""
from __future__ import annotations

from data.config import is_dev
from data.repositories import users as user_repo
from data.supabase_client import get_service_client

# ---------------------------------------------------------------------------
# Edit this list to provision default accounts.
# role: admin | engineer | supervisor | geologist | viewer
# ---------------------------------------------------------------------------
DEFAULT_USERS: list[dict] = [
    {
        "username": "admin",
        "full_name": "Administrator",
        "email": "admin@rigtools.local",
        "role": "admin",
        "password": "changeme",
    },
]

# ---------------------------------------------------------------------------
# Dev-only login user — seeded only when APP_ENV=dev.
# ---------------------------------------------------------------------------
DEV_USER: dict = {
    "username": "devadmin",
    "full_name": "Dev Admin",
    "email": "admin@email.com",
    "role": "admin",
    "password": "admin 123!",
}


def _users_to_seed() -> list[dict]:
    users = list(DEFAULT_USERS)
    if is_dev():
        users.append(DEV_USER)
    return users


def _existing_emails() -> set[str]:
    client = get_service_client()
    resp = client.auth.admin.list_users(per_page=1000)
    users = resp if isinstance(resp, list) else getattr(resp, "users", []) or []
    return {(u.email or "").lower() for u in users}


def seed_default_users() -> None:
    """Insert any default users not already present (matched by email)."""
    existing = _existing_emails()
    for entry in _users_to_seed():
        if entry["email"].lower() in existing:
            continue
        user_repo.create_user(
            username=entry["username"],
            full_name=entry.get("full_name", ""),
            email=entry["email"],
            role=entry.get("role", "viewer"),
            password=entry["password"],
        )

