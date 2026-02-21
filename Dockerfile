FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash git && \
    rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Install package with all optional deps
RUN pip install --no-cache-dir -e ".[dev]" && \
    pip install --no-cache-dir faker detect-secrets || true

# Default: run tests
CMD ["python", "-m", "pytest", "-v", "--tb=short"]
