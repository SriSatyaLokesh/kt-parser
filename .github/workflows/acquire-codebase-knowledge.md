---
description: Structured procedure for mapping codebase knowledge into templates
---

# Workflow: Acquire Codebase Knowledge

Follow these steps every time you need to map or update the codebase documentation. This workflow MUST be executed using the `acquire-codebase-knowledge` skill.

## Phase 1: Preparation (Docs & Intent)
1. **Locate Intent Documents**:
   - Search for `PRD`, `TRD`, `roadmap`, `specs`, or `design` folders.
   - Example command: `fd -e md -i "prd|trd|spec|design"`
2. **Review README**:
   - Read the main `README.md` for high-level description and setup.
3. **Capture Goal**:
   - Briefly summarize in your thought trace: "What is this project intended to be?"

## Phase 2: Structural Audit (Reality)
1. **Tree Analysis**:
   - Run `tree` or `list_dir` on top-level and `src/` (if exists).
   - Identify entry points (`index.ts`, `main.go`, `app.py`).
2. **Stack Verification**:
   - Read build/package files (`package.json`, `go.mod`, `pom.xml`).
   - Identify primary frameworks and critical dependencies.

## Phase 3: Detailed Template Population
Execute the `acquire-codebase-knowledge` skill and follow the inquiry checkpoints for each file in `docs/codebase/`.

### 1. Populate `stack.md`
- **Investigate**: Check `package.json` or equivalent for direct dependencies vs dev dependencies.
- **Confirm with User**: "I see both `axios` and `fetch` being used; which is the preferred standard?"

### 2. Populate `structure.md`
- **Investigate**: List all top-level directories and their recursive child count.
- **Confirm with User**: "There is a `scripts/` folder with 50+ files. Is this for CI/CD or internal tooling?"

### 3. Populate `architecture.md`
- **Investigate**: Trace a single data flow (e.g., from a route handler to a database service).
- **Confirm with User**: "The code shows a semi-hexagonal pattern, but some services call the DB directly. Is this the intended design?"

### 4. Populate `conventions.md`
- **Investigate**: Check for `.editorconfig`, `.eslintrc`, or `lint-staged`.
- **Confirm with User**: "The codebase uses both `PascalCase` and `camelCase` for some file names. Which should I document as the standard?"

### 5. Populate `integrations.md`
- **Investigate**: Search for API keys, base URLs, or connection strings (factually, don't expose secrets).
- **Confirm with User**: "I see references to Stripe and Twilio. Are these the only primary external integrations?"

### 6. Populate `testing.md`
- **Investigate**: Check `scripts` for a `test` command. Count the number of test files.
- **Confirm with User**: "I see many unit tests but no integration tests. Is there a separate repo for E2E, or should I mark them as missing?"

### 7. Populate `concerns.md`
- **Investigate**: Run a grep for `TODO`, `FIXME`, `HACK`. Check `git log` for filenames with frequent changes (churn).
- **Confirm with User**: "The `AuthService` has high churn and several 'HACK' comments. Should I list this as a fragile area?"

## Phase 4: Interactive Sync
1. **Present Draft**:
   - Provide a concise summary of what you've mapped.
2. **Ask clarifying questions**:
   - Present the "Confirm with User" points gathered in Phase 3.
   - "The PRD mentions X, but I don't see code for it yet. Should I mark it as missing in CONCERNS.md?"

## Phase 5: Finalization
1. Update `docs/codebase/` with finalized content.
2. Commit changes with a descriptive message.
