# tzes

> "Me think, why waste tokens say lot word, when few word do trick."

Executor-advisor agent trio for **VS Code Copilot**.

**Pattern:** GPT-5.6 Luna main agent (tzes) handles coding with minimal-code discipline. GPT-5.6 Luna advisory subagents fire only when needed — planner on complex tasks, reviewer after every code change.

## Agents

| Agent | Model | Visible | Role |
|-------|-------|---------|------|
| `tzes` | GPT-5.6 Luna (copilot) | ✅ | Main coding agent for Yannis — asks questions, minimal-code discipline, per-project memory |
| `Advisor — Plan` | GPT-5.6 Luna (copilot) | ❌ subagent only | Deep planner for complex/ambiguous tasks |
| `Advisor — Review` | GPT-5.6 Luna (copilot) | ❌ subagent only | Mandatory post-change reviewer (minimal-code lens + OWASP) |

## Install

### User-level (all workspaces)

```
copilot plugin marketplace add kalfasyan/tzes
copilot plugin install tzes@tzes
```

Or in an interactive Copilot CLI session:

```
/plugin marketplace add kalfasyan/tzes
/plugin install tzes@tzes
```

Then run **Chat: Reload Custom Agents** (`Ctrl+Shift+P`) in VS Code.

### Workspace-level (one repo)

Copy `agents/` to `.github/agents/` in your repo — VS Code auto-discovers them.

```bash
cp -r agents/ path/to/your-repo/.github/agents/
```

## Customise

- **Agent name**: change `name:` in `agents/tzes.agent.md`.
- **Model**: swap model names in any `.agent.md` to match your Copilot subscription.
- **Tools**: extend the `tools:` list in `agents/tzes.agent.md` with MCP servers (e.g. `io.github.tavily-ai/tavily-mcp/*`).
- **Memory**: agents read `/memories/repo/` — add project-specific notes there to persist knowledge across sessions.

## Inspired by

- [caveman](https://github.com/JuliusBrussee/caveman) — terse communication, minimal token usage
- [ponytail](https://github.com/DietrichGebert/ponytail) — minimal-code discipline, YAGNI ladder
