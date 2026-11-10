#!/usr/bin/env python3
"""Universal installer for egm-product across Qwen CLI (and forks), Gemini CLI, Claude Code, Codex, and Antigravity."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]

CORE_DIRS = [
    "skills",
    "agents",
    "resources",
    "docs",
    "rules",
    "assets",
]

CORE_FILES = [
    "plugin.json",
    "qwen-extension.json",
    "gemini-extension.json",
    "QWEN.md",
    "README.md",
    "LICENSE",
]

DEFAULT_TARGET_DIRS = {
    "qwen": (".qwen", "QWEN.md"),
    "gemini": (".gemini", "GEMINI.md"),
    "claude": (".claude", "CLAUDE.md"),
    "codex": (".codex", "AGENTS.md"),
    "antigravity": (".gemini/config", "AGENTS.md"),
}


def _copy_tree_contents(src_dir: Path, dst_dir: Path) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    for item in src_dir.iterdir():
        target = dst_dir / item.name
        if item.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def install_extension_bundle(base_config_dir: Path, subdir_name: str = "extensions") -> Path:
    """Install the complete egm-product bundle into <base_config_dir>/<subdir_name>/egm-product."""
    ext_root = base_config_dir / subdir_name / "egm-product"
    if ext_root.exists():
        shutil.rmtree(ext_root)
    ext_root.mkdir(parents=True, exist_ok=True)

    for folder in CORE_DIRS:
        src = REPO_ROOT / folder
        if src.is_dir():
            shutil.copytree(src, ext_root / folder)

    for dot_folder in (".claude-plugin", ".codex-plugin", ".agents"):
        src = REPO_ROOT / dot_folder
        if src.is_dir():
            shutil.copytree(src, ext_root / dot_folder)

    for filename in CORE_FILES:
        src = REPO_ROOT / filename
        if src.is_file():
            shutil.copy2(src, ext_root / filename)

    return ext_root


def install_flat_into_config_dir(base_config_dir: Path) -> None:
    """Install skills/, agents/, commands/, resources/, and docs/ directly into <base_config_dir>/."""
    base_config_dir.mkdir(parents=True, exist_ok=True)
    for folder in ("skills", "agents", "resources", "docs"):
        src = REPO_ROOT / folder
        if src.is_dir():
            _copy_tree_contents(src, base_config_dir / folder)

    # Also materialize top-level <base_config_dir>/commands/pm-*.md for CLIs scanning <config_dir>/commands/
    commands_src = REPO_ROOT / "resources" / "commands"
    commands_dst = base_config_dir / "commands"
    commands_dst.mkdir(parents=True, exist_ok=True)
    for cmd_file in commands_src.glob("*.md"):
        raw = cmd_file.read_text(encoding="utf-8")
        adjusted = (
            raw.replace("../../skills/", "../skills/")
            .replace("../../docs/", "../docs/")
            .replace("../execution_instructions.md", "../resources/execution_instructions.md")
            .replace("../templates/", "../resources/templates/")
            .replace("../document_standards/", "../resources/document_standards/")
        )
        (commands_dst / cmd_file.name).write_text(adjusted, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install egm-product into Qwen CLI (or any Qwen CLI fork), Gemini CLI, Claude Code, Codex, or Antigravity."
    )
    parser.add_argument(
        "--target",
        choices=["qwen", "gemini", "claude", "codex", "antigravity"],
        default="qwen",
        help="Target CLI family (default: qwen). Use --config-dir for custom Qwen CLI forks.",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=None,
        help="Explicit CLI configuration directory (e.g. ~/.qwen, ~/.my-qwen-fork, or ./.qwen).",
    )
    parser.add_argument(
        "--project",
        action="store_true",
        help="Install into the current working directory's dot-folder (e.g. ./.qwen) instead of $HOME.",
    )
    parser.add_argument(
        "--mode",
        choices=["extension", "flat", "both"],
        default="both",
        help=(
            "'extension' installs into <config-dir>/extensions/egm-product; "
            "'flat' merges skills/, agents/, commands/, resources/, docs/ directly into <config-dir>/; "
            "'both' (default) performs both so any Qwen/Gemini CLI fork discovers it."
        ),
    )
    args = parser.parse_args(argv)

    default_rel_dir, _ = DEFAULT_TARGET_DIRS[args.target]
    if args.config_dir is not None:
        base_dir = args.config_dir.expanduser().resolve()
    elif args.project:
        base_dir = (Path.cwd() / default_rel_dir).resolve()
    else:
        base_dir = (Path.home() / default_rel_dir).resolve()

    if args.target == "antigravity" and args.config_dir is None:
        ext_path = install_extension_bundle(base_dir, subdir_name="plugins")
        print(f"[ok] Installed egm-product plugin for Antigravity at: {ext_path}")
        return 0

    if args.mode in ("extension", "both"):
        ext_path = install_extension_bundle(base_dir, subdir_name="extensions")
        print(f"[ok] Installed extension bundle at: {ext_path}")

    if args.mode in ("flat", "both"):
        install_flat_into_config_dir(base_dir)
        print(
            f"[ok] Installed flat skills/, agents/, commands/, resources/, docs/ into: {base_dir}"
        )

    print(
        "\nAvailable slash commands & skills:\n"
        "  /pm-discover    - Discover repo capabilities, UI tokens, and product metrics\n"
        "  /pm-brainstorm  - Stress-test feature ideas with the 4+1 PM Goldfish swarm\n"
        "  /pm-prd         - Draft a stack-grounded PRD separating MVP from BLOCKED_NOW\n"
        "  /pm-review      - Audit and resolve PRD findings (max 2 rounds)\n"
        "  /pm-prototype   - Generate a zero-build interactive HTML preview"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
