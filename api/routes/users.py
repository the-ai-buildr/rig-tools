"""User REST endpoints (`/api/users`)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import UserCreate, UserRead
from data.repositories import users as user_repo

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def list_users():
    return user_repo.list_users()


@router.post("", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate):
    if user_repo.get_user_by_email(payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    if user_repo.get_user_by_username(payload.username):
        raise HTTPException(status_code=409, detail="Username already taken")
    return user_repo.create_user(
        username=payload.username,
        full_name=payload.full_name,
        email=payload.email,
        role=payload.role,
        password=payload.password,
    )


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str):
    user = user_repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str):
    if not user_repo.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
