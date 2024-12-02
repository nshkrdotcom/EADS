#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up EADS environment"

# Check for python3-venv
if ! dpkg -l | grep -q python3-venv; then
    echo "📦 Installing python3-venv..."
    sudo apt-get update
    sudo apt-get install -y python3-venv python3-pip
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Make both scripts executable
chmod +x init.sh
chmod +x setup.sh

echo "✨ Environment setup completed!"
echo "
To start EADS:
1. First activate the virtual environment:
   source .venv/bin/activate

2. Then run the initialization script:
   ./init.sh

3. When you're done, deactivate the virtual environment:
   deactivate
"
