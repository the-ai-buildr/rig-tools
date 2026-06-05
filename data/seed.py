"""Default user seeding.

Edit ``DEFAULT_USERS`` with the emails/passwords you want provisioned.
Seeding is idempotent — existing users (matched by email) are left untouched.

Set ``APP_ENV=dev`` to additionally provision the local development login user.
"""
from __future__ import annotations

import os

from sqlmodel import Session, select

from data.db import engine
from data.security import hash_password
from data.tables import User

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


def is_dev() -> bool:
    """True when running in the local development environment."""
    return os.getenv("APP_ENV", "").strip().lower() == "dev"


def _users_to_seed() -> list[dict]:
    users = list(DEFAULT_USERS)
    if is_dev():
        users.append(DEV_USER)
    return users


def seed_default_users() -> None:
    """Insert any default users not already present (matched by email)."""
    with Session(engine) as session:
        for entry in _users_to_seed():
            exists = session.exec(
                select(User).where(User.email == entry["email"])
            ).first()
            if exists:
                continue
            session.add(
                User(
                    username=entry["username"],
                    full_name=entry.get("full_name", ""),
                    email=entry["email"],
                    role=entry.get("role", "viewer"),
                    hashed_password=hash_password(entry["password"]),
                )
            )
        session.commit()

