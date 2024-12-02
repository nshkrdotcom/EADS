#!/bin/bash

# Exit on error
set -e

# Function to manage Docker services
manage_docker_services() {
    local action=$1
    echo "🐳 $action Docker services..."

    case $action in
        "stop")
            echo "🛑 Stopping all services..."
            docker-compose down -v
            ;;
        "start")
            echo "🚀 Starting services..."
            docker-compose up -d

            echo "⏳ Waiting for services to initialize..."
            echo "  - This may take up to a minute"
            echo "  - Neo4j needs time to start and set up the database"
            sleep 45

            # Verify services are running
            if ! docker-compose ps | grep -q "Up"; then
                echo "❌ Services failed to start properly"
                echo "📋 Service logs:"
                docker-compose logs
                exit 1
            fi
            echo "✅ All services are running"
            ;;
        *)
            echo "❌ Invalid action: $action"
            exit 1
            ;;
    esac
}

# Check if running in virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Virtual environment not activated!"
    echo "Please run: source .venv/bin/activate"
    echo "Or use setup.sh to handle everything automatically"
    exit 1
fi

echo "🚀 Initializing EADS (Evolutionary Autonomous Development System)"

# Docker setup
echo "🐳 Setting up Docker environment..."

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
fi

# Add user to docker group
if ! groups | grep -q docker; then
    echo "Adding user to docker group..."
    sudo usermod -aG docker $USER
    echo "⚠️ You may need to log out and log back in for group changes to take effect"
fi

# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock

# Start Docker service
sudo service docker start

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

# Stop any existing services
manage_docker_services "stop"

# Pull latest images
echo "📥 Pulling latest Docker images..."
docker-compose pull

# Start services with proper initialization
manage_docker_services "start"

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
- NLP Service: http://localhost:8000
- GP Engine: http://localhost:8001
- PostgreSQL: localhost:5432

Commands:
- Stop all services:    docker-compose down
- Remove all data:      docker-compose down -v
- View service logs:    docker-compose logs
- Check service status: docker-compose ps
"
