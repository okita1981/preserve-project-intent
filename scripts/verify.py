#!/usr/bin/env python3
"""Verify repository structure, skill metadata, references, and manifests."""

from __future__ import annotations

import json
import re
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


def main() -> int:
    try:
        verify_skill()
        verify_manifests()
        verify_trigger_fixtures()
        marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
        entries = marketplace.get("plugins", [])
        if len(entries) != 1 or entries[0].get("name") != "preserve-project-intent":
            fail("Codex marketplace entry is incorrect")
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
