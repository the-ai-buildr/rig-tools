"""Global application settings repository (single-row ``app_settings`` table)."""
from __future__ import annotations

from data.entities import AppSettings
from data.supabase_client import get_service_client

GLOBAL_ID = "global"


def get_app_settings() -> AppSettings:
    """Return the global settings row, creating it with defaults if absent."""
    client = get_service_client()
    rows = (
        client.table("app_settings").select("*").eq("id", GLOBAL_ID).limit(1).execute().data
    )
    if not rows:
        client.table("app_settings").insert({"id": GLOBAL_ID}).execute()
        rows = (
            client.table("app_settings")
            .select("*")
            .eq("id", GLOBAL_ID)
            .limit(1)
            .execute()
            .data
        )
    return AppSettings.model_validate(rows[0])


def update_app_settings(**fields) -> AppSettings:
    """Apply the provided fields to the global settings row and persist."""
    get_app_settings()  # ensure the row exists
    fields = {
        k: v
        for k, v in fields.items()
        if v is not None and k in AppSettings.model_fields and k != "id"
    }
    if fields:
        client = get_service_client()
        client.table("app_settings").update(fields).eq("id", GLOBAL_ID).execute()
    return get_app_settings()
