# 🌌 NOVA v3.1 - THE FORENSIC CODE AUDITOR
# Dockerized Python 3.11 CLI

FROM python:3.11-slim

# Set labels
LABEL maintainer="NOVA Team"
LABEL version="3.1"
LABEL description="NOVA - The Forensic Code Auditor"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash nova && \
    chown -R nova:nova /app

# Switch to non-root user
USER nova

# Set entrypoint
ENTRYPOINT ["python", "-m", "nova.cli"]

# Default command (show help)
CMD ["--help"]
