# &#x1F9EC; EADS: Evolutionary Autonomous Development System

## &#x1F680; Paradigm-Shifting Software Engineering

EADS is a revolutionary approach to autonomous software development using AI, genetic programming, and adaptive learning to create a self-evolving software engineering ecosystem.  The project aims to build an Evolutionary Automated Development System (EADS) for generating, testing, and refining software applications through iterative evolution.  EADS leverages Large Language Models (LLMs), Genetic Programming (GP), and advanced analysis techniques to create robust and adaptable software.  The system is highly scalable, resilient, and adaptable to various software development tasks, exceeding traditional manual or simpler automated systems.

### &#x1F52D; Core Innovation

EADS is an intelligent, self-improving system that learns, adapts, and generates high-quality software with minimal human intervention.

## &#x2728; Key Features

### Intelligent Code Generation
- &#x1F9E0; LLM-powered code synthesis
- &#x1F9EC; Genetic programming for optimization
- &#x1F50D; Semantic understanding via advanced embeddings

### Robust Quality Assurance
- &#x1F4CA; Comprehensive testing frameworks: Unit Testing, Integration Testing, Performance Optimization, Security Hardening
- &#x1F6E1;&#xFE0F; Fault Tolerance: Circuit breaker pattern, Retry with exponential backoff, Fallback strategies with caching

### Advanced Learning Mechanisms
- &#x1F504; Recursive self-improvement cycle
- &#x1F4DA; Semantic knowledge base
- &#x1F916; Decentralized AI engine

## &#x1F3D7;&#xFE0F; System Architecture

### Components

1. **Genetic Programming Engine:** Population-based code evolution using DEAP; Individual representation with code and fitness attributes; Configurable evolution parameters (population size, generations, mutation/crossover rates); FastAPI-based service for evolution operations.
2. **NLP Service:** Sentence Transformer-based code analysis; Semantic code pattern matching; Code similarity computation; FastAPI-based service for NLP operations.
3. **Knowledge Management:** Neo4j Graph Database integration; Asynchronous database operations; Structured code pattern storage; Environment-based configuration.
4. **Testing & Quality Assurance:** Comprehensive test suite with pytest; Pre-commit hooks for code quality; Type checking with mypy; Linting with flake8 and black.

## &#x1F31F; Unique Selling Points

- &#x1F510; Self-securing code generation
- &#x1F4A1; Adaptive learning paradigms
- &#x1F680; Reduced human intervention
- &#x1F30E; Scalable, cloud-native architecture

## &#x1F6E0;&#xFE0F; Technology Stack

### Core Components
| Component               | Technology            | Purpose                                                                                                      |
|------------------------|----------------------|--------------------------------------------------------------------------------------------------------------|
| **AI/ML**               |                      |                                                                                                              |
| LLM Integration        | LangChain 0.1.0+     | Framework for LLM application development                                                                    |
| Vector Search          | LlamaIndex 0.9.15+   | Semantic search and document indexing                                                                        |
| Vector Database        | Weaviate 4.4.0+      | Vector embeddings storage and search                                                                         |
| NLP Models             | sentence-transformers | Code analysis and understanding                                                                              |
| ML Pipeline            | scikit-learn 1.4.0+  | Feature processing and traditional ML                                                                        |
| Neural Networks        | PyTorch 2.1.0+       | Deep learning models and training                                                                            |
| Experiment Tracking    | MLflow 2.10.0+       | ML experiment versioning and tracking                                                                        |
| **Genetic Programming**  |                      |                                                                                                              |
| Evolution Framework    | DEAP 1.4.1+          | Primary framework for evolutionary computation                                                               |
| Alternative Framework  | PyGAD 3.2.0+         | Alternative genetic algorithm implementation                                                                 |
| **Orchestration**       |                      |                                                                                                              |
| Workflow Engine        | Dagster 1.5.0+       | Data and ML pipeline orchestration                                                                           |
| Distributed Computing  | Ray 2.9.0+           | Distributed ML training and inference                                                                        |
| **Development**         |                      |                                                                                                              |
| API Framework          | FastAPI 0.110.0+     | High-performance API development                                                                             |
| HTTP Client           | httpx 0.26.0+        | Modern async HTTP client                                                                                     |
| Version Control        | DVC 3.38.1+          | Data and model versioning                                                                                    |
| Code Quality          | flake8, black, mypy  | Linting, formatting, and type checking                                                                       |
| Testing               | pytest 7.4.0+        | Testing framework with async support                                                                         |
| **Infrastructure**      |                      |                                                                                                              |
| Database              | Neo4j 5.x            | Graph database for knowledge storage                                                                         |
| Containerization      | Docker 24.x          | Application containerization                                                                                 |
| **Utilities**          |                      |                                                                                                              |
| Logging               | structlog 24.1.0+    | Structured logging                                                                                           |
| Config Management     | python-dotenv 1.0.0+ | Environment configuration                                                                                    |
| Code Analysis         | tree-sitter 0.20.4+  | AST parsing and code analysis                                                                               |

## Getting Started

### Prerequisites
- Python 3.11+
- Docker and Docker Compose (optional, for production)

1. Clone the repository:
   ```bash
   git clone https://github.com/nshkrdotcom/EADS.git
   cd EADS
   ```

2. Install Dependencies:
   ```bash
   # Install Poetry and project dependencies
   ./install_requirements.sh
   ```

3. Development Setup:
   ```bash
   # Activate core environment
   poetry shell

   # Install git hooks
   pre-commit install
   ```

4. Run Services:

   Option A - Docker (Recommended):
   ```bash
   # Start all services
   docker-compose up --build -d

   # View logs
   docker-compose logs -f
   ```

   Option B - Local Development:
   ```bash
   # Run NLP service
   cd services/nlp
   poetry shell
   python -m eads_nlp.main

   # Run GP service (in another terminal)
   cd services/gp
   poetry shell
   python -m eads_gp.main
   ```

5. Development Commands:
   ```bash
   # Format and lint
   poetry run black .
   poetry run isort .
   poetry run mypy .

   # Run tests
   poetry run pytest
   ```

6. Access Services:
   - Dagster UI: http://localhost:3000/dagster
   - NLP API: http://localhost:8001
   - GP API: http://localhost:8002
   - Neo4j: http://localhost:7474

## &#x1F4AC; Vision

To create a self-healing, continuously improving software ecosystem that autonomously adapts to emerging technological landscapes.

## &#x1F527; Setup & Installation

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Git
- Linux environment (recommended)
- System packages: `sudo apt-get update && sudo apt-get install -y python3-venv python3-pip`

### Environment Setup

1. **Clone the Repository:** `git clone https://github.com/nshkrdotcom/EADS.git && cd EADS`
2. **Run Setup Script:** `chmod +x setup.sh init.sh install_requirements.sh requirements/lock_deps.sh && ./setup.sh` (Installs system packages, creates a Python virtual environment, and makes initialization scripts executable).
3. **Activate Virtual Environment:** `source .venv/bin/activate`
4. **Install Dependencies:** `./install_requirements.sh` (Installs core dependencies, development tools, and ML libraries).
5. **Environment Configuration:** `cp .env.example .env` (Configure database connections, Weaviate settings, Ray cluster configuration, MLflow tracking, and DVC remote storage).


## Dependency Management

The project uses service-specific dependency management to handle conflicting requirements:

```bash
requirements/
├── nlp.txt      # NLP service dependencies
├── nlp.lock     # Locked versions for NLP
├── gp.txt       # GP Engine dependencies
├── gp.lock      # Locked versions for GP
├── dev.txt      # Development environment (includes all)
└── dev.lock     # Locked versions for development
```

Generate locked dependencies:
```bash
./requirements/lock_deps.sh  # Creates .lock files with exact versions
```

- Each service has its own requirements to handle conflicts (e.g., different httpx versions)
- Development environment includes all dependencies for local work
- Lock files should be committed to version control

### Development Workflow

1. **System Requirements:** Python 3.8 or higher; Docker and Docker Compose; Git; 8GB RAM minimum (16GB recommended); 20GB free disk space.
2. **Python Dependencies:** `sudo apt-get update && sudo apt-get install -y python3-venv python3-pip`
3. **Docker Installation:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

### Initial Setup

1. **Clone the Repository:** `git clone https://github.com/yourusername/EADS.git && cd EADS`
2. **Environment Setup:** `chmod +x setup.sh init.sh install_requirements.sh requirements/lock_deps.sh && ./setup.sh`
3. **Configure Environment Variables:** `cp .env.example .env && nano .env`

### Development Workflow

1. **Start Development Environment:** `source .venv/bin/activate && ./init.sh`
2. **Verify Services:** `docker-compose -f docker/docker-compose.yml ps`; Access service endpoints: Neo4j Browser (http://localhost:7474), NLP Service (http://localhost:8000/docs), GP Engine (http://localhost:8001/docs).
3. **Development Commands:**  `pytest` (run tests), `mypy .` (run type checking), `black . && isort .` (format code), `flake8` (run linting).
4. **Pre-commit Hooks:** `pre-commit install` and `pre-commit run --all-files`.

### Troubleshooting

1. **Docker Issues:** `docker-compose -f docker/docker-compose.yml down -v && docker-compose -f docker/docker-compose.yml up -d`
2. **Database Issues:**  `docker-compose -f docker/docker-compose.yml down -v neo4j && docker-compose -f docker/docker-compose.yml up -d neo4j`; `docker-compose -f docker/docker-compose.yml down -v postgres && docker-compose -f docker/docker-compose.yml up -d postgres`
3. **Common Problems:** Services not starting (check Docker logs and ensure ports are not in use); Neo4j connection failed (wait 45 seconds after startup); Permission errors (ensure Docker has proper permissions); Memory issues (check Docker memory allocation).

### Development Best Practices

1. **Code Quality:** Run pre-commit hooks; Maintain test coverage above 80%; Follow type hints; Document new functions and classes.
2. **Git Workflow:** Create feature branches from `main`; Keep commits atomic; Run tests before pushing; Use conventional commit messages.
3. **Service Development:** Follow async/await patterns; Implement proper error handling; Add appropriate logging; Design for future message queue integration.


### IDE Setup

1. **VSCode Configuration:**
   ```json
   {
     "python.linting.enabled": true,
     "python.linting.flake8Enabled": true,
     "python.formatting.provider": "black",
     "editor.formatOnSave": true,
     "python.linting.mypyEnabled": true
   }
   ```
2. **PyCharm Configuration:** Enable Python type hints; Set Black as formatter; Enable Flake8 linting; Configure test runner for pytest.

### Updating Dependencies

1. **Python Dependencies:** `pip install --upgrade -r requirements/dev.txt` or `pip install --upgrade package_name`
2. **Docker Images:** `docker-compose -f docker/docker-compose.yml pull && docker-compose -f docker/docker-compose.yml build --no-cache`

# EADS Logging and Instrumentation Guide

## Overview

EADS uses structured logging and instrumentation to provide comprehensive visibility into service operations, performance, and errors during development. The system is built on **structlog** for structured logging with JSON output, making it easy to analyze and debug issues.

## Core Features

- Structured JSON logging with timing and context
- Request/response tracking across all services
- Operation-specific metrics and error tracking
- Performance timing built into all operations
- Automatic sensitive data filtering
- Service-specific logging patterns

## Quick Start

### Basic Operation Logging

```python
from eads_core.logging import log_operation

def process_text(text: str) -> dict:
    with log_operation("process_text", text_length=len(text)) as ctx:
        result = do_processing(text)
        ctx.update(result_size=len(result))
        return result
```

**Output:**
```json
{"event": "process_text_started", "text_length": 150, "service": "nlp", "timestamp": "2024-02-20T10:30:45Z"}
{"event": "process_text_completed", "text_length": 150, "result_size": 42, "elapsed_seconds": 0.125, "service": "nlp", "timestamp": "2024-02-20T10:30:45Z"}
```

### Service Setup

```python
from fastapi import FastAPI
from eads_core.logging import ServiceLogger

app = FastAPI()
logger = ServiceLogger("my_service")

# Log service startup
logger.log_startup({
    "service": "my_service",
    "config": {
        "host": "localhost",
        "port": 8080
    }
})

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    ctx = logger.log_request(request.method, request.url.path)
    response = await call_next(request)
    logger.log_response(response.status_code, request_id=ctx.get("request_id"))
    return response
```

## Common Use Cases

### 1. Error Tracking

```python
def analyze_code(code: str) -> dict:
    with log_operation("analyze_code", code_length=len(code)) as ctx:
        try:
            result = perform_analysis(code)
            ctx.update(num_findings=len(result["findings"]))
            return result
        except TemporaryError as e:
            ctx.update(error=str(e))
            raise  # Log will include error and stack trace
```

### 2. Performance Monitoring

```python
def batch_process(items: List[str]) -> List[dict]:
    with log_operation("batch_process", batch_size=len(items)) as ctx:
        start_memory = get_memory_usage()
        results = [process_item(item) for item in items]
        ctx.update(
            memory_delta=get_memory_usage() - start_memory,
            processed_count=len(results)
        )
        return results
```

### 3. Complex Operations

```python
async def train_model(dataset: Dataset, epochs: int):
    with log_operation("model_training",
                      dataset_size=len(dataset),
                      epochs=epochs) as ctx:
        for epoch in range(epochs):
            loss = await train_epoch(dataset)
            ctx.update({f"loss_epoch_{epoch}": loss})
```

## Development Tools

### 1. Log Viewing

During development, logs are output in JSON format to stdout. Use jq for easy filtering and viewing:

```bash
# Watch all logs in pretty format
tail -f service.log | jq '.'

# Filter for specific events
tail -f service.log | jq 'select(.event | contains("model_training"))'

# Watch timing metrics
tail -f service.log | jq 'select(.elapsed_seconds != null)'
```

### 2. Performance Analysis

```bash
# Get average response times for each endpoint
cat service.log | jq -r 'select(.event == "http_response") | {path: .path, time: .elapsed_seconds}' | \
  jq -s 'group_by(.path) | map({path: .[0].path, avg_time: (map(.time) | add / length)})'
```

### 3. Error Investigation

```bash
# Find all errors with stack traces
cat service.log | jq 'select(.error != null)'

# Get error frequency by type
cat service.log | jq -r 'select(.error_type != null) | .error_type' | sort | uniq -c
```

## Best Practices

### Operation Context
- Always include relevant input sizes and counts
- Update context with operation-specific metrics
- Add timing for operations that might be slow

```python
with log_operation("process_document",
                  doc_size=len(document),
                  doc_type=document.type) as ctx:
    # Processing...
    ctx.update(
        sections_processed=len(sections),
        cache_hits=cache_hits,
        warnings=warning_count
    )
```

### Error Handling
- Log errors with full context
- Include relevant state information
- Use appropriate log levels

```python
try:
    result = risky_operation()
except ValueError as e:
    logger.warning("Invalid input", error=str(e), input_value=value)
except Exception as e:
    logger.error("Operation failed",
                error=str(e),
                state=current_state,
                traceback=traceback.format_exc())
```

### Performance Tracking
- Log resource usage for heavy operations
- Track timing for all network calls
- Monitor memory usage for large data processing

```python
with log_operation("data_processing") as ctx:
    ctx.update(initial_memory=get_memory_usage())
    result = process_large_dataset(data)
    ctx.update(
        final_memory=get_memory_usage(),
        records_processed=len(result)
    )
```

## Future Extensions

The logging system is designed to be extensible. Future additions might include:

- Integration with Grafana for metrics visualization
- OpenTelemetry integration for distributed tracing
- Custom log aggregation with Loki
- Automated performance regression detection
- Real-time alerting based on log patterns

## Technical Details

### Core Components

- **structlog**: Structured logging with JSON output
- **FastAPI middleware** for HTTP request tracking
- **Context managers** for operation tracking
- **Time and resource usage measurements**

### Configuration

The logging system is configured in `eads_core/logging.py` and provides:

- JSON formatting for machine readability
- ISO timestamp formatting
- Automatic context propagation
- Environment-based configuration
- Sensitive data filtering

### Performance Impact

The logging system is designed to have minimal overhead:

- JSON serialization is done asynchronously
- Context managers have microsecond-level overhead
- Log levels prevent unnecessary processing
- Sampling can be enabled for high-volume operations



## &#x1F6E0;&#xFE0F; Message Queue Readiness & Roadmap

### Current Architecture (HTTP)
The EADS system uses direct HTTP communication between services, optimized for development and debugging.  This provides simple request/response patterns, easy debugging and monitoring, direct error handling, and straightforward local development.

```mermaid
graph TB
    subgraph Current["Current Architecture (HTTP)"]
        direction LR
        Main[Main Service] -->|HTTP| NLP[NLP Service]
        Main -->|HTTP| GP[GP Engine]
        subgraph Operations["Long-Running Operations"]
            GPOp[Evolution Tasks]
            NLPOp[Code Analysis]
        end
        GP -->|Async| GPOp
        NLP -->|Async| NLPOp
    end
```

### Message Queue Ready Design

The codebase is designed to be "message queue ready" using:

1. **Async Operation Pattern:** Long-running operations return job IDs; Status checking endpoints; Results retrievable via separate endpoints.
2. **Decoupled Processing:** Services operate independently; State management via databases; No direct service-to-service dependencies.
3. **Configurable Timeouts:** `REQUEST_TIMEOUT` environment variable; Adjustable worker processes; Async mode toggle.

### Future Message Queue Architecture

For scaling, a message queue architecture will be implemented:

```mermaid
graph TB
    subgraph Future["Future Architecture (Message Queue)"]
        direction LR
        Main[Main Service] -->|Publish| Queue[(Message Queue)]
        Queue -->|Subscribe| NLP[NLP Service]
        Queue -->|Subscribe| GP[GP Engine]
        subgraph AsyncOps["Asynchronous Operations"]
            GPOp[Evolution Tasks]
            NLPOp[Code Analysis]
        end
        GP -->|Process| GPOp
        NLP -->|Process| NLPOp
    end
```

### Migration Path

1. **Phase 1: Current (HTTP with Async)**
2. **Phase 2: Message Queue Integration:** Add message queue service; Implement publishers/subscribers; Maintain HTTP endpoints; Parallel operation support.
3. **Phase 3: Full Message Queue:** Scale out workers; Advanced retry policies; Dead letter queues; Event-driven processing.

### Code Design Principles
To ensure smooth future migration to message queues, we follow these principles:

1. **Service Independence**
   ```python
   # Example service pattern
   class Service:
       async def process_task(self, task_id: str, payload: dict):
           # Can be triggered by HTTP or message queue
           job = await self.create_job(task_id, payload)
           await self.process_async(job)
           return job.id
   ```

2. **State Management**
   ```python
   # Example state handling
   class JobManager:
       async def get_job_status(self, job_id: str):
           # Consistent state checking regardless of trigger method
           return await self.db.get_job(job_id)
   ```

3. **Result Handling**
   ```python
   # Example result pattern
   class ResultHandler:
       async def store_result(self, job_id: str, result: dict):
           # Results stored in DB, retrievable via ID
           await self.db.store_result(job_id, result)
   ```

## Detailed Message Queue Implementation

#### Message Queue Architecture Details

```mermaid
graph TB
    subgraph Producer["Producer Services"]
        Main[Main Service]
        API[API Gateway]
    end
    subgraph Queue["Message Queue System"]
        Exchange[Exchange/Topics]
        DLQ[Dead Letter Queue]
        RetryQ[Retry Queue]
    end
    subgraph Consumers["Consumer Services"]
        NLP[NLP Service]
        GP[GP Engine]
        subgraph Workers["Worker Pools"]
            NLPWork1[NLP Worker 1]
            NLPWork2[NLP Worker 2]
            GPWork1[GP Worker 1]
            GPWork2[GP Worker 2]
        end
    end
    Main -->|Publish| Exchange
    API -->|Publish| Exchange
    Exchange -->|Route| NLP
    Exchange -->|Route| GP
    Exchange -->|Failed| DLQ
    DLQ -->|Retry| RetryQ
    RetryQ -->|Reprocess| Exchange
    NLP --> NLPWork1
    NLP --> NLPWork2
    GP --> GPWork1
    GP --> GPWork2
```

#### Message Types and Routing

1. **Code Analysis Messages:**  A JSON message specifying `message_type`, `priority`, `payload` (code_id, repository, file_paths, analysis_type), and `metadata` (timestamp, retry_count, timeout).
2. **Evolution Task Messages:** A JSON message specifying `message_type`, `priority`, `payload` (population_id, generation, individuals, fitness_criteria), and `metadata` (timestamp, retry_count, timeout).

#### Queue Configuration

```yaml
# Future docker-compose.yml addition
services:
  rabbitmq:
    image: rabbitmq:3-management
    environment:
      - RABBITMQ_DEFAULT_USER=eads
      - RABBITMQ_DEFAULT_PASS=secure_password
      - RABBITMQ_VM_MEMORY_HIGH_WATERMARK=0.6
    configs:
      - source: rabbitmq_config
        target: /etc/rabbitmq/rabbitmq.conf
configs:
  rabbitmq_config:
    content: |
      queue.max_priority = 10
      queue.max_length = 100000
      consumer_timeout = 3600000
```

#### Error Handling and Retry Strategy

```python
# Future message handling pattern
class MessageProcessor:
    RETRY_DELAYS = [60, 300, 900, 3600]  # Exponential backoff
    async def process_message(self, message: dict):
        try:
            result = await self._process(message)
            await self.acknowledge(message)
            return result
        except TemporaryError as e:
            retry_count = message['metadata']['retry_count']
            if retry_count < len(self.RETRY_DELAYS):
                await self.retry_later(message, delay=self.RETRY_DELAYS[retry_count])
            else:
                await self.move_to_dlq(message, str(e))
        except PermanentError as e:
            await self.move_to_dlq(message, str(e))
```

### Current Service Implementation Examples

#### NLP Service Pattern (Excerpt)

```python
# src/nlp/service.py
from typing import Dict, List, Optional
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

class CodeAnalysisRequest(BaseModel):
    code_id: str
    repository: str
    file_paths: List[str]
    analysis_type: str

class NLPService:
    def __init__(self):
        self.job_store = JobStore()
        self.result_store = ResultStore()

    async def analyze_code(self, request: CodeAnalysisRequest, background_tasks: BackgroundTasks) -> Dict[str, str]:
        job_id = await self.job_store.create_job(task_type="code_analysis", payload=request.dict())
        background_tasks.add_task(self._process_analysis, job_id, request)
        return {"job_id": job_id}

    async def _process_analysis(self, job_id: str, request: CodeAnalysisRequest):
        try:
            result = await self.analyzer.analyze(repository=request.repository, file_paths=request.file_paths)
            await self.result_store.store_result(job_id, result)
            await self.job_store.mark_completed(job_id)
        except Exception as e:
            await self.job_store.mark_failed(job_id, str(e))

    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        return await self.job_store.get_status(job_id)
```

#### GP Engine Pattern (Excerpt)

```python
# src/gp_engine/service.py
from typing import Dict, List, Optional
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

class EvolutionRequest(BaseModel):
    population_id: str
    generation: int
    individuals: List[str]
    fitness_criteria: Dict[str, float]

class GPService:
    def __init__(self):
        self.evolution_store = EvolutionStore()
        self.population_store = PopulationStore()

    async def evolve_population(self, request: EvolutionRequest, background_tasks: BackgroundTasks) -> Dict[str, str]:
        task_id = await self.evolution_store.create_task(population_id=request.population_id, generation=request.generation, payload=request.dict())
        background_tasks.add_task(self._process_evolution, task_id, request)
        return {"task_id": task_id}

    async def _process_evolution(self, task_id: str, request: EvolutionRequest):
        try:
            population = await self.population_store.get_population(request.population_id)
            result = await self.evolution_engine.evolve(population=population, fitness_criteria=request.fitness_criteria)
            await self.population_store.update_population(population_id=request.population_id, new_generation=result)
            await self.evolution_store.mark_completed(task_id)
        except Exception as e:
            await self.evolution_store.mark_failed(task_id, str(e))

    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        return await self.evolution_store.get_status(task_id)
```

These examples demonstrate how the services are designed with message queue patterns in mind, simplifying future migration.  Key aspects include job/task-based processing, asynchronous execution, status tracking, result storage, and error handling.


## Environment Variables and Configuration

EADS uses a two-level configuration system:

1. Project-wide settings (`.env`):
   - Default configurations shared across the team
   - Version controlled with placeholders
   - Copy `.env.template` to `.env` and fill in values

2. Personal overrides (`~/.eads/config`):
   - User-specific settings and API keys
   - Takes precedence over `.env`
   - Not version controlled

### Required Variables

- `GOOGLE_API_KEY`: Google API key for Gemini
- `XAI_API_KEY`: xAI API key for Grok (format: `xai-*`)

### Optional Settings

- `GEMINI_MODEL`: Gemini model to use (default: `gemini-pro`)
- `GROK_MODEL`: Grok model to use (default: `grok-1-base`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `LOG_FILE`: Log file path (default: `eads.log`)

### Example Configuration

Example `.env`:
```ini
# API Keys
GOOGLE_API_KEY=your-google-api-key
XAI_API_KEY=xai-your-key-here

# Model Configurations
GEMINI_MODEL=gemini-pro
GROK_MODEL=grok-1-base

# Other Settings
LOG_LEVEL=INFO
LOG_FILE=eads.log
```

Example `~/.eads/config`:
```ini
# Personal API Keys
GOOGLE_API_KEY=actual-google-key
XAI_API_KEY=xai-actual-key

# Override Models
GEMINI_MODEL=gemini-pro-vision
```

### Security Best Practices

When working with API keys and sensitive configuration:

1. Never commit actual API keys to version control
2. Use `.env.template` as a reference for required variables
3. Keep personal API keys in `~/.eads/config`
4. Use secure environment variable management in production
5. Rotate API keys regularly
6. In production, use a secure secrets management service

## Configuration

The system uses environment variables. Copy `.env.example` to `.env` and adjust the values (`cp .env.example .env`).  Required settings include Neo4j ( `NEO4J_*` variables) and PostgreSQL (`POSTGRES_*` variables).

## Configuration Management

This project uses a two-level configuration system:

### 1. Project Configuration (.env)

The `.env` file in the project root contains default settings and is used for:
- Development environment setup
- Docker configuration
- CI/CD pipelines
- Team-wide settings

```bash
# Copy the template
cp .env.template .env

# Edit with your settings
vim .env  # or your preferred editor
```

### 2. Personal Configuration (~/.eads/config)

The `~/.eads/config` file is for personal settings and overrides:
- Personal API keys
- User-specific configurations
- Settings you don't want in the project directory

```bash
# Create personal config directory
mkdir -p ~/.eads

# Copy the template
cp config.template ~/.eads/config

# Edit with your personal settings
vim ~/.eads/config  # or your preferred editor
```

### Configuration Priority

Environment variables are loaded in this order:
1. `~/.eads/config` (personal overrides)
2. `.env` (project defaults)
3. Existing environment variables

This means:
- Team settings go in `.env`
- Personal overrides go in `~/.eads/config`
- Either file is optional
- Personal settings take precedence

### API Keys

For security:
- Keep personal API keys in `~/.eads/config`
- Never commit API keys to version control
- Use placeholder values in templates

Example `.env`:
```env
# Project-wide settings
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379
```

Example `~/.eads/config`:
```env
# Personal API keys
GOOGLE_API_KEY=your-actual-key
XAI_API_KEY=your-actual-key
```

## &#x1F063; System Architecture

EADS uses a modular microservices architecture: GP Service (`gp_engine`), NLP Service (`nlp`), Knowledge Base (Neo4j), and Configuration Management (environment variables).

1. **GP Service (`gp_engine`):**
   - Manages code evolution through genetic programming
   - Handles population initialization and evolution
   - Configurable evolution parameters
   - RESTful API endpoints for evolution operations

2. **NLP Service (`nlp`):**
   - Code analysis using transformer models
   - Pattern matching and similarity computation
   - RESTful API endpoints for NLP operations
   - Configurable model selection

3. **Knowledge Management:**
   - Neo4j Graph Database integration
   - Asynchronous database operations
   - Structured code pattern storage
   - Environment-based configuration

4. **Configuration Management:**
   - Environment variables for sensitive data
   - Service-specific configuration
   - Logging configuration
   - Development and production settings

## &#x1F4C8; System Diagrams

### High-Level Component Architecture

```mermaid
graph TB
    subgraph Services
        NLP[NLP Service<br>:8000]
        GP[GP Engine<br>:8001]
    end

    subgraph Databases
        Neo4j[(Neo4j<br>:7474/:7687)]
        Postgres[(PostgreSQL<br>:5432)]
        Weaviate[(Weaviate<br>:8080)]
    end

    subgraph Storage
        VectorStore[Vector Store]
        GraphDB[Graph Database]
        MetadataDB[Metadata Store]
    end

	subgraph LLM Layer
		LocalLLM[llama.cpp Models]
		CloudLLM[Cloud LLM APIs]
	end
	NLP --> LocalLLM
	NLP --> CloudLLM

    NLP --> Neo4j
    NLP --> Weaviate
    GP --> Neo4j
    GP --> Postgres

    Weaviate --> VectorStore
    Neo4j --> GraphDB
    Postgres --> MetadataDB
```

### Service Integration Flow

```mermaid
sequenceDiagram
    participant Client
    participant NLP as NLP Service
    participant GP as GP Engine
    participant Neo4j
    participant Weaviate
    participant Postgres

    Client->>NLP: Analyze Code Pattern
    NLP->>Weaviate: Store Embeddings
    NLP->>Neo4j: Store Pattern Structure

    Client->>GP: Evolve Solution
    GP->>Neo4j: Query Patterns
    GP->>Postgres: Track Evolution
    GP->>Client: Return Solution
	NLP->>LocalLLM: Quick Analysis
	NLP->>CloudLLM: Complex Reasoning
```

### Container Architecture

```mermaid
graph TB
    subgraph Docker["Docker Environment"]
        NLP[NLP Service]
        GP[GP Engine]
        Neo4j[Neo4j Service]
        Postgres[PostgreSQL]
        Weaviate[Weaviate Service]
    end

    subgraph Network["Network Configuration"]
        Internal[Internal Network]
        External[External Network]
    end

    subgraph Volumes["Persistent Storage"]
        Neo4jData[Neo4j Data]
        PostgresData[Postgres Data]
        WeaviateData[Weaviate Data]
    end

    External --> NLP
    External --> GP
    NLP --> Internal
    GP --> Internal
    Internal --> Neo4j
    Internal --> Postgres
    Internal --> Weaviate
    Neo4j --> Neo4jData
    Postgres --> PostgresData
    Weaviate --> WeaviateData
```

### Data Flow Architecture

```mermaid
graph LR
    subgraph Input
        Code[Code Input]
        Pattern[Pattern Input]
    end

    subgraph Processing
        NLP[NLP Service]
        GP[GP Engine]
        Evolution[Evolution Process]
		LocalInference[Local Inference]
		CloudInference[Cloud Inference]
    end

    subgraph Storage
        Neo4j[(Neo4j)]
        Weaviate[(Weaviate)]
        Postgres[(PostgreSQL)]
    end

    Code --> NLP
    Pattern --> NLP
    NLP --> Weaviate
    NLP --> Neo4j
    Neo4j --> GP
    GP --> Evolution
    Evolution --> Postgres
    Evolution --> |Optimized Solution| Output
```

### Module Dependencies

```mermaid
graph LR
    subgraph Core
        Config[config]
        ErrorHandling[error_handling]
    end

    subgraph Services
        NLP[nlp]
        GP[gp_engine]
        VectorStore[vector_store]
    end

    subgraph Infrastructure
        Tracking[tracking]
        Orchestration[orchestration]
        Deployment[deployment]
    end

    NLP --> Config
    NLP --> ErrorHandling
    NLP --> VectorStore
    GP --> Config
    GP --> ErrorHandling
    GP --> Core
    VectorStore --> Config
    Tracking --> Config
    Orchestration --> Config
    Deployment --> Config
```

### Component Interaction Flow
```mermaid
graph TB
    subgraph User["User Interface"]
        CLI[CLI Interface]
        API[API Endpoints]
    end

    subgraph Core["Core Services"]
        NLP[NLP Service<br>:8000]
        GP[GP Engine<br>:8001]
        Orchestrator[Orchestration Service]
    end

    subgraph Storage["Data Storage"]
        Neo4j[(Neo4j Graph DB)]
        Postgres[(PostgreSQL)]
        Weaviate[(Weaviate Vector DB)]
    end

    subgraph Processing["Processing Pipeline"]
        CodeGen[Code Generation]
        Testing[Testing & Validation]
        Evolution[Evolution Engine]
    end

    CLI --> Orchestrator
    API --> Orchestrator
    Orchestrator --> NLP
    Orchestrator --> GP
    NLP --> Weaviate
    NLP --> Neo4j
    GP --> Neo4j
    GP --> Postgres
    CodeGen --> Testing
    Testing --> Evolution
    Evolution --> CodeGen
```

### Data Processing Pipeline
```mermaid
graph LR
    subgraph Input
        Code[Source Code]
        Specs[Requirements]
    end

    subgraph Processing
        Parse[Code Parser]
        Embed[Embeddings Generator]
        Match[Pattern Matcher]
        Gen[Code Generator]
    end

    subgraph Storage
        Vec[(Vector Store)]
        Graph[(Graph DB)]
        SQL[(SQL DB)]
    end

    Code --> Parse
    Specs --> Parse
    Parse --> Embed
    Embed --> Vec
    Embed --> Match
    Match --> Graph
    Graph --> Gen
    Gen --> SQL
```

### Fault Tolerance Mechanism
```mermaid
graph TD
    subgraph FaultTolerance["Fault Tolerance Mechanism"]
        Request[Client Request]
        CB[Circuit Breaker]
        Retry[Retry Mechanism]
        Service[Service Call]
        Cache[Fallback Cache]
        Fallback[Fallback Handler]

        Request --> CB
        CB -->|Open| Fallback
        CB -->|Closed| Retry
        Retry -->|Attempt| Service
        Service -->|Success| Cache
        Service -->|Failure| Retry
        Retry -->|Max Attempts| Fallback
        Fallback -->|Check| Cache
        Cache -->|Available| Response
        Fallback -->|Compute| Response
    end
```

### Fault Tolerance Architecture
```mermaid
graph TB
    subgraph Architecture["Fault Tolerance Architecture"]
        subgraph Services["Service Layer"]
            NLP[NLP Service]
            GP[GP Engine]
        end

        subgraph FaultTolerance["Fault Tolerance Layer"]
            CB[Circuit Breaker]
            Retry[Retry Mechanism]
            Fallback[Fallback Handler]
            Cache[Response Cache]
        end

        subgraph States["Circuit States"]
            Closed[Closed State]
            Open[Open State]
            HalfOpen[Half-Open State]
        end

        Client[Client Request] --> CB
        CB --> |Success Rate OK| Closed
        CB --> |High Failure Rate| Open
        CB --> |Testing Recovery| HalfOpen

        Closed --> Retry
        Retry --> |Attempt| Services
        Services --> |Success| Cache
        Services --> |Failure| Retry
        Retry --> |Max Attempts| Fallback
        Fallback --> |Check| Cache
        Cache --> |Available| Response[Response]
        Fallback --> |Compute| Response
    end
```

### Development Workflow
```mermaid
graph TD
    subgraph Local["Local Development"]
        Code[Write Code]
        Test[Run Tests]
        Lint[Lint & Format]
    end

    subgraph CI["CI Pipeline"]
        Build[Build Images]
        IntTest[Integration Tests]
        Deploy[Deploy Services]
    end

    subgraph QA["Quality Assurance"]
        PreCommit[Pre-commit Hooks]
        TypeCheck[Type Checking]
        Coverage[Test Coverage]
    end

    Code --> PreCommit
    PreCommit --> TypeCheck
    TypeCheck --> Test
    Test --> Coverage
    Coverage --> Lint
    Lint --> Build
    Build --> IntTest
    IntTest --> Deploy
```

### Deployment Architecture
```mermaid
graph TB
    subgraph Docker["Docker Environment"]
        NLP[NLP Service]
        GP[GP Engine]
        Neo4j[Neo4j Service]
        Postgres[PostgreSQL]
        Weaviate[Weaviate Service]
    end

    subgraph Network["Network Configuration"]
        Internal[Internal Network]
        External[External Network]
    end

    subgraph Volumes["Persistent Storage"]
        Neo4jData[Neo4j Data]
        PostgresData[Postgres Data]
        WeaviateData[Weaviate Data]
    end

    External --> NLP
    External --> GP
    NLP --> Internal
    GP --> Internal
    Internal --> Neo4j
    Internal --> Postgres
    Internal --> Weaviate
    Neo4j --> Neo4jData
    Postgres --> PostgresData
    Weaviate --> WeaviateData
```

### Testing Strategy
```mermaid
graph TB
    subgraph Tests["Test Suite"]
        Unit[Unit Tests]
        Integration[Integration Tests]
        E2E[End-to-End Tests]
    end

    subgraph Coverage["Test Coverage"]
        Code[Code Coverage]
        Branch[Branch Coverage]
        Integration[Integration Points]
    end

    subgraph CI["Continuous Integration"]
        Build[Build Pipeline]
        Test[Test Pipeline]
        Deploy[Deploy Pipeline]
    end

    Unit --> Code
    Integration --> Branch
    E2E --> Integration
    Code --> Build
    Branch --> Test
    Integration --> Deploy
```

# Assessment of the Initial Phase

## Strengths:

### Architecture Design
- Clean separation of services (NLP, GP Engine)
- Well-thought-out fault tolerance patterns (circuit breakers, retries)
- Message-queue ready design for future scaling

### Development Experience
- Comprehensive documentation
- Service-specific dependency management
- Good development tooling:
  - `pytest`
  - `mypy`
  - `black`
  - `flake8`

### Infrastructure
- Docker-based deployment
- Multiple database integrations:
  - Neo4j
  - PostgreSQL
  - Weaviate
- Environment-based configuration

## Areas for Consideration:

### Testing Infrastructure
- While the testing strategy is documented, not many actual tests are present yet.
- Consider adding integration test examples between NLP and GP services.
- Add performance benchmarking tests early.

### Monitoring & Observability
- Consider adding logging infrastructure.
- Add health check endpoints.
- Implement metrics collection.

### Development Flow
- Could benefit from example notebooks/scripts.
- Add more concrete examples of genetic programming patterns.
- Consider adding development environment setup scripts.

### Documentation
- Add API documentation.
- Include sequence diagrams for key flows.
- Add troubleshooting guides.

## Recommendations for Next Phase:

### Core Functionality
- Implement basic GP operations.
- Add NLP analysis patterns.
- Create initial integration points.

### Developer Experience
- Add example workflows.
- Create debugging tools.
- Implement development data generators.

### Quality Assurance
- Set up CI/CD pipeline.
- Add integration tests.
- Implement automated testing.

### Infrastructure
- Add monitoring stack.
- Implement proper logging.
- Set up development environment automation.

## LLM Integration

This project integrates with multiple LLM providers including Google's Gemini and xAI's Grok.

### Configuration Setup

This project uses a centralized configuration file located in `~/.eads/config`.

1. Create the configuration directory:
```bash
mkdir -p ~/.eads
```

2. Copy the template configuration:
```bash
cp config.template ~/.eads/config
```

3. Get your API keys:
   - For Gemini: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - For xAI: Access your key from [xAI Console](https://console.x.ai/api-keys)

4. Update your configuration:
```bash
# Open with your preferred editor
vim ~/.eads/config  # or nano, code, etc.
```

5. Configuration Structure:
```env
# API Keys
GOOGLE_API_KEY=your-google-api-key-here
XAI_API_KEY=your-xai-api-key-here

# Model Configurations
GEMINI_MODEL=gemini-pro
GROK_MODEL=grok-1-base
```

### Environment Management

The project automatically loads configuration from `~/.eads/config`. You can also:

1. Load configuration manually:
```python
from utils.env import load_env

# Load from default location (~/.eads/config)
load_env()

# Or specify a custom path
load_env("/path/to/custom/config")
```

2. Access configuration values:
```python
from utils.env import get_required_env

# Get required values (raises ValueError if not set)
api_key = get_required_env("GOOGLE_API_KEY")

# Get optional values
import os
optional_value = os.getenv("OPTIONAL_VAR", "default_value")
```

### Available Models

#### Gemini
- Default model: `gemini-pro`
- Configuration in `services/llm/gemini.py`
- Uses LangChain for integration
- Async support included

#### Grok (xAI)
- Available models:
  - `grok-2-1212`: Latest text model
  - `grok-2-vision-1212`: Image understanding model
- Configuration in `services/llm/xai.py`
- Direct API integration
- Supports:
  - Temperature control
  - Stream mode
  - System messages
  - Stop sequences

### Dagster Assets

Both LLM integrations are available as Dagster assets:

- Gemini assets in `orchestration/assets/llm_assets.py`:
  - `gemini_service`: Creates and configures Gemini service instance
  - `gemini_response`: Generates responses using Gemini

- xAI assets in `orchestration/assets/xai_assets.py`:
  - `grok_service`: Creates and configures Grok service instance
  - `grok_response`: Generates responses using Grok

### Security Notes

- The `~/.eads` directory is created with user-only permissions
- Never commit your actual configuration file
- Use secure environment variable management in production environments
- API keys should be kept confidential and rotated regularly
- In production, use a secure secrets management service
