# tzes

> "Me think, why waste tokens say lot word, when few word do trick."

Token-efficient coding agent for **VS Code Copilot**.

**Goal:** spend tokens where they change the outcome. Tzes acts directly on small work, plans only complex or high-risk work, reviews meaningful changes, and validates focused slices.

All agents use GPT-5.6 Luna (copilot). Change the model in each `.agent.md` if your subscription exposes a different identifier.

## Agents

| Agent | Model | Visible | Role |
|-------|-------|---------|------|
| `tzes` | GPT-5.6 Luna (copilot) | ✅ | Main agent; terse by default, adaptive when ambiguity or risk needs detail |
| `Advisor — Plan` | GPT-5.6 Luna (copilot) | ❌ subagent only | Plans complex, multi-step, ambiguous, or architectural work |
| `Advisor — Review` | GPT-5.6 Luna (copilot) | ❌ subagent only | Reviews meaningful code and configuration after focused validation |

## Workflow

1. **Trivial:** answer, docs, config, or one-line mechanical change without behavioral, security, or deployment risk. Act directly.
2. **Complex/high-risk:** multi-step, ambiguous, architectural, security-sensitive, CI, deployment, migration, or data work. Plan before editing.
3. **Meaningful code or configuration:** make the smallest edit, run a focused check, then review.
4. **Failure:** repair the same slice and rerun its check before widening scope.

Advisors receive a compact handoff: goal, constraints, relevant evidence, diff, validation, and open risks. They never receive the full transcript. Plan output is capped at 180 words; review output at 160.

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

To refresh an existing install after a repository update:

```bash
copilot plugin update tzes@tzes
```

### Workspace-level (one repo)

Copy agents and skills to `.github/` in your repo — VS Code auto-discovers them. Workspace-only setup does not install the optional MCP server.

```bash
mkdir -p path/to/your-repo/.github/agents path/to/your-repo/.github/skills
cp agents/*.agent.md path/to/your-repo/.github/agents/
cp -r skills/* path/to/your-repo/.github/skills/
```

Install the plugin instead when you also want the optional Tavily MCP server.

## Customise

- **Agent name**: change `name:` in `agents/tzes.agent.md`.
- **Model**: swap model names in any `.agent.md` to match your Copilot subscription.
- **MCP**: `.mcp.json` pins direct package `tavily-mcp@0.2.22`; npm still resolves its transitive dependencies. It requires a Tavily key and sends external searches to Tavily. Use it only for unfamiliar or current facts.
- **Memory**: agents use `/memories/repo/` when available; add only durable, concise project notes there.

## Origins

Tzes started as a personal adaptation inspired by my colleague Victor Verhaert's coding agent. It grew through ideas from [caveman](https://github.com/JuliusBrussee/caveman) and [ponytail](https://github.com/DietrichGebert/ponytail), with Yannis's additions for complexity gates, focused validation, compact advisor handoffs, and adaptive terse communication.
