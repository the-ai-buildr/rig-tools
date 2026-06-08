"""Settings REST endpoints — per-user preferences and global app settings."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import (
    AppSettingsRead,
    AppSettingsUpdate,
    UserPreferences,
)
from data.repositories import app_settings as app_settings_repo
from data.repositories import users as user_repo

router = APIRouter(prefix="/api", tags=["settings"])


# ── Per-user preferences ────────────────────────────────────────────
@router.get("/users/{user_id}/preferences", response_model=UserPreferences)
def get_user_preferences(user_id: str):
    user = user_repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPreferences(**(user.preferences or {}))


@router.patch("/users/{user_id}/preferences", response_model=UserPreferences)
def update_user_preferences(user_id: str, payload: UserPreferences):
    user = user_repo.update_user_preferences(
        user_id, payload.model_dump(exclude_unset=True)
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPreferences(**(user.preferences or {}))


# ── Global app settings (single row) ────────────────────────────────
@router.get("/app-settings", response_model=AppSettingsRead)
def get_app_settings():
    return app_settings_repo.get_app_settings()


@router.patch("/app-settings", response_model=AppSettingsRead)
def update_app_settings(payload: AppSettingsUpdate):
    return app_settings_repo.update_app_settings(
        **payload.model_dump(exclude_unset=True)
    )
