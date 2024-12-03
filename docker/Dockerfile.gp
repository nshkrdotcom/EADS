FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY services/core/eads_core /app/eads_core
COPY services/gp/eads_gp /app/eads_gp
COPY services/gp/requirements/gp.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 8002

# Command to run the application
CMD ["uvicorn", "eads_gp.main:app", "--host", "0.0.0.0", "--port", "8002"]
