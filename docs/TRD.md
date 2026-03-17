# TRD — KT-parser: Technical Reference Document

## 1. Technology Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Language | Python 3.11+ | Whisper and most ML tooling is native Python |
| CLI framework | [Typer](https://typer.tiangolo.com/) | Typed CLI with auto-generated help, built on Click |
| Progress output | [Rich](https://github.com/Textualize/rich) | Progress bars, tables, coloured stage output |
| Transcription | [openai-whisper](https://github.com/openai/whisper) | Best offline transcription, runs on CPU and CUDA |
| LLM inference | [Ollama](https://ollama.com) via HTTP | Local model server; decoupled from Python env |
| Ollama Python client | `ollama` (official Python SDK) | Handles streaming responses and model management |
| Video processing | `ffmpeg` + `ffmpeg-python` | Industry standard; `ffmpeg-python` is the Python wrapper |
| Config parsing | PyYAML + `pydantic` | YAML config parsed into validated Pydantic model |
| Checkpointing | JSON state file per run | Simple, human-readable, no external dependencies |
| Tokenisation | `tiktoken` | Accurate token counting for transcript chunking |
| Testing | `pytest` + `pytest-mock` | Standard Python testing |
| Packaging | `pyproject.toml` + `hatchling` | Modern Python packaging; produces a `kt-parser` CLI entry point |

---

## 2. Repository Layout

```
KT-parser/
├── PRD.md
├── TRD.md
├── SETUP.md
├── AGENTS.md
├── README.md
├── pyproject.toml
├── .kt-parser.yaml.example
├── src/
│   └── kt_parser/
│       ├── __init__.py
│       ├── cli.py              # Typer app and command definitions
│       ├── config.py           # Config file loading and Pydantic model
│       ├── pipeline.py         # Orchestrates stages, manages checkpoints
│       ├── stages/
│       │   ├── __init__.py
│       │   ├── extract_audio.py
│       │   ├── extract_frames.py
│       │   ├── transcribe.py
│       │   └── generate_docs.py
│       ├── templates/
│       │   ├── __init__.py
│       │   ├── context_hub.py
│       │   ├── generic.py
│       │   └── api_docs.py
│       └── utils/
│           ├── __init__.py
│           ├── ffmpeg.py       # ffprobe validation helpers
│           ├── hashing.py      # File hash for checkpoint comparison
│           └── tokens.py       # Token counting and chunking
├── tests/
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_pipeline.py
│   ├── test_stages/
│   │   ├── test_extract_audio.py
│   │   ├── test_extract_frames.py
│   │   ├── test_transcribe.py
│   │   └── test_generate_docs.py
│   └── fixtures/
│       └── sample_transcript.txt
└── .github/
    └── copilot-instructions.md
```

---

## 3. Component Design

### 3.1 CLI (`cli.py`)

Built with Typer. Three main commands, each mapped to a pipeline entry point:

```python
app = typer.Typer()

@app.command()
def process(video: Path, output: Path, template: str, ...): ...

@app.command()
def transcribe(video: Path, output: Path, ...): ...

@app.command()
def generate(transcript: Path, output: Path, template: str, ...): ...

config_app = typer.Typer()
app.add_typer(config_app, name="config")

@config_app.command("init")
def config_init(): ...

@config_app.command("show")
def config_show(): ...
```

### 3.2 Config (`config.py`)

Pydantic v2 model with nested sub-models. Resolution order:

1. Load `~/.kt-parser.yaml` if it exists
2. Overlay `./.kt-parser.yaml` if it exists
3. Overlay CLI-provided kwargs (non-None values only)

```python
class WhisperConfig(BaseModel):
    model: str = "large-v3"
    language: str = "en"
    device: str = "auto"

class OllamaConfig(BaseModel):
    model: str = "llama3.1"
    host: str = "http://localhost:11434"
    temperature: float = 0.3

class FFmpegConfig(BaseModel):
    keyframe_threshold: float = 0.4
    fixed_interval_seconds: int = 60

class OutputConfig(BaseModel):
    default_template: str = "context-hub"
    directory: Path = Path("./kt-output")

class LimitsConfig(BaseModel):
    max_file_size_gb: int = 10

class KTParserConfig(BaseModel):
    whisper: WhisperConfig = WhisperConfig()
    ollama: OllamaConfig = OllamaConfig()
    ffmpeg: FFmpegConfig = FFmpegConfig()
    output: OutputConfig = OutputConfig()
    limits: LimitsConfig = LimitsConfig()
```

### 3.3 Pipeline Orchestrator (`pipeline.py`)

Manages stage execution order and checkpointing.

**State file**: `{work_dir}/state.json`

```json
{
  "video_path": "/abs/path/to/session.mp4",
  "audio_hash": "sha256:abc123...",
  "transcript_hash": "sha256:def456...",
  "completed_stages": ["extract_audio", "extract_frames", "transcribe"],
  "started_at": "2026-03-17T10:00:00Z",
  "last_updated": "2026-03-17T10:45:00Z"
}
```

**Stage execution logic:**

```python
STAGES = [
    "extract_audio",
    "extract_frames",
    "transcribe",
    "generate_docs",
]

def run_pipeline(video_path, work_dir, config, template, no_resume):
    state = load_state(work_dir) if not no_resume else fresh_state(video_path)
    for stage_name in STAGES:
        if stage_name in state.completed_stages:
            print(f"[skip] {stage_name} — already completed")
            continue
        run_stage(stage_name, work_dir, config)
        state.completed_stages.append(stage_name)
        save_state(work_dir, state)
```

### 3.4 Stage: Audio Extraction (`stages/extract_audio.py`)

```python
def extract_audio(video_path: Path, work_dir: Path) -> Path:
    output = work_dir / "audio.mp3"
    ffmpeg.input(str(video_path))
          .output(str(output), ac=1, ar=16000, audio_bitrate="64k")
          .overwrite_output()
          .run(quiet=True)
    return output
```

### 3.5 Stage: Keyframe Extraction (`stages/extract_frames.py`)

Two-pass approach:

1. Scene-change pass: `select=gt(scene,{threshold}),scale=1280:-1`
2. Count frames. If < 5, run fixed-interval pass at `{interval}` seconds.
3. Write `frames-index.txt` mapping filename → timestamp.

Filenames derived from presentation timestamp (PTS):
```
frame_{MM}m{SS}s.jpg
```

### 3.6 Stage: Transcription (`stages/transcribe.py`)

```python
import whisper

def transcribe(audio_path: Path, work_dir: Path, cfg: WhisperConfig):
    model = whisper.load_model(cfg.model, device=resolve_device(cfg.device))
    result = model.transcribe(str(audio_path), language=cfg.language, verbose=True)
    
    (work_dir / "transcript.txt").write_text(result["text"])
    (work_dir / "transcript.json").write_text(json.dumps(result, indent=2))
    
    return result
```

`resolve_device`: returns `"cuda"` if `cfg.device == "auto"` and CUDA is available
via `torch.cuda.is_available()`, otherwise `"cpu"`.

### 3.7 Stage: Documentation Generation (`stages/generate_docs.py`)

**Chunking** (`utils/tokens.py`):

```python
def chunk_transcript(text: str, max_tokens: int = 3500, overlap: int = 200) -> list[str]:
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunks.append(enc.decode(tokens[start:end]))
        start += max_tokens - overlap
    return chunks
```

**LLM call** (per chunk):

```python
import ollama

def call_ollama(chunk: str, system_prompt: str, cfg: OllamaConfig) -> str:
    response = ollama.chat(
        model=cfg.model,
        options={"temperature": cfg.temperature},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chunk},
        ],
    )
    return response["message"]["content"]
```

**Post-processing**: After all chunks are processed per output file section,
a final LLM call merges/deduplicates the combined chunk outputs for coherence.

### 3.8 Templates (`templates/`)

Each template module exposes:

```python
SYSTEM_PROMPTS: dict[str, str]   # section_name → system prompt
OUTPUT_FILES: list[str]          # relative paths to produce
def build(chunk_outputs: dict[str, list[str]], work_dir: Path) -> None: ...
```

Template `context_hub.py` example section prompt:

```
You are a technical documentation writer for a microservices platform.
You are reading a transcript chunk from a knowledge transfer session.

Extract every microservice mentioned. For each service output:
- Service name (heading)
- Responsibilities (bullet list)
- Key API endpoints mentioned (method + path + one-line purpose)
- Interactions with other services

Output raw Markdown only. No preamble.
```

---

## 4. Work Directory Layout

```
./kt-output/<video-stem>/
├── state.json              # Checkpoint state
├── run.log                 # Full debug log
├── audio.mp3               # Extracted audio
├── frames/
│   ├── frame_00m30s.jpg
│   ├── frame_01m15s.jpg
│   └── frames-index.txt
├── transcript.txt          # Plain text transcript
├── transcript.json         # Whisper JSON with timestamps
├── raw-llm-output.md       # Unprocessed LLM output (debug)
└── docs/
    ├── session-summary.md
    ├── services-mentioned.md
    ├── key-concepts.md
    ├── detailed-notes.md
    └── open-questions.md
```

---

## 5. Dependency Management

### `pyproject.toml` (key sections)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "kt-parser"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "typer[all]>=0.12",
    "rich>=13",
    "openai-whisper>=20231117",
    "ollama>=0.2",
    "ffmpeg-python>=0.2",
    "pydantic>=2.0",
    "pyyaml>=6.0",
    "tiktoken>=0.6",
    "torch>=2.0",
]

[project.scripts]
kt-parser = "kt_parser.cli:app"

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-mock>=3", "ruff>=0.4"]
```

---

## 6. External Tool Dependencies

These must be installed separately (not Python packages):

| Tool | Version | Used For | Install |
|------|---------|----------|---------|
| FFmpeg | ≥ 6.0 | Audio extraction, keyframe extraction | See SETUP.md |
| Ollama | ≥ 0.2 | Local LLM server | See SETUP.md |
| CUDA Toolkit | ≥ 12.0 (optional) | GPU-accelerated Whisper | Optional, see SETUP.md |

---

## 7. Error Handling Strategy

| Scenario | Behaviour |
|----------|-----------|
| `ffmpeg`/`ffprobe` not on PATH | `SystemExit` with error message + install command |
| `ffprobe` reports no audio stream | `SystemExit` with human error |
| Ollama unreachable (connection refused) | `SystemExit` with "start Ollama: `ollama serve`" |
| Ollama model not found (404) | `SystemExit` with exact `ollama pull <model>` command |
| LLM returns empty / truncated response | Log warning, write partial output, continue |
| Whisper CUDA OOM | Catch `RuntimeError`, retry with CPU, log warning |
| Stage crashes mid-run | Exception propagates, state file already written up to last completed stage |
| Re-run after partial failure | Checkpoint detects completed stages, skips them |

---

## 8. Testing Strategy

| Test type | Coverage target | Notes |
|-----------|----------------|-------|
| Unit — config | All resolution logic | Mock filesystem |
| Unit — chunking | Edge cases: empty, single token, exact boundary | |
| Unit — pipeline | Stage skipping, state file read/write | Mock all stages |
| Unit — templates | Prompt construction, output file paths | |
| Integration — extract_audio | Requires ffmpeg on PATH | Marked `@pytest.mark.integration` |
| Integration — transcription | Requires `tiny` Whisper model | Marked `@pytest.mark.integration`, uses a 10s fixture audio file |
| Integration — ollama | Requires running Ollama instance | Marked `@pytest.mark.integration` |

Run unit tests only:
```bash
pytest -m "not integration"
```

---

## 9. Coding Conventions

- All public functions fully type-hinted
- Pydantic models for all config and state structures — no raw dicts passed around
- No global mutable state
- All file I/O goes through `pathlib.Path` — no `os.path` string manipulation
- FFmpeg calls always use `ffmpeg-python` wrapper — no `subprocess` shell string
- Logging: use Python `logging` module; Rich handler for console; file handler for `run.log`
- Linting: `ruff` with default rules
- Max line length: 100

---

## 10. Copilot Instructions File

The project includes `.github/copilot-instructions.md` which tells GitHub Copilot:
- The project structure and module purposes
- Which external tools are required and their versions
- Coding conventions (type hints, Pydantic, pathlib)
- That chunking/checkpointing logic is the critical path — handle carefully
- Template system extension pattern
