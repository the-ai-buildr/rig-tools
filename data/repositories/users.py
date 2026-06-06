"""User CRUD + authentication helpers."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select

from data.security import hash_password, verify_password
from data.tables import User


def _now() -> datetime:
    return datetime.now(timezone.utc)


def list_users(session: Session) -> list[User]:
    return list(session.exec(select(User)).all())


def get_user(session: Session, user_id: str) -> Optional[User]:
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    return session.exec(select(User).where(User.username == username)).first()


def create_user(
    session: Session,
    *,
    username: str,
    full_name: str,
    email: str,
    role: str,
    password: str,
) -> User:
    user = User(
        username=username,
        full_name=full_name,
        email=email,
        role=role,
        hashed_password=hash_password(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user_preferences(
    session: Session, user_id: str, prefs: dict
) -> Optional[User]:
    """Merge ``prefs`` into the user's stored preferences and persist.

    Only non-``None`` values are applied so partial updates leave other
    preferences untouched.
    """
    user = session.get(User, user_id)
    if not user:
        return None
    merged = dict(user.preferences or {})
    merged.update({k: v for k, v in prefs.items() if v is not None})
    user.preferences = merged
    user.updated_at = _now()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if user and user.is_active and verify_password(password, user.hashed_password):
        return user
    return None


def delete_user(session: Session, user_id: str) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True
