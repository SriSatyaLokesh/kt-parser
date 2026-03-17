# Agent Mode vs TDD Agent — When to Use Which

## Overview

The `/execute` prompt offers **two execution modes**:

1. **Agent Mode** — Delegate to Copilot's built-in agent for flexible, context-aware implementation
2. **TDD Agent** — Use structured TDD Implementer agent for disciplined, test-first development

Both modes plug into the same workflow and end with `/verify` for quality checks.

---

## Agent Mode (Recommended for Most Work)

### What It Is
Hands off implementation to **GitHub Copilot's agent mode** with a comprehensive context bundle (requirements, research, plan).

### When to Use
- ✅ Complex features with many moving parts
- ✅ Unfamiliar codebase areas (need exploration)
- ✅ Multi-file changes spanning different systems
- ✅ When you want conversational implementation ("what if we try X?")
- ✅ Time-sensitive work (faster for bulk coding)

### How It Works
1. `/execute work/ISSUE-042-name` → Choose "Agent Mode"
2. Prompt generates a context bundle with:
   - Requirements (Phase 1)
   - Research findings (Phase 2)
   - Implementation tasks (Phase 3)
   - Quality standards
   - File locations
3. You copy bundle → Open new chat → Paste → Let agent implement
4. Agent updates `result.md` Phase 4 as it works
5. When agent says "Ready for /verify", return to workflow
6. Run `/verify work/ISSUE-042-name`

### Pros
- 🚀 **Faster**: Agent mode is optimized for bulk implementation
- 🧠 **Smarter**: Full workspace context, can ask clarifying questions
- 🔄 **Flexible**: Can adapt mid-implementation if plan needs tweaking
- 💬 **Conversational**: Can discuss trade-offs during coding

### Cons
- ⚠️ **Less disciplined**: Doesn't enforce TDD cycle strictly
- ⚠️ **Manual commit**: You decide when to commit (more flexibility, less structure)
- ⚠️ **Context switch**: Requires opening new chat (intentional for clean context)

---

## TDD Agent (For Strict TDD Discipline)

### What It Is
Uses the **TDD Implementer agent** that enforces Red → Green → Refactor cycle for every task.

### When to Use
- ✅ Learning TDD (agent won't let you skip steps)
- ✅ High-risk code (financial, security, medical) where discipline is critical
- ✅ Team training (new devs learning test-first)
- ✅ Small, well-defined tasks (under 10 tasks)
- ✅ When you want automatic commit discipline

### How It Works
1. `/execute work/ISSUE-042-name` → Choose "TDD Agent"
2. Prompt invokes `@tdd work/ISSUE-042-name`
3. Agent reads plan, verifies branch, starts TDD cycle:
   - Write failing test
   - Run test (must fail)
   - Write minimal code to pass
   - Run test (must pass)
   - Refactor if needed
   - Commit automatically
4. After every 3 tasks → code review checkpoint
5. When all tasks done → hands off to `/verify`

### Pros
- 🎯 **Disciplined**: Enforces TDD rigorously
- ✅ **Automatic commits**: Logical units committed automatically
- 🔍 **Built-in review**: Code reviewed every 3 tasks
- 📝 **Progress tracking**: Updates result.md automatically

### Cons
- ⏱️ **Slower**: TDD cycle takes time (worth it for critical code)
- 🔒 **Rigid**: Can't deviate from plan mid-stream
- 📚 **Learning curve**: Requires understanding TDD principles

---

## Decision Matrix

| Scenario | Recommended Mode | Why |
|----------|------------------|-----|
| Complex feature (10+ tasks, multiple systems) | **Agent Mode** | Need flexibility and speed |
| Simple feature (3-5 tasks, single system) | **TDD Agent** | Discipline is manageable |
| Unfamiliar codebase | **Agent Mode** | Need exploration and questions |
| High-risk code (security, payments) | **TDD Agent** | Discipline prevents bugs |
| Tight deadline | **Agent Mode** | Faster implementation |
| Learning/training | **TDD Agent** | Enforces best practices |
| Research spike | **Agent Mode** | Exploration over discipline |
| Well-defined bug fix | **TDD Agent** | Test-first prevents regression |

---

## Hybrid Approach (Recommended)

You don't have to pick one forever! Use both:

### Pattern 1: Agent Mode → TDD Agent Cleanup
1. Use **Agent Mode** for bulk implementation (80% of work)
2. Switch to **TDD Agent** for critical edge cases
3. Run `/verify` when done

### Pattern 2: TDD Agent → Agent Mode Rescue
1. Start with **TDD Agent** for discipline
2. If you get stuck on a complex task, switch to **Agent Mode** for that task
3. Return to **TDD Agent** for remaining tasks

### Pattern 3: Phase-Based
- **Backend (critical)**: TDD Agent
- **Frontend (UI polish)**: Agent Mode
- **Tests**: TDD Agent
- **Docs**: Agent Mode

---

## Context Bundle Breakdown (Agent Mode)

When you choose Agent Mode, the prompt generates a bundle with:

### 1. Meta Information
```
Work Folder: work/ISSUE-042-name
Branch: fix/42-rate-limiting
GitHub Issue: #42
```

### 2. Requirements (from plan.md Phase 1)
- What we're building
- Why
- Requirements checklist
- Acceptance criteria

### 3. Research Context (from plan.md Phase 2)
- Existing patterns to follow
- Files to modify
- Dependencies
- Risks

### 4. Implementation Plan (from plan.md Phase 3)
- Task breakdown (backend, frontend, tests, docs)
- Architecture decisions
- Acceptance criteria

### 5. Instructions
- TDD guidance (write tests first)
- Quality standards
- Where to write code
- Where to document progress

### 6. Exit Criteria
- How to know you're done
- What to update before returning
- How to hand back to workflow

---

## Verification (Same for Both Modes)

After either mode completes, run:
```
/verify work/ISSUE-042-name
```

The Verify agent checks:
- ✅ All Phase 1 requirements met
- ✅ All tests passing
- ✅ No TypeScript/lint errors
- ✅ Docs updated
- ✅ Code quality standards met

If all green → Offers to create/merge PR automatically.

---

## Migration from Old Workflow

### Old (Single Mode)
```
/execute → TDD Agent only → /verify
```

### New (Dual Mode)
```
/execute → Choose:
           ├─ Agent Mode → Implement → Return → /verify
           └─ TDD Agent → Implement → /verify
```

**No breaking changes**: If you always choose "TDD Agent", workflow is identical to before.

---

## Tips for Success

### Agent Mode Tips
1. **Copy the full bundle** — don't summarize, agent needs complete context
2. **Use fresh chat** — prevents context pollution from other conversations
3. **Update result.md** — agent should fill Phase 4 as it works
4. **Commit frequently** — don't wait until everything is done
5. **Ask questions** — agent can explain trade-offs mid-implementation

### TDD Agent Tips
1. **Trust the discipline** — don't skip the Red step even if "obvious"
2. **Keep tasks small** — if a task feels too big, split it in planning phase
3. **Fix Critical reviews immediately** — don't accumulate tech debt
4. **Refactor freely** — but only in the Refactor step, never in Green
5. **Let it commit** — don't manually commit mid-task

---

## FAQ

**Q: Can I switch modes mid-implementation?**
A: Yes! Commit your work, then invoke the other mode. Both read the same plan.

**Q: Which mode is "better"?**
A: Agent Mode for speed, TDD Agent for discipline. Both are correct choices.

**Q: Does Agent Mode still do TDD?**
A: Yes, the context bundle instructs it to write tests first. But it's self-enforced, not agent-enforced.

**Q: Can I use Agent Mode without the context bundle?**
A: Not recommended. The bundle ensures agent has full context and quality standards.

**Q: What if Agent Mode goes off-plan?**
A: That's a feature! If the plan has issues, agent can adapt. Fix the plan later in result.md.

**Q: Which mode do experienced teams use?**
A: Fast teams use Agent Mode for implementation, TDD Agent for critical subsystems.

---

**Last Updated**: March 12, 2026  
**Status**: Production Ready  
**Related**: [execute.prompt.md](../.github/prompts/execute.prompt.md)
