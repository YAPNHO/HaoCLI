---
name: code-review
description: "Code review guidelines: review Python files for correctness, clarity, performance, and security, then output a structured review."
---

# Code Review Skill

## Purpose
Review Python source code files in the workspace for correctness, clarity, performance, and security. Output a structured review report.

## Review Checklist

### 1. Correctness
- [ ] Does the code produce the expected output?
- [ ] Are edge cases handled (empty input, boundary values, exceptions)?
- [ ] Are there any logic bugs, off-by-one errors, or race conditions?
- [ ] Do function signatures match their call sites?

### 2. Clarity & Maintainability
- [ ] Are variable/function names descriptive and consistent?
- [ ] Is there appropriate documentation (docstrings, comments for non-obvious logic)?
- [ ] Is the code organized logically (functions, classes, modules)?
- [ ] Are there any overly complex or nested structures that should be simplified?
- [ ] Are magic numbers or hardcoded values extracted as named constants?

### 3. Performance
- [ ] Are there any obvious performance bottlenecks (nested loops, repeated I/O)?
- [ ] Are appropriate data structures used (e.g., set for membership test, dict for lookup)?
- [ ] Is there unnecessary computation that could be cached or lazily evaluated?

### 4. Security
- [ ] Are user inputs validated and sanitized?
- [ ] Is there any risk of injection attacks (shell injection, SQL injection)?
- [ ] File path traversal: are paths resolved safely (no user-controlled paths without checks)?
- [ ] Are secrets, API keys, or tokens hardcoded?

### 5. Style & Standards
- [ ] Does the code follow PEP 8 conventions?
- [ ] Are imports properly organized (stdlib, third-party, local)?
- [ ] Is the code free of commented-out or dead code?

## Output Format
After reviewing, produce a report in the following structure:

```
## Code Review: <filename>

### Summary
<1-2 sentence overall assessment>

### Issues Found
1. **[Severity: High/Medium/Low]** <title>
   - File: <path>
   - Line: <line number(s)>
   - Description: <what and why it's an issue>
   - Suggestion: <how to fix it>

2. ...

### Positive Highlights
- <what was done well>

### Overall Score
- **Correctness**: X/5
- **Clarity**: X/5
- **Performance**: X/5
- **Security**: X/5
- **Style**: X/5
```

## Instructions for the Agent
1. When asked to perform a code review, first identify all Python files in the workspace (or the specific files requested).
2. Read each file completely.
3. Evaluate against the checklist above.
4. Write the review report using `write_file` to `code-review-<filename>.md` (one report per file).
5. Present the summary to the user.
