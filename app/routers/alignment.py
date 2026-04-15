from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.alignment_service import run_alignment
from app.models.pipeline import AlignmentResponse


router = APIRouter(tags=["Alignment"])

@router.post("/run/align", response_model=AlignmentResponse)
async def align(file: UploadFile = File(...)):
    if not file.filename.endswith((".fastq", ".fastq.gz", ".fq", ".fq.gz")):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only FASTQ files are allowed."
        )
    
    file_bytes = await file.read()
    result = run_alignment(file_bytes, file.filename)

    return AlignmentResponse(
        success=result["success"],
        message=result["message"],
        stdout=result["stdout"],
        stderr=result["stderr"],
        bam_path=str(result["bam_path"]),
        bai_path=str(result["bai_path"]),
    )