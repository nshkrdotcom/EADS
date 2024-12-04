# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements files first to leverage Docker cache
COPY services/core/requirements/base.txt /app/requirements/base.txt
COPY services/gp/requirements/gp.txt /app/requirements/gp.txt

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r /app/requirements/gp.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only necessary source code
COPY services/core/eads_core /app/eads_core
COPY services/gp/eads_gp /app/eads_gp

ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 8002

# Command to run the application
CMD ["uvicorn", "eads_gp.main:app", "--host", "0.0.0.0", "--port", "8002"]
