from fastapi import FastAPI
from app.routers import health


app = FastAPI(
    title="NGS Variant Calling Pipeline",
    description="REST API for running NGS pipeline: FastQC → Trimmomatic → BWA → SAMtools → GATK → VCF Annotation",
    version="1.0.0",
)

app.include_router(health.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "NGS Variant Pipeline API is running. Visit /docs for the API documentation."}