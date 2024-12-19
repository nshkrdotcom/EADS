# EADS NLP Service

This directory contains the Natural Language Processing service for EADS.

## Setup

1. Create virtual environment:
```bash
python -m venv venv-nlp
source venv-nlp/bin/activate  # Linux/Mac
# or
.\venv-nlp\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements/nlp.txt
```

## Contents

- `requirements/`: NLP-specific dependencies
  - `nlp.txt`: NLP service dependencies
  - `nlp.lock`: Generated lock file (coming soon)

## Dependencies

This service builds on top of core dependencies and adds:
- LangChain for LLM orchestration
- Sentence Transformers for embeddings
- Weaviate for vector storage
- LlamaIndex for data indexing
