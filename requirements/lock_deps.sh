#!/bin/bash

# Install pip-tools if not present
pip install pip-tools

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Function to generate lock file with error handling
generate_lock() {
    local input="$SCRIPT_DIR/$1"
    local output="$SCRIPT_DIR/$2"
    echo "Generating $output..."
    if ! pip-compile --generate-hashes "$input" --output-file "$output"; then
        echo "Error generating $output"
        exit 1
    fi
}

# Generate service-specific locks
generate_lock "nlp.txt" "nlp.lock"
generate_lock "gp.txt" "gp.lock"

# Generate development environment locks
generate_lock "dev.txt" "dev.lock"

echo "Done! Generated lock files with exact versions and hashes."
echo "Note: dev.lock includes all dependencies needed for local development."
