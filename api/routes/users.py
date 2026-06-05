"""User REST endpoints (`/api/users`)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from api.schemas import UserCreate, UserRead
from data.db import get_session
from data.repositories import users as user_repo

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    return user_repo.list_users(session)


@router.post("", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    if user_repo.get_user_by_email(session, payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    if user_repo.get_user_by_username(session, payload.username):
        raise HTTPException(status_code=409, detail="Username already taken")
    return user_repo.create_user(
        session,
        username=payload.username,
        full_name=payload.full_name,
        email=payload.email,
        role=payload.role,
        password=payload.password,
    )


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, session: Session = Depends(get_session)):
    user = user_repo.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, session: Session = Depends(get_session)):
    if not user_repo.delete_user(session, user_id):
        raise HTTPException(status_code=404, detail="User not found")
