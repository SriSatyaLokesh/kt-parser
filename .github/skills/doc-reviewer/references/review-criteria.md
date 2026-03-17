# Doc Reviewer — Full Review Criteria

Use this rubric for every review. Check every section. Do not skip any.

---

## 1. Beginner-Friendliness Checklist

### Assumed Knowledge
- [ ] Does the doc assume tools are installed without explaining how to install them?
- [ ] Does it use acronyms or jargon without defining them on first use? (e.g., OData, ORM, JWT, TDD)
- [ ] Does it assume the reader knows why they're doing a step, not just what to do?
- [ ] Are there terms that only make sense to someone in the same team/company?

### Step Completeness
- [ ] Are there gaps between steps where the reader has to figure something out themselves?
- [ ] Does every command show the expected output or confirm what success looks like?
- [ ] If something could go wrong at a step, is there troubleshooting info?
- [ ] Is the "happy path" clear — can a beginner start and finish without detours?

### Clarity
- [ ] Does every paragraph have a clear purpose? (If you can delete a paragraph without losing meaning, it should be deleted.)
- [ ] Are sentences longer than 25 words? (Flag them — they usually hide two ideas.)
- [ ] Is passive voice overused? ("it should be noted" vs "note that")
- [ ] Are there walls of text with no visual breaks (headers, bullets, code blocks)?

### Code and Commands
- [ ] Is every command in a fenced code block with the correct language tag?
- [ ] Are placeholder values clearly marked? (e.g., `your-project-name` vs undocumented variable)
- [ ] Do code examples actually work, or are they illustrative-only? (If illustrative, is that stated?)
- [ ] Are there partial examples where the reader has to guess what's missing?

---

## 2. Markdown Lint Checks

### Structure
- [ ] Is there exactly one `# H1` heading? (Multiple H1s = lint error)
- [ ] Do heading levels increment correctly? (H1 → H2 → H3, never H1 → H3)
- [ ] Are headings consistently capitalised? (Pick Title Case or Sentence case, not both)
- [ ] Are blank lines present before and after every heading, list, and code block?

### Links
- [ ] Do all relative links use the correct relative path from this file's location?
- [ ] Are any links to `docs/learn/` that should now be `learn/` (stale after folder move)?
- [ ] Are external links working and pointing to the right resource?
- [ ] Are any links just `[text]()` with empty hrefs?

### Frontmatter
- [ ] Does the file have frontmatter only if it is an agent, prompt, or skill file?
- [ ] Are frontmatter YAML keys valid and correctly indented?

### Lists and Tables
- [ ] Are list items consistently punctuated? (All end with period, or none — not mixed)
- [ ] Do tables have a header row and alignment dashes on every column?
- [ ] Are there any tables with broken column count (mismatched `|` count per row)?

### Code Blocks
- [ ] Do all code blocks have a language tag? (` ```bash `, ` ```typescript `, ` ```json `, etc.)
- [ ] Are inline code items using single backticks, not double?

---

## 3. Documentation Quality Checks

### Purpose and Audience
- [ ] Is the purpose of the document clear in the first 3 lines?
- [ ] Is the target audience stated (or obvious from context)?
- [ ] Does the doc match its Diátaxis type? (Tutorial = learning step-by-step; How-to = solving a specific problem; Reference = lookup; Explanation = conceptual)

### Completeness
- [ ] Does the doc cover the full scope of its topic, or are sections obviously incomplete?
- [ ] Are there `TODO`, `TBD`, or `FIXME` comments left in the doc?
- [ ] Are all example file paths consistent with the actual project structure?

### References and Further Reading
- [ ] Are external tools and concepts linked to their official documentation on first mention?
- [ ] For every major decision or pattern mentioned, is there a reference or rationale?
- [ ] Are there topics where a beginner would naturally want to go deeper, but no link is provided?

Common missing references to check for:
- GitHub Copilot → `https://code.visualstudio.com/docs/copilot/overview`
- OData queries → Microsoft Dynamics docs
- Playwright → `https://playwright.dev/docs/intro`
- JWT → RFC 7519 or jwt.io
- Diátaxis framework → `https://diataxis.fr/`
- awesome-copilot → `https://github.com/github/awesome-copilot`

---

## 4. Scoring Guide

| Score | Meaning |
|-------|---------|
| 9–10 | Exceptional — a non-technical reader could follow it |
| 7–8 | Good — a developer can follow it, minor gaps |
| 5–6 | Acceptable — works for experienced devs, fails for beginners |
| 3–4 | Needs significant rework — multiple beginner-blocking issues |
| 1–2 | Needs full rewrite — fundamental structure or content problems |

**A doc cannot score above 7 if:**
- Any command in the doc doesn't have a code block
- Any link is broken or stale
- Assumed knowledge isn't defined on first use
- A beginner has to Google something just to reach the next step
