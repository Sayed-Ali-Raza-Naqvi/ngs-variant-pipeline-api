from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.pipeline import FastQCResponse
from app.services.fastqc_service import run_fastqc


router = APIRouter(tags=["FastQC"])

@router.post("/fastqc", response_model=FastQCResponse)
async def fastqc_endpoint(file: UploadFile = File(...)) -> FastQCResponse:
    if not file.filename.endswith((".fastq", ".fq", ".fastq.gz", ".fq.gz")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a .fastq or .fastq.gz file."
        )

    file_bytes = await file.read()
    result = run_fastqc(file_bytes, file.filename)

    return FastQCResponse(
        success=result["success"],
        message=result["message"],
        stdout=result["stdout"],
        stderr=result["stderr"],
        output_path=result["output_path"]
    )