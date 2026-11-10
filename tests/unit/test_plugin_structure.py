"""Structural, manifest, frontmatter, link, icon, and template verification suite for egm-product."""

from __future__ import annotations

import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

EXPECTED_SKILLS = [
    "pm-discover",
    "pm-brainstorm",
    "pm-prd",
    "pm-review",
    "pm-prototype",
]

EXPECTED_AGENTS = {
    "pm_value_metrics.md": "pm-value-metrics",
    "pm_tech_lead.md": "pm-tech-lead",
    "pm_data_eval.md": "pm-data-eval",
    "pm_ux_risk.md": "pm-ux-risk",
    "pm_scope_slicer.md": "pm-scope-slicer",
}

ALLOWED_SVG_HEX = {"#1b6ef3", "#7cacf8", "none"}


def _parse_frontmatter(md_path: Path) -> dict[str, object]:
    """Parse simple YAML frontmatter key-value pairs without requiring external PyYAML."""
    text = md_path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{md_path} must start with YAML frontmatter delimiter '---'"
    end_idx = text.find("\n---\n", 4)
    assert end_idx != -1, f"{md_path} is missing closing YAML frontmatter delimiter '---'"
    raw_block = text[4:end_idx]
    parsed: dict[str, object] = {}
    for line in raw_block.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        assert ":" in stripped, f"Invalid frontmatter line in {md_path}: {line!r}"
        key, val = stripped.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val in ("true", "True"):
            parsed[key] = True
        elif val in ("false", "False"):
            parsed[key] = False
        elif val.startswith("[") and val.endswith("]"):
            items = [item.strip().strip("'\"") for item in val[1:-1].split(",") if item.strip()]
            parsed[key] = items
        else:
            parsed[key] = val.strip("'\"")
    return parsed


def _parse_openai_yaml(yaml_path: Path) -> dict[str, str]:
    """Parse interface block in agents/openai.yaml."""
    lines = yaml_path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0].strip() == "interface:", f"{yaml_path} must start with 'interface:'"
    result: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, val = stripped.split(":", 1)
        result[key.strip()] = val.strip().strip('"').strip("'")
    return result


# ---------------------------------------------------------------------------
# 1. Multi-Harness Manifest Parity Tests
# ---------------------------------------------------------------------------


def test_root_and_harness_manifests_are_valid_and_consistent() -> None:
    root_manifest_path = REPO_ROOT / "plugin.json"
    claude_manifest_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    claude_market_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    codex_manifest_path = REPO_ROOT / ".codex-plugin" / "plugin.json"
    agents_market_path = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
    license_path = REPO_ROOT / "LICENSE"

    for path in (
        root_manifest_path,
        claude_manifest_path,
        claude_market_path,
        codex_manifest_path,
        agents_market_path,
        license_path,
    ):
        assert path.is_file(), f"Missing required packaging file: {path}"

    root_manifest = json.loads(root_manifest_path.read_text(encoding="utf-8"))
    claude_manifest = json.loads(claude_manifest_path.read_text(encoding="utf-8"))
    claude_market = json.loads(claude_market_path.read_text(encoding="utf-8"))
    codex_manifest = json.loads(codex_manifest_path.read_text(encoding="utf-8"))
    agents_market = json.loads(agents_market_path.read_text(encoding="utf-8"))

    # Root plugin.json must omit $schema so omp does not reject disable-model-invocation: true
    assert "$schema" not in root_manifest
    assert root_manifest["name"] == "egm-product"
    assert root_manifest["version"] == "0.1.0"
    assert root_manifest["license"] == "Apache-2.0"
    openai_ext = root_manifest["extensions"]["com.openai"]
    assert openai_ext["requires_local_executor"] is True
    assert openai_ext["interface"]["brandColor"] == "#1B6EF3"
    assert (REPO_ROOT / openai_ext["interface"]["composerIcon"]).is_file()
    assert (REPO_ROOT / openai_ext["interface"]["logo"]).is_file()

    # Claude plugin.json checks
    assert claude_manifest["name"] == root_manifest["name"]
    assert claude_manifest["version"] == root_manifest["version"]
    assert claude_manifest["icon"] == "./assets/icon.svg"
    expected_claude_agent_paths = [
        f"./.claude-plugin/agents/{filename}" for filename in EXPECTED_AGENTS
    ]
    assert claude_manifest["agents"] == expected_claude_agent_paths
    for rel_agent in claude_manifest["agents"]:
        assert (REPO_ROOT / rel_agent).is_file(), f"Missing Claude adapter: {rel_agent}"

    # Codex plugin.json top-level keys check
    assert codex_manifest["name"] == root_manifest["name"]
    assert codex_manifest["version"] == root_manifest["version"]
    assert codex_manifest["skills"] == "./skills/"
    assert codex_manifest["requires_local_executor"] is True
    assert codex_manifest["interface"] == openai_ext["interface"]

    # Marketplace manifests check
    assert claude_market["name"] == "egm-product"
    assert claude_market["plugins"][0]["name"] == "egm-product"
    assert claude_market["plugins"][0]["source"] == "./"

    assert agents_market["name"] == "egm-product"
    assert agents_market["plugins"][0]["name"] == "egm-product"
    assert agents_market["plugins"][0]["source"] == {"source": "local", "path": "./"}


# ---------------------------------------------------------------------------
# 2. Skill & Subagent Frontmatter Separation Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
def test_skill_frontmatter_and_openai_yaml(skill_name: str) -> None:
    skill_dir = REPO_ROOT / "skills" / skill_name
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    icon_svg = skill_dir / "assets" / "icon.svg"

    assert skill_md.is_file(), f"Missing {skill_md}"
    assert openai_yaml.is_file(), f"Missing {openai_yaml}"
    assert icon_svg.is_file(), f"Missing {icon_svg}"

    fm = _parse_frontmatter(skill_md)
    assert fm["name"] == skill_name
    assert isinstance(fm.get("description"), str) and len(str(fm["description"])) >= 20
    assert fm["license"] == "Apache-2.0"
    assert fm["disable-model-invocation"] is True

    ui_cfg = _parse_openai_yaml(openai_yaml)
    assert "display_name" in ui_cfg and ui_cfg["display_name"].startswith("PM ")
    short_desc = ui_cfg.get("short_description", "")
    assert 25 <= len(short_desc) <= 64, (
        f"{openai_yaml} short_description must be 25-64 chars, got {len(short_desc)}: {short_desc!r}"
    )
    assert ui_cfg["icon_small"] == "./assets/icon.svg"
    assert ui_cfg["icon_large"] == "./assets/icon.svg"
    assert ui_cfg["brand_color"] == "#1B6EF3"


@pytest.mark.parametrize(("filename", "expected_name"), list(EXPECTED_AGENTS.items()))
def test_canonical_agent_and_claude_adapter_frontmatter(
    filename: str, expected_name: str
) -> None:
    canonical_path = REPO_ROOT / "agents" / filename
    adapter_path = REPO_ROOT / ".claude-plugin" / "agents" / filename

    assert canonical_path.is_file(), f"Missing canonical persona: {canonical_path}"
    assert adapter_path.is_file(), f"Missing Claude adapter: {adapter_path}"

    # Canonical persona frontmatter: strictly name, description, license (no tools key)
    canonical_fm = _parse_frontmatter(canonical_path)
    assert set(canonical_fm.keys()) == {"name", "description", "license"}, (
        f"Canonical agent {canonical_path} must only contain name, description, license in frontmatter"
    )
    assert canonical_fm["name"] == expected_name
    assert canonical_fm["license"] == "Apache-2.0"

    canonical_body = canonical_path.read_text(encoding="utf-8")
    assert "Mode: BRAINSTORM" in canonical_body
    assert "Mode: REVIEW" in canonical_body

    # Claude adapter frontmatter: includes tools, model, color, omitClaudeMd: true
    adapter_fm = _parse_frontmatter(adapter_path)
    assert adapter_fm["name"] == expected_name
    assert adapter_fm["license"] == "Apache-2.0"
    assert adapter_fm["tools"] == ["Read", "Grep", "Glob"]
    assert adapter_fm["model"] == "inherit"
    assert adapter_fm["color"] in {"blue", "cyan", "green", "red", "yellow"}
    assert adapter_fm["omitClaudeMd"] is True

    adapter_body = adapter_path.read_text(encoding="utf-8")
    assert f"${{CLAUDE_PLUGIN_ROOT}}/agents/{filename}" in adapter_body


# ---------------------------------------------------------------------------
# 3. SVG Icon Validation Tests
# ---------------------------------------------------------------------------


def test_all_svg_icons_conform_to_geometry_and_palette() -> None:
    svg_paths = [REPO_ROOT / "assets" / "icon.svg"] + [
        REPO_ROOT / "skills" / skill / "assets" / "icon.svg" for skill in EXPECTED_SKILLS
    ]
    for svg_path in svg_paths:
        assert svg_path.is_file(), f"Missing SVG icon: {svg_path}"
        tree = ET.parse(svg_path)
        root = tree.getroot()
        assert root.attrib.get("viewBox") == "0 0 24 24", f"{svg_path} must have viewBox='0 0 24 24'"
        title_elems = [elem for elem in root.iter() if elem.tag.endswith("title")]
        assert title_elems and (title_elems[0].text or "").strip(), (
            f"{svg_path} must contain a non-empty <title> element"
        )
        for elem in root.iter():
            for attr in ("fill", "stroke"):
                if attr in elem.attrib:
                    color = elem.attrib[attr].strip().lower()
                    assert color in ALLOWED_SVG_HEX, (
                        f"{svg_path} uses disallowed {attr} color {color!r}; allowed: {ALLOWED_SVG_HEX}"
                    )


# ---------------------------------------------------------------------------
# 4. Relative Markdown Link Resolution Tests
# ---------------------------------------------------------------------------

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def test_all_relative_markdown_links_resolve() -> None:
    search_roots = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "docs",
        REPO_ROOT / "skills",
        REPO_ROOT / "agents",
        REPO_ROOT / "resources",
    ]
    md_files: list[Path] = []
    for root in search_roots:
        if root.is_file():
            md_files.append(root)
        elif root.is_dir():
            md_files.extend(sorted(root.rglob("*.md")))

    assert md_files, "No Markdown files found to check"

    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        # Strip fenced code blocks before extracting links
        text_no_fences = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for match in LINK_PATTERN.finditer(text_no_fences):
            raw_target = match.group(1).strip()
            if (
                not raw_target
                or raw_target.startswith("#")
                or raw_target.startswith(("http://", "https://", "mailto:", "file://", "conversation://"))
                or "${CLAUDE_PLUGIN_ROOT}" in raw_target
            ):
                continue
            clean_target = raw_target.split("#", 1)[0]
            resolved = (md_file.parent / clean_target).resolve()
            assert resolved.exists(), (
                f"Broken relative link in {md_file.relative_to(REPO_ROOT)}: "
                f"{raw_target!r} -> {resolved} does not exist"
            )


# ---------------------------------------------------------------------------
# 5. Template Section Headers & Line Cap Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("template_name", "required_headers"),
    [
        (
            "product_context.template.md",
            [
                "## Machine-Discovered Context (Auto-Refreshed)",
                "## Human-Curated Strategy (Preserved Across Runs)",
            ],
        ),
        (
            "metrics.template.md",
            [
                "## Human-Curated Metric Targets (Preserved Across Runs)",
                "## Machine-Discovered Telemetry Inventory (Auto-Refreshed)",
            ],
        ),
        (
            "opportunity_brief.template.md",
            [
                "## 4+1 Swarm Execution Audit Table",
                "## Overview & Metric Causal Chain",
                "## Cross-Functional Reality Check Matrix",
                "## Goals vs. Non-Goals",
                "## Alternatives Weighed",
                "## Prerequisite Ledger (BLOCKED_NOW)",
            ],
        ),
        (
            "prd.template.md",
            [
                "## Overview",
                "## The Problem",
                "## Goals",
                "## Non-Goals",
                "## Metrics & Telemetry Contract",
                "## Critical User Journeys (CUJs)",
                "### UX State & Fallback Matrix",
                "## Scope Classification (READY_NOW / ADAPT_NOW)",
                "## Data, Quality & Evaluation Gates",
                "## Security, Cost & Operational Guardrails",
                "## Alternatives Considered (Alternatives Weighed)",
                "## Prerequisite Ledger (BLOCKED_NOW)",
            ],
        ),
    ],
)
def test_templates_enforce_line_caps_and_required_sections(
    template_name: str, required_headers: list[str]
) -> None:
    template_path = REPO_ROOT / "resources" / "templates" / template_name
    assert template_path.is_file(), f"Missing template: {template_path}"
    content = template_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) <= 300, (
        f"Template {template_name} exceeds 300-line cap ({len(lines)} lines)"
    )
    for header in required_headers:
        assert header in content, (
            f"Template {template_name} is missing required section header: {header!r}"
        )


# ---------------------------------------------------------------------------
# 6. End-to-End Pipeline & Behavioral Invariant Tests
# ---------------------------------------------------------------------------


def test_end_to_end_pipeline_invariants_across_skills_and_agents() -> None:
    # Every skill must load ../../resources/execution_instructions.md
    for skill_name in EXPECTED_SKILLS:
        skill_text = (REPO_ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "../../resources/execution_instructions.md" in skill_text, (
            f"{skill_name}/SKILL.md must link to ../../resources/execution_instructions.md"
        )

    # pm-brainstorm and pm-prd must include the Inline Bootstrap Recovery Gate to ../pm-discover/SKILL.md
    for skill_name in ("pm-brainstorm", "pm-prd"):
        skill_text = (REPO_ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "Inline Bootstrap Recovery Gate" in skill_text
        assert "../pm-discover/SKILL.md" in skill_text

    # pm-value-metrics must map INSTRUMENTATION_REQUIRED to ADAPT_NOW
    value_metrics_text = (REPO_ROOT / "agents" / "pm_value_metrics.md").read_text(encoding="utf-8")
    assert "INSTRUMENTATION_REQUIRED" in value_metrics_text
    assert "ADAPT_NOW" in value_metrics_text

    # pm-scope-slicer must enforce strict BLOCKED_NOW > ADAPT_NOW > READY_NOW precedence
    slicer_text = (REPO_ROOT / "agents" / "pm_scope_slicer.md").read_text(encoding="utf-8")
    assert "BLOCKED_NOW > ADAPT_NOW > READY_NOW" in slicer_text
    assert "## 4+1 Swarm Execution Audit Table" in slicer_text

    # pm-prototype must enforce 400-line cap, zero external network requests, and Stageshow craft rules
    proto_text = (REPO_ROOT / "skills" / "pm-prototype" / "SKILL.md").read_text(encoding="utf-8")
    assert "400 lines" in proto_text
    assert "Zero External Network Requests" in proto_text
    assert "tabular-nums" in proto_text
    assert "stageshow-critic" in proto_text

