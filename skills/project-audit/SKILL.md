---
name: project-audit
description: >
  Audit a project's Copilot setup, instructions, AGENTS.md, knowledge base,
  memory, skills, prompts, tests, hooks, and guardrails. Use when asked to find
  workflow gaps, improve agent configuration, or identify risky actions that
  need deterministic hooks.
---

Audit only unless edits are explicitly requested.

## Inspect

Use GitHub Copilot equivalents rather than assuming `CLAUDE.md`:

1. `AGENTS.md`, `.github/copilot-instructions.md`, and `.github/instructions/`
2. README, architecture docs, knowledge graph, and `/memories/repo/`
3. `.github/agents/`, `.github/skills/`, `.agents/skills/`, and prompts
4. `.github/hooks/`, agent hooks, permission settings, and deployment controls
5. Tests, CI, formatters, linters, and executable validation commands

Read only relevant files. Prefer evidence over generic best practices.

## Rank

Return exactly the five highest-impact gaps, ordered by risk then leverage:

| File | Problem | Exact fix | Hook? |
|---|---|---|---|

- Name the existing file, or the precise target path if missing.
- Make each fix directly actionable; no vague recommendations.
- Set `Hook?` to the event and action when guidance can be bypassed.
- Use `No` when instructions or tests are sufficient.

## Hook threshold

Recommend hooks only for deterministic enforcement: destructive operations,
secret exposure, production deploys, database migrations, publishing, or
required validation. State false-positive risk and whether the hook should ask
or deny.

After the table, add at most three assumptions or evidence gaps. Stay under 500 words.