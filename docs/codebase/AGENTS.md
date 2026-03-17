# AGENTS.md — KT-parser

> **For AI coding agents (GitHub Copilot, Claude Code, Cursor, etc.)**
> Read this fully before writing any code in this project.

---

## What this project is

KT-parser is a Python CLI that converts knowledge transfer session video recordings
into structured Markdown documentation. It runs fully offline using local models.

**Pipeline**: `video file → FFmpeg (audio + keyframes) → Whisper (transcription) → Ollama (docs)`

---

## Project documents — read these first

| File | Read it for |
|------|-------------|
| `PRD.md` | What the tool must do, user stories, all functional requirements |
| `TRD.md` | Tech stack, module design, data structures, coding conventions |
| `SETUP.md` | External dependencies (FFmpeg, Ollama), install steps |

**Do not guess** at requirements. If something is not in these files, ask the user.

---

## Repository layout

```
src/kt_parser/
├── cli.py              # Typer CLI entry point — commands: process, transcribe, generate, config
├── config.py           # Config loading + Pydantic models
├── pipeline.py         # Stage orchestration + checkpoint logic
├── stages/
│   ├── extract_audio.py
│   ├── extract_frames.py
│   ├── transcribe.py
│   └── generate_docs.py
├── templates/
│   ├── context_hub.py  # Default template for context hub output
│   ├── generic.py
│   └── api_docs.py
└── utils/
    ├── ffmpeg.py       # ffprobe validation helpers
    ├── hashing.py      # SHA-256 file hashing for checkpoints
    └── tokens.py       # tiktoken-based chunking
```

---

## Critical implementation rules

### 1. Checkpointing is essential — do not break it
Every stage must check `state.completed_stages` before running.
Every stage must append its name to `state.completed_stages` and call `save_state()`
immediately after it completes — before the next stage starts.
The state file is `{work_dir}/state.json`.

### 2. Never use subprocess shell strings for FFmpeg
Always use `ffmpeg-python` wrapper. Never do `subprocess.run("ffmpeg ...")`.
Safe pattern:
```python
ffmpeg.input(str(video_path)).output(...).overwrite_output().run(quiet=True)
```

### 3. Config is always a Pydantic model — never a raw dict
Any function that needs config takes a typed Pydantic model (e.g. `WhisperConfig`,
`OllamaConfig`). Never pass `dict` around. See `config.py`.

### 4. All file paths are `pathlib.Path` — never strings
No `os.path.join`. No string concatenation for paths. Every path is a `Path` object.

### 5. CLI flags override config, not the other way around
The resolution order is: built-in defaults → `~/.kt-parser.yaml` → `./.kt-parser.yaml` → CLI flags.
Implement this in `config.py:load_config()`. The CLI should pass only non-None
values to the config merger.

### 6. Transcript chunking uses token count, not character count
Use `tiktoken` with `cl100k_base` encoding. Chunk at 3500 tokens with 200-token overlap.
See `utils/tokens.py`.

### 7. LLM calls go through `ollama` Python SDK — never raw HTTP
```python
import ollama
response = ollama.chat(model=..., messages=[...], options={...})
```

### 8. Ollama connection errors must produce actionable messages
If Ollama is unreachable, print: `Ollama is not running. Start it with: ollama serve`
If model is missing (404), print: `Model not found. Run: ollama pull <model-name>`
Then call `raise SystemExit(1)`.

### 9. Rich for all user-facing output
Use `rich.console.Console` and `rich.progress.Progress` — no bare `print()` except
in tests. Stage names should appear as `[bold cyan]Stage: extract_audio[/]`.

---

## Template system

Each template module exports:
```python
SECTIONS: list[str]                    # section names, order matters
SYSTEM_PROMPTS: dict[str, str]         # section → LLM system prompt
OUTPUT_FILES: dict[str, str]           # section → relative output file path

def build(chunk_outputs: dict[str, list[str]], docs_dir: Path) -> None:
    """Merge chunk outputs and write final files to docs_dir."""
```

To add a new template: create a new module in `templates/`, follow the above
interface, and register it in `templates/__init__.py:TEMPLATES` dict.

---

## Work directory structure (runtime)

```
./kt-output/<video-stem>/
├── state.json              # MUST exist after first stage completes
├── run.log
├── audio.mp3
├── frames/
│   ├── frame_00m30s.jpg
│   └── frames-index.txt
├── transcript.txt
├── transcript.json         # Full Whisper output — source of truth for transcription
├── raw-llm-output.md       # Debug: raw LLM output before template processing
└── docs/                   # Final output — users care about this folder only
    ├── session-summary.md
    ├── services-mentioned.md
    ├── key-concepts.md
    ├── detailed-notes.md
    └── open-questions.md
```

---

## What to implement first (suggested build order)

1. `pyproject.toml` — packaging, dependencies, entry point
2. `config.py` — Pydantic models and `load_config()` 
3. `utils/hashing.py` and `utils/tokens.py` — no external dependencies, easy to test
4. `pipeline.py` — state file, `load_state()`, `save_state()`, `run_pipeline()` skeleton
5. `stages/extract_audio.py` — FFmpeg call, checkpoint check
6. `stages/extract_frames.py` — FFmpeg scene filter, fixed-interval fallback
7. `stages/transcribe.py` — Whisper call, output files
8. `stages/generate_docs.py` — chunking + Ollama calls
9. `templates/context_hub.py` — default template
10. `templates/generic.py` and `templates/api_docs.py`
11. `cli.py` — Typer commands wiring everything together
12. `tests/` — unit tests, then integration tests

---

## Running the tool during development

```bash
# Install in editable mode
pip install -e ".[dev]"

# Run CLI
kt-parser --help
kt-parser process ./test-video.mp4 --dry-run

# Run tests
pytest -m "not integration"   # fast, no external tools needed
pytest -m integration          # needs ffmpeg, Whisper tiny model, Ollama
```

---

## Things NOT to do

- Do not add a web server, REST API, or GUI — this is a CLI tool only
- Do not add cloud API calls (OpenAI, Azure, AWS) — everything runs locally
- Do not add auto git commit / PR creation
- Do not add speaker diarization — out of scope for v1
- Do not add multilingual support — hard-coded to English for v1
- Do not use `os.path` — use `pathlib.Path`
- Do not call FFmpeg via `subprocess` shell string — use `ffmpeg-python`
- Do not pass config as a raw dict to any function
