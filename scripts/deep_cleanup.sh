#!/bin/bash
set -e

echo "Starting deep cleanup..."

# Clean up cache and build files
echo "Cleaning cache and build files..."
rm -rf .coverage .mypy_cache .pytest_cache __pycache__ htmlcov src/eads.egg-info
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Consolidate environment files
echo "Consolidating environment files..."
mkdir -p config/env
mv .env* config/env/ 2>/dev/null || true
mv config.template config/env/ 2>/dev/null || true

# Update docker files
echo "Organizing docker files..."
mv docker-compose.yml docker/ 2>/dev/null || true
mv requirements.txt docker/requirements.txt 2>/dev/null || true

# Clean up empty directories
echo "Removing empty directories..."
find . -type d -empty -delete

# Update .gitignore
echo "Updating .gitignore..."
cat << EOF > .gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Logs
*.log

# Type checking
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/

# Project specific
config/env/*
!config/env/.env.example
docker/**/data/
EOF

echo "Deep cleanup complete!"
