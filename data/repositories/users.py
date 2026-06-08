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


def _auth_users():
    """Return all auth users from GoTrue admin API."""
    client = get_service_client()
    resp = client.auth.admin.list_users(per_page=1000)
    return resp if isinstance(resp, list) else getattr(resp, "users", []) or []


def _emails_by_id() -> dict[str, str]:
    """Map auth user id → email across all users (admin listing)."""
    return {u.id: (u.email or "") for u in _auth_users()}


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


def _build_auth_only_user(auth_user) -> User:
    """Fallback model when an auth user exists but no profile row is present."""
    metadata = getattr(auth_user, "user_metadata", None) or {}
    email = getattr(auth_user, "email", None)
    email_local = (email or "").split("@")[0] if email else ""
    return User(
        id=getattr(auth_user, "id"),
        username=metadata.get("username") or email_local or None,
        full_name=metadata.get("full_name") or "",
        email=email,
        role=metadata.get("role") or "viewer",
        is_active=True,
        preferences={},
        created_at=getattr(auth_user, "created_at", None),
        updated_at=getattr(auth_user, "updated_at", None),
    )


def list_users() -> list[User]:
    client = get_service_client()
    profiles = client.table("profiles").select("*").execute().data or []
    auth_users = _auth_users()

    users_by_id: dict[str, User] = {}
    emails_by_id = {u.id: (u.email or "") for u in auth_users}

    for profile in profiles:
        users_by_id[profile["id"]] = _build_user(profile, emails_by_id.get(profile["id"]))

    # Include auth users missing a profile row so they appear in admin UI.
    for auth_user in auth_users:
        uid = getattr(auth_user, "id", None)
        if uid and uid not in users_by_id:
            users_by_id[uid] = _build_auth_only_user(auth_user)

    return list(users_by_id.values())


def get_user(user_id: str) -> Optional[User]:
    client = get_service_client()
    rows = (
        client.table("profiles").select("*").eq("id", user_id).limit(1).execute().data
    )

    auth_user = None
    try:
        au = client.auth.admin.get_user_by_id(user_id)
        auth_user = getattr(au, "user", None)
    except Exception:
        auth_user = None

    if rows:
        email = getattr(auth_user, "email", None) if auth_user else _emails_by_id().get(user_id)
        return _build_user(rows[0], email)

    if auth_user:
        return _build_auth_only_user(auth_user)

    return None


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
