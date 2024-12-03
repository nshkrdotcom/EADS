#!/bin/bash

# Function to create and setup a virtual environment
setup_venv() {
    local service=$1
    local requirements=$2

    echo "Setting up $service environment..."

    # Create venv
    python3.11 -m venv venv-$service

    # Activate and install dependencies
    source venv-$service/bin/activate
    pip install --upgrade pip
    pip install -r $requirements
    deactivate

    echo "$service environment setup complete!"
}

# Create service directories if they don't exist
mkdir -p services/core/src
mkdir -p services/nlp/src
mkdir -p services/gp/src

# Setup each service's virtual environment
setup_venv "core" "services/core/requirements/base.txt"
setup_venv "nlp" "services/nlp/requirements/nlp.txt"
setup_venv "gp" "services/gp/requirements/gp.txt"

echo "All virtual environments have been created!"
