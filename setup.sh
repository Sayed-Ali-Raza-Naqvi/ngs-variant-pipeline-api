#!/bin/bash
 
set -e
 
mkdir -p app/models
mkdir -p app/routers
mkdir -p app/services
mkdir -p data/raw
mkdir -p data/trimmed
mkdir -p data/aligned
mkdir -p data/variants
mkdir -p data/annotated
mkdir -p logs
mkdir -p tests
 
touch app/__init__.py
touch app/main.py
touch app/config.py
touch app/models/__init__.py
touch app/models/pipeline.py

touch app/routers/__init__.py
touch app/routers/health.py
touch app/routers/fastqc.py
touch app/routers/trimming.py
touch app/routers/alignment.py
touch app/routers/variant_call.py
touch app/routers/annotate.py

touch app/services/__init__.py
touch app/services/fastqc_service.py
touch app/services/trimming_service.py
touch app/services/alignment_service.py
touch app/services/variant_service.py
touch app/services/annotation_service.py

touch tests/__init__.py

touch tests/test.py
touch .env.example

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.pyo
.Python
*.egg-info/
dist/
build/
 
# Virtual environment
.venv/
venv/
env/
 
# Environment variables
.env
 
# Large genomics data files
data/raw/*.fastq
data/raw/*.fastq.gz
data/raw/*.fq
data/raw/*.fq.gz
data/aligned/*.bam
data/aligned/*.bai
data/variants/*.vcf
data/annotated/*.vcf
*.bam
*.bai
*.vcf.gz
*.tbi
*.fa
*.fasta
*.fai
*.dict
 
# Logs
logs/
*.log
 
# IDE
.vscode/
.idea/
*.swp
 
# OS
.DS_Store
Thumbs.db
 
# pytest
.pytest_cache/
.coverage
htmlcov/
EOF
 
cat > requirements.txt << 'EOF'
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic==2.7.1
python-multipart==0.0.9
httpx==0.27.0
pytest==8.2.0
pytest-asyncio==0.23.6
python-dotenv==1.0.1
biopython==1.83
EOF

touch Dockerfile
touch docker-compose.yml
touch README.md

echo "Project structure for ngs-variant-pipeline-api created successfully!"