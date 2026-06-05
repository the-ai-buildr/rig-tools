"""SQLModel ORM tables for users, projects, and wells.

The rich nested ``Well`` pydantic model (data/models.py) is stored as a JSON
document column on ``WellRecord`` while a few hot fields are mirrored into
indexed columns for querying.
"""
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=_uuid, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: str = ""
    email: str = Field(index=True, unique=True)
    role: str = "viewer"
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: str = Field(default_factory=_uuid, primary_key=True)
    name: str = Field(index=True)
    project_type: str = "single"  # single | pad
    description: Optional[str] = None
    status: str = "planned"
    owner_id: Optional[str] = Field(default=None, foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

    wells: list["WellRecord"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class WellRecord(SQLModel, table=True):
    __tablename__ = "wells"

    id: str = Field(default_factory=_uuid, primary_key=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)
    # Mirrored hot fields for querying/listing without parsing the document.
    well_name: str = Field(index=True)
    api_number: Optional[str] = Field(default=None, index=True)
    status: str = "Planning"
    well_type: str = "Horizontal"
    # Full ``Well`` pydantic model serialized as JSON.
    document: dict = Field(sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

    project: Optional[Project] = Relationship(back_populates="wells")
