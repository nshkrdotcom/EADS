#!/bin/bash
set -e

# Create new directory structure
echo "Creating new directory structure..."
mkdir -p .github
mkdir -p src/{core,services,utils,nlp,gp_engine,orchestration}
mkdir -p scripts/{setup,deployment}
mkdir -p config/templates
mkdir -p requirements

# Move source code directories
echo "Moving source code..."
mv core/* src/core/ 2>/dev/null || true
mv services/* src/services/ 2>/dev/null || true
mv utils/* src/utils/ 2>/dev/null || true
mv nlp/* src/nlp/ 2>/dev/null || true
mv gp_engine/* src/gp_engine/ 2>/dev/null || true
mv orchestration/* src/orchestration/ 2>/dev/null || true

# Move configuration files
echo "Moving configuration files..."
mv .env* config/templates/
mv config.template config/templates/
cp config/templates/.env.example config/.env

# Consolidate requirements
echo "Consolidating requirements..."
mv requirements.txt requirements/base.txt
touch requirements/{dev,test,prod}.txt
echo "-r base.txt" | tee requirements/{dev,test,prod}.txt

# Move scripts
echo "Moving scripts..."
mv *.sh scripts/setup/
mv docker-compose.yml docker/

# Clean up virtual environments
echo "Cleaning up virtual environments..."
rm -rf venv-* 2>/dev/null || true
python3 -m venv .venv

# Update .gitignore
echo "Updating .gitignore..."
cat << EOF >> .gitignore

# Additional ignores
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/
*.log
.env
EOF

# Remove empty directories
echo "Cleaning up empty directories..."
find . -type d -empty -delete

# Fix permissions
echo "Fixing permissions..."
chown -R $(whoami):$(whoami) .

echo "Project reorganization complete!"
echo "Please review the changes and update import statements as needed."
