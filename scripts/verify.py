#!/usr/bin/env python3
"""Verify repository structure, skill metadata, references, and manifests."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "preserve-project-intent"


def fail(message: str) -> None:
    raise ValueError(message)


def verify_skill() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(?P<frontmatter>.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md frontmatter is missing")
    frontmatter = match.group("frontmatter")
    if "name: preserve-project-intent" not in frontmatter:
        fail("skill name is incorrect")
    description = next((line for line in frontmatter.splitlines() if line.startswith("description:")), "")
    if len(description.removeprefix("description:").strip()) < 80:
        fail("skill description is not discriminating enough")
    if "TODO" in text or "[TODO" in text:
        fail("unfinished placeholder found")
    links = re.findall(r"\]\((references/[^)]+\.md)\)", text)
    if not links:
        fail("SKILL.md does not route to supporting references")
    for link in links:
        if not (SKILL / link).is_file():
            fail(f"broken reference: {link}")


def verify_json(path: Path, expected_name: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("name") != expected_name:
        fail(f"incorrect name in {path.relative_to(ROOT)}")


def verify_manifests() -> None:
    codex_path = ROOT / "plugins" / "preserve-project-intent" / ".codex-plugin" / "plugin.json"
    claude_path = ROOT / "plugin" / "preserve-project-intent" / ".claude-plugin" / "plugin.json"
    verify_json(codex_path, "preserve-project-intent")
    verify_json(claude_path, "preserve-project-intent")
    codex = json.loads(codex_path.read_text(encoding="utf-8"))
    claude = json.loads(claude_path.read_text(encoding="utf-8"))
    if codex.get("version") != claude.get("version"):
        fail("Codex and Claude plugin versions differ")


def verify_marketplaces() -> None:
    codex_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    codex = json.loads(codex_path.read_text(encoding="utf-8"))
    codex_entries = codex.get("plugins", [])
    if len(codex_entries) != 1 or codex_entries[0].get("name") != "preserve-project-intent":
        fail("Codex marketplace entry is incorrect")

    claude_path = ROOT / ".claude-plugin" / "marketplace.json"
    claude = json.loads(claude_path.read_text(encoding="utf-8"))
    if claude.get("name") != "preserve-project-intent":
        fail("Claude marketplace name is incorrect")
    claude_entries = claude.get("plugins", [])
    if len(claude_entries) != 1 or claude_entries[0].get("name") != "preserve-project-intent":
        fail("Claude marketplace entry is incorrect")
    source = claude_entries[0].get("source")
    if source != "./plugin/preserve-project-intent":
        fail("Claude marketplace source is incorrect")
    if not (ROOT / source).is_dir():
        fail("Claude marketplace source does not exist")


def verify_trigger_fixtures() -> None:
    """Validate fixture structure only; this does not evaluate model behavior."""
    path = ROOT / "fixtures" / "trigger-cases.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for group in ("should_trigger", "should_not_trigger"):
        cases = data.get(group)
        if not isinstance(cases, list) or len(cases) < 4:
            fail(f"{group} must contain at least four cases")
        for case in cases:
            if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                fail(f"empty prompt in {group}")
            if not isinstance(case.get("reason"), str) or not case["reason"].strip():
                fail(f"empty reason in {group}")
            allowed = {
                "TRIGGER_INIT",
                "TRIGGER_CONTROL",
                "TRIGGER_HANDOFF",
                "TRIGGER_RESUME",
            } if group == "should_trigger" else {"DO_NOT_TRIGGER"}
            if case.get("expected") not in allowed:
                fail(f"invalid expected value in {group}")
    boundary_cases = data.get("boundary_cases")
    if not isinstance(boundary_cases, list) or len(boundary_cases) < 6:
        fail("boundary_cases must contain at least six cases")
    for case in boundary_cases:
        for field in ("prompt", "context", "reason"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                fail(f"empty {field} in boundary_cases")
        if case.get("expected") not in {"TRIGGER_CONTROL", "TRIGGER_RESUME", "DO_NOT_TRIGGER", "ASK_FOR_STATE"}:
            fail("invalid expected value in boundary_cases")


def verify_plugin_evals() -> None:
    eval_root = ROOT / "plugin" / "preserve-project-intent" / "evals"
    required_cases = {
        "local-completion-boundary",
        "depth2-checkpoint",
        "return-point",
        "missing-resume-state",
        "init-persistence-decision",
        "unrelated-one-step",
    }
    actual_cases = {path.name for path in eval_root.iterdir() if path.is_dir() and path.name != "results"}
    if actual_cases != required_cases:
        fail("Claude plugin eval case set is incorrect")
    for case_name in required_cases:
        case = eval_root / case_name
        prompt = case / "prompt.md"
        graders = case / "graders"
        if not prompt.is_file() or not graders.is_dir():
            fail(f"incomplete Claude plugin eval case: {case_name}")
        grader_files = list(graders.glob("*.md"))
        if not grader_files:
            fail(f"Claude plugin eval case has no graders: {case_name}")
        for path in [prompt, *grader_files]:
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---\n") or "\n---\n" not in text[4:]:
                fail(f"invalid eval frontmatter: {path.relative_to(ROOT)}")


def verify_with_claude_cli() -> None:
    claude = shutil.which("claude")
    required = os.environ.get("REQUIRE_CLAUDE_PLUGIN_VALIDATE") == "1"
    if claude is None:
        if required:
            fail("Claude CLI is required but was not found")
        print("Claude CLI not found; skipping official plugin validation.")
        return
    for path in (ROOT, ROOT / "plugin" / "preserve-project-intent"):
        subprocess.run(
            [claude, "plugin", "validate", str(path)],
            cwd=ROOT,
            check=True,
        )


def main() -> int:
    try:
        verify_skill()
        verify_manifests()
        verify_marketplaces()
        verify_trigger_fixtures()
        verify_plugin_evals()
        verify_with_claude_cli()
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "sync-distributions.py"), "--check"],
            cwd=ROOT,
            check=True,
        )
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
        return 1
    print("Repository verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
