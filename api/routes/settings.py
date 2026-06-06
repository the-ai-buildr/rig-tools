"""Settings REST endpoints — global app settings (single row)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.schemas import AppSettingsRead, AppSettingsUpdate
from data.db import get_session
from data.repositories import app_settings as app_settings_repo

router = APIRouter(prefix="/api", tags=["settings"])


# ── Global app settings (single row) ────────────────────────────────
@router.get("/app-settings", response_model=AppSettingsRead)
def get_app_settings(session: Session = Depends(get_session)):
    return app_settings_repo.get_app_settings(session)


@router.patch("/app-settings", response_model=AppSettingsRead)
def update_app_settings(
    payload: AppSettingsUpdate, session: Session = Depends(get_session)
):
    return app_settings_repo.update_app_settings(
        session, **payload.model_dump(exclude_unset=True)
    )
