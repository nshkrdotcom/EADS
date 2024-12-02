#!/bin/bash

# Exit on error
set -e

echo "🚀 Initializing EADS (Evolutionary Autonomous Development System)"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️ Please update the .env file with your actual credentials before continuing"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p init/data

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Initialize databases
echo "🗄️ Initializing databases..."
python init/db_init.py

# Initialize knowledge base
echo "🧠 Initializing knowledge base..."
python init/knowledge_base_init.py

echo "✨ EADS initialization completed!"
echo "
Available services:
- Neo4j Browser: http://localhost:7474
- Airflow UI: http://localhost:8080
- PostgreSQL: localhost:5432

Next steps:
1. Access Neo4j browser and verify the knowledge graph
2. Check Airflow UI for workflow status
3. Start developing with EADS!
"
