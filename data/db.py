"""SQLite engine + session management for the rig-tools persistence layer."""
from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

# SQLite database lives alongside the data package.
DB_PATH = Path(__file__).resolve().parent / "rig_tools.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False lets the connection be shared across FastAPI's threadpool.
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def init_db() -> None:
    """Create all tables. Safe to call repeatedly (no-op if they exist)."""
    # Import tables so their metadata is registered before create_all.
    from data import tables  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """FastAPI dependency yielding a scoped database session."""
    with Session(engine) as session:
        yield session
