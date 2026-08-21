---
name: minimal-code
description: >
  Enforces the laziest solution that works. Applied to all coding tasks and
  as the primary lens for code review. Use when writing, fixing, reviewing,
  or designing code. Rewards deletion over addition, stdlib over custom code,
  one line over fifty.
---

Laziest solution that works. Deletion beats addition. Boring beats clever.

## The ladder

Stop at first rung that holds:

1. **YAGNI** — need to exist? Skip, say why.
2. **Already in codebase?** Reuse.
3. **Stdlib?** Use it.
4. **Native platform feature?** Use it.
5. **Installed dep?** Use it.
6. **One line?** One line.
7. Minimum code that works.

## Rules

- No interface with one implementation. No factory for one product. No config for a value that never changes.
- No boilerplate "for later" — later can scaffold for itself.
- Bug fix = root cause, not symptom. One fix where all callers route through.
- Non-trivial logic leaves one runnable check — smallest thing that fails if logic breaks.

## Output

Code first. Then max 3 lines: what was skipped, when to add it.

Mark deliberate shortcuts: `# <skipped>, add when <condition>`

## Review lens

Flag anything that could be: deleted, reused from stdlib or existing code, or reduced to fewer lines. Reward the shortest diff that solves the problem correctly.
