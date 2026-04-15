import subprocess
import tempfile
from pathlib import Path

from app.config import DATA_ALIGNED, LOGS_DIR, REFERENCE_GENOME


def run_alignment(file_bytes: bytes, filename: str) -> dict:
    stem = Path(filename).stem.replace(".fastq.gz", "").replace(".fq", "")
    DATA_ALIGNED.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    sorted_bam = DATA_ALIGNED / f"{stem}.sorted.bam"
    bai_path = DATA_ALIGNED / f"{stem}.sorted.bam.bai"
    log_file = LOGS_DIR / f"{stem}.log"

    if not REFERENCE_GENOME:
        return {
            "success": False,
            "message": "Reference genome not found",
            "stdout": None,
            "stderr": None,
            "bam_path": None,
            "bai_path": None,
        }

    with tempfile.NamedTemporaryFile(
        suffix=".fastq.gz", delete=False
    ) as temp:
        temp.write(file_bytes)
        temp_path = Path(temp.name)
    
    logs = []

    try:
        bwa_command = [
            "bwa",
            "mem",
            "-t",
            "4",
            str(REFERENCE_GENOME),
            str(temp_path),
        ]

        samtools_sort_command = [
            "samtools",
            "sort",
            "-o",
            str(sorted_bam),
            "-",
        ]

        bwa_process = subprocess.Popen(
            bwa_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        sort_process = subprocess.Popen(
            samtools_sort_command,
            stdin=bwa_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        bwa_process.stdout.close()
        sort_stdout, sort_stderr = sort_process.communicate()
        _, bwa_stderr = bwa_process.communicate()

        logs.append(f"BWA stderr: {bwa_stderr.decode()}")
        logs.append(f"Samtools sort stderr: {sort_stderr.decode()}")

        if bwa_process.returncode != 0 or sort_process.returncode != 0:
            log_file.write_text("\n".join(logs))

            return {
                "success": False,
                "message": "Alignment failed",
                "stdout": sort_stdout.decode(),
                "stderr": sort_stderr.decode(),
                "bam_path": None,
                "bai_path": None,
            }
        
        index_command = subprocess.run(
            ["samtools",
            "index",
            str(sorted_bam)],
            capture_output=True,
            text=True,
        )

        logs.append(f"Samtools index stderr: {index_command.stderr}")
        log_file.write_text("\n".join(logs))

        if index_command.returncode != 0:
            return {
                "success": False,
                "message": "BAM indexing failed",
                "stdout": index_command.stdout,
                "stderr": index_command.stderr,
                "bam_path": str(sorted_bam),
                "bai_path": None,
            }
        
        return {
            "success": True,
            "message": "Alignment successful",
            "stdout": sort_stdout.decode(),
            "stderr": sort_stderr.decode(),
            "bam_path": str(sorted_bam),
            "bai_path": str(bai_path),
        }