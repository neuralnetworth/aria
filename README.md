# Aria
Meet Aria. A local and uncensored AI entity.

![Aria](https://github.com/lef-fan/aria/blob/main/assets/aria.png?raw=true)

https://github.com/lef-fan/aria/assets/23457676/d90b3f04-6d56-43a7-86ab-674fc558abe2

https://github.com/user-attachments/assets/362cdf14-e5f5-4855-aa5f-dc834fbca5ad

## Installation

### Prerequisites
- Python 3.10 or higher
- NVIDIA GPU with CUDA support (required for flash-attn)
- System dependencies:
  - **Ubuntu/Debian**: `sudo apt install python3.12-dev portaudio19-dev libopus-dev`
  - **Arch Linux**: `sudo pacman -S python portaudio opus`
  - **macOS**: `brew install portaudio opus`

### Method 1 - Using uv (Recommended)
[uv](https://github.com/astral-sh/uv) is a fast Python package manager that provides better dependency resolution and faster installations.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repo
git clone https://github.com/neuralnetwork/aria.git
cd aria

# Install dependencies
uv sync
```

### Method 2 - Using pip (Traditional)
```bash
# Install from pyproject.toml
pip install -e .
# Note: flash-attn requires CUDA Toolkit and may need manual installation
```


(Tested on Arch Linux + NVIDIA GPUs with Python 3.12)

### Syncing Across Multiple Computers
When using uv, you can easily sync your environment across multiple computers:

```bash
# On your first computer (after installation)
git add uv.lock
git commit -m "Add uv.lock for dependency sync"
git push

# On your other computers
git pull
uv sync
```

The `uv.lock` file ensures all your computers use exactly the same package versions.

## Usage
First run will take a while to download all the required models.\
You may edit the default config for your device or use case (change model, specify devices, etc...)\
If you have the resources, strongly recommended to use bigger model and/or bigger quant method.

### Default Model
Aria now uses **Qwen2.5-14B-Instruct-1M-abliterated** (Q6_K quantization) by default:
- Model size: ~12.2 GB
- Recommended VRAM: 16GB+ (works well on RTX 4080 Super)
- Downloads automatically on first run to HuggingFace cache
- Abliterated version (uncensored) for unrestricted responses

### Windows Users with WSL
If you're developing with WSL but running Aria on Windows:
1. Edit code in WSL using your preferred tools
2. Run Aria directly on Windows for best GPU performance
3. Use Windows terminal: `uv run python main.py`
4. Flash-attn builds properly on native Windows with CUDA

### Non server/client mode:

```
python main.py
```
### Server and Client Mode

#### server machine:
```
python server.py 
```

#### client machine (edit client target ip in the config):
```
python client.py
```

## Upcoming Features
* Android client
* Raspberry Pi client
* Ollama support (currently uses GGUF format directly)

## Documentation
Work in progress...

## Contributions
🌟 We'd love your contribution! Please submit your changes via pull request to join in the fun! 🚀

## Disclaimer
Aria is a powerful AI entity designed for local use. Users are advised to exercise caution and responsibility when interacting with Aria, as its capabilities may have unintended consequences if used improperly or without careful consideration.

By engaging with Aria, you understand and agree that the suggestions and responses provided are for informational purposes only, and should be used with caution and discretion.

We cannot be held responsible for any actions, decisions, or outcomes resulting from the use of Aria. We explicitly disclaim liability for any direct, indirect, incidental, consequential, or punitive damages arising from reliance on Aria's responses.

We encourage users to exercise discernment, judgment, and thorough consideration when utilizing information from Aria. Your use of this service constitutes acceptance of these disclaimers and limitations.

Should you have any doubts regarding the accuracy or suitability of Aria's responses, we advise consulting with qualified professionals or experts in the relevant field.

## Acknowledgments

- [silero-vad](https://github.com/snakers4/silero-vad)
- [transformers](https://github.com/huggingface/transformers)
- [whisper](https://github.com/openai/whisper)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [TTS](https://github.com/coqui-ai/TTS)
- [TTS fork](https://github.com/idiap/coqui-ai-TTS)
- [kokoro](https://github.com/hexgrad/kokoro)
- [opuslib](https://github.com/orion-labs/opuslib)
- [TheBloke](https://huggingface.co/TheBloke)
- [Bartowski](https://huggingface.co/bartowski)
- [mradermacher](https://huggingface.co/mradermacher)
- [mlabonne](https://huggingface.co/mlabonne)

## License Information

### ❗ Important Note:
While this project is licensed under GNU AGPLv3, the usage of some of the components it depends on might not and they will be listed below:

#### TTS MODEL
- **License**: Open-source only for non-commercial projects.
- **Commercial Use**: Requires a paid plan.
- **Details**: [Coqui Public Model License 1.0.0](https://coqui.ai/cpml)

#### opuslib
- **License**: BSD-3-Clause license
- **Details**: [opuslib license](https://github.com/orion-labs/opuslib?tab=BSD-3-Clause-1-ov-file#readme)

#### Llama
- **License**: llama3.1
- **Details**: [llama license](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/LICENSE)
