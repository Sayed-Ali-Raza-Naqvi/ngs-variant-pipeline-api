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


class FastQCResponse(PipelineResponse):
    success: bool
    step: str = "fastqc"
    message: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    output_path: Optional[str] = None