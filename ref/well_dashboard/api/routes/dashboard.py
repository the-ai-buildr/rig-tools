"""
Dashboard Routes — /api/dashboard

Aggregate endpoints used by the Streamlit frontend's summary views.

Endpoints:
    GET /api/dashboard/stats            Summary counts for the current user
    GET /api/dashboard/recent-activity  Latest status changes across all wells
"""

from fastapi import APIRouter, Depends, Query

from api.auth import get_current_user
from api.database import Database

router = APIRouter()
db = Database()


@router.get("/stats")
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    """
    Return aggregate counts for the authenticated user:

    - total_projects
    - total_wells
    - wells_by_status  (dict mapping status → count)
    - recent_exports   (last 5 export filenames)
    """
    return await db.get_dashboard_stats(current_user["id"])


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = Query(10, ge=1, le=100, description="Max items to return"),
    current_user: dict = Depends(get_current_user),
):
    """
    Return the most recent status-change events across all of the user's wells.

    Each item contains: well_name, old_status, new_status, changed_at, notes.
    """
    return await db.get_recent_activity(current_user["id"], limit=limit)


# ── Placeholder for Agno AI routes ────────────────────────────────────────────
# When Agno integration is added, create api/routes/agno.py and register it
# in api/routes/__init__.py. Example structure:
#
# router = APIRouter()
#
# @router.post("/chat")
# async def agno_chat(message: str, current_user = Depends(get_current_user)):
#     """Send a message to an Agno AI agent with well context."""
#     ...
#
# @router.get("/agents")
# async def list_agents(current_user = Depends(get_current_user)):
#     """Return available Agno agents."""
#     ...
