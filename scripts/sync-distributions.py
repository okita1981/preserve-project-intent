#!/usr/bin/env python3
"""Synchronize distributable skill copies from the canonical skill."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "preserve-project-intent"
TARGETS = (
    (ROOT / ".claude" / "skills" / "preserve-project-intent", False),
    (ROOT / "plugin" / "preserve-project-intent" / "skills" / "preserve-project-intent", False),
    (ROOT / "plugins" / "preserve-project-intent" / "skills" / "preserve-project-intent", True),
)


def expected_files(include_openai_metadata: bool) -> list[Path]:
    files = [Path("SKILL.md")]
    files.extend(path.relative_to(SOURCE) for path in sorted((SOURCE / "references").glob("*.md")))
    if include_openai_metadata:
        files.append(Path("agents/openai.yaml"))
    return sorted(files)


def check_target(target: Path, include_openai_metadata: bool) -> list[str]:
    errors: list[str] = []
    expected = expected_files(include_openai_metadata)
    actual = sorted(path.relative_to(target) for path in target.rglob("*") if path.is_file()) if target.exists() else []
    if actual != expected:
        errors.append(f"file set differs: {target.relative_to(ROOT)}")
        return errors
    for relative in expected:
        if not filecmp.cmp(SOURCE / relative, target / relative, shallow=False):
            errors.append(f"content differs: {(target / relative).relative_to(ROOT)}")
    return errors


def sync_target(target: Path, include_openai_metadata: bool) -> None:
    if target.exists():
        shutil.rmtree(target)
    (target / "references").mkdir(parents=True)
    shutil.copy2(SOURCE / "SKILL.md", target / "SKILL.md")
    for path in sorted((SOURCE / "references").glob("*.md")):
        shutil.copy2(path, target / "references" / path.name)
    if include_openai_metadata:
        (target / "agents").mkdir()
        shutil.copy2(SOURCE / "agents" / "openai.yaml", target / "agents" / "openai.yaml")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="check without writing")
    args = parser.parse_args()

    if args.check:
        errors = [error for target, metadata in TARGETS for error in check_target(target, metadata)]
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("All distribution copies match the canonical skill.")
        return 0

    for target, metadata in TARGETS:
        sync_target(target, metadata)
    print("Synchronized Claude Code and Codex plugin copies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
