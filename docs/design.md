# Aria Design Documentation

## Overview
Aria is a local AI voice assistant that provides real-time voice conversation capabilities. This document outlines the architectural design decisions and patterns used in the system.

## Current Architecture

### Component-Based Design
The system is built using a modular component architecture where each component handles a specific responsibility:

1. **Audio Input (mic.py)** - Captures audio from microphone
2. **Voice Activity Detection (vad.py)** - Detects speech using Silero VAD
3. **Speech-to-Text (stt.py)** - Transcribes speech using Whisper
4. **Language Model (llm.py)** - Generates responses using LLM
5. **Text-to-Speech (tts.py)** - Synthesizes speech using Kokoro/Coqui
6. **Audio Output (ap.py)** - Plays generated audio
7. **User Interface (ui.py)** - Displays visual feedback and text

### Communication Pattern
Components communicate through:
- **Asyncio queues** for data flow
- **Direct method calls** for control flow
- **Callback patterns** for real-time updates

### Deployment Modes

#### Standalone Mode
- All components run in a single process
- Direct communication between components
- Simpler deployment, suitable for single-user scenarios

#### Client-Server Mode
- **Server**: Runs compute-intensive components (STT, LLM, TTS)
- **Client**: Handles UI and audio I/O
- **Network Protocol**: JSON messages with compressed audio data
- Supports multiple users with isolated contexts

## Ollama Migration Design

### Architectural Shift
Moving from embedded inference to client-server architecture:

**Before (llama-cpp-python)**:
- Application loads models into memory
- Direct inference calls
- Full control over model parameters

**After (Ollama)**:
- Application connects to Ollama daemon
- API-based inference
- Ollama manages models and resources

### Key Design Decisions

#### 1. Response Format Adaptation
Create a unified response handler that:
- Accepts Ollama's streaming format
- Converts to expected internal format
- Maintains compatibility with existing components

#### 2. Configuration Simplification
- Remove model file management
- Simplify to just model names
- Let Ollama handle quantization and optimization

#### 3. Error Handling Enhancement
- Add connection failure detection
- Implement retry logic
- Provide user-friendly error messages

#### 4. Streaming Preservation
- Maintain real-time streaming for TTS
- Preserve code block detection
- Keep text processing pipeline intact

### Component Interaction Changes

**Current Flow**:
```
User Speech → Mic → VAD → STT → LLM (embedded) → TTS → Speaker
```

**Ollama Flow**:
```
User Speech → Mic → VAD → STT → Ollama API → TTS → Speaker
```

### Benefits of New Design
1. **Faster Startup**: No model loading required
2. **Better Resource Management**: Ollama handles GPU allocation
3. **Easier Updates**: Model updates through Ollama
4. **Simplified Deployment**: No GGUF file distribution

### Challenges to Address
1. **Network Latency**: API calls vs embedded inference
2. **Error Recovery**: Network failures need handling
3. **Model Consistency**: Ensuring same model behavior
4. **Configuration Migration**: Helping users transition

## Future Considerations

### Extensibility
- Plugin system for new components
- Support for multiple LLM backends
- Custom TTS/STT providers

### Scalability
- Better multi-user support
- Load balancing for server mode
- Caching for common responses

### User Experience
- Better error feedback in UI
- Progress indicators for long operations
- Voice command customization