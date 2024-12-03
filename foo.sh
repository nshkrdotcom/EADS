#!/bin/bash

# Ensure each lock file ends with exactly one newline
for f in requirements/*.lock; do
    if [ -f "$f" ]; then
        # Ensure file ends with exactly one newline
        sed -i -e '$a\' "$f"
    fi
done
