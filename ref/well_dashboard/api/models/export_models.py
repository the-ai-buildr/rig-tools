"""Export Pydantic Models"""

from typing import Optional
from pydantic import BaseModel


class ExportRequest(BaseModel):
    """Optional request body for export endpoints (filename override)."""
    filename: Optional[str] = None


class ExportResponse(BaseModel):
    """Standard response returned after a successful export."""
    message: str
    filename: str
    download_url: str
