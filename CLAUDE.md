# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Aria is a local AI voice assistant that provides real-time voice conversation capabilities using VAD, STT, LLM, and TTS technologies. It supports both standalone and client-server deployment modes.

## Development Environment
- **Code editing**: WSL (Windows Subsystem for Linux) with Claude Code
- **Running Aria**: Native Windows for optimal GPU performance
- **Package manager**: uv by Astral (replaces pip)
- **Git remote**: https://github.com/neuralnetwork/aria
- **Default LLM**: Qwen2.5-14B-Instruct-1M-abliterated (Q6_K GGUF, ~12.2GB)

## Common Development Commands

### Running the Application
```bash
# Using uv (recommended)
uv run python main.py

# Server mode (handles STT/LLM/TTS)
uv run python server.py

# Client mode (UI and audio I/O only)
uv run python client.py

# With custom config
uv run python main.py --config configs/myconfig.json

# Note: Run these commands on Windows directly, not in WSL
```

### Docker Commands
```bash
# Build server image
docker buildx build --tag ghcr.io/lef-fan/aria-server:latest .

# Run server container
docker run --net=host --gpus all --name aria-server -it ghcr.io/lef-fan/aria-server:latest
```

### Installation
```bash
# Using uv (recommended - single mode for all deployments)
uv sync

# Legacy pip method (if needed)
pip install -r requirements.txt
pip install --no-build-isolation flash-attn==2.7.4.post1
```

## Architecture Overview

### Component Pipeline
1. **Audio Input** → `mic.py` captures audio from microphone
2. **Voice Detection** → `vad.py` detects speech using Silero VAD
3. **Speech Recognition** → `stt.py` transcribes using Whisper
4. **Language Model** → `llm.py` generates response using Qwen2.5-14B (GGUF format)
5. **Speech Synthesis** → `tts.py` converts to speech using Kokoro/Coqui
6. **Audio Output** → `ap.py` plays the generated audio

### Deployment Modes
- **Standalone**: All components run locally via `main.py`
- **Client-Server**: 
  - Server (`server.py`): Runs compute-intensive STT/LLM/TTS
  - Client (`client.py`): Handles UI and audio I/O
  - Network (`nw.py`): Manages communication with audio compression

### Key Design Patterns
- **Async Architecture**: Uses asyncio for concurrent processing
- **Queue-based Communication**: Components communicate via asyncio queues
- **Streaming**: Supports streaming LLM responses and audio playback
- **Modular Components**: Each component is independent and replaceable

## Configuration System
- Main config: `configs/default.json`
- Component-specific settings under respective keys (Mic, Vad, Stt, Llm, Tts, Ap, Ui, Nw)
- Critical settings:
  - `Nw.params.client_target_ip`: Server IP for client mode
  - `Llm.params.model_name/model_file`: LLM model selection
  - `Stt.params.device`: CUDA device for Whisper
  - `Tts.params.tts_type`: "kokoro" or "coqui"

## Development Guidelines
- Components use `start()` and `stop()` methods for lifecycle management
- Error handling uses logging module (not print statements)
- Audio data flows as numpy arrays through queues
- Network protocol uses JSON messages with binary audio data
- UI built with tkinter, runs in separate thread from async components

## Voice Commands
- "delete messages" / "clear history" - Clears conversation context
- "skip" - Interrupts current response

## Testing Considerations
- No formal test suite exists currently
- Manual testing required for:
  - Audio device compatibility
  - Model loading and inference
  - Client-server connectivity
  - Voice command recognition

## Important Notes
- First run downloads several GB of model files (Qwen2.5 ~12.2GB + Whisper + TTS models)
- Requires CUDA-capable GPU for optimal performance (16GB+ VRAM recommended)
- Default credentials in config should be changed for production
- Audio device configuration may need adjustment per system
- Flash-attn requires native Windows environment to build properly (not WSL)
- Models are stored in HuggingFace cache: `~/.cache/huggingface/hub/`