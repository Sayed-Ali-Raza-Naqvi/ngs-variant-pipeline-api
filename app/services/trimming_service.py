import subprocess
from pathlib import Path
import tempfile

from app.config import DATA_TRIMMED, LOGS_DIR


def run_trimmomatic(file_bytes: bytes, filename: str) -> dict:
    stem = Path(filename).stem.replace(".fastq", "")
    output_path = DATA_TRIMMED / f"{stem}_trimmed.fastq.gz"
    DATA_TRIMMED.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        suffix=".fastq.gz", delete=False
    ) as temp_file:
        temp_file.write(file_bytes)
        temp_path = Path(temp_file.name)

    try:
        result = subprocess.run(
            [
                "trimmomatic", "SE",
                "-threads", "4",
                str(temp_path),
                str(output_path),
                "ILLUMINACLIP:TruSeq3-SE.fa:2:30:10",
                "LEADING:3",
                "TRAILING:3",
                "SLIDINGWINDOW:4:15",
                "MINLEN:36",
            ],
            capture_output=True,
            text=True,
        )

        log_file = LOGS_DIR / f"{stem}_trimmomatic.log"
        log_file.write_text(result.stdout + "\n" + result.stderr)

        if result.returncode != 0:
            return {
                "success": False,
                "message": f"Trimmomatic failed: {result.stderr.strip()}",
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "output_path": None,
            }
        
        return {
            "success": True,
            "message": f"Trimming completed. Output saved to {output_path}",
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "output_path": str(output_path),
        }
    
    finally:
        temp_path.unlink(missing_ok=True)