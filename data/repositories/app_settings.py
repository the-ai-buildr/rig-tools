"""Global application settings repository (single-row ``app_settings`` table)."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlmodel import Session

from data.tables import AppSettings

GLOBAL_ID = "global"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def get_app_settings(session: Session) -> AppSettings:
    """Return the global settings row, creating it with defaults if absent."""
    settings = session.get(AppSettings, GLOBAL_ID)
    if settings is None:
        settings = AppSettings(id=GLOBAL_ID)
        session.add(settings)
        session.commit()
        session.refresh(settings)
    return settings


def update_app_settings(session: Session, **fields) -> AppSettings:
    """Apply the provided fields to the global settings row and persist."""
    settings = get_app_settings(session)
    for key, value in fields.items():
        if value is not None and hasattr(settings, key):
            setattr(settings, key, value)
    settings.updated_at = _now()
    session.add(settings)
    session.commit()
    session.refresh(settings)
    return settings
