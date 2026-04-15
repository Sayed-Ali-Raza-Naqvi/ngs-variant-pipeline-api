import subprocess
import tempfile
from pathlib import Path

from app.config import DATA_ANNOTATED, LOGS_DIR

SNPEFF_GENOME = "hg38"

def run_annotation(file_bytes: bytes, filename: str) -> dict:
    stem = Path(filename).stem.replace(".vcf", "")
    DATA_ANNOTATED.mkdir(exist_ok=True, parents=True)
    LOGS_DIR.mkdir(exist_ok=True, parents=True)

    annotated_vcf = DATA_ANNOTATED / f"{stem}_annotated.vcf"
    log_file = LOGS_DIR / f"{stem}_snpeff.log"

    with tempfile.NamedTemporaryFile(
        suffix=".vcf", delete=False
    ) as temp:
        temp.write(file_bytes)
        temp_path = Path(temp.name)
    
    try:
        result = subprocess.run(
            [
                "snpeff",
                "-v",
                "nolog",
                SNPEFF_GENOME,
                str(temp_path),
            ],
            capture_output=True,
            text=True,
        )

        log_file.write_text(result.stdout + "\n" + result.stderr)

        if result.returncode != 0:
            return {
                "success": False,
                "message": f"SnpEff annotation failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "annotated_vcf_path": None,
            }
        
        annotated_vcf.write_text(result.stdout)

        return {
            "success": True,
            "message": f"Annotation completed successfully. Annotated VCF file is available at {annotated_vcf}",
            "stdout": None,
            "stderr": result.stderr,
            "annotated_vcf_path": str(annotated_vcf),
        }

    finally:
        temp_path.unlink(missing_ok=True)