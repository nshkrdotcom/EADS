# EADS GP Service

This directory contains the GPU/ML service for EADS.

## Setup

1. Create virtual environment:
```bash
python -m venv venv-gp
source venv-gp/bin/activate  # Linux/Mac
# or
.\venv-gp\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements/gp.txt
```

## Contents

- `requirements/`: ML/GPU-specific dependencies
  - `gp.txt`: GPU service dependencies
  - `gp.lock`: Generated lock file (coming soon)

## Dependencies

This service builds on top of core dependencies and adds:
- TensorFlow for deep learning
- PyTorch for deep learning
- Ray for distributed computing
- Hugging Face Transformers for ML models
