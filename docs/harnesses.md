# Multi-Harness Compatibility & Subagent Delegation (`egm-product`)

`egm-product` is packaged as a universal multi-harness Agent Plugin & CLI Extension supporting **Qwen Code (`qwen` CLI and any custom Qwen CLI fork)**, **Gemini CLI (`gemini`)**, **Antigravity (`agy`)**, **Claude Code**, **Claude Cowork**, **OpenAI Codex**, **ChatGPT Work**, and **`omp`**.

---

## 1. Installation Across All CLIs & Forks

| CLI / Harness | Native Manifests & Files | Installation Command |
| :--- | :--- | :--- |
| **Qwen Code (`qwen` CLI)** | [`qwen-extension.json`](../qwen-extension.json), [`QWEN.md`](../QWEN.md), `resources/commands/*.md`, `skills/`, `agents/` | `qwen extensions install https://github.com/Meddelin/egm-product` *(or `python scripts/install.py --target qwen`)* |
| **Custom Qwen CLI Fork** | `qwen-extension.json`, `QWEN.md`, `resources/commands/*.md`, `skills/`, `agents/` | `python scripts/install.py --target qwen --config-dir ~/.<your-cli-dir>` *(or `--project --config-dir ./.<your-cli-dir>`)* |
| **Gemini CLI (`gemini`)** | [`gemini-extension.json`](../gemini-extension.json), [`QWEN.md`](../QWEN.md), `resources/commands/*.md`, `skills/`, `agents/` | `gemini extensions install https://github.com/Meddelin/egm-product` *(or `python scripts/install.py --target gemini`)* |
| **Antigravity (`agy`)** | [`plugin.json`](../plugin.json), `rules/AGENTS.md`, `skills/`, `agents/` | `agy plugin install ./egm-product && agy plugin enable egm-product` |
| **Claude Code / Cowork** | [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json), [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) | `claude plugin marketplace add Meddelin/egm-product && claude plugin install egm-product@egm-product` |
| **OpenAI Codex** | [`.codex-plugin/plugin.json`](../.codex-plugin/plugin.json), [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json) | `codex plugin marketplace add Meddelin/egm-product && codex plugin add egm-product@egm-product` |
| **`omp` CLI** | `plugin.json`, `.claude-plugin/plugin.json` | `omp plugin marketplace add Meddelin/egm-product && omp plugin install egm-product@egm-product` |

---

## 2. Fresh-Context Goldfish Isolation Invariant

The core guarantee of the Elephant-Goldfish Model is **zero-context reviewer isolation**: when `/pm-brainstorm` or `/pm-review` spawns the 4 + 1 PM Goldfish swarm, each subagent must evaluate the artifact and repository contracts with a **fresh context window** unpolluted by the Elephant's drafting conversation history.

### Harness-Specific Subagent Delegation Matrix

| Harness | Subagent Tool | Fresh-Context Invocation Contract | Persona Source |
| :--- | :--- | :--- | :--- |
| **Qwen Code & Qwen CLI Forks** | `task` (or fork's subagent tool) | Spawn `pm-value-metrics`, `pm-tech-lead`, `pm-data-eval`, `pm-ux-risk`, and `pm-scope-slicer` registered under Extension/Custom Agents (`agents/pm_*.md`). If the fork uses a generic `task` tool without named agents, instruct the subagent to read `agents/pm_<role>.md` first and use read-only tools (`read_file`, `grep_search`, `glob`). | [`agents/pm_value_metrics.md`](../agents/pm_value_metrics.md), [`agents/pm_tech_lead.md`](../agents/pm_tech_lead.md), [`agents/pm_data_eval.md`](../agents/pm_data_eval.md), [`agents/pm_ux_risk.md`](../agents/pm_ux_risk.md), [`agents/pm_scope_slicer.md`](../agents/pm_scope_slicer.md) |
| **Gemini CLI** | Subagent / `task` tool | Spawn the named subagent from `agents/pm_*.md` (or pass the persona file path to a fresh read-only subagent task). | `./agents/pm_*.md` |
| **Antigravity** | `invoke_subagent` (with `define_subagent` if not pre-registered) | Invoke the subagent with `EnableWriteTools: false` and pass the explicit target artifact path plus `PRODUCT_CONTEXT.md` and `METRICS.md`. Wait reactively for completion notifications (never poll in a loop). | `./agents/pm_*.md` |
| **Claude Code / Cowork** | `Agent` (`subagent_type`) | Spawn `pm-value-metrics`, `pm-tech-lead`, `pm-data-eval`, `pm-ux-risk`, and `pm-scope-slicer` via the `Agent` tool. The adapter enforces `tools: [Read, Grep, Glob]` and `omitClaudeMd: true`. | [`.claude-plugin/agents/pm_value_metrics.md`](../.claude-plugin/agents/pm_value_metrics.md), [`.claude-plugin/agents/pm_tech_lead.md`](../.claude-plugin/agents/pm_tech_lead.md), [`.claude-plugin/agents/pm_data_eval.md`](../.claude-plugin/agents/pm_data_eval.md), [`.claude-plugin/agents/pm_ux_risk.md`](../.claude-plugin/agents/pm_ux_risk.md), [`.claude-plugin/agents/pm_scope_slicer.md`](../.claude-plugin/agents/pm_scope_slicer.md) |
| **OpenAI Codex / ChatGPT Work** | `spawn_agent` | Call `spawn_agent` with `fork_context: false` (or `fork_turns: "none"`) and pass the full persona prompt from `./agents/pm_<role>.md` plus the target artifact paths. | `./agents/pm_*.md` |
| **`omp` CLI** | `task` tool | Spawn the registered named subagents (`pm-value-metrics`, `pm-tech-lead`, `pm-data-eval`, `pm-ux-risk`, `pm-scope-slicer`). | `./agents/pm_*.md` |
| **Single-Agent / No Subagent Tool** | *None* | **Hard Stop on Swarm Dispatch**: Do not role-play all 5 Goldfish personas inside the Elephant's single conversation window during `/pm-review`. If subagent spawning tools are unavailable in the harness, report that fresh-context Goldfish isolation requires subagent tool support and halt the swarm step. | N/A |

---

## 3. Two-Phase 4 + 1 Swarm Orchestration Contract

Across all supported harnesses, the root **Elephant** agent owns file mutations and orchestrates the 4 + 1 swarm in two sequential phases:

1. **Phase 1 (Parallel Diagnostic Dispatch)**:
   - The Elephant spawns [`pm-value-metrics`](../agents/pm_value_metrics.md), [`pm-tech-lead`](../agents/pm_tech_lead.md), [`pm-data-eval`](../agents/pm_data_eval.md), and [`pm-ux-risk`](../agents/pm_ux_risk.md) concurrently in read-only mode.
   - Each Phase 1 subagent is strictly bounded to reading `PRODUCT_CONTEXT.md`, `METRICS.md`, the active feature artifact, and at most **8 targeted repository files (or 1,500 lines of source code)**.
   - **Retry & Degraded-Quorum Rule**: If any Phase 1 subagent fails or times out, the Elephant retries that subagent **once**. If it still fails after 1 retry, the Elephant records its status as `failed` in the `4+1 Swarm Execution Audit Table` and performs a bounded inline check (under the same 8-file cap) or marks affected requirements `UNVERIFIED (NEEDS_MANUAL_CHECK)`.

2. **Phase 2 (Sequential Read-Only Synthesis)**:
   - After all 4 Phase 1 diagnostic reports are collected, the Elephant spawns [`pm-scope-slicer`](../agents/pm_scope_slicer.md) in read-only mode, passing the 4 raw diagnostic outputs and their execution statuses (`completed | retried | failed`).
   - `pm-scope-slicer` deduplicates findings under strict **`BLOCKED_NOW > ADAPT_NOW > READY_NOW`** precedence, assigns stable `REQ-001`, `REQ-002` identifiers, and returns the compiled Markdown payload.
   - The **Elephant** writes the returned Markdown payload to `docs/product/<feature-slug>/opportunity_brief.md` (in [`/pm-brainstorm`](../skills/pm-brainstorm/SKILL.md)) or `docs/product/<feature-slug>/pm_review_report.md` (in [`/pm-review`](../skills/pm-review/SKILL.md)).

---

## 4. Coexistence with Engineering `egm`

`egm-product` is designed to run alongside the engineering `egm` plugin in the same workspace:
- **Zero Namespace Collisions**: All skills and commands are prefixed with `pm-` (`pm-discover`, `pm-brainstorm`, `pm-prd`, `pm-review`, `pm-prototype`) and all subagents are prefixed with `pm-` (`pm-value-metrics`, `pm-tech-lead`, `pm-data-eval`, `pm-ux-risk`, `pm-scope-slicer`).
- **Read-Only Consumption of `README.md` Contracts**: `/pm-discover` reads existing directory `README.md` contracts generated by `/egm-bootstrap` to accelerate capability discovery, but never modifies or overwrites any `README.md` file in the host repository.
- **Direct PRD-to-Design Handoff**: Once `/pm-review` approves `docs/product/<feature-slug>/prd.md`, the PM or Tech Lead can invoke `/egm-draft docs/product/<feature-slug>/prd.md` to generate the engineering specification at `docs/designs/<feature-slug>.md`.
