#!/bin/bash

# Exit on error
set -e

echo "🔧 Installing Python requirements for EADS"

# Check if running in virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Virtual environment not activated!"
    echo "Please run: source .venv/bin/activate"
    echo "Or use setup.sh to handle everything automatically"
    exit 1
fi

# Install requirements
echo "📦 Installing Python packages..."
pip install -r requirements.txt

echo "✅ Python requirements installed successfully!"
