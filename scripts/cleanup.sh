#!/bin/bash
set -e

echo "Cleaning up duplicate directories..."
# Move remaining files from root directories to src
mv -n orchestration/* src/orchestration/ 2>/dev/null || true
mv -n error_handling/* src/error_handling/ 2>/dev/null || true
mv -n code_generation/* src/core/ 2>/dev/null || true
mv -n init/* src/init/ 2>/dev/null || true

# Remove empty directories from root
rm -rf orchestration error_handling code_generation init 2>/dev/null || true

# Consolidate config directories
mv -n config/* src/config/ 2>/dev/null || true
rm -rf config 2>/dev/null || true

# Clean up any remaining empty directories
find . -type d -empty -delete

echo "Cleanup complete!"
