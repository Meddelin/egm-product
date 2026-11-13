#!/usr/bin/env python3
"""Build clean, reproducible runtime folders and ZIP archives for egm-product without dev/test artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile
import zipfile

SHARED_PATTERNS = (
    "plugin.json",
    "LICENSE",
    "README.md",
    "skills/*/SKILL.md",
    "skills/*/agents/openai.yaml",
    "skills/*/assets/*.svg",
    "agents/*.md",
    "resources/pm_execution_instructions.md",
    "resources/document_standards/*.md",
    "resources/templates/*.md",
    "docs/harnesses.md",
    "docs/claude.md",
    "docs/codex.md",
    "assets/*.svg",
)

HOST_PATTERNS: dict[str, tuple[str, ...]] = {
    "claude": (
        ".claude-plugin/plugin.json",
        ".claude-plugin/agents/*.md",
    ),
    "openai": (
        ".codex-plugin/plugin.json",
    ),
    "antigravity": (
        "rules/AGENTS.md",
    ),
    "qwen": (
        "qwen-extension.json",
        "QWEN.md",
        "resources/commands/*.md",
    ),
    "gemini": (
        "gemini-extension.json",
        "GEMINI_EXTENSION.md",
        "resources/commands/*.md",
    ),
}

EXPECTED_SKILLS = (
    "pm-discover",
    "pm-brainstorm",
    "pm-prd",
    "pm-prototype",
)

EXPECTED_AGENTS = (
    "pm_product_scanner",
    "pm_value_strategy",
    "pm_ux_flows",
    "pm_metrics_experiment",
    "pm_business_logic",
    "pm_synthesizer",
)

REQUIRED_SHARED = (
    (
        "plugin.json",
        "LICENSE",
        "README.md",
        "assets/icon.svg",
        "docs/harnesses.md",
        "docs/claude.md",
        "docs/codex.md",
        "resources/pm_execution_instructions.md",
        "resources/document_standards/prd-standard.md",
        "resources/templates/company_context.template.md",
        "resources/templates/product_context.template.md",
        "resources/templates/metrics.template.md",
        "resources/templates/opportunity_brief.template.md",
        "resources/templates/prd.template.md",
    )
    + tuple(
        f"skills/{skill}/{rel}"
        for skill in EXPECTED_SKILLS
        for rel in ("SKILL.md", "agents/openai.yaml", "assets/icon.svg")
    )
    + tuple(f"agents/{agent}.md" for agent in EXPECTED_AGENTS)
)


def build(root: Path, target: str, output: Path) -> tuple[Path, Path]:
    """Write a clean runtime folder and deterministic ZIP archive; reject symlinks, escapes, or overwrites."""
    if target not in HOST_PATTERNS:
        raise ValueError(f"Unsupported target: {target!r}; expected one of {sorted(HOST_PATTERNS)}")

    root = root.resolve()
    output_resolved = output.resolve()
    folder = output_resolved / f"egm-product-{target}"
    archive = folder.with_suffix(".zip")

    if any(p.exists() or p.is_symlink() for p in (folder, archive)):
        raise ValueError(f"Output folder or ZIP already exists: {folder}")
    if folder == root or root.is_relative_to(folder):
        raise ValueError("Output directory must not contain the source tree")

    files: set[Path] = set()
    for pattern in SHARED_PATTERNS + HOST_PATTERNS[target]:
        for path in root.glob(pattern):
            relative = path.relative_to(root)
            if any((root / Path(*relative.parts[:i])).is_symlink() for i in range(1, len(relative.parts) + 1)):
                raise ValueError(f"Symlink in runtime path: {relative}")
            if not path.resolve().is_relative_to(root):
                raise ValueError(f"Path escapes source root: {relative}")
            if path.is_file():
                files.add(relative)

    required_for_target = REQUIRED_SHARED + (HOST_PATTERNS[target][0],)
    if target in ("qwen", "gemini"):
        required_for_target += tuple(f"resources/commands/{skill}.md" for skill in EXPECTED_SKILLS)
    for req_name in required_for_target:
        if Path(req_name) not in files:
            raise ValueError(f"Missing required file: {req_name}")

    portable = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    openai_ext = portable.get("extensions", {}).get("com.openai", {})
    host_manifest: dict[str, object] = {}
    first_host_file = root / HOST_PATTERNS[target][0]
    if first_host_file.suffix == ".json":
        host_manifest = json.loads(first_host_file.read_text(encoding="utf-8"))

    if host_manifest.get("hooks") or portable.get("hooks") or openai_ext.get("hooks"):
        raise ValueError("Distributable plugin packages must not bundle hooks")
    for metadata in (host_manifest, portable, openai_ext):
        if any(metadata.get(k) for k in ("mcpServers", "mcp", "apps")):
            raise ValueError("Distributable builder does not bundle unverified MCP or app dependencies")

    references: list[str] = []
    if target == "claude":
        references.extend(str(a) for a in host_manifest.get("agents", []))  # type: ignore[union-attr]
        icon_ref = host_manifest.get("icon")
        if isinstance(icon_ref, str):
            references.append(icon_ref)
    elif target == "openai":
        ifaces = [m.get("interface") for m in (openai_ext, host_manifest) if m.get("interface") is not None]
        if not ifaces:
            raise ValueError("Missing OpenAI interface object")
        for iface in ifaces:
            if not isinstance(iface, dict):
                raise ValueError("Invalid OpenAI interface object")
            for key in ("composerIcon", "logo"):
                val = iface.get(key)
                if not isinstance(val, str) or not val:
                    raise ValueError(f"Missing OpenAI interface reference: {key}")
                references.append(val)
    else:
        logo_ref = portable.get("logo")
        if isinstance(logo_ref, str):
            references.append(logo_ref)
        if target in ("qwen", "gemini"):
            ctx_ref = host_manifest.get("contextFileName")
            if not isinstance(ctx_ref, str) or not ctx_ref:
                raise ValueError(f"Missing contextFileName in {first_host_file.name}")
            references.append(ctx_ref)

    for reference in references:
        ref_path = Path(reference)
        if ref_path.is_absolute() or ".." in ref_path.parts or ref_path not in files:
            raise ValueError(f"Unbundled manifest reference: {reference}")

    output_resolved.mkdir(parents=True, exist_ok=True)
    folder.mkdir()
    with tempfile.TemporaryDirectory(prefix=".egm-product-", dir=output_resolved) as tmp_dir:
        staged = Path(tmp_dir) / archive.name
        with zipfile.ZipFile(staged, "x", zipfile.ZIP_DEFLATED) as bundle:
            for relative in sorted(files):
                data = (root / relative).read_bytes()
                dest = folder / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                dest.chmod(0o644)

                info = zipfile.ZipInfo(relative.as_posix(), (1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(info, data)
        if archive.exists() or archive.is_symlink():
            raise FileExistsError(f"Archive already claimed: {archive}")
        archive.hardlink_to(staged)

    return folder, archive


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=sorted(HOST_PATTERNS))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    runtime, archive = build(Path(__file__).resolve().parents[1], args.target, args.output)
    print(f"Runtime: {runtime}\nZIP: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
