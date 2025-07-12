# Aria Implementation Documentation

## Ollama Integration Implementation Guide

### Prerequisites
- Ollama installed and running (`ollama serve`)
- Python 3.10+ environment
- Required models pulled: `ollama pull qwen2.5:14b`

### Implementation Steps

#### 1. Dependencies Update

**Remove from `pyproject.toml`**:
```toml
# Remove these
"llama-cpp-python==0.3.4",
"huggingface-hub==0.28.1",
```

**Add to `pyproject.toml`**:
```toml
"ollama==0.4.4",  # or latest version
```

#### 2. Response Formatter Implementation

Create `components/response_formatter.py`:

```python
class ResponseFormatter:
    """Unified response formatting for different LLM backends"""
    
    def __init__(self):
        self.code_block_pattern = "```"
        self.sentence_endings = [".", "!", "?", ":", "..", "..."]
    
    def format_ollama_stream(self, chunk):
        """Convert Ollama format to expected format"""
        # Ollama: chunk['message']['content']
        # Expected: {'choices': [{'delta': {'content': text}}]}
        
        if 'message' in chunk and 'content' in chunk['message']:
            return {
                'choices': [{
                    'delta': {
                        'content': chunk['message']['content']
                    }
                }]
            }
        return None
    
    def detect_code_block(self, text, current_state):
        """Detect code block boundaries"""
        # Implementation for code block detection
        pass
    
    def extract_tts_text(self, text):
        """Extract text suitable for TTS"""
        # Remove code blocks, emojis, etc.
        pass
```

#### 3. Ollama LLM Component

Replace `components/llm.py`:

```python
import ollama
from .response_formatter import ResponseFormatter
from .utils import remove_emojis, remove_nonverbal_cues

class Llm:
    def __init__(self, params=None):
        self.params = params or {}
        self.model_name = self.params.get("model_name", "qwen2.5:14b")
        self.ollama_host = self.params.get("ollama_host", "http://localhost:11434")
        self.streaming_output = self.params.get("streaming_output", True)
        self.system_message = self.params.get("system_message", "You are a helpful assistant")
        
        # Initialize Ollama client
        self.client = ollama.Client(host=self.ollama_host)
        self.formatter = ResponseFormatter()
        
        # Initialize conversation
        self.messages = [{"role": "system", "content": self.system_message}]
        
        # Verify connection
        try:
            self.client.list()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Ollama at {self.ollama_host}: {e}")
    
    def get_answer(self, ui, ap, tts, data):
        self.messages.append({"role": "user", "content": data})
        
        try:
            if self.streaming_output:
                # Streaming implementation
                stream = self.client.chat(
                    model=self.model_name,
                    messages=self.messages,
                    stream=True
                )
                
                llm_output = ""
                tts_text_buffer = []
                # ... (streaming logic with formatter)
                
            else:
                # Non-streaming implementation
                response = self.client.chat(
                    model=self.model_name,
                    messages=self.messages,
                    stream=False
                )
                llm_output = response['message']['content']
                
        except Exception as e:
            ui.add_message("system", f"Error: {str(e)}", new_entry=True)
            return ""
        
        self.messages.append({"role": "assistant", "content": llm_output})
        return llm_output
```

#### 4. Configuration Updates

Update `configs/default.json`:

```json
{
  "Llm": {
    "params": {
      "model_name": "qwen2.5:14b",
      "ollama_host": "http://localhost:11434",
      "streaming_output": true,
      "system_message": "You are Mia...",
      "verbose": false
    }
  }
}
```

#### 5. Error Handling Enhancement

Add connection monitoring and retry logic:

```python
class OllamaConnectionManager:
    def __init__(self, host, max_retries=3):
        self.host = host
        self.max_retries = max_retries
        self.client = None
        self.connected = False
    
    def connect(self):
        """Establish connection with retry logic"""
        for attempt in range(self.max_retries):
            try:
                self.client = ollama.Client(host=self.host)
                self.client.list()  # Test connection
                self.connected = True
                return True
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise ConnectionError(f"Failed to connect after {self.max_retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
        return False
    
    def ensure_connected(self):
        """Ensure connection is alive"""
        if not self.connected:
            self.connect()
```

#### 6. Migration Path for Users

Create migration script:

```python
def migrate_config(old_config_path, new_config_path):
    """Migrate from llama-cpp config to Ollama config"""
    with open(old_config_path, 'r') as f:
        old_config = json.load(f)
    
    # Map old model names to Ollama equivalents
    model_mapping = {
        "Qwen2.5-14B-Instruct-1M-abliterated.Q6_K.gguf": "qwen2.5:14b",
        # Add more mappings
    }
    
    # Update LLM params
    if "Llm" in old_config:
        old_llm = old_config["Llm"]["params"]
        new_llm = {
            "model_name": model_mapping.get(old_llm.get("model_file", ""), "qwen2.5:14b"),
            "ollama_host": "http://localhost:11434",
            "streaming_output": old_llm.get("streaming_output", True),
            "system_message": old_llm.get("system_message", ""),
            "verbose": old_llm.get("verbose", False)
        }
        old_config["Llm"]["params"] = new_llm
    
    # Save migrated config
    with open(new_config_path, 'w') as f:
        json.dump(old_config, f, indent=2)
```

### Testing Strategy

#### Unit Tests
```python
def test_ollama_connection():
    """Test Ollama connection"""
    client = ollama.Client()
    assert client.list() is not None

def test_response_formatting():
    """Test response format conversion"""
    formatter = ResponseFormatter()
    ollama_chunk = {"message": {"content": "Hello"}}
    formatted = formatter.format_ollama_stream(ollama_chunk)
    assert formatted["choices"][0]["delta"]["content"] == "Hello"

def test_streaming_response():
    """Test streaming response handling"""
    # Mock Ollama streaming response
    # Verify TTS buffer handling
    # Check code block detection
```

#### Integration Tests
1. **Startup Test**: Verify app starts with Ollama
2. **Conversation Test**: Full conversation flow
3. **Error Recovery**: Disconnect and reconnect Ollama
4. **Performance Test**: Measure response latency

### Performance Optimization

#### Caching Strategy
```python
class ResponseCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
    
    def get_cached_response(self, prompt_hash):
        return self.cache.get(prompt_hash)
    
    def cache_response(self, prompt_hash, response):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest = min(self.cache.items(), key=lambda x: x[1]['timestamp'])
            del self.cache[oldest[0]]
        self.cache[prompt_hash] = {
            'response': response,
            'timestamp': time.time()
        }
```

#### Connection Pooling
- Reuse Ollama client connections
- Implement connection timeout handling
- Add health check endpoint

### Deployment Considerations

#### Docker Removal
Since we're removing Docker support:
1. Document native installation steps
2. Provide platform-specific guides
3. Create install scripts for common platforms

#### Ollama Setup Guide
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull required model
ollama pull qwen2.5:14b

# Verify installation
ollama list
```

### Troubleshooting Guide

Common issues and solutions:

1. **Connection Refused**
   - Ensure Ollama is running: `systemctl status ollama`
   - Check firewall settings
   - Verify port 11434 is accessible

2. **Model Not Found**
   - Pull the model: `ollama pull model-name`
   - Check available models: `ollama list`

3. **Slow Response**
   - Check GPU utilization: `nvidia-smi`
   - Verify model is loaded in GPU
   - Consider using smaller quantization

4. **Memory Issues**
   - Monitor Ollama memory usage
   - Configure Ollama memory limits
   - Use smaller models if needed