FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy core requirements first
COPY ../core/requirements/base.txt core-requirements.txt
RUN pip install --no-cache-dir -r core-requirements.txt

# Copy GP service requirements
COPY requirements/gp.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the GP service code
COPY . .

EXPOSE 8002

CMD ["uvicorn", "gp.main:app", "--host", "0.0.0.0", "--port", "8002"]
