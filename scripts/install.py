#!/usr/bin/env python3
"""Collision-safe installer & uninstaller for egm-product across Antigravity, Qwen CLI (and forks), Gemini CLI, Claude Code, and Codex."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]

RUNTIME_PATTERNS = (
    "plugin.json",
    "qwen-extension.json",
    "gemini-extension.json",
    "QWEN.md",
    "GEMINI_EXTENSION.md",
    "README.md",
    "LICENSE",
    "assets/*.svg",
    "rules/AGENTS.md",
    "skills/*/SKILL.md",
    "skills/*/agents/openai.yaml",
    "skills/*/assets/*.svg",
    "agents/pm_*.md",
    "resources/pm_execution_instructions.md",
    "resources/commands/pm-*.md",
    "resources/document_standards/prd-standard.md",
    "resources/templates/*.template.md",
    "docs/harnesses.md",
    "docs/claude.md",
    "docs/codex.md",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".claude-plugin/agents/pm_*.md",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
)

DEFAULT_TARGET_DIRS: dict[str, str] = {
    "qwen": ".qwen",
    "gemini": ".gemini",
    "antigravity": ".gemini/config",
    "claude": ".claude",
    "codex": ".codex",
}


def install_clean_bundle(base_config_dir: Path, subdir_name: str = "extensions") -> Path:
    """Install only verified runtime files (zero tests, zero docs/designs, zero .dev scratch) into <base_config_dir>/<subdir_name>/egm-product."""
    ext_root = base_config_dir / subdir_name / "egm-product"
    if ext_root.exists():
        shutil.rmtree(ext_root)
    ext_root.mkdir(parents=True, exist_ok=True)

    for pattern in RUNTIME_PATTERNS:
        for src in sorted(REPO_ROOT.glob(pattern)):
            if not src.is_file():
                continue
            rel = src.relative_to(REPO_ROOT)
            dst = ext_root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    return ext_root


KNOWN_PM_TEMPLATES = (
    "company_context.template.md",
    "product_context.template.md",
    "metrics.template.md",
    "opportunity_brief.template.md",
    "prd.template.md",
    # Legacy pre-v0.4.0 templates removed on upgrade/uninstall without touching sibling plugins
    "portfolio_status.template.md",
    "schemas.template.md",
    "ui_tokens.template.md",
    "pm_review_report.template.md",
)


def _cleanup_flat_namespaced(base_config_dir: Path) -> None:
    """Remove current and legacy namespaced pm-* flat files and prune empty directories without touching sibling plugins."""
    for skill_dir in base_config_dir.glob("skills/pm-*"):
        if skill_dir.is_dir():
            shutil.rmtree(skill_dir)
    for agent_file in base_config_dir.glob("agents/pm_*.md"):
        agent_file.unlink(missing_ok=True)
    for cmd_file in base_config_dir.glob("commands/pm-*.md"):
        cmd_file.unlink(missing_ok=True)

    (base_config_dir / "resources" / "pm_execution_instructions.md").unlink(missing_ok=True)
    (base_config_dir / "resources" / "document_standards" / "prd-standard.md").unlink(missing_ok=True)
    for tmpl_name in KNOWN_PM_TEMPLATES:
        (base_config_dir / "resources" / "templates" / tmpl_name).unlink(missing_ok=True)

    pm_docs = base_config_dir / "docs" / "egm-product"
    if pm_docs.is_dir():
        shutil.rmtree(pm_docs)

    for rel_dir in (
        "commands",
        "agents",
        "skills",
        "resources/templates",
        "resources/document_standards",
        "resources",
        "docs",
    ):
        candidate = base_config_dir / rel_dir
        if candidate.is_dir() and not any(candidate.iterdir()):
            candidate.rmdir()


def install_flat_namespaced(base_config_dir: Path) -> list[Path]:
    """Install only namespaced pm-* files into <base_config_dir>/ without ever deleting or overwriting sibling plugins (such as engineering egm)."""
    written: list[Path] = []
    base_config_dir.mkdir(parents=True, exist_ok=True)
    _cleanup_flat_namespaced(base_config_dir)

    # 1. Namespaced skills/pm-*/, agents/pm_*.md, and namespaced resources/
    flat_patterns = (
        "skills/pm-*/SKILL.md",
        "skills/pm-*/agents/openai.yaml",
        "skills/pm-*/assets/*.svg",
        "agents/pm_*.md",
        "resources/pm_execution_instructions.md",
        "resources/document_standards/prd-standard.md",
        "resources/templates/*.template.md",
    )
    for pattern in flat_patterns:
        for src in sorted(REPO_ROOT.glob(pattern)):
            if not src.is_file():
                continue
            rel = src.relative_to(REPO_ROOT)
            dst = base_config_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            written.append(dst)

    # 2. Namespaced docs under docs/egm-product/ so docs/harnesses.md of engineering egm is never overwritten!
    pm_docs_dir = base_config_dir / "docs" / "egm-product"
    pm_docs_dir.mkdir(parents=True, exist_ok=True)
    for doc_name in ("harnesses.md", "claude.md", "codex.md"):
        src_doc = REPO_ROOT / "docs" / doc_name
        dst_doc = pm_docs_dir / doc_name
        raw_doc = src_doc.read_text(encoding="utf-8").replace("(../", "(../../")
        dst_doc.write_text(raw_doc, encoding="utf-8")
        written.append(dst_doc)

    # Rewrite doc links inside flat-installed skills/pm-*/SKILL.md so ../../docs/*.md points to ../../docs/egm-product/*.md
    for skill_md in (base_config_dir / "skills").glob("pm-*/SKILL.md"):
        updated_skill = (
            skill_md.read_text(encoding="utf-8")
            .replace("../../docs/harnesses.md", "../../docs/egm-product/harnesses.md")
            .replace("../../docs/codex.md", "../../docs/egm-product/codex.md")
            .replace("../../docs/claude.md", "../../docs/egm-product/claude.md")
        )
        skill_md.write_text(updated_skill, encoding="utf-8")

    # 3. Top-level commands/pm-*.md for custom CLI forks scanning <config_dir>/commands/
    commands_dst = base_config_dir / "commands"
    commands_dst.mkdir(parents=True, exist_ok=True)
    for cmd_file in sorted((REPO_ROOT / "resources" / "commands").glob("pm-*.md")):
        adjusted = (
            cmd_file.read_text(encoding="utf-8")
            .replace("../../skills/", "../skills/")
            .replace("../../docs/harnesses.md", "../docs/egm-product/harnesses.md")
            .replace("../pm_execution_instructions.md", "../resources/pm_execution_instructions.md")
            .replace("../templates/", "../resources/templates/")
            .replace("../document_standards/", "../resources/document_standards/")
        )
        dst_cmd = commands_dst / cmd_file.name
        dst_cmd.write_text(adjusted, encoding="utf-8")
        written.append(dst_cmd)

    return written


def uninstall_from_config_dir(base_config_dir: Path, target: str) -> None:
    """Cleanly remove egm-product bundle and namespaced pm-* flat files without touching sibling plugins."""
    subdir = "plugins" if target == "antigravity" else "extensions"
    bundle_dir = base_config_dir / subdir / "egm-product"
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    bundle_parent = base_config_dir / subdir
    if bundle_parent.is_dir() and not any(bundle_parent.iterdir()):
        bundle_parent.rmdir()

    _cleanup_flat_namespaced(base_config_dir)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install or uninstall egm-product cleanly across Antigravity, Qwen CLI (and forks), Gemini CLI, Claude Code, or Codex."
    )
    parser.add_argument(
        "--target",
        choices=["qwen", "gemini", "antigravity", "claude", "codex"],
        default="qwen",
        help="Target CLI family (default: qwen).",
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
        help="Install into the current working directory's dot-folder instead of $HOME.",
    )
    parser.add_argument(
        "--mode",
        choices=["extension", "flat", "both"],
        default="extension",
        help=(
            "'extension' (default, isolated) installs into <config-dir>/extensions/egm-product (or plugins/egm-product for Antigravity); "
            "'flat' installs only namespaced pm-* files directly into <config-dir>/ for custom CLI forks; "
            "'both' performs both safely without overwriting engineering egm."
        ),
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Cleanly remove egm-product from the target configuration directory.",
    )
    args = parser.parse_args(argv)

    default_rel_dir = DEFAULT_TARGET_DIRS[args.target]
    if args.config_dir is not None:
        base_dir = args.config_dir.expanduser().resolve()
    elif args.project:
        base_dir = (Path.cwd() / default_rel_dir).resolve()
    else:
        base_dir = (Path.home() / default_rel_dir).resolve()

    if args.uninstall:
        uninstall_from_config_dir(base_dir, args.target)
        print(f"[ok] Uninstalled local egm-product files from: {base_dir}")
        if args.target in ("claude", "codex") and args.config_dir is None:
            native_un = (
                "claude plugin uninstall egm-product@egm-product"
                if args.target == "claude"
                else "codex plugin remove egm-product@egm-product"
            )
            print(f"[info] If installed via {args.target} marketplace, also run: {native_un}")
        return 0

    if args.target in ("claude", "codex") and args.config_dir is None:
        native_cmd = (
            "claude plugin marketplace add Meddelin/egm-product && claude plugin install egm-product@egm-product"
            if args.target == "claude"
            else "codex plugin marketplace add Meddelin/egm-product && codex plugin add egm-product@egm-product"
        )
        print(
            f"[info] {args.target} uses native marketplace plugin management rather than ~/.{args.target}/extensions.\n"
            f"Run: {native_cmd}\n"
            f"(Or pass --config-dir explicitly to stage files into a custom fork directory.)"
        )
        return 0

    subdir = "plugins" if args.target == "antigravity" else "extensions"
    if args.mode in ("extension", "both"):
        ext_path = install_clean_bundle(base_dir, subdir_name=subdir)
        print(f"[ok] Installed clean {subdir[:-1]} bundle at: {ext_path}")

    if args.mode in ("flat", "both"):
        install_flat_namespaced(base_dir)
        print(f"[ok] Installed collision-safe namespaced pm-* files into: {base_dir}")

    print(
        "\nAvailable slash commands & skills:\n"
        "  /pm-discover    - Map product strategy, company context, empirical roles, UI tokens & metrics\n"
        "  /pm-brainstorm  - Shape and challenge feature ideas with the 4+1 Product Goldfish swarm\n"
        "  /pm-prd         - Draft a user-focused PRD and polish it with built-in 4+1 Product review\n"
        "  /pm-prototype   - Generate and verify a zero-build interactive HTML preview"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
