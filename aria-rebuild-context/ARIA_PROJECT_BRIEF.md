# Aria Project Brief

## Overview
Aria is a local AI voice assistant designed for real-time, natural voice conversations. The system runs entirely on the user's hardware, ensuring privacy and low latency.

## Core Requirements

### Functional Requirements
- **Real-time voice conversations**: Sub-second response times
- **Streaming responses**: Start speaking while LLM is still generating
- **Natural interaction**: No wake words, automatic speech detection
- **Voice commands**: Support for "clear history", "skip response"
- **Multiple personas**: Configurable AI personalities

### Technical Requirements
- **Platform**: Windows 11 with NVIDIA GPU
- **Hardware**: RTX 4080 Super (16GB VRAM)
- **Models**: Qwen2.5-14B via Ollama
- **Latency target**: < 500ms to first spoken word
- **Audio quality**: 16kHz minimum, 48kHz preferred

## Key Design Decisions

### 1. Ollama as LLM Backend
- **Rationale**: Simplified model management, better resource control
- **Model**: `ollama pull qwen2.5:14b`
- **No embedded inference**: Application is a client, not an engine
- **Benefits**: Faster startup, easier updates, shared model cache

### 2. Modern Async Architecture
- **Backend**: FastAPI with WebSockets
- **Frontend**: TBD (Web or Native)
- **Communication**: Real-time bidirectional streaming
- **Error handling**: Proper boundaries and recovery

### 3. Development Environment
- **Coding**: WSL2 with Claude Code
- **Execution**: Native Windows for GPU performance
- **Package management**: uv (Astral)
- **No Docker**: Direct installation only

## Success Criteria
1. Natural conversation flow without awkward pauses
2. System responds before user finishes speaking (when appropriate)
3. Clear audio with minimal artifacts
4. Graceful handling of errors and edge cases
5. Easy to install and configure

## Out of Scope
- Multi-user support (single user only)
- Cloud connectivity (fully local)
- Mobile clients (desktop only)
- Model training/fine-tuning
- Docker containerization