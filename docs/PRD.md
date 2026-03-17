# PRD — KT-parser: Knowledge Transfer Video → Documentation Pipeline

## 1. Problem Statement

Engineering teams capture knowledge transfer (KT) sessions as screen recordings
(1–1.5 hours each). This knowledge stays locked in video format — inaccessible to
new joiners, AI coding assistants, and automated documentation systems.

Extracting it manually is slow, inconsistent, and rarely happens in practice.

**KT-parser** is a fully self-hosted, one-command CLI that converts KT video
recordings into structured Markdown documentation ready to drop into any context hub.

No cloud APIs. No subscriptions. Run once, get docs.

---

## 2. Goals

| # | Goal |
|---|------|
| G-1 | Process a 1–1.5 hour video end-to-end with a single command |
| G-2 | No cloud APIs — fully offline after initial one-time model downloads |
| G-3 | Resumable — crash at any stage, re-run continues from last checkpoint |
| G-4 | Output structured Markdown matching the context hub folder conventions |
| G-5 | Easy to hand to anyone: install instructions fit on one page |

---

## 3. Non-Goals (v1)

- GUI or web interface
- Multi-language support (English only for v1)
- Real-time / streaming transcription
- Automatic git commit or PR creation
- Speaker diarization (who said what)
- Cloud deployment or SaaS offering
- Video editing or annotation

---

## 4. Users

**Primary**: A tech lead or senior engineer who has KT video recordings and needs
them converted to documentation once (or a handful of times). They are comfortable
running CLI tools and installing Python packages.

**Secondary**: A DevOps or tooling engineer setting this up for a team as a
shared utility.

---

## 5. User Stories

### Core Pipeline

- As a user, I run `kt-parser process ./session.mp4` and receive a folder of
  structured Markdown documents.
- As a user, I point to a folder and all `.mp4` / `.mov` / `.mkv` files within
  it are processed in sequence.
- As a user, I see real-time progress bars and stage labels because each stage
  takes several minutes.
- As a user, a summary line at the end tells me how many files were written and
  where they are.

### Resumability

- As a user, if the pipeline crashes mid-way, re-running the same command
  resumes from the last completed stage without re-doing expensive work.
- As a user, I can force a full re-run from scratch with `--no-resume`.

### Configuration

- As a user, I configure Whisper model size, Ollama model, and output template
  in a YAML config file so I don't repeat flags every run.
- As a user, any CLI flag overrides the config file for that one run.
- As a user, `kt-parser config init` creates a pre-filled config file in my
  current directory.
- As a user, `kt-parser config show` prints the fully resolved config so I can
  verify what will run.

### Selective Execution

- As a user, I run only transcription (`kt-parser transcribe`) if I only want
  the transcript without generating docs yet.
- As a user, I run only doc generation (`kt-parser generate`) from an existing
  transcript when I want to re-generate docs with a different template or model.

### Output Templates

- As a user, I choose a `context-hub` template that produces files matching the
  `business-portal-ctx` hub conventions.
- As a user, I choose a `generic` template for general-purpose session notes.
- As a user, I choose an `api-docs` template when the KT session was specifically
  about API usage.

---

## 6. Functional Requirements

### FR-1 — Video Ingestion

- Accept file formats: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`
- Validate the file with `ffprobe` before starting any stage; exit with a
  human-readable error if the file is unreadable or has no audio/video streams.
- Accept a folder as input: discover and process all supported video files within
  it, printing a count before starting.
- Reject files larger than a configurable max size (default: 10 GB) with a clear
  warning (not a crash).

### FR-2 — Audio Extraction

- Extract the audio track with FFmpeg → `{work_dir}/audio.mp3`
- Normalise to mono, 16 kHz (Whisper's native format) to reduce file size and
  improve transcription speed.
- If no audio track is found, exit with error: `No audio track found in <file>`.
- Skip this step if `{work_dir}/audio.mp3` already exists (checkpoint).

### FR-3 — Keyframe Extraction

- Extract frames at scene changes using FFmpeg `select=gt(scene,{threshold})`
  filter. Default threshold: `0.4`.
- Fallback: if fewer than 5 frames are detected, supplement with fixed-interval
  frames every 60 seconds.
- Name frames with human-readable timestamps: `frame_00m30s.jpg`, `frame_01m15s.jpg`.
- Output directory: `{work_dir}/frames/`
- Include a `frames-index.txt` listing each frame filename and its timestamp.
- Skip this step if `{work_dir}/frames/` already exists and contains files
  (checkpoint).

### FR-4 — Transcription

- Use locally running OpenAI Whisper (Python package `openai-whisper`).
- Configurable model: `tiny | base | small | medium | large-v3` (default: `large-v3`).
- Configurable device: `auto | cpu | cuda` (default: `auto` — use CUDA if
  available, else CPU).
- Outputs:
  - `{work_dir}/transcript.txt` — plain text, one paragraph per Whisper segment
  - `{work_dir}/transcript.json` — full Whisper output with per-segment timestamps
- Checkpoint: skip if `transcript.json` already exists and the `audio.mp3` hash
  stored in `{work_dir}/state.json` matches the current file.

### FR-5 — Documentation Generation

- Use locally running Ollama (default model: `llama3.1`).
- Configurable Ollama host URL (default: `http://localhost:11434`).
- Configurable temperature (default: `0.3` for factual, consistent output).
- Split transcript into chunks of ≤ 3500 tokens with 200-token overlap to stay
  within context windows.
- Send each chunk with a system prompt appropriate to the chosen template.
- Merge chunk outputs into a coherent final document (LLM-assisted merge for
  the summary; simple concatenation for detail sections).
- Save raw unmerged LLM output to `{work_dir}/raw-llm-output.md` for debugging.
- Checkpoint: skip if `raw-llm-output.md` already exists for the same transcript
  hash.

### FR-6 — Output Templates

#### `context-hub` (default)

Produces files matching the structure expected by a microservices context hub:

| File | Content |
|------|---------|
| `docs/session-summary.md` | Date, participants (if mentioned), services discussed, TL;DR |
| `docs/services-mentioned.md` | Each service: name, responsibilities, key endpoints, interactions |
| `docs/key-concepts.md` | Domain rules, business logic, architectural decisions mentioned |
| `docs/detailed-notes.md` | Full technical detail, verbatim-important quotes with timestamps |
| `docs/open-questions.md` | Questions raised but not answered; TODOs mentioned |

#### `generic`

| File | Content |
|------|---------|
| `docs/summary.md` | High-level summary |
| `docs/detailed-notes.md` | Full notes |
| `docs/action-items.md` | Action items extracted |
| `docs/open-questions.md` | Open questions |

#### `api-docs`

| File | Content |
|------|---------|
| `docs/endpoints.md` | HTTP method, path, purpose, request/response shape |
| `docs/auth-notes.md` | Auth patterns mentioned |
| `docs/integration-notes.md` | Integration gotchas and notes |
| `docs/open-questions.md` | Open questions |

### FR-7 — CLI Interface

```
kt-parser process <video-or-folder> [options]
kt-parser transcribe <video> [options]
kt-parser generate <transcript-file> [options]
kt-parser config init
kt-parser config show
kt-parser --version
kt-parser --help
```

**Options on `process` and `transcribe`:**

| Flag | Default | Description |
|------|---------|-------------|
| `--output, -o` | `./kt-output/<video-stem>/` | Output directory |
| `--template, -t` | `context-hub` | Output template |
| `--whisper-model` | config value | Whisper model size |
| `--ollama-model` | config value | Ollama model name |
| `--scene-threshold` | `0.4` | FFmpeg scene detection threshold |
| `--no-resume` | false | Force full re-run |
| `--dry-run` | false | Print execution plan only |
| `--verbose, -v` | false | Debug-level output |

### FR-8 — Configuration File

Location resolution order:
1. `./.kt-parser.yaml` (current directory)
2. `~/.kt-parser.yaml` (user home)
3. Built-in defaults

CLI flags always override config file values.

```yaml
whisper:
  model: large-v3        # tiny | base | small | medium | large-v3
  language: en
  device: auto           # auto | cpu | cuda

ollama:
  model: llama3.1
  host: http://localhost:11434
  temperature: 0.3

ffmpeg:
  keyframe_threshold: 0.4
  fixed_interval_seconds: 60

output:
  default_template: context-hub
  directory: ./kt-output

limits:
  max_file_size_gb: 10
```

### FR-9 — Progress and Logging

- Each pipeline stage prints its name and a progress indicator before starting.
- Transcription and LLM stages show progress within the stage (Whisper has
  native progress output; LLM shows chunk N of M).
- All output is also written to `{work_dir}/run.log` at DEBUG level regardless
  of `--verbose`.
- On completion: print a summary table listing every output file, its size, and
  its path.

### FR-10 — Error Handling

- `ffprobe` / `ffmpeg` not found → clear install instruction in the error.
- `whisper` not importable → clear install instruction.
- Ollama not reachable → clear instruction to start Ollama.
- Ollama model not pulled → print the exact `ollama pull <model>` command to run.
- Partial output from LLM (truncated context) → warn and continue, do not crash.

---

## 7. Out-of-Scope for v1 (Future)

- Web UI for browsing generated docs
- Automatic placement into a context hub folder structure
- Batch progress dashboard
- GitHub Action integration
- Speaker identification
- Multilingual transcription
