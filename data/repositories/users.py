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


def authenticate(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if user and user.is_active and verify_password(password, user.hashed_password):
        return user
    return None


def update_user(
    session: Session,
    user_id: str,
    *,
    username: Optional[str] = None,
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    password: Optional[str] = None,
) -> Optional[User]:
    """Update mutable fields on a user. Only non-None values are applied.

    Passing a non-empty ``password`` re-hashes and replaces the stored hash.
    """
    user = session.get(User, user_id)
    if not user:
        return None
    if username is not None:
        user.username = username
    if full_name is not None:
        user.full_name = full_name
    if email is not None:
        user.email = email
    if role is not None:
        user.role = role
    if is_active is not None:
        user.is_active = is_active
    if password:
        user.hashed_password = hash_password(password)
    user.updated_at = _now()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: str) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True
