# EADS Core Service

This directory contains the core shared utilities and base dependencies for the EADS project.

## Setup

1. Create virtual environment:
```bash
python -m venv venv-core
source venv-core/bin/activate  # Linux/Mac
# or
.\venv-core\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements/base.txt
```

## Contents

- `requirements/`: Base dependencies for development, testing, and shared utilities
  - `base.txt`: Core dependencies
  - `base.lock`: Generated lock file (coming soon)
