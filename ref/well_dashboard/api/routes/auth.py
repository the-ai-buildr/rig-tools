"""
Authentication Routes — /api/auth

Endpoints:
    POST /api/auth/register   Register a new user account
    POST /api/auth/login      Login and receive a JWT token
    GET  /api/auth/me         Return the currently authenticated user
"""

from fastapi import APIRouter, HTTPException, Depends, status

from api.auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from api.database import Database
from api.models import UserCreate, UserLogin, UserResponse

router = APIRouter()
db = Database()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user.

    - Checks for duplicate usernames.
    - Hashes the password before storing.
    - Returns the created user object (without the password hash).
    """
    existing = await db.get_user_by_username(user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed = get_password_hash(user_data.password)
    user_id = await db.create_user(
        username=user_data.username,
        password_hash=hashed,
        email=user_data.email,
    )
    return await db.get_user_by_id(user_id)


@router.post("/login")
async def login(user_data: UserLogin):
    """
    Authenticate with username/password and receive a Bearer token.

    Returns:
        ``access_token`` (JWT), ``token_type`` = "bearer", and a ``user`` summary.
    """
    user = await db.get_user_by_username(user_data.username)
    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(
        data={"user_id": user["id"], "username": user["username"]}
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user["id"], "username": user["username"], "email": user["email"]},
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Return the profile of the currently authenticated user."""
    return current_user
