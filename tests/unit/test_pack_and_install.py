"""Tests for reproducible pack_plugin.py archives and collision-safe install.py coexistence with engineering egm."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import zipfile

import pytest

from scripts.install import main as install_main
from scripts.pack_plugin import HOST_PATTERNS, build
from tests.unit.test_plugin_structure import EXPECTED_SKILLS, REPO_ROOT, check_markdown_links_in_root


@pytest.mark.parametrize("target", sorted(HOST_PATTERNS))
def test_pack_plugin_builds_clean_reproducible_bundles(target: str, tmp_path: Path) -> None:
    first_folder, first_zip = build(REPO_ROOT, target, tmp_path / "run1")
    _, second_zip = build(REPO_ROOT, target, tmp_path / "run2")

    assert first_zip.read_bytes() == second_zip.read_bytes(), "ZIP output must be byte-for-byte deterministic"

    with zipfile.ZipFile(first_zip) as zf:
        assert zf.testzip() is None
        names = set(zf.namelist())
        assert len([n for n in names if n.endswith("/SKILL.md")]) == len(EXPECTED_SKILLS)
        assert "resources/pm_execution_instructions.md" in names
        assert "resources/document_standards/prd-standard.md" in names
        assert "assets/icon.svg" in names

        # Dev, test, design docs, and marketplace catalogs must never leak into runtime archives
        assert not any(
            n.startswith(("tests/", "docs/designs/", ".dev/", ".agents/", "scripts/"))
            or n.endswith("marketplace.json")
            or "__pycache__" in n
            for n in names
        )
        assert (".claude-plugin/plugin.json" in names) == (target == "claude")
        assert (".codex-plugin/plugin.json" in names) == (target == "openai")
        assert ("rules/AGENTS.md" in names) == (target == "antigravity")

        for info in zf.infolist():
            assert info.date_time == (1980, 1, 1, 0, 0, 0)
            assert info.external_attr >> 16 == 0o100644

    # Relative Markdown links inside the built runtime folder must all resolve cleanly
    check_markdown_links_in_root(first_folder)


def test_pack_plugin_rejects_overwrites_and_escaping_manifest_refs(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    build(REPO_ROOT, "openai", out_dir)
    with pytest.raises(ValueError, match="already exists"):
        build(REPO_ROOT, "openai", out_dir)

    # Copy minimal source tree to test manifest path escape rejection
    staged_src = tmp_path / "staged_src"
    shutil.copytree(
        REPO_ROOT,
        staged_src,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__", ".dev"),
    )
    manifest_path = staged_src / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["extensions"]["com.openai"]["interface"]["logo"] = "../escape.svg"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(ValueError, match="Unbundled manifest reference"):
        build(staged_src, "openai", tmp_path / "escaped_out")


def test_installer_coexists_with_engineering_egm_and_uninstalls_cleanly(tmp_path: Path) -> None:
    fork_dir = tmp_path / ".custom-qwen-fork"
    # Pre-populate engineering egm files that previously collided in flat mode!
    egm_exec = fork_dir / "resources" / "execution_instructions.md"
    egm_harnesses = fork_dir / "docs" / "harnesses.md"
    egm_skill = fork_dir / "skills" / "egm-draft" / "SKILL.md"
    for p in (egm_exec, egm_harnesses, egm_skill):
        p.parent.mkdir(parents=True, exist_ok=True)
    egm_exec.write_text("ENGINEERING EGM EXECUTION INSTRUCTIONS", encoding="utf-8")
    egm_harnesses.write_text("ENGINEERING EGM HARNESSES DOC", encoding="utf-8")
    egm_skill.write_text("ENGINEERING EGM DRAFT SKILL", encoding="utf-8")

    # 1. Default install mode is isolated 'extension' (zero flat files written unless requested)
    rc = install_main(["--target", "qwen", "--config-dir", str(fork_dir)])
    assert rc == 0
    ext_root = fork_dir / "extensions" / "egm-product"
    assert (ext_root / "qwen-extension.json").is_file()
    assert not (ext_root / "design_draft.md").exists()
    assert not (ext_root / "tests").exists()
    assert not (fork_dir / "skills" / "pm-discover").exists()

    # Pre-populate legacy pre-v0.4.0 flat pm-* files to verify upgrade cleanup!
    legacy_skill = fork_dir / "skills" / "pm-status" / "SKILL.md"
    legacy_cmd = fork_dir / "commands" / "pm-review.md"
    legacy_agent = fork_dir / "agents" / "pm_tech_lead.md"
    legacy_tmpl = fork_dir / "resources" / "templates" / "portfolio_status.template.md"
    for lp in (legacy_skill, legacy_cmd, legacy_agent, legacy_tmpl):
        lp.parent.mkdir(parents=True, exist_ok=True)
        lp.write_text("LEGACY PRE-V0.4.0 ARTIFACT", encoding="utf-8")

    # 2. Explicit '--mode both' installs flat namespaced pm-* files, purges legacy pm-* artifacts, and NEVER touches engineering egm!
    rc_both = install_main(["--target", "qwen", "--config-dir", str(fork_dir), "--mode", "both"])
    assert rc_both == 0
    assert egm_exec.read_text(encoding="utf-8") == "ENGINEERING EGM EXECUTION INSTRUCTIONS"
    assert egm_harnesses.read_text(encoding="utf-8") == "ENGINEERING EGM HARNESSES DOC"
    assert egm_skill.read_text(encoding="utf-8") == "ENGINEERING EGM DRAFT SKILL"
    assert not legacy_skill.exists()
    assert not legacy_cmd.exists()
    assert not legacy_agent.exists()
    assert not legacy_tmpl.exists()

    for skill_name in EXPECTED_SKILLS:
        flat_skill = fork_dir / "skills" / skill_name / "SKILL.md"
        flat_cmd = fork_dir / "commands" / f"{skill_name}.md"
        assert flat_skill.is_file()
        assert flat_cmd.is_file()
        assert (flat_skill.parent / "../../resources/pm_execution_instructions.md").resolve().is_file()
        assert (flat_skill.parent / "../../docs/egm-product/codex.md").resolve().is_file()
        assert (flat_cmd.parent / f"../skills/{skill_name}/SKILL.md").resolve().is_file()
        assert (flat_cmd.parent / "../resources/pm_execution_instructions.md").resolve().is_file()

    # Verify all relative links inside flat-installed docs/egm-product, skills/pm-*, agents/pm_*, and resources/ resolve!
    check_markdown_links_in_root(fork_dir)

    # 3. '--uninstall' removes egm-product cleanly while preserving all engineering egm files!
    rc_un = install_main(["--target", "qwen", "--config-dir", str(fork_dir), "--uninstall"])
    assert rc_un == 0
    assert not ext_root.exists()
    assert not (fork_dir / "skills" / "pm-discover").exists()
    assert not (fork_dir / "resources" / "pm_execution_instructions.md").exists()
    assert egm_exec.read_text(encoding="utf-8") == "ENGINEERING EGM EXECUTION INSTRUCTIONS"
    assert egm_harnesses.read_text(encoding="utf-8") == "ENGINEERING EGM HARNESSES DOC"
    assert egm_skill.read_text(encoding="utf-8") == "ENGINEERING EGM DRAFT SKILL"
