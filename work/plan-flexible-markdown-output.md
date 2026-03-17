# Plan: Flexible Markdown Output

## Problem
KT-parser must produce structured Markdown documentation from KT session videos, supporting multiple templates and user-driven sectioning. Output should not be limited to context hub format.

## Approach
- Modular template system (context-hub, generic, api-docs, extensible)
- User selects template and sectioning via CLI/config
- Pipeline stages checkpointed for resumability
- Output always Markdown, structure defined by template

## Todos
- [ ] Design template interface (sections, prompts, output files)
- [ ] Implement template selection logic in pipeline
- [ ] Support user-driven sectioning (CLI/config)
- [ ] Update pipeline to use selected template
- [ ] Document template extension pattern

## Notes
- Reference PRD.md, TRD.md, AGENTS.md for requirements and conventions
- Ensure all output is Markdown, no other formats
- Allow easy addition of new templates
