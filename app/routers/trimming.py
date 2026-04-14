from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.pipeline import TrimmingResponse
from app.services.trimming_service import run_trimming


router = APIRouter(tags=["Trimming"])

@router.post("/trimming", response_model=TrimmingResponse)
async def trimming_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".fastq", ".fastq.gz", ".fq", ".fq.gz"):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Please upload a .fastq, .fastq.gz, .fq, or .fq.gz file."
        )

    file_bytes = await file.read()
    result = run_trimming(file_bytes, file.filename)

    return TrimmingResponse(
        success=result["success"],
        message=result["message"],
        stdout=result["stdout"],
        stderr=result["stderr"],
        output_path=result["output_path"]
    )