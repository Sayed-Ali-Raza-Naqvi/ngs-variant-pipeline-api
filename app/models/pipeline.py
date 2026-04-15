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


class FastQCResponse(BaseModel):
    success: bool
    step: str = "fastqc"
    message: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    output_path: Optional[str] = None


class TrimmomaticResponse(BaseModel):
    success: bool
    setp: str = "trimmomatic"
    message: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    output_path: Optional[str] = None


class AlignmentResponse(BaseModel):
    success: bool
    step: str = "alignment"
    message: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    bai_path: Optional[str] = None
    bam_path: Optional[str] = None


class VariantCallingResponse(BaseModel):
    success: bool
    step: str = "variant_calling"
    message: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    vcf_path: Optional[str] = None


class AnnotationResponse(BaseModel):
    success: bool
    step: str = "annotation"
    message: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    annotated_vcf_path: Optional[str] = None