#!/usr/bin/env python3
import json
import re
import sys


RISK_PATTERNS = (
    ("recursive or forced file removal", r"(?:^|[;&|\r\n]\s*)rm\s+(?:-[^\s]*[rf][^\s]*\s+)+"),
    ("filesystem removal", r"(?:^|[;&|\r\n]\s*)(?:rm|rmdir)\s+"),
    ("destructive Git operation", r"\bgit\s+(?:reset\s+--hard|clean\s+-[^\s]*f|checkout\s+--|restore\b|branch\s+-D)"),
    ("publishing Git changes", r"\bgit\s+push\b"),
    ("privileged or machine-level command", r"\b(?:sudo|shutdown|reboot|mkfs(?:\.\w+)?|fdisk)\b"),
    ("raw disk write", r"\bdd\s+[^\n]*\bof="),
    ("destructive database statement", r"\b(?:drop|truncate)\s+(?:database|schema|table)\b|\bdelete\s+from\b"),
    ("infrastructure or deployment change", r"\b(?:kubectl\s+(?:apply|delete)|helm\s+(?:install|upgrade|uninstall)|terraform\s+(?:apply|destroy)|docker\s+(?:push|system\s+prune))\b"),
    ("package publication", r"\b(?:npm|pnpm|yarn|pixi|cargo)\s+publish\b|\btwine\s+upload\b|\bgh\s+release\s+create\b"),
    ("cloud deployment", r"\b(?:gcloud|vercel|netlify)\b[^\n]*(?:deploy|publish)\b|\baz\b[^\n]*\bdeployment\b|\baws\b[^\n]*\bdeploy\b"),
    ("external file transfer", r"\b(?:scp|sftp)\b|\brsync\b[^\n]*\b[^\s]+@[^:]+:"),
    ("recursive permission change", r"\b(?:chmod|chown)\s+-R\b"),
)

COMMAND_KEYS = {"command", "cmd", "script", "code"}
PATH_KEYS = {"path", "filepath", "file_path", "files"}
PROTECTED_PATHS = {
    ".mcp.json",
    "hooks.json",
    "workspace/hooks.json",
    "plugin.json",
    "marketplace.json",
    "hooks/approve_risky.py",
    "agents/tzes.agent.md",
    "agents/advisor-plan.agent.md",
    "agents/advisor-review.agent.md",
    ".github/agents/tzes.agent.md",
    ".github/agents/advisor-plan.agent.md",
    ".github/agents/advisor-review.agent.md",
    ".github/hooks/tzes.json",
    "scripts/approve_risky.py",
}


def command_text(value):
    if not isinstance(value, dict):
        return ""

    commands = []
    for key, item in value.items():
        if key.lower() in COMMAND_KEYS:
            if isinstance(item, str):
                commands.append(item)
            elif isinstance(item, list):
                commands.extend(part for part in item if isinstance(part, str))
        elif isinstance(item, dict):
            nested = command_text(item)
            if nested:
                commands.append(nested)
    return "\n".join(commands)


def target_paths(value):
    if not isinstance(value, dict):
        return set()

    paths = set()
    for key, item in value.items():
        if key.lower() in PATH_KEYS:
            if isinstance(item, str):
                paths.add(item)
            elif isinstance(item, list):
                paths.update(part for part in item if isinstance(part, str))
        elif key.lower() == "input" and isinstance(item, str):
            paths.update(
                match.group(1).strip()
                for match in re.finditer(
                    r"^\*\*\* (?:Add|Update|Delete) File: (.+)$",
                    item,
                    flags=re.MULTILINE,
                )
            )
        elif isinstance(item, dict):
            paths.update(target_paths(item))
    return paths


def is_protected(path):
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    normalized = normalized.lstrip("/")
    return any(normalized == protected or normalized.endswith(f"/{protected}") for protected in PROTECTED_PATHS)


def ask(reason):
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }


def decision(payload):
    tool_name = str(payload.get("tool_name", "")).lower()
    tool_input = payload.get("tool_input", {})

    if tool_name.startswith("tavily") or "/tavily" in tool_name:
        return ask("This call sends query data to Tavily. Confirm external data sharing.")

    if any(is_protected(path) for path in target_paths(tool_input)):
        return ask("This edit changes tzes policy or guardrail files. Confirm the exact change.")

    if any(word in tool_name for word in ("delete", "remove")):
        return ask("This tool removes data or files. Confirm the exact target.")

    serialized_input = json.dumps(tool_input, ensure_ascii=True)
    if "*** Delete File:" in serialized_input:
        return ask("This edit deletes a file. Confirm the exact target.")

    command = command_text(tool_input)
    for reason, pattern in RISK_PATTERNS:
        if re.search(pattern, command, flags=re.IGNORECASE):
            return ask(f"Recognized {reason}. Confirm this operation.")

    return {}


def main():
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError("hook input must be an object")
        output = decision(payload)
    except (json.JSONDecodeError, TypeError, ValueError):
        output = ask("Could not inspect this tool call safely. Confirm before continuing.")

    json.dump(output, sys.stdout)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()