# SETUP.md — KT-parser Installation & Setup

## Prerequisites

You need three things installed before the Python setup:

1. **Python 3.11+**
2. **FFmpeg 6.0+**
3. **Ollama**

GPU acceleration is optional but recommended for large videos.

---

## Step 1 — Install FFmpeg

### Windows
```powershell
# With winget (Windows 11 / updated Windows 10)
winget install Gyan.FFmpeg

# Or with Chocolatey
choco install ffmpeg

# Or manually: download from https://ffmpeg.org/download.html
# Extract and add the bin/ folder to your PATH
```

### macOS
```bash
brew install ffmpeg
```

### Ubuntu / Debian
```bash
sudo apt update && sudo apt install -y ffmpeg
```

**Verify:**
```bash
ffmpeg -version   # should show version 6.x or higher
ffprobe -version
```

---

## Step 2 — Install Ollama

### Windows
Download and run the installer from: https://ollama.com/download/windows

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Start the Ollama server** (must be running before you use kt-parser):
```bash
ollama serve
```

**Pull the default model** (one-time, ~4 GB download):
```bash
ollama pull llama3.1
```

If you want a smaller/faster model (less accurate):
```bash
ollama pull mistral      # ~4 GB, faster
ollama pull phi3         # ~2 GB, lighter
```

**Verify:**
```bash
ollama list   # should show the model(s) you pulled
```

---

## Step 3 — Install Python Dependencies

```bash
# Clone or copy the KT-parser project
cd KT-parser

# Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Install kt-parser and all dependencies
pip install -e ".[dev]"
```

**Verify:**
```bash
kt-parser --version
kt-parser --help
```

---

## Step 4 — (Optional) GPU Acceleration

If you have an NVIDIA GPU, Whisper will use it automatically and run 5–10x faster.

**Requirements:**
- NVIDIA GPU with CUDA Compute Capability ≥ 3.5
- CUDA Toolkit 12.x: https://developer.nvidia.com/cuda-downloads

**Install PyTorch with CUDA support** (replace the CPU-only torch from the base install):
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

**Verify CUDA is available:**
```bash
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

When CUDA is available, kt-parser will use it automatically (`device: auto` in config).

---

## Step 5 — (Optional) Create a Config File

```bash
kt-parser config init
```

This writes `.kt-parser.yaml` to your current directory. Edit it to set your
preferred Whisper model, Ollama model, and output directory.

```yaml
whisper:
  model: large-v3    # or medium for faster runs
  language: en
  device: auto

ollama:
  model: llama3.1
  host: http://localhost:11434
  temperature: 0.3

output:
  default_template: context-hub
  directory: ./kt-output
```

---

## Quick-Start: Process Your First Video

Make sure Ollama is running (`ollama serve` in a separate terminal), then:

```bash
kt-parser process ./my-kt-session.mp4
```

Output will be at `./kt-output/my-kt-session/docs/`.

---

## Troubleshooting

### `ffmpeg: command not found` or `'ffmpeg' is not recognized`
FFmpeg is not on your PATH. Re-run Step 1 and restart your terminal.

### `Ollama connection refused`
Ollama is not running. Start it: `ollama serve`

### `model "llama3.1" not found`
Pull the model: `ollama pull llama3.1`

### Whisper is very slow (CPU only)
Without a GPU, `large-v3` on a 1-hour video can take 60–90 minutes on CPU.
Switch to `medium` or `small` in your config for faster (slightly less accurate)
results: `whisper: model: medium`

### `No audio track found`
Your video file has no audio stream. Check with: `ffprobe -v error -select_streams a your-file.mp4`

### Out of memory during Whisper (GPU)
kt-parser will automatically fall back to CPU and log a warning.
Alternatively, use a smaller model: `--whisper-model medium`

---

## Verifying the Full Pipeline (Smoke Test)

```bash
# Run unit tests (no external tools needed)
pytest -m "not integration"

# Run integration tests (requires ffmpeg, Whisper tiny model, and Ollama)
pytest -m integration
```
