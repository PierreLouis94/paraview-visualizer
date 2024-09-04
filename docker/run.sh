#!/usr/bin/env bash

# Run the build script
echo "Building Docker image..."
./scripts/build_image.sh

# Run the Docker image
echo "Running Docker image..."
./scripts/run_image.sh
