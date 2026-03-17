# Architecture

**Analysis Date:** [YYYY-MM-DD]

## Pattern Overview

**Overall:** Monolithic CLI pipeline (video → audio/frames → transcript → docs)

**Key Characteristics:**

- Fully offline, local-first, checkpointed, modular stages
- User-driven template selection, Markdown output

## Layers

CLI (Typer) → Pipeline Orchestrator → Stages (audio, frames, transcribe, docs) → Templates

**[Layer Name]:**
- Purpose: [What this layer does]
- Contains: [Types of code]
- Depends on: [What it uses]
- Used by: [What uses it]

## Data Flow

[Describe the typical request/execution lifecycle]

**[Flow Name]:**
1. [Entry point]
2. [Processing step]
3. [Output]

**State Management:**
- [How state is handled]

## Key Abstractions

[Core concepts/patterns used throughout the codebase]

**[Abstraction Name]:**
- Purpose: [What it represents]
- Examples: [Concrete examples]
- Pattern: [Pattern used]

## Entry Points

**[Entry Point]:**
- Location: [Path]
- Triggers: [Invocation]
- Responsibilities: [What it does]

## Error Handling

**Strategy:** [Overall strategy]

**Patterns:**
- [Pattern 1]

## Cross-Cutting Concerns

**Logging:**
- [Approach]

**Validation:**
- [Approach]

**Authentication:**
- [Approach]

---
*Architecture analysis: [date]*
*Update when major patterns change*
