"""
Export Routes — /api/export

Endpoints:
    POST  /api/export/well/{id}         Export a single well to Excel
    POST  /api/export/project/{id}      Export an entire project to Excel
    GET   /api/export/download/{fname}  Download a previously exported file
    GET   /api/export/files             List all exported files

Files are stored in the ``EXPORT_PATH`` directory (configured via env var).
Each export generates a timestamped .xlsx file returned via a download URL.
"""

import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from api.auth import get_current_user
from api.config import settings
from api.database import Database
from api.excel_export import export_project_to_excel, export_well_to_excel, get_export_files

router = APIRouter()
db = Database()


@router.post("/well/{well_id}")
async def export_well(
    well_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Generate a 10-sheet Excel workbook for a single well.

    Sheets: Well Header, Status History, Wellbore Plan/Actual,
            Casing Plan/Actual, Tubular Plan/Actual, Survey Plan/Actual.

    Returns the filename and a ``download_url`` for immediate retrieval.
    """
    well = await db.get_well_by_id(well_id)
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")

    project = await db.get_project_by_id(well["project_id"])
    if not project or project["created_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    well_data = await db.get_complete_well_data(well_id)
    filepath = await export_well_to_excel(well_data)
    filename = os.path.basename(filepath)

    return {
        "message": "Export successful",
        "filename": filename,
        "download_url": f"/api/export/download/{filename}",
    }


@router.post("/project/{project_id}")
async def export_project(
    project_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Generate an Excel workbook for an entire project (all wells).

    Includes a Project Summary sheet, a Wells Summary sheet,
    and one summary sheet per well.
    """
    project = await db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project["created_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    project_data = await db.get_complete_project_data(project_id)
    filepath = await export_project_to_excel(project_data)
    filename = os.path.basename(filepath)

    return {
        "message": "Export successful",
        "filename": filename,
        "download_url": f"/api/export/download/{filename}",
    }


@router.get("/download/{filename}")
async def download_export(filename: str):
    """
    Stream an exported .xlsx file to the caller.

    The filename must exactly match a file present in the EXPORT_PATH directory.
    Path traversal characters are rejected by FastAPI's path parameter parsing.
    """
    # Prevent path traversal attacks
    safe_filename = os.path.basename(filename)
    export_path = os.path.join(settings.EXPORT_PATH, safe_filename)

    if not os.path.exists(export_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        export_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=safe_filename,
    )


@router.get("/files")
async def list_exports(current_user: dict = Depends(get_current_user)):
    """Return metadata (name, size, created date) for all files in EXPORT_PATH."""
    return await get_export_files()
