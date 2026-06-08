# Canonical, pinned CPU-only environment for the BioBenchGuard paper artifact. No GPU required.
FROM python:3.11-slim

LABEL org.opencontainers.image.title="BioBenchGuard paper artifact" \
      org.opencontainers.image.description="Rule-based benchmark-metrology audit + reproduction package (not a trained model)." \
      org.opencontainers.image.licenses="Apache-2.0"

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MPLBACKEND=Agg

# Pinned dependencies first (layer caching)
COPY requirements.lock /app/requirements.lock
RUN pip install --no-cache-dir -r /app/requirements.lock

# Artifact (CLI package + examples + locked source data + tests)
COPY biobenchguard /app/biobenchguard
COPY examples /app/examples
COPY source_data /app/source_data
COPY results_locked /app/results_locked
COPY tests /app/tests
COPY pyproject.toml README.md LICENSE /app/
RUN pip install --no-cache-dir --no-deps -e .

# Default: show help (few, stable commands)
ENTRYPOINT []
CMD ["biobenchguard", "--help"]
