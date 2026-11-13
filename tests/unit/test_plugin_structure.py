"""Structural, manifest, YAML frontmatter, OpenAI/Antigravity limit, link, icon, and pure-product invariant tests for egm-product."""

from __future__ import annotations

import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

EXPECTED_SKILLS = [
    "pm-discover",
    "pm-brainstorm",
    "pm-prd",
    "pm-prototype",
]

EXPECTED_AGENTS = {
    "pm_product_scanner.md": "pm-product-scanner",
    "pm_value_strategy.md": "pm-value-strategy",
    "pm_ux_flows.md": "pm-ux-flows",
    "pm_metrics_experiment.md": "pm-metrics-experiment",
    "pm_business_logic.md": "pm-business-logic",
    "pm_synthesizer.md": "pm-synthesizer",
}

ALLOWED_SVG_HEX = {"#1b6ef3", "#7cacf8", "none"}
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _parse_frontmatter(md_path: Path) -> dict[str, object]:
    """Parse YAML frontmatter strictly using PyYAML."""
    text = md_path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{md_path} must start with YAML frontmatter delimiter '---'"
    parts = text.split("---", 2)
    assert len(parts) == 3, f"{md_path} is missing closing YAML frontmatter delimiter '---'"
    parsed = yaml.safe_load(parts[1])
    assert isinstance(parsed, dict), f"{md_path} frontmatter must parse to a mapping"
    return parsed


# ---------------------------------------------------------------------------
# 1. Multi-Harness Manifest Parity & OpenAI Submission Limits
# ---------------------------------------------------------------------------


def test_root_and_harness_manifests_are_valid_consistent_and_within_limits() -> None:
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

    # Root plugin.json omits $schema so omp does not reject disable-model-invocation: true
    assert "$schema" not in root_manifest
    assert root_manifest["name"] == "egm-product"
    assert root_manifest["version"] == "0.4.0"
    assert root_manifest["license"] == "Apache-2.0"
    assert len(root_manifest["suggestedPrompts"]) == 3

    openai_ext = root_manifest["extensions"]["com.openai"]
    assert openai_ext["requires_local_executor"] is True
    iface = openai_ext["interface"]
    assert iface["brandColor"] == "#1B6EF3"

    # Strict OpenAI Plugin Directory field length ceilings
    for field, limit in (
        ("displayName", 30),
        ("shortDescription", 30),
        ("longDescription", 4000),
        ("developerName", 80),
    ):
        assert 0 < len(iface[field]) <= limit, (
            f"interface.{field} length {len(iface[field])} exceeds limit {limit}: {iface[field]!r}"
        )
    assert 0 < len(iface["capabilities"]) <= 20
    assert all(0 < len(item) <= 120 for item in iface["capabilities"])
    assert (REPO_ROOT / iface["composerIcon"]).is_file()
    assert (REPO_ROOT / iface["logo"]).is_file()

    # Claude plugin.json parity
    for shared_key in ("name", "version", "description", "author", "homepage", "repository", "license"):
        assert claude_manifest[shared_key] == root_manifest[shared_key]
    assert claude_manifest["icon"] == "./assets/icon.svg"
    expected_claude_agent_paths = [
        f"./.claude-plugin/agents/{filename}" for filename in EXPECTED_AGENTS
    ]
    assert claude_manifest["agents"] == expected_claude_agent_paths
    for rel_agent in claude_manifest["agents"]:
        assert (REPO_ROOT / rel_agent).is_file(), f"Missing Claude adapter: {rel_agent}"

    # Codex plugin.json parity
    for shared_key in ("name", "version", "description", "author", "homepage", "repository", "license"):
        assert codex_manifest[shared_key] == root_manifest[shared_key]
    assert codex_manifest["skills"] == "./skills/"
    assert codex_manifest["requires_local_executor"] is True
    assert codex_manifest["interface"] == iface

    # Marketplace catalogs resolve cleanly to REPO_ROOT
    for market_name, market in (("claude", claude_market), ("agents", agents_market)):
        assert market["name"] == "egm-product"
        assert len(market["plugins"]) == 1
        entry = market["plugins"][0]
        assert entry["name"] == "egm-product"
        assert isinstance(entry["source"], str), f"{market_name} marketplace source must be a string path"
        assert (REPO_ROOT / entry["source"]).resolve() == REPO_ROOT

    assert agents_market["plugins"][0]["policy"] == {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }
    assert agents_market["plugins"][0]["category"] == "Productivity"


# ---------------------------------------------------------------------------
# 2. Skill Body Size Limits, Multi-Harness Headers & Frontmatter Separation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
def test_skill_frontmatter_load_limits_and_harness_links(skill_name: str) -> None:
    skill_dir = REPO_ROOT / "skills" / skill_name
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    icon_svg = skill_dir / "assets" / "icon.svg"

    assert skill_md.is_file()
    assert openai_yaml.is_file()
    assert icon_svg.is_file()

    fm = _parse_frontmatter(skill_md)
    assert fm["name"] == skill_name
    assert isinstance(fm.get("description"), str) and len(str(fm["description"])) >= 20
    assert fm["license"] == "Apache-2.0"
    assert fm["disable-model-invocation"] is True

    raw_text = skill_md.read_text(encoding="utf-8")
    body = raw_text.split("---", 2)[2].strip()
    assert len(body.encode("utf-8")) <= 24_000, f"{skill_name} exceeds Antigravity 24KB skill body limit"

    # Every skill must link Codex guide, Claude ${CLAUDE_PLUGIN_ROOT} guide, and pm_execution_instructions.md
    assert "[Codex integration](../../docs/codex.md)" in body
    assert "${CLAUDE_PLUGIN_ROOT}/docs/claude.md" in body
    assert "../../resources/pm_execution_instructions.md" in body
    assert "${CLAUDE_PLUGIN_ROOT}/resources/pm_execution_instructions.md" in body

    ui_meta = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
    ui_cfg = ui_meta["interface"]
    assert ui_cfg["display_name"].startswith("PM ")
    short_desc = ui_cfg["short_description"]
    assert 25 <= len(short_desc) <= 64
    assert ui_cfg["icon_small"] == "./assets/icon.svg"
    assert ui_cfg["icon_large"] == "./assets/icon.svg"
    assert ui_cfg["brand_color"] == "#1B6EF3"


@pytest.mark.parametrize(("filename", "expected_name"), list(EXPECTED_AGENTS.items()))
def test_canonical_agent_and_claude_adapter_frontmatter(
    filename: str, expected_name: str
) -> None:
    canonical_path = REPO_ROOT / "agents" / filename
    adapter_path = REPO_ROOT / ".claude-plugin" / "agents" / filename

    assert canonical_path.is_file()
    assert adapter_path.is_file()

    canonical_fm = _parse_frontmatter(canonical_path)
    assert set(canonical_fm.keys()) == {"name", "description", "license"}
    assert canonical_fm["name"] == expected_name
    assert canonical_fm["license"] == "Apache-2.0"

    adapter_fm = _parse_frontmatter(adapter_path)
    assert adapter_fm["name"] == expected_name
    assert adapter_fm["description"] == canonical_fm["description"]
    assert adapter_fm["license"] == "Apache-2.0"
    assert adapter_fm["tools"] == ["Read", "Grep", "Glob"]
    assert adapter_fm["model"] == "inherit"
    assert adapter_fm["color"] in {"blue", "cyan", "green", "red", "yellow"}
    assert adapter_fm["omitClaudeMd"] is True
    assert "memory" not in adapter_fm
    assert f"${{CLAUDE_PLUGIN_ROOT}}/agents/{filename}" in adapter_path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 3. SVG Icon Dimensions, Geometry & Palette Validation
# ---------------------------------------------------------------------------


def test_all_svg_icons_conform_to_dimensions_geometry_and_palette() -> None:
    root_icon = REPO_ROOT / "assets" / "icon.svg"
    skill_icons = [REPO_ROOT / "skills" / skill / "assets" / "icon.svg" for skill in EXPECTED_SKILLS]

    for svg_path in [root_icon, *skill_icons]:
        assert svg_path.is_file()
        root = ET.parse(svg_path).getroot()
        assert root.attrib.get("viewBox") == "0 0 24 24"
        width = float(root.attrib["width"])
        height = float(root.attrib["height"])
        min_dim = 128 if svg_path == root_icon else 48
        assert width == height >= min_dim, f"{svg_path} must be square >= {min_dim}px, got {width}x{height}"
        title_elems = [elem for elem in root.iter() if elem.tag.endswith("title")]
        assert title_elems and (title_elems[0].text or "").strip()
        for elem in root.iter():
            for attr in ("fill", "stroke"):
                if attr in elem.attrib:
                    color = elem.attrib[attr].strip().lower()
                    assert color in ALLOWED_SVG_HEX


# ---------------------------------------------------------------------------
# 4. Relative Link Resolution & Rules / Harness Integrity
# ---------------------------------------------------------------------------


def check_markdown_links_in_root(base_root: Path) -> None:
    search_roots = [
        base_root / "README.md",
        base_root / "QWEN.md",
        base_root / "GEMINI_EXTENSION.md",
        base_root / "docs",
        base_root / "skills",
        base_root / "agents",
        base_root / "resources",
        base_root / "rules",
        base_root / "commands",
    ]
    md_files: list[Path] = []
    for root in search_roots:
        if root.is_file():
            md_files.append(root)
        elif root.is_dir():
            md_files.extend(sorted(root.rglob("*.md")))

    assert md_files, f"No Markdown files found in {base_root}"

    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        text_no_fences = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for match in LINK_PATTERN.finditer(text_no_fences):
            raw_target = match.group(1).strip().strip("<>")
            if (
                not raw_target
                or raw_target.startswith("#")
                or raw_target.startswith(("http://", "https://", "mailto:", "file://", "conversation://", "/absolute/"))
                or "${CLAUDE_PLUGIN_ROOT}" in raw_target
            ):
                continue
            clean_target = raw_target.split("#", 1)[0]
            resolved = (md_file.parent / clean_target).resolve()
            assert resolved.exists(), (
                f"Broken relative link in {md_file.relative_to(base_root)}: "
                f"{raw_target!r} -> {resolved} does not exist"
            )


def test_all_relative_markdown_links_and_rules_routing_resolve() -> None:
    check_markdown_links_in_root(REPO_ROOT)

    # rules/AGENTS.md must use portable relative paths (zero ~/.gemini hardcoding)
    rules_text = (REPO_ROOT / "rules" / "AGENTS.md").read_text(encoding="utf-8")
    assert "~/.gemini" not in rules_text
    for skill_name in EXPECTED_SKILLS:
        assert f"../skills/{skill_name}/SKILL.md" in rules_text

    # Removed technical stages must not exist anywhere in skills/ or commands/
    for removed_stage in ("pm-review", "pm-status"):
        assert not (REPO_ROOT / "skills" / removed_stage).exists()
        assert not (REPO_ROOT / "resources" / "commands" / f"{removed_stage}.md").exists()

    # Scratch/working report files must never sit in REPO_ROOT
    for forbidden_root_doc in (
        "design_draft.md",
        "concepts_brief.md",
        "critic_report.md",
        "comprehension_report.md",
        "implementation_readiness_report.md",
        "zoom_out_report.md",
    ):
        assert not (REPO_ROOT / forbidden_root_doc).exists(), (
            f"Scratch report {forbidden_root_doc} must live in .dev/docs/, not repo root"
        )


# ---------------------------------------------------------------------------
# 5. Template Section Headers, Top-Level Handoff Directive & Line Caps
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("template_name", "line_cap", "required_headers"),
    [
        (
            "company_context.template.md",
            200,
            [
                "## 1. Organization Profile & Strategic Priorities",
                "## 2. Organizational Role Directory (Context Only — Not Assumed Product Users)",
                "## 3. Shared Domain Glossary",
                "## 4. Business Governance, Privacy & Approval Norms",
            ],
        ),
        (
            "product_context.template.md",
            250,
            [
                "## 1. Existing Product Surface (Observed User Capabilities)",
                "## 2. Product Identity, Company Context & Strategy (Human-Curated)",
                "## 3. Active Product Roles & Workflows (Empirical — Zero Assumed Personas)",
                "Customer & Problem Evidence Sources",
            ],
        ),
        (
            "metrics.template.md",
            200,
            [
                "## 1. Product Metric Tree",
                "## 2. Domain Product Events & Rollout Norms",
            ],
        ),
        (
            "opportunity_brief.template.md",
            200,
            [
                "## 4+1 Product Goldfish Audit Summary",
                "## 1. Problem, Evidence & Causal Hypothesis",
                "Affected Product Roles",
                "Demand Evidence Posture",
                "Validation Hypothesis & Kill/Pivot Criterion",
                "## 2. Proposed Product Solution & MVP Scope Cut",
                "## 3. Product Alternatives Weighed",
                "## 4. Key Risks & Open Questions for Engineering",
            ],
        ),
        (
            "prd.template.md",
            250,
            [
                "Engineering Handoff Directive (`/egm-draft` & Coding Agents)",
                "## 1. Problem & Strategic Context",
                "Demand Evidence Posture",
                "## 2. Goals & Non-Goals",
                "## 3. Target Roles & Critical User Journeys (CUJs)",
                "### Cross-Role Handoffs & Permissions",
                "## 4. Functional Requirements, Business Rules & Edge Cases",
                "## 5. UX States & Copy Guidelines",
                "## 6. Success Metrics, Product Events & Rollout Plan",
                "## 7. Alternatives Considered & Open Questions for Engineering",
            ],
        ),
    ],
)
def test_templates_enforce_line_caps_and_required_sections(
    template_name: str, line_cap: int, required_headers: list[str]
) -> None:
    template_path = REPO_ROOT / "resources" / "templates" / template_name
    assert template_path.is_file()
    content = template_path.read_text(encoding="utf-8")
    assert len(content.splitlines()) <= line_cap
    for header in required_headers:
        assert header in content, f"{template_name} missing {header!r}"

    if template_name == "prd.template.md":
        assert content.index("Engineering Handoff Directive") < content.index("## 1. Problem & Strategic Context")


# ---------------------------------------------------------------------------
# 6. Pure-Product Boundary & 4+1 Swarm Behavioral Invariants
# ---------------------------------------------------------------------------


def test_pure_product_boundary_and_4_plus_1_swarm_invariants() -> None:
    # Ensure zero engineering-grooming bloat remains in templates, standards, skills, or agents
    forbidden_technical_tokens = (
        ".pm/schemas.md",
        "READY_NOW",
        "ADAPT_NOW",
        "BLOCKED_NOW",
        "Prerequisite Ledger",
        "generated_at_commit",
        "[file:symbol_or_line]",
        "pm-tech-lead",
        "pm-data-eval",
        "pm-security-ops",
        "pm-scope-slicer",
        "pm-repo-scanner",
    )
    runtime_dirs = [
        REPO_ROOT / "skills",
        REPO_ROOT / "agents",
        REPO_ROOT / ".claude-plugin" / "agents",
        REPO_ROOT / "resources",
        REPO_ROOT / "rules",
    ]
    for directory in runtime_dirs:
        for md_file in directory.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            for forbidden in forbidden_technical_tokens:
                assert forbidden not in text, (
                    f"Technical bloat token {forbidden!r} leaked into pure-product file {md_file.relative_to(REPO_ROOT)}"
                )

    # pm-discover uses light pm-product-scanner and supports --scope and --context with Zero Assumed Personas
    discover_text = (REPO_ROOT / "skills" / "pm-discover" / "SKILL.md").read_text(encoding="utf-8")
    assert "pm-product-scanner" in discover_text
    assert "--scope <subdir>" in discover_text
    assert "--context <path>" in discover_text
    assert "Zero Assumed Personas" in discover_text

    # pm-prd includes built-in 4+1 Product Goldfish Review Loop
    prd_skill_text = (REPO_ROOT / "skills" / "pm-prd" / "SKILL.md").read_text(encoding="utf-8")
    for lens in ("pm-value-strategy", "pm-ux-flows", "pm-metrics-experiment", "pm-business-logic", "pm-synthesizer"):
        assert lens in prd_skill_text
    assert "Inline Bootstrap Recovery Gate" in prd_skill_text

    # pm-prototype verifies craft via pm-ux-flows Mode: PROTOTYPE_AUDIT and conditional Role switcher
    proto_text = (REPO_ROOT / "skills" / "pm-prototype" / "SKILL.md").read_text(encoding="utf-8")
    assert "Mode: PROTOTYPE_AUDIT" in proto_text
    assert "pm-ux-flows" in proto_text
    assert "400 lines" in proto_text
    assert "Zero External Network Requests" in proto_text
    assert "Role` switcher" in proto_text

    # pm_execution_instructions enforces Zero Assumed Personas and Progression vs. Neutral Trade-Off Gates
    exec_text = (REPO_ROOT / "resources" / "pm_execution_instructions.md").read_text(encoding="utf-8")
    assert "Zero Assumed Personas" in exec_text
    assert "Progression Gates" in exec_text
    assert "Trade-Off & Escalation Gates" in exec_text
    assert "Owner Decides Product Scope" in exec_text

    # Qwen & Gemini extension parity
    qwen_ext = json.loads((REPO_ROOT / "qwen-extension.json").read_text(encoding="utf-8"))
    gemini_ext = json.loads((REPO_ROOT / "gemini-extension.json").read_text(encoding="utf-8"))
    assert qwen_ext["contextFileName"] == "QWEN.md"
    assert gemini_ext["contextFileName"] == "GEMINI_EXTENSION.md"
    for ext in (qwen_ext, gemini_ext):
        assert ext["version"] == "0.4.0"
        assert ext["commands"] == "resources/commands"
        assert ext["skills"] == "skills"
        assert ext["agents"] == "agents"

    for cmd_name in EXPECTED_SKILLS:
        cmd_path = REPO_ROOT / "resources" / "commands" / f"{cmd_name}.md"
        assert cmd_path.is_file()
        fm = _parse_frontmatter(cmd_path)
        assert isinstance(fm.get("description"), str) and len(str(fm["description"])) >= 20
        cmd_text = cmd_path.read_text(encoding="utf-8")
        assert "{{args}}" in cmd_text
        assert f"../../skills/{cmd_name}/SKILL.md" in cmd_text
