# Aria Features Documentation

## Core Features

### Real-Time Voice Conversation
- **Continuous listening** with voice activity detection
- **Low-latency response** through streaming architecture
- **Natural conversation flow** without wake words
- **Interrupt handling** to stop responses mid-stream

### Multi-Model Support

#### Speech Recognition (STT)
- **Whisper Large V3 Turbo** for accurate transcription
- GPU acceleration with CUDA
- Automatic language detection
- Real-time transcription with minimal delay

#### Language Models (LLM)
- **Current**: GGUF models via llama-cpp-python
  - Default: Qwen2.5-14B-Instruct (Q6_K quantization)
  - Support for various quantization levels
  - Custom model loading from local paths
- **Future**: Ollama integration
  - Access to Ollama's model library
  - Automatic model management
  - Easy model switching

#### Text-to-Speech (TTS)
- **Kokoro TTS** (default)
  - High-quality voices
  - Adjustable speech speed
  - Multiple voice options
- **Coqui TTS** (alternative)
  - Voice cloning support
  - XTTS v2 model
  - Custom voice training

### Voice Commands
- **"delete messages" / "clear history"** - Reset conversation context
- **"skip"** - Interrupt current response
- **Extensible** - Easy to add new commands

### Visual Feedback

#### Loading States
- Animated loading spinner during initialization
- Transition animations between states
- Clear ready indicator

#### Speaking Visualization
- Audio waveform visualization while listening
- Animated bars while AI is speaking
- Visual feedback for muted microphone

#### Text Display
- Color-coded messages (user vs AI)
- Code syntax highlighting
- Scrollable conversation history
- Copy functionality for messages

### Deployment Flexibility

#### Standalone Mode
- Single executable for personal use
- All processing done locally
- No network dependencies

#### Client-Server Mode
- Separate UI from compute resources
- Multi-user support with isolated contexts
- Network audio compression
- Authentication system

### Audio Processing

#### Smart Audio Handling
- Automatic sample rate conversion
- Stereo to mono conversion
- Buffer management for smooth playback
- Sound effects for state transitions

#### Voice Activity Detection
- Silero VAD for accurate speech detection
- Configurable silence thresholds
- Automatic recording start/stop
- Background noise handling

### Configuration System

#### Flexible Configuration
- JSON-based configuration files
- Per-component settings
- Multiple persona support
- Easy customization

#### Persona System
- Customizable AI personalities
- System message configuration
- Multiple persona files
- Quick switching between personas

## Advanced Features

### Streaming Architecture
- **Token-by-token streaming** from LLM
- **Sentence-level TTS** processing
- **Parallel processing** of speech synthesis
- **Low-latency pipeline** for natural conversation

### Text Processing
- **Emoji removal** for TTS compatibility
- **Code block detection** and skipping
- **Nonverbal cue removal** (e.g., *laughs*)
- **Smart punctuation handling**

### Multi-User Support (Server Mode)
- **User isolation** - Separate contexts per user
- **Authentication** - Username/password system
- **Concurrent sessions** - Multiple users simultaneously
- **Resource sharing** - Efficient GPU utilization

### Error Handling
- **Graceful degradation** for component failures
- **Automatic recovery** attempts
- **User notification** for critical errors
- **Logging system** for debugging

## Planned Features (Ollama Migration)

### Improved Model Management
- **No manual downloads** - Ollama handles everything
- **Model versioning** - Pin specific versions
- **Easy updates** - Simple model pulling
- **Model sharing** - Use system-wide models

### Enhanced Performance
- **Faster startup** - No model loading
- **Better memory usage** - Ollama optimization
- **Dynamic scaling** - Automatic resource management
- **Model swapping** - Quick model changes

### Better User Experience
- **Connection status** - Ollama health checks
- **Model availability** - List available models
- **Download progress** - When pulling new models
- **Error recovery** - Automatic reconnection

## Feature Comparison

| Feature | Current (llama-cpp) | Future (Ollama) |
|---------|-------------------|-----------------|
| Startup Time | 2-5 minutes | <10 seconds |
| Model Management | Manual GGUF files | Automatic via Ollama |
| Memory Usage | Full model in RAM | Shared with other apps |
| Model Switching | Requires restart | Dynamic switching |
| Updates | Manual download | `ollama pull` |
| Resource Control | Direct (GPU layers) | Ollama managed |