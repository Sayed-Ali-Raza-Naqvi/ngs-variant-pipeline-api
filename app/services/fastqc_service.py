import subprocess
import tempfile
import shutil
from pathlib import Path

from app.config import DATA_RAW, LOGS_DIR


def run_fastqc(file_bytes: bytes, filename: str) -> dict:
    output_dir = DATA_RAW / f"{Path(filename).stem}_fastqc_results"
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        suffix=".fastq.gz", delete=False
    ) as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name
    
    try:
        result = subprocess.run(
            ["fastqc", temp_path, "--outdir", str(output_dir), "--quiet"],
            capture_output=True,
            text=True,
        )

        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOGS_DIR / f"{Path(filename).stem}_fastqc.log"
        log_file.write_text(result.stdout + "\n" + result.stderr)

        if result.returncode != 0:
            return {
                "success": False,
                "message": f"FastQC failed: {result.stderr.strip()}",
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "output_path": None,
            }
        
        return {
            "success": True,
            "message": f"FastQC completed successfully. Results saved to {output_dir}",
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "output_path": str(output_dir),
        }

    finally:
        Path(temp_path).unlink(missing_ok=True)