"""User CRUD backed by Supabase Auth (GoTrue) + the ``profiles`` table.

Identity (email/password) lives in ``auth.users`` and is managed through the
GoTrue admin API; the app-specific fields (username, full_name, role, is_active,
preferences) live in ``public.profiles``. All calls use the service-role client,
which bypasses RLS, so these helpers are server-side only.
"""
from __future__ import annotations

from typing import Optional

from data.entities import User
from data.supabase_client import get_service_client


def _emails_by_id() -> dict[str, str]:
    """Map auth user id → email across all users (admin listing)."""
    client = get_service_client()
    resp = client.auth.admin.list_users(per_page=1000)
    users = resp if isinstance(resp, list) else getattr(resp, "users", []) or []
    return {u.id: (u.email or "") for u in users}


def _build_user(profile: dict, email: Optional[str]) -> User:
    return User(
        id=profile["id"],
        username=profile.get("username"),
        full_name=profile.get("full_name") or "",
        email=email,
        role=profile.get("role") or "viewer",
        is_active=profile.get("is_active", True),
        preferences=profile.get("preferences") or {},
        created_at=profile.get("created_at"),
        updated_at=profile.get("updated_at"),
    )


def list_users() -> list[User]:
    client = get_service_client()
    profiles = client.table("profiles").select("*").execute().data or []
    emails = _emails_by_id()
    return [_build_user(p, emails.get(p["id"])) for p in profiles]


def get_user(user_id: str) -> Optional[User]:
    client = get_service_client()
    rows = (
        client.table("profiles").select("*").eq("id", user_id).limit(1).execute().data
    )
    if not rows:
        return None
    email = None
    try:
        au = client.auth.admin.get_user_by_id(user_id)
        email = getattr(getattr(au, "user", None), "email", None)
    except Exception:
        email = _emails_by_id().get(user_id)
    return _build_user(rows[0], email)


def get_user_by_email(email: str) -> Optional[User]:
    target = (email or "").lower()
    match_id = next(
        (uid for uid, em in _emails_by_id().items() if em.lower() == target), None
    )
    return get_user(match_id) if match_id else None


def get_user_by_username(username: str) -> Optional[User]:
    client = get_service_client()
    rows = (
        client.table("profiles")
        .select("*")
        .eq("username", username)
        .limit(1)
        .execute()
        .data
    )
    if not rows:
        return None
    return _build_user(rows[0], _emails_by_id().get(rows[0]["id"]))


def create_user(
    *,
    username: str,
    full_name: str,
    email: str,
    role: str,
    password: str,
) -> User:
    """Create an auth user; the DB trigger seeds the matching profile row."""
    client = get_service_client()
    res = client.auth.admin.create_user(
        {
            "email": email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {
                "username": username,
                "full_name": full_name,
                "role": role,
            },
        }
    )
    user_id = res.user.id
    return get_user(user_id) or _build_user(
        {
            "id": user_id,
            "username": username,
            "full_name": full_name,
            "role": role,
            "is_active": True,
            "preferences": {},
        },
        email,
    )


def update_user_preferences(user_id: str, prefs: dict) -> Optional[User]:
    """Merge ``prefs`` into the profile's stored preferences and persist.

    Only non-``None`` values are applied so partial updates leave other
    preferences untouched.
    """
    client = get_service_client()
    rows = (
        client.table("profiles")
        .select("preferences")
        .eq("id", user_id)
        .limit(1)
        .execute()
        .data
    )
    if not rows:
        return None
    merged = dict(rows[0].get("preferences") or {})
    merged.update({k: v for k, v in prefs.items() if v is not None})
    client.table("profiles").update({"preferences": merged}).eq("id", user_id).execute()
    return get_user(user_id)


def update_user(
    user_id: str,
    *,
    username: Optional[str] = None,
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    password: Optional[str] = None,
) -> Optional[User]:
    """Update mutable fields. Email/password go to auth; the rest to profiles."""
    client = get_service_client()

    auth_attrs: dict = {}
    if email is not None:
        auth_attrs["email"] = email
        auth_attrs["email_confirm"] = True
    if password:
        auth_attrs["password"] = password
    if auth_attrs:
        client.auth.admin.update_user_by_id(user_id, auth_attrs)

    profile_attrs: dict = {}
    if username is not None:
        profile_attrs["username"] = username
    if full_name is not None:
        profile_attrs["full_name"] = full_name
    if role is not None:
        profile_attrs["role"] = role
    if is_active is not None:
        profile_attrs["is_active"] = is_active
    if profile_attrs:
        client.table("profiles").update(profile_attrs).eq("id", user_id).execute()

    return get_user(user_id)


def delete_user(user_id: str) -> bool:
    client = get_service_client()
    try:
        client.auth.admin.delete_user(user_id)
    except Exception:
        return False
    return True
