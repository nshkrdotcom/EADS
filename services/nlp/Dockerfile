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

# Copy NLP service requirements
COPY requirements/nlp.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the NLP service code
COPY . .

EXPOSE 8001

CMD ["uvicorn", "nlp.main:app", "--host", "0.0.0.0", "--port", "8001"]
