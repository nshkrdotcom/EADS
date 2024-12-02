#!/bin/bash

# Exit on error
set -e

# Check if running in virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Virtual environment not activated!"
    echo "Please run: source .venv/bin/activate"
    echo "Or use setup.sh to handle everything automatically"
    exit 1
fi

echo "🚀 Initializing EADS (Evolutionary Autonomous Development System)"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
fi

# Check Docker permissions
if ! groups | grep -q docker; then
    echo "⚠️ Adding user to docker group..."
    sudo usermod -aG docker $USER
    echo "✨ Please log out and log back in for the changes to take effect."
    echo "Then run this script again."
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "🔄 Starting Docker daemon..."
    sudo service docker start
    sleep 5
fi

# Check for python3-venv
if ! dpkg -l | grep -q python3-venv; then
    echo "📦 Installing python3-venv..."
    sudo apt-get update
    sudo apt-get install -y python3-venv python3-pip
fi

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

# Create and activate virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies in batches
echo "📦 Installing Python dependencies..."
pip install --upgrade pip

echo "Installing base requirements..."
pip install python-dotenv pytest black flake8

echo "Installing database requirements..."
pip install psycopg2-binary neo4j pinecone-client

echo "Installing data science requirements..."
pip install numpy pandas scikit-learn

echo "Installing ML requirements..."
pip install torch
pip install tensorflow

echo "Installing genetic programming requirements..."
pip install deap pygad

echo "Installing PDF processing requirements..."
pip install PyPDF2

# Start Docker services
echo "🐳 Starting Docker services..."
if ! docker-compose up -d; then
    echo "❌ Failed to start Docker services. Please check the error messages above."
    echo "You might need to run: sudo chmod 666 /var/run/docker.sock"
    echo "Then try running this script again."
    exit 1
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Initialize databases
echo "🗄️ Initializing databases..."
python init/db_init.py

# Initialize knowledge base
echo "🧠 Initializing knowledge base..."
python init/knowledge_base_init.py

# Deactivate virtual environment
deactivate

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

To activate the virtual environment in the future, run:
source .venv/bin/activate
"
