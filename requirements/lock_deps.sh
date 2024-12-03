#!/bin/bash

# Install pip-tools if not present
pip install pip-tools

# Generate locked requirements with hashes
echo "Generating base.lock..."
pip-compile --generate-hashes base.txt --output-file base.lock

echo "Generating dev.lock..."
pip-compile --generate-hashes dev.txt --output-file dev.lock

echo "Done! Generated base.lock and dev.lock with exact versions and hashes."
