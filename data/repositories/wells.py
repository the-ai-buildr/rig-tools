"""Well CRUD. Bridges the rich ``Well`` pydantic model and the JSON document column."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select

from data.models import Well
from data.tables import WellRecord


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _enum_value(value) -> str:
    return value.value if hasattr(value, "value") else str(value)


def _index_fields(well: Well) -> dict:
    """Hot fields mirrored onto the record for listing/querying."""
    header = well.header
    return {
        "well_name": header.well_name,
        "status": _enum_value(header.status),
        "well_type": _enum_value(header.well_type),
    }


def list_wells(session: Session, project_id: Optional[str] = None) -> list[WellRecord]:
    stmt = select(WellRecord)
    if project_id:
        stmt = stmt.where(WellRecord.project_id == project_id)
    return list(session.exec(stmt).all())


def get_well(session: Session, well_id: str) -> Optional[WellRecord]:
    return session.get(WellRecord, well_id)


def create_well(
    session: Session,
    well: Well,
    *,
    project_id: Optional[str] = None,
    api_number: Optional[str] = None,
) -> WellRecord:
    record = WellRecord(
        project_id=project_id,
        api_number=api_number,
        document=well.model_dump(mode="json"),
        **_index_fields(well),
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def update_well(session: Session, well_id: str, well: Well) -> Optional[WellRecord]:
    record = session.get(WellRecord, well_id)
    if not record:
        return None
    record.document = well.model_dump(mode="json")
    for key, value in _index_fields(well).items():
        setattr(record, key, value)
    record.updated_at = _now()
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def delete_well(session: Session, well_id: str) -> bool:
    record = session.get(WellRecord, well_id)
    if not record:
        return False
    session.delete(record)
    session.commit()
    return True


def to_well_model(record: WellRecord) -> Well:
    """Rehydrate the stored JSON document into a ``Well`` pydantic model."""
    return Well.model_validate(record.document)
