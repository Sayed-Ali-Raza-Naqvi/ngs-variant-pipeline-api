FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    default-jre \
    bwa \
    samtools \
    fastqc \
    trimmomatic \
    && rm -rf /var/lib/apt/lists/*

# Install GATK
ARG GATK_VERSION=4.5.0.0
RUN wget -q https://github.com/broadinstitute/gatk/releases/download/${GATK_VERSION}/gatk-${GATK_VERSION}.zip \
    && unzip -q gatk-${GATK_VERSION}.zip \
    && mv gatk-${GATK_VERSION} /opt/gatk \
    && rm gatk-${GATK_VERSION}.zip

ENV PATH="/opt/gatk:${PATH}"

# Install SnpEff
ARG SNPEFF_VERSION=5.2
RUN wget -q https://snpeff.blob.core.windows.net/versions/snpEff_v${SNPEFF_VERSION}_core.zip \
    && unzip -q snpEff_v${SNPEFF_VERSION}_core.zip \
    && mv snpEff /opt/snpeff \
    && rm snpEff_v${SNPEFF_VERSION}_core.zip

# Wrapper script so we can call snpEff from anywhere
RUN echo '#!/bin/bash\njava -jar /opt/snpeff/snpEff.jar "$@"' > /usr/local/bin/snpEff \
    && chmod +x /usr/local/bin/snpEff

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data and log directories
RUN mkdir -p data/raw data/trimmed data/aligned data/variants data/annotated logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]