#!/bin/bash

# Exit on error
set -e

echo "🔧 Installing Poetry and setting up EADS environments"

# Install Poetry if not already installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Configure Poetry to create virtual environments in the project directory
poetry config virtualenvs.in-project true

# Install core package dependencies
echo "📦 Installing core package dependencies..."
poetry install

# Install GP service dependencies
echo "📦 Installing GP service dependencies..."
cd services/gp
poetry install
cd ../..

# Install NLP service dependencies
echo "📦 Installing NLP service dependencies..."
cd services/nlp
poetry install
cd ../..

echo "✅ All Python environments set up successfully!"
echo ""
echo "To activate an environment, use:"
echo "  poetry shell              # For core development"
echo "  cd services/gp && poetry shell   # For GP service"
echo "  cd services/nlp && poetry shell  # For NLP service"
