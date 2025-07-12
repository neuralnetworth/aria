# Project Setup Guide

## Prerequisites

### System Requirements
- **OS**: Windows 11 (for production) / WSL2 (for development)
- **GPU**: NVIDIA RTX 4080 Super or equivalent (16GB+ VRAM)
- **RAM**: 32GB recommended
- **Python**: 3.11 or 3.12
- **CUDA**: Drivers installed (via NVIDIA)

### Required Software
```bash
# Install Ollama (Windows)
# Download from: https://ollama.ai/download/windows

# Pull the model
ollama pull qwen2.5:14b

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

### Development Tools
```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# For Windows PowerShell:
# irm https://astral.sh/uv/install.ps1 | iex
```

## Project Structure

```
aria/
├── pyproject.toml          # Project metadata and dependencies
├── README.md              # Project documentation
├── .gitignore            # Git ignore rules
├── configs/              # Configuration files
│   └── default.yaml      # Default settings
├── src/                  # Source code
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── api/             # FastAPI application
│   │   ├── __init__.py
│   │   ├── server.py    # Main API server
│   │   ├── websocket.py # WebSocket handlers
│   │   └── models.py    # Pydantic models
│   ├── services/        # Core services
│   │   ├── __init__.py
│   │   ├── ollama.py    # Ollama client
│   │   ├── whisper.py   # STT service
│   │   ├── tts.py       # TTS service
│   │   └── audio.py     # Audio processing
│   └── utils/           # Utility functions
│       ├── __init__.py
│       └── config.py    # Configuration loader
├── frontend/            # Frontend application
│   └── (TBD: React or Native Python)
├── tests/              # Test suite
│   ├── __init__.py
│   ├── test_api.py
│   └── test_services.py
└── scripts/            # Utility scripts
    ├── setup.py        # First-time setup
    └── benchmark.py    # Performance testing
```

## Initial Setup

### 1. Create Project Directory
```bash
# In WSL or Windows terminal
mkdir aria && cd aria
git init
```

### 2. Create pyproject.toml
```toml
[project]
name = "aria"
version = "0.1.0"
description = "Local AI voice assistant with Ollama"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "websockets>=13.0",
    "httpx>=0.27.0",
    "openai-whisper>=20231117",
    "numpy>=1.26.0",
    "scipy>=1.14.0",
    "pyaudio>=0.2.14",
    "pyyaml>=6.0.2",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "black>=24.10.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
]

# TTS options (choose one)
tts-coqui = ["coqui-tts>=0.25.0"]
tts-kokoro = ["kokoro>=0.7.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
```

### 3. Create Basic Configuration
```yaml
# configs/default.yaml
api:
  host: "0.0.0.0"
  port: 8000
  cors_origins: ["http://localhost:3000"]

ollama:
  base_url: "http://localhost:11434"
  model: "qwen2.5:14b"
  options:
    temperature: 0.7
    top_k: 40
    top_p: 0.9
  timeout: 30.0

whisper:
  model_size: "base"
  device: "cuda"
  language: "en"
  
audio:
  sample_rate: 16000
  chunk_duration_ms: 30
  vad_threshold: 0.5
  
tts:
  engine: "coqui"  # or "kokoro"
  voice: "default"
  speed: 1.0
```

### 4. Install Dependencies
```bash
# Create virtual environment and install
uv sync

# Install with TTS option
uv sync --extra tts-coqui

# Install dev dependencies
uv sync --extra dev
```

### 5. Create Entry Point
```python
# src/main.py
import asyncio
import uvicorn
from api.server import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
```

## Development Workflow

### Running the Application
```bash
# Development mode (with auto-reload)
uv run uvicorn src.api.server:app --reload

# Production mode
uv run python src/main.py
```

### Code Quality
```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test
uv run pytest tests/test_api.py::test_websocket
```

## Environment Variables
```bash
# .env file (create in project root)
OLLAMA_HOST=http://localhost:11434
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
```

## Troubleshooting

### Common Issues

1. **Ollama not responding**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Start Ollama service (Windows)
   ollama serve
   ```

2. **CUDA not available**
   ```python
   # Check CUDA availability
   import torch
   print(torch.cuda.is_available())
   ```

3. **Audio device errors**
   ```python
   # List audio devices
   import pyaudio
   p = pyaudio.PyAudio()
   for i in range(p.get_device_count()):
       print(p.get_device_info_by_index(i))
   ```

## Next Steps

1. **Research Phase**: Use MCP tools to research Ollama API
2. **Prototype**: Build minimal WebSocket echo server
3. **Integration**: Add Ollama streaming
4. **Audio Pipeline**: Implement VAD and STT
5. **Full System**: Complete the conversation loop

## Important Notes

- **No Docker**: This project uses native installation only
- **No flash-attn**: Use standard attention mechanisms
- **Development**: Use WSL for coding, Windows for running
- **Models**: Managed by Ollama, not downloaded directly