import subprocess
import tempfile
from pathlib import Path

from app.config import DATA_VARIANTS, LOGS_DIR, REFERENCE_GENOME


def run_variant_calling(file_bytes: bytes, filename: str) -> dict:
    stem = Path(filename).stem.replace(".bam", "")
    DATA_VARIANTS.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    vcf_path = DATA_VARIANTS / f"{stem}_raw_variants.vcf"
    log_file = LOGS_DIR / f"{stem}_gatk.log"

    if not REFERENCE_GENOME:
        return {
            "success": False,
            "message": "Reference genome path is not configured.",
            "stdout": None,
            "stderr": None,
            "vcf_path": None,
        }

    with tempfile.NamedTemporaryFile(
        suffix=".bam", delete=False
    ) as temp_bam:
        temp_bam.write(file_bytes)
        temp_bam_path = Path(temp_bam.name)

    temp_bai_path = Path(str(temp_bam_path) + ".bai")

    try:
        index_result = subprocess.run(
            ["samtools", "index", str(temp_bam_path)],
            capture_output=True,
            text=True,
        )

        if index_result.returncode != 0:
            return {
                "success": False,
                "message": "Failed to index BAM file.",
                "stdout": None,
                "stderr": index_result.stderr,
                "vcf_path": None,
            }

        gatk_result = subprocess.run(
            [
                "gatk",
                "HaplotypeCaller",
                "-R",
                REFERENCE_GENOME,
                "-I",
                str(temp_bam_path),
                "-O",
                str(vcf_path),
                "--sample-ploidy",
                "2",
            ],
            capture_output=True,
            text=True,
        )

        log_file.write_text(gatk_result.stdout + "\n" + gatk_result.stderr)

        if gatk_result.returncode != 0:
            return {
                "success": False,
                "message": "GATK HaplotypeCaller failed.",
                "stdout": gatk_result.stdout,
                "stderr": gatk_result.stderr,
                "vcf_path": None,
            }
        
        return {
            "success": True,
            "message": "Variant calling completed successfully.",
            "stdout": gatk_result.stdout,
            "stderr": gatk_result.stderr,
            "vcf_path": str(vcf_path),
        }
    
    finally:
        temp_bam_path.unlink(missing_ok=True)
        temp_bai_path.unlink(missing_ok=True)