"""Well REST endpoints (`/api/wells`)."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from api.schemas import WellCreate, WellRead
from data.entities import WellRecord
from data.repositories import wells as well_repo

router = APIRouter(prefix="/api/wells", tags=["wells"])


def _to_read(record: WellRecord) -> WellRead:
    return WellRead(
        id=record.id,
        project_id=record.project_id,
        well_name=record.well_name,
        api_number=record.api_number,
        status=record.status,
        well_type=record.well_type,
        well=well_repo.to_well_model(record),
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


@router.get("", response_model=list[WellRead])
def list_wells(project_id: Optional[str] = None):
    return [_to_read(r) for r in well_repo.list_wells(project_id=project_id)]


@router.post("", response_model=WellRead, status_code=201)
def create_well(payload: WellCreate):
    record = well_repo.create_well(
        payload.well, project_id=payload.project_id, api_number=payload.api_number
    )
    return _to_read(record)


@router.get("/{well_id}", response_model=WellRead)
def get_well(well_id: str):
    record = well_repo.get_well(well_id)
    if not record:
        raise HTTPException(status_code=404, detail="Well not found")
    return _to_read(record)


@router.put("/{well_id}", response_model=WellRead)
def update_well(well_id: str, payload: WellCreate):
    record = well_repo.update_well(well_id, payload.well)
    if not record:
        raise HTTPException(status_code=404, detail="Well not found")
    return _to_read(record)


@router.delete("/{well_id}", status_code=204)
def delete_well(well_id: str):
    if not well_repo.delete_well(well_id):
        raise HTTPException(status_code=404, detail="Well not found")
