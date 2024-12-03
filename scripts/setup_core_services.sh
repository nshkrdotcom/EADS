#!/bin/bash

# Exit on error
set -e

echo "Setting up EADS core services..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is required but not installed. Please install Docker first."
    exit 1
fi

# Create docker network if it doesn't exist
docker network create eads-network 2>/dev/null || true

# Start Neo4j
echo "Starting Neo4j..."
docker run -d \
    --name eads-neo4j \
    --network eads-network \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    neo4j:latest

# Start Weaviate
echo "Starting Weaviate..."
docker run -d \
    --name eads-weaviate \
    --network eads-network \
    -p 8080:8080 \
    -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
    -e PERSISTENCE_DATA_PATH="/var/lib/weaviate" \
    semitechnologies/weaviate:latest

# Start PostgreSQL
echo "Starting PostgreSQL..."
docker run -d \
    --name eads-postgres \
    --network eads-network \
    -p 5432:5432 \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=eads \
    postgres:latest

# Start MLflow
echo "Starting MLflow..."
docker run -d \
    --name eads-mlflow \
    --network eads-network \
    -p 5000:5000 \
    -e MLFLOW_TRACKING_URI=http://localhost:5000 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=mlflow \
    ghcr.io/mlflow/mlflow:latest

echo "Core services setup complete!"
echo "
Services running:
- Neo4j: http://localhost:7474 (Browser)
- Weaviate: http://localhost:8080
- PostgreSQL: localhost:5432
- MLflow: http://localhost:5000

Default credentials are in .env.example
"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete! You can now start using EADS."
