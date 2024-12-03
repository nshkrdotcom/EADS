#!/bin/bash

# Build the requirements Docker image
docker build -t eads-requirements -f docker/Dockerfile.requirements .

# Run the container to generate lock files
docker run --rm -v $(pwd)/requirements:/requirements eads-requirements

echo "Lock files generated!"
