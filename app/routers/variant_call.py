from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models import VariantCallingResponse
from app.services.variant_service import run_variant_calling


router = APIRouter(tags=["Variant Calling"])

@router.post("/run/variant-calling", response_model=VariantCallingResponse)
async def variant_calling_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".bam"):
        raise HTTPException(status_code=400, detail="Only BAM files are accepted.")
    
    file_bytes = await file.read()
    result = run_variant_calling(file_bytes, file.filename)

    return {
        "success": result["success"],
        "message": result["message"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "vcf_path": result["vcf_path"],
    }