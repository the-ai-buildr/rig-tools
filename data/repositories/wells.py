"""Well CRUD via Supabase. Bridges the rich ``Well`` pydantic model and the
JSON ``document`` column on the ``wells`` table (service-role client)."""
from __future__ import annotations

from typing import Optional

from data.entities import WellRecord
from tmp.models import Well
from data.supabase_client import get_service_client


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


def list_wells(project_id: Optional[str] = None) -> list[WellRecord]:
    client = get_service_client()
    query = client.table("wells").select("*")
    if project_id:
        query = query.eq("project_id", project_id)
    return [WellRecord.model_validate(row) for row in (query.execute().data or [])]


def get_well(well_id: str) -> Optional[WellRecord]:
    client = get_service_client()
    rows = client.table("wells").select("*").eq("id", well_id).limit(1).execute().data
    return WellRecord.model_validate(rows[0]) if rows else None


def create_well(
    well: Well,
    *,
    project_id: Optional[str] = None,
    api_number: Optional[str] = None,
) -> WellRecord:
    client = get_service_client()
    row = {
        "project_id": project_id,
        "api_number": api_number,
        "document": well.model_dump(mode="json"),
        **_index_fields(well),
    }
    res = client.table("wells").insert(row).execute().data
    return WellRecord.model_validate(res[0])


def update_well(well_id: str, well: Well) -> Optional[WellRecord]:
    client = get_service_client()
    row = {"document": well.model_dump(mode="json"), **_index_fields(well)}
    res = client.table("wells").update(row).eq("id", well_id).execute().data
    return WellRecord.model_validate(res[0]) if res else None


def delete_well(well_id: str) -> bool:
    client = get_service_client()
    res = client.table("wells").delete().eq("id", well_id).execute().data
    return bool(res)


def to_well_model(record: WellRecord) -> Well:
    """Rehydrate the stored JSON document into a ``Well`` pydantic model."""
    return Well.model_validate(record.document)
