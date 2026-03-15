"""
Supabase client factory — the ONLY place in the codebase where create_client() is called.

Two client types:
  get_supabase_client()          — service-role client (bypasses RLS). Use only from get_db().
  get_user_supabase_client(jwt)  — anon-key + user JWT client (respects RLS). Use from get_user_db().

Produced by: backend-agent / supabase-crud skill
"""
from functools import lru_cache

from supabase import Client, create_client

from api.config import settings


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Returns a cached service-role Supabase client.
    # SERVICE ROLE: bypasses RLS — for internal server-side operations only.
    Never expose this client's credentials or responses directly to users.
    """
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in the environment. "
            "Copy docker/.env.example to docker/.env and fill in the Supabase values."
        )
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def get_user_supabase_client(jwt: str) -> Client:
    """
    Returns a per-request Supabase client scoped to the authenticated user's JWT.
    Uses the anon key + Bearer token so RLS policies apply.
    """
    if not settings.supabase_url or not settings.supabase_anon_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_ANON_KEY must be set in the environment."
        )
    client = create_client(settings.supabase_url, settings.supabase_anon_key)
    client.auth.set_session(jwt, "")
    return client
