"""Default user seeding.

Edit ``DEFAULT_USERS`` with the emails/passwords you want provisioned.
Seeding is idempotent — existing users (matched by email) are left untouched.
"""
from __future__ import annotations

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


def seed_default_users() -> None:
    """Insert any DEFAULT_USERS not already present (matched by email)."""
    with Session(engine) as session:
        for entry in DEFAULT_USERS:
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
