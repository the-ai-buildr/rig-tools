"""Template Pydantic Models"""

from typing import Any, Dict, Optional
from pydantic import BaseModel


class TemplateCreate(BaseModel):
    """Request body for POST /api/templates"""
    template_name: str
    template_type: str = "custom"        # "prebuilt" | "custom"
    category: Optional[str] = None
    description: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None


class TemplateResponse(TemplateCreate):
    id: int
    created_by: Optional[int] = None
    is_default: bool = False

    class Config:
        from_attributes = True
