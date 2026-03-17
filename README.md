# KT-parser

Convert knowledge transfer session recordings into structured Markdown documentation.
Runs fully offline. No cloud APIs.

```
video file  →  FFmpeg  →  Whisper  →  Ollama  →  Markdown docs
```

---

## Quick Start

```bash
# 1. Install external tools (one-time)
#    See SETUP.md for full instructions

# 2. Install kt-parser
pip install -e .

# 3. Start Ollama (in a separate terminal)
ollama serve

# 4. Process a video
kt-parser process ./my-kt-session.mp4
```

Output: `./kt-output/my-kt-session/docs/`

---

## Commands

```
kt-parser process <video>        Full pipeline: audio → frames → transcript → docs
kt-parser transcribe <video>     Transcription only
kt-parser generate <transcript>  Doc generation from existing transcript
kt-parser config init            Create .kt-parser.yaml config file
kt-parser config show            Show resolved config
```

---

## Output (context-hub template)

| File | Contents |
|------|---------|
| `docs/session-summary.md` | Services discussed, TL;DR |
| `docs/services-mentioned.md` | Service responsibilities, endpoints, interactions |
| `docs/key-concepts.md` | Domain rules, architectural decisions |
| `docs/detailed-notes.md` | Full technical detail with timestamps |
| `docs/open-questions.md` | Unanswered questions, TODOs |

Templates: `context-hub` (default), `generic`, `api-docs`

---

## Requirements

- Python 3.11+
- FFmpeg 6.0+ (`ffmpeg` and `ffprobe` on PATH)
- Ollama running locally (`ollama serve`)
- One Ollama model pulled (`ollama pull llama3.1`)

See [SETUP.md](SETUP.md) for full installation instructions including optional GPU setup.

---

## Configuration

```yaml
# .kt-parser.yaml
whisper:
  model: large-v3    # tiny | base | small | medium | large-v3
  device: auto       # auto | cpu | cuda

ollama:
  model: llama3.1
  temperature: 0.3

output:
  default_template: context-hub
```

---

## Project Documents

| File | Purpose |
|------|---------|
| [PRD.md](PRD.md) | What it does — requirements, user stories |
| [TRD.md](TRD.md) | How it's built — architecture, module design |
| [SETUP.md](SETUP.md) | Installation and troubleshooting |
| [AGENTS.md](AGENTS.md) | Instructions for AI coding agents |
