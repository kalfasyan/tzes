# tzes

> "Me think, why waste tokens say lot word, when few word do trick."

Token-efficient coding agent for **VS Code Copilot**.

**Goal:** spend tokens where they change the outcome. Tzes interviews before meaningful work, turns goals into small specs with explicit success criteria, and uses a second AI to review the result.

All agents use GPT-5.6 Luna (copilot). Change the model in each `.agent.md` if your subscription exposes a different identifier.

## Agents

| Agent | Model | Visible | Role |
|-------|-------|---------|------|
| `tzes` | GPT-5.6 Luna (copilot) | ✅ | Main agent; terse by default, adaptive when ambiguity or risk needs detail |
| `Advisor — Plan` | GPT-5.6 Luna (copilot) | ❌ subagent only | Plans complex, multi-step, ambiguous, or architectural work |
| `Advisor — Review` | GPT-5.6 Luna (copilot) | ❌ subagent only | Reviews meaningful code and configuration after focused validation |

## Workflow

1. **Trivial:** answer, docs, config, or one-line mechanical change without behavioral, security, or deployment risk. Act directly.
2. **Interview:** for meaningful work, confirm the real goal, non-goals, key decisions, and small specs.
3. **Criteria:** define observable success criteria; ask for a past example, then find the nearest repo example if none is provided.
4. **Plan:** complex or high-risk work uses `Advisor — Plan` before editing.
5. **Validate and review:** run a focused check, then `Advisor — Review` checks criteria, decisions, and reference fidelity.
6. **Failure:** repair the same slice and rerun its check before widening scope.

Advisors receive a compact handoff: goal, confirmed decisions, success criteria, reference example, constraints, evidence, diff, validation, and risks. They never receive the full transcript. Plan output is capped at 220 words; review output at 160.

## Project audit

The `project-audit` skill reviews GitHub Copilot equivalents of `CLAUDE.md`: `AGENTS.md`, `.github/copilot-instructions.md`, scoped instructions, knowledge and memory, skills, prompts, tests, CI, and guardrails. It returns exactly five prioritized gaps with file, problem, exact fix, and whether deterministic enforcement needs a hook.

## Approval hook

The optional workspace setup includes a small `PreToolUse` hook. Safe calls keep normal host behavior. Recognized destructive, publish, deployment, database, or privileged operations return `ask` so the user must confirm.

The user-level plugin does not auto-enable this hook. VS Code currently does not expose a documented, stable plugin-root variable for bundled command hooks; an invalid path can fail closed and block every tool. Use the workspace installation below, where the script path is stable.

The hook is defense-in-depth, not a complete command sandbox. It uses pattern matching and can miss novel commands or ask on unusual safe commands. VS Code hooks are currently preview; inspect **GitHub Copilot Chat Hooks** output if it does not load.

## Install

### User-level (all workspaces)

Register the marketplace once, then install:

```bash
copilot plugin marketplace add kalfasyan/tzes
copilot plugin install tzes@tzes
```

Or in an interactive Copilot CLI session:

```text
/plugin marketplace add kalfasyan/tzes
/plugin install tzes@tzes
```

Then run **Chat: Reload Custom Agents** (`Ctrl+Shift+P`) in VS Code.

### Update

```bash
copilot plugin update tzes@tzes
```

Then run **Chat: Reload Custom Agents** in VS Code. Check the installed version with:

```bash
copilot plugin list
```

### Uninstall

```bash
copilot plugin uninstall tzes@tzes
```

Then run **Developer: Reload Window**. If a broken `PreToolUse` hook blocks all agent tools, run the uninstall command manually in a terminal before reloading VS Code.

### Workspace-level (one repo)

Copy agents, skills, and the hook to `.github/` in your repo — VS Code auto-discovers them. Workspace-only setup does not install the optional MCP server.

```bash
mkdir -p path/to/your-repo/.github/agents path/to/your-repo/.github/skills path/to/your-repo/.github/hooks path/to/your-repo/scripts
cp agents/*.agent.md path/to/your-repo/.github/agents/
cp -r skills/* path/to/your-repo/.github/skills/
cp workspace/hooks.json path/to/your-repo/.github/hooks/tzes.json
cp hooks/approve_risky.py path/to/your-repo/scripts/
```

Install the plugin instead when you also want the optional Tavily MCP server.

## Customise

- **Agent name**: change `name:` in `agents/tzes.agent.md`.
- **Model**: swap model names in any `.agent.md` to match your Copilot subscription.
- **MCP**: `.mcp.json` pins direct package `tavily-mcp@0.2.22`; npm still resolves its transitive dependencies. It requires a Tavily key and sends external searches to Tavily. Use it only for unfamiliar or current facts.
- **Memory**: agents use `/memories/repo/` when available; add only durable, concise project notes there.
- **Hook policy**: edit `hooks/approve_risky.py` to tune which operations require approval. Protect hook scripts from automatic edits in VS Code settings.

## Origins

Tzes started as a personal adaptation inspired by my colleague Victor Verhaert's coding agent. It grew through ideas from [caveman](https://github.com/JuliusBrussee/caveman) and [ponytail](https://github.com/DietrichGebert/ponytail), with Yannis's additions for complexity gates, focused validation, compact advisor handoffs, and adaptive terse communication.
