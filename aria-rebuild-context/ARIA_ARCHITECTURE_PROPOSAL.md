# Aria Architecture Proposal

## System Overview
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend    │────▶│   Ollama    │
│  (UI/Audio) │◀────│  (FastAPI)   │◀────│   Server    │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                    ┌───────┴────────┐
                    │                │
                ┌───▼───┐       ┌───▼───┐
                │  STT  │       │  TTS  │
                └───────┘       └───────┘
```

## Component Architecture

### 1. Backend (FastAPI)
**Purpose**: Central orchestrator for all AI services

**Endpoints**:
- `WebSocket /ws` - Main conversation channel
- `POST /config` - Update configuration
- `GET /health` - Service health check
- `GET /models` - List available Ollama models

**Core Services**:
```python
- OllamaService: Manages LLM interactions
- WhisperService: Speech-to-text processing
- TTSService: Text-to-speech generation
- AudioProcessor: VAD and audio utilities
- ConversationManager: Context and history
```

### 2. Ollama Integration
**Model**: qwen2.5:14b (or user-configurable)

**API Usage**:
```python
# Streaming completion
POST /api/generate
{
    "model": "qwen2.5:14b",
    "prompt": "...",
    "stream": true,
    "options": {
        "temperature": 0.7,
        "top_k": 40
    }
}
```

**Key Features**:
- Streaming responses for low latency
- Context window management
- Automatic model loading/unloading

### 3. Speech-to-Text (Whisper)
**Library**: openai-whisper or faster-whisper

**Configuration**:
```python
- Model size: base, small, or medium
- Device: cuda
- Language: auto-detect or fixed
- VAD: Silero-VAD for speech detection
```

### 4. Text-to-Speech
**Options**:
1. **Coqui-TTS**: Open source, good quality
2. **Kokoro**: Lightweight, fast
3. **Edge-TTS**: Microsoft's free TTS

**Requirements**:
- Streaming synthesis
- Low latency (< 200ms)
- Natural sounding voices

### 5. Frontend Options

#### Option A: Web Application
**Tech Stack**: React/Vue + Web Audio API
```
- WebSocket client for real-time comms
- MediaRecorder for audio capture
- Web Audio for playback
- Modern, responsive UI
```

#### Option B: Native Python
**Tech Stack**: Tkinter/PyQt + PyAudio
```
- Direct audio device access
- Lower latency potential
- System tray integration
- Native look and feel
```

## Communication Protocol

### WebSocket Messages
```typescript
// Client -> Server
interface ClientMessage {
    type: "audio" | "text" | "command"
    data: ArrayBuffer | string
    timestamp: number
}

// Server -> Client  
interface ServerMessage {
    type: "transcript" | "response" | "audio" | "status"
    data: string | ArrayBuffer
    metadata?: {
        model?: string
        processingTime?: number
        confidence?: number
    }
}
```

### Audio Streaming
- **Format**: 16-bit PCM, 16kHz mono
- **Chunk size**: 512 samples (32ms)
- **Compression**: Optional Opus for bandwidth

## Data Flow

### Conversation Flow
1. **Audio Input** → Frontend captures audio chunks
2. **VAD** → Detect speech start/end
3. **STT** → Convert speech to text
4. **LLM** → Generate response (streaming)
5. **TTS** → Convert text to speech (streaming)
6. **Audio Output** → Play synthesized speech

### Streaming Pipeline
```
User speaks: ─────────────▶ 
              VAD detects
                   STT processes ──▶ "Hello, how are you?"
                                         LLM streams ──▶ "I'm doing well..."
                                                           TTS streams ──▶ 🔊
                                                                            User hears
```

## State Management

### Backend State
- Conversation history (in-memory)
- Active connections (WebSocket sessions)
- Model state (loaded/unloaded)
- Audio buffers (temporary)

### Frontend State
- UI state (recording/playing/idle)
- Audio visualizations
- Settings/preferences
- Error states

## Error Handling

### Connection Failures
- Automatic reconnection with exponential backoff
- Offline mode with graceful degradation
- Clear error messages to user

### Processing Errors
- Fallback responses for LLM failures
- Alternative TTS if primary fails
- Audio device switching

## Performance Targets
- **First word latency**: < 500ms
- **End-to-end latency**: < 2 seconds
- **Audio quality**: 48kHz/16-bit
- **Concurrent users**: 1 (local only)