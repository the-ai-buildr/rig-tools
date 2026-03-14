"""
Template Routes — /api/templates

Endpoints:
    POST   /api/templates        Create a custom template
    GET    /api/templates        List all templates (prebuilt + user's custom)
    GET    /api/templates/{id}   Get a single template with its JSON data
    DELETE /api/templates/{id}   Delete a custom template (prebuilt are protected)
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.auth import get_current_user
from api.database import Database
from api.models import TemplateCreate, TemplateResponse

router = APIRouter()
db = Database()


@router.post("", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template: TemplateCreate,
    current_user: dict = Depends(get_current_user),
):
    """Save a custom template. ``template_type`` is forced to ``'custom'``."""
    data = template.model_dump()
    data["created_by"] = current_user["id"]
    data["template_type"] = "custom"  # Users cannot create prebuilt templates
    template_id = await db.create_template(data)
    return await db.get_template_by_id(template_id)


@router.get("", response_model=List[TemplateResponse])
async def list_templates(
    template_type: Optional[str] = Query(None, description="prebuilt | custom"),
    current_user: dict = Depends(get_current_user),
):
    """Return all prebuilt templates plus the user's own custom templates."""
    return await db.get_all_templates(
        template_type=template_type,
        user_id=current_user["id"],
    )


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Return a template by ID. Access is allowed for prebuilt or owned custom templates."""
    template = await db.get_template_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if template["template_type"] != "prebuilt" and template["created_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return template


@router.delete("/{template_id}", status_code=status.HTTP_200_OK)
async def delete_template(
    template_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Delete a custom template. Prebuilt templates are immutable."""
    template = await db.get_template_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if template["template_type"] == "prebuilt":
        raise HTTPException(status_code=400, detail="Cannot delete prebuilt templates")
    if template["created_by"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.delete_template(template_id)
    return {"message": "Template deleted successfully"}
