# Ollama Migration Progress & Knowledge Gaps

## Migration Overview
- **Goal**: Replace llama-cpp-python with Ollama (no GGUF files)
- **Model Management**: Use `ollama pull` instead of HuggingFace downloads
- **Approach**: Full refactor (not wrapper) - This is an ARCHITECTURE change, not a library swap

## Critical Realization: Paradigm Shift
### Current Architecture
- Application IS the inference engine
- Downloads and loads model files into memory
- Direct control over GPU layers, memory, context

### Ollama Architecture  
- Application is a CLIENT to an inference server
- Ollama daemon manages all models
- No direct model file access

## Key Architecture Changes
### Before (llama-cpp-python)
1. Download GGUF from HuggingFace (~12GB)
2. Load model into application memory
3. Direct inference calls
4. Application manages GPU memory

### After (Ollama)
1. User runs: `ollama pull qwen2.5:14b`
2. Application connects to Ollama API
3. API calls to Ollama daemon
4. Ollama manages everything

## Completed Analysis

### 1. Code Structure Understanding
- **llm.py**: 118 lines, handles streaming, TTS integration, code block detection
- **llm_server.py**: 115 lines, adds multi-user context management
- **Key logic**: Lines 46-111 handle streaming with TTS buffering

### 2. Response Format Differences
```python
# Current (llama-cpp-python)
out["choices"][0]["delta"]["content"]

# Ollama
chunk["message"]["content"]
```

### 3. Critical Features to Preserve
- Streaming responses with real-time TTS
- Code block detection (```) and skipping for TTS
- Text processing (emoji removal, nonverbal cue removal)
- Per-user context in server mode
- Voice commands: "clear history", "skip"

## Critical Knowledge Gaps

### 1. Model Management Philosophy
**Current config uses:**
```json
"model_name": "mradermacher/Qwen2.5-14B-Instruct-1M-abliterated-GGUF",
"model_file": "Qwen2.5-14B-Instruct-1M-abliterated.Q6_K.gguf"
```

**Questions:**
- How does Ollama name this model? 
- Can we specify quantization (Q6_K vs Q8_0)?
- How to ensure consistent model versions?
- Where does Ollama store models?

### 2. Configuration Parameter Mapping
**Current parameters that may be obsolete:**
- `num_gpu_layers: -1` - Does Ollama expose this?
- `context_length: 8192` - Server setting or per-request?
- `chat_format: "qwen2"` - Auto-detected by Ollama?
- `custom_path` - Completely obsolete
- `model_file` - No longer needed

**Need to research:** Which parameters have Ollama equivalents?

### 3. Performance & Resource Control
**Current:** Application explicitly controls GPU layers
**Ollama:** Server manages everything

**Unknowns:**
- How to optimize for RTX 4080 Super (16GB)?
- Can we control memory usage?
- How does Ollama handle concurrent users?
- Auto-unloading of models?

### 4. System Message & Persona Management
**Current:** System message in config, passed with each request
**Ollama:** Is this part of Modelfile? API parameter? Both?

**Impact:** Might need new approach for Mia/Ava personas

### 5. Advanced Streaming Details
**Beyond basic format:**
- Token probabilities available?
- Custom stop sequences?
- Handling partial responses?
- Error recovery mid-stream?

### 6. Hidden Dependencies
- Does removing huggingface-hub break other components?
- Are there hardcoded paths expecting model files?
- Native deployment considerations?
- How does this affect the client-server network protocol?

## Research Priority (Need context7 MCP)

### 1. Ollama Model Ecosystem
- [ ] Exact model naming for Qwen2.5 14B
- [ ] How to specify quantization levels
- [ ] Model version pinning strategies
- [ ] Custom/fine-tuned model support

### 2. Ollama Server Configuration  
- [ ] Context length configuration
- [ ] Memory management options
- [ ] Multi-user handling patterns
- [ ] Performance tuning for RTX 4080

### 3. Complete API Documentation
- [ ] Full request/response schemas
- [ ] All available parameters
- [ ] Streaming edge cases
- [ ] Error handling patterns

### 4. Migration Best Practices
- [ ] Examples of llama-cpp → Ollama migrations
- [ ] Common pitfalls and solutions
- [ ] Performance comparisons
- [ ] Native installation patterns

## Current Issues

### Application Hanging at Startup (NOT RESOLVED)
- **Symptom**: UI shows loading spinner indefinitely
- **Console output**: Shows successful model downloads, then "No module named pip" error
- **Never reaches**: "Ready..." message that should print after initialization
- **Root cause**: Application crashes during component initialization
- **The error**: "C:\Users\chinm\cline\aria\.venv\Scripts\python.exe: No module named pip"
  - This is a FATAL error causing the app to exit
  - UI keeps spinning because main loop never starts
  - Something in the initialization is trying to invoke pip at runtime

### Architectural Issue Revealed
- **False assumption**: "UI is architecturally clean and decoupled"
- **Reality**: UI hangs when backend crashes, no error handling
- **Problem**: No crash recovery or error display in UI
- **Impact**: Users see infinite spinner with no feedback

## Next Steps After Restart

1. **Use context7 MCP to research:**
   - Ollama model naming conventions
   - Complete API parameter documentation
   - TTS integration patterns
   - Performance optimization guides

2. **Create documentation:**
   - `docs/design.md` - Architecture decisions
   - `docs/features.md` - Feature specifications  
   - `docs/implementation.md` - Technical details

3. **Begin implementation:**
   - Start with response_formatter.py
   - Then migrate llm.py
   - Finally update llm_server.py

## Key Insight
This is not just replacing a library - it's changing from an embedded inference engine to a client-server architecture. This fundamental shift affects every assumption about model management, resource control, and deployment strategy.