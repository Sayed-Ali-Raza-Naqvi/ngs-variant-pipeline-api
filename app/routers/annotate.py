from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.annotation_service import run_annotation
from app.models.pipeline import AnnotationResponse


router = APIRouter(tags=["Annotate"])

@router.post("/run/annotate", response_model=AnnotationResponse)
async def annotation_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".vcf"):
        raise HTTPException(status_code=400, detail="Only VCF files are accepted.")
    
    file_bytes = await file.read()
    result = run_annotation(file_bytes, file.filename)

    return {
        "success": result["success"],
        "message": result["message"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "annotated_vcf_path": result["annotated_vcf_path"],
    }