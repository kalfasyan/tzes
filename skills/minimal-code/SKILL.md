---
name: minimal-code
description: >
  Use for coding, debugging, refactoring, reviewing, or design. Enforces
  token-efficient decisions, complexity-gated planning, focused validation,
  and the smallest correct change.
---

Smallest correct change. Deletion beats addition. Boring beats clever.

## The ladder

Stop at first rung that holds:

1. **YAGNI** — need to exist? Skip, say why.
2. **Already in codebase?** Reuse.
3. **Stdlib?** Use it.
4. **Native platform feature?** Use it.
5. **Installed dep?** Use it.
6. **One line?** One line.
7. Minimum code that works.

## Complexity gate

- **Trivial**: answer, docs, config, or mechanical one-liner without behavioral, security, or deployment risk → act directly.
- **Complex/high-risk**: multi-step, ambiguous, architectural, security-sensitive, CI, deployment, migration, or data work → plan before editing.
- **Meaningful code or configuration**: edit → focused executable check → review.
- **Failed check**: repair same slice and rerun before widening scope.

Skip an advisor when it cannot change the outcome. Explain exceptions when risk is real.

## Rules

- No interface with one implementation. No factory for one product. No config for a value that never changes.
- No boilerplate "for later" — later can scaffold for itself.
- Bug fix = root cause, not symptom. One fix where all callers route through.
- Non-trivial logic leaves one runnable check — smallest thing that fails if logic breaks.
- Read only enough context to identify the controlling path and cheapest check.
- Prefer local code and tests; browse only for unfamiliar or current facts.
- Pass advisors summary, constraints, evidence, diff, validation, and open risks; never transcript.

## Output

Code or decision first. Then max 3 lines: changed, skipped, validation.

Mark deliberate shortcuts: `# <skipped>, add when <condition>`

## Review lens

Flag anything deletable, reusable from stdlib or existing code, or reducible. Reward the shortest diff that solves the problem correctly.
