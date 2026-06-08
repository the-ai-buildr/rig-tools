"""Supabase client factories.

Two trust levels:

* ``get_service_client()`` — authenticated with the **service-role** key. Bypasses
  RLS and is used by server-side code (Dash callbacks, FastAPI routes, seeding)
  for trusted data operations. The service-role key never reaches the browser.
* ``get_auth_client()`` — authenticated with the public **anon** key. Used only
  to run the GoTrue sign-in flow (``sign_in_with_password``).

Both are cached module-level singletons. ``get_user_client(access_token)`` returns
an anon client scoped to a specific user's JWT, for RLS-honouring operations.
"""

from __future__ import annotations
from functools import lru_cache
from supabase import Client, create_client

from data.config import (
    SUPABASE_ANON_KEY,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_URL,
)


@lru_cache(maxsize=1)
def get_service_client() -> Client:
    """Trusted server-side client (service-role; bypasses RLS)."""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


@lru_cache(maxsize=1)
def get_auth_client() -> Client:
    """Anon client used for the GoTrue sign-in flow."""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def get_user_client(access_token: str) -> Client:
    """Anon client scoped to a user's JWT so Postgres RLS policies apply."""
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    client.postgrest.auth(access_token)
    return client
