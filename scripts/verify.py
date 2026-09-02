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


def main() -> int:
    try:
        verify_skill()
        verify_json(ROOT / "plugins" / "preserve-project-intent" / ".codex-plugin" / "plugin.json", "preserve-project-intent")
        verify_json(ROOT / "plugin" / "preserve-project-intent" / ".claude-plugin" / "plugin.json", "preserve-project-intent")
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
