import os
from pathfile import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW = BASE_DIR / "data" / "raw"
DATA_TRIMMED = BASE_DIR / "data" / "trimmed"
DATA_VARIANTS = BASE_DIR / "data" / "variants"
DATA_ALIGNED = BASE_DIR / "data" / "aligned"
DATA_ANNOTATED = BASE_DIR / "data" / "annotated"

LOGS_DIR = BASE_DIR / "logs"

REFERENCE_GENOME = os.getenv("REFERENCE_GENOME", "")
THREADS = int(os.getenv("THREADS", "4"))