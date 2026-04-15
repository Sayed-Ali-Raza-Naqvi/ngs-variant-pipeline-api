# NGS Variant Calling Pipeline

A production-style REST API built with **FastAPI** that orchestrates a full NGS variant calling workflow.

```
FastQC → Trimmomatic → BWA → SAMtools → GATK HaplotypeCaller → SnpEff
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| API Framework | FastAPI + Uvicorn |
| Quality Control | FastQC |
| Adapter Trimming | Trimmomatic |
| Read Alignment | BWA MEM |
| BAM Processing | SAMtools |
| Variant Calling | GATK HaplotypeCaller |
| VCF Annotation | SnpEff |
| Containerisation | Docker + docker-compose |
| Language | Python 3.11 |

---

## Project Structure

```
ngs-variant-pipeline/
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── config.py             # Paths and environment settings
│   ├── models/
│   │   └── pipeline.py       # Pydantic request/response models
│   ├── routers/
│   │   ├── health.py         # GET  /api/v1/health
│   │   ├── fastqc.py         # POST /api/v1/run/fastqc
│   │   ├── trimming.py       # POST /api/v1/run/trim
│   │   ├── alignment.py      # POST /api/v1/run/align
│   │   ├── variant_call.py   # POST /api/v1/run/variant-call
│   │   └── annotate.py       # POST /api/v1/run/annotate
│   └── services/
│       ├── fastqc_service.py
│       ├── trimming_service.py
│       ├── alignment_service.py
│       ├── variant_service.py
│       └── annotation_service.py
├── data/
│   ├── raw/                  # FastQC output
│   ├── trimmed/              # Trimmomatic output
│   ├── aligned/              # BAM + BAI files
│   ├── variants/             # Raw VCF files
│   └── annotated/            # Annotated VCF files
├── logs/                     # Per-step log files
├── reference/                # Reference genome (not committed)
├── tests/
│   └── test_health.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Quickstart (Local)

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/ngs-variant-pipeline
cd ngs-variant-pipeline

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Set environment variable for reference genome
export REFERENCE_GENOME=/path/to/hg38.fa

# 5. Run the API
uvicorn app.main:app --reload

# 6. Open interactive docs
# http://localhost:8000/docs
```

---

## Quickstart (Docker)

```bash
# 1. Place your reference genome files in ./reference/
#    Required: hg38.fa, hg38.fa.fai, hg38.dict
#    BWA index: hg38.fa.amb, hg38.fa.ann, hg38.fa.bwt, hg38.fa.pac, hg38.fa.sa

# 2. Build and run
docker-compose up --build

# 3. Open interactive docs
# http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Input | Output |
|---|---|---|---|
| GET | `/api/v1/health` | — | API status |
| POST | `/api/v1/run/fastqc` | `.fastq.gz` | QC report in `data/raw/` |
| POST | `/api/v1/run/trim` | `.fastq.gz` | Trimmed FASTQ in `data/trimmed/` |
| POST | `/api/v1/run/align` | `.fastq.gz` | BAM + BAI in `data/aligned/` |
| POST | `/api/v1/run/variant-call` | `.bam` | VCF in `data/variants/` |
| POST | `/api/v1/run/annotate` | `.vcf` | Annotated VCF in `data/annotated/` |

---

## One-time Reference Genome Setup

```bash
# Index for SAMtools
samtools faidx hg38.fa

# Dictionary for GATK
gatk CreateSequenceDictionary -R hg38.fa

# Index for BWA
bwa index hg38.fa

# Download SnpEff database
snpEff download hg38
```

---

## Running Tests

```bash
pytest tests/
```

---

## Pipeline Data Flow

```
raw FASTQ
    │
    ▼
FastQC ─────────────────────► QC report (data/raw/)
    │
    ▼
Trimmomatic ─────────────────► trimmed FASTQ (data/trimmed/)
    │
    ▼
BWA MEM + SAMtools ──────────► sorted BAM + BAI (data/aligned/)
    │
    ▼
GATK HaplotypeCaller ────────► raw VCF (data/variants/)
    │
    ▼
SnpEff ──────────────────────► annotated VCF (data/annotated/)
```