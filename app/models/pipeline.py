from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    status: str
    message: Optional[str] = None


class PipelineResponse(BaseModel):
    success: bool
    step: str
    message: str
    output_path: Optional[str] = None