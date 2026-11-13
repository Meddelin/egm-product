# Multi-Harness Compatibility & Subagent Delegation (`egm-product`)

`egm-product` is a single source of pure-product skills, personas, templates, and standards shared across **Antigravity (`agy`)**, **Claude Code**, **Claude Cowork**, **OpenAI Codex**, **ChatGPT Work**, **Qwen Code (`qwen` CLI & forks)**, **Gemini CLI (`gemini`)**, and **`omp`**.

---

## 1. Installation & Manifest Mapping

| Harness | Native Manifests & Context | Installation Command | Invocation |
| :--- | :--- | :--- | :--- |
| **Antigravity (`agy`)** | `plugin.json`, `rules/AGENTS.md`, `skills/`, `agents/` | `python scripts/install.py --target antigravity` *(or `agy plugin install ./egm-product`)* | `/pm-discover`, `/pm-brainstorm`, `/pm-prd`, `/pm-prototype` |
| **Claude Code / Cowork** | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, [Claude guide](./claude.md) | `claude plugin marketplace add Meddelin/egm-product && claude plugin install egm-product@egm-product` | `/egm-product:pm-discover`, `/egm-product:pm-brainstorm`, `/egm-product:pm-prd`, `/egm-product:pm-prototype` |
| **OpenAI Codex / ChatGPT** | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, [Codex guide](./codex.md) | `codex plugin marketplace add Meddelin/egm-product && codex plugin add egm-product@egm-product` *(ChatGPT ZIP: `pack_plugin.py --target openai`)* | Select `pm-*` skill / `@egm-product` |
| **Qwen Code & Forks** | `qwen-extension.json`, `QWEN.md`, `resources/commands/*.md` | `qwen extensions install ./egm-product` *(or `python scripts/install.py --target qwen --config-dir ~/.fork`)* | `/pm-discover`, `/pm-brainstorm`, `/pm-prd`, `/pm-prototype` |
| **Gemini CLI (`gemini`)** | `gemini-extension.json`, `GEMINI_EXTENSION.md`, `resources/commands/*.md` | `gemini extensions install ./egm-product` *(or `python scripts/install.py --target gemini`)* | `/pm-discover`, `/pm-brainstorm`, `/pm-prd`, `/pm-prototype` |
| **`omp` CLI** | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | `omp plugin marketplace add Meddelin/egm-product && omp plugin install egm-product@egm-product` | `/skill:pm-discover`, `/skill:pm-brainstorm`, `/skill:pm-prd`, `/skill:pm-prototype` |

---

## 2. Fresh-Context Product Goldfish Isolation Invariant

Every subagent in `egm-product` (`pm-product-scanner`, `pm-value-strategy`, `pm-ux-flows`, `pm-metrics-experiment`, `pm-business-logic`, `pm-synthesizer`) must run in a **fresh context window** unpolluted by the Elephant's conversation history.

### Harness-Specific Subagent Delegation Matrix

| Harness | Subagent Tool | Fresh-Context Invocation Contract | Persona Source |
| :--- | :--- | :--- | :--- |
| **Antigravity** | `invoke_subagent` | Call `invoke_subagent` with `TypeName` set to the registered persona name (e.g. `"pm-value-strategy"`), `Role`, and `Prompt` containing explicit target paths (`PRODUCT_CONTEXT.md`, `METRICS.md`, artifact). Only call `define_subagent` (`EnableWriteTools: false`) if running loose files outside an installed plugin. Wait reactively without polling. | [`agents/pm_*.md`](../agents/pm_value_strategy.md) |
| **Claude Code / Cowork** | `Agent` (`subagent_type`) | Spawn `egm-product:pm-<role>` via the `Agent` tool. Adapters enforce `tools: [Read, Grep, Glob]` and `omitClaudeMd: true`. See [Claude integration](./claude.md) for `/permissions` cache read rules. | `.claude-plugin/agents/pm_*.md` |
| **OpenAI Codex / ChatGPT** | `spawn_agent` | Call `spawn_agent` with `fork_context: false` (or `fork_turns: "none"`) and pass absolute paths to `./agents/pm_<role>.md`, standards, contracts, and the target artifact. See [Codex integration](./codex.md). | `./agents/pm_*.md` |
| **Qwen Code / Gemini CLI** | `task` / subagent tool | Spawn registered named subagents (`pm-value-strategy`, etc.) or instruct a fresh read-only `task` worker to read `agents/pm_<role>.md` first. | `./agents/pm_*.md` |
| **`omp` CLI** | `task` tool | Spawn registered named subagents (`pm-product-scanner`, `pm-value-strategy`, `pm-ux-flows`, `pm-metrics-experiment`, `pm-business-logic`, `pm-synthesizer`). | `./agents/pm_*.md` |
| **No Subagent Tool** | *None* | **Hard Stop on 4+1 Product Goldfish Swarms (`/pm-brainstorm` & `/pm-prd` review)**: Never simulate all 4 product critics inside the Elephant's single conversation window; stop and report that fresh-context subagent tools are required. Single-pass helpers (`/pm-discover` and `/pm-prototype`) permit bounded inline fallback. | N/A |

---

## 3. Two-Phase 4 + 1 Product Goldfish Swarm Contract

1. **Phase 1 (Parallel Product Critics)**:
   - The Elephant spawns [`pm-value-strategy`](../agents/pm_value_strategy.md), [`pm-ux-flows`](../agents/pm_ux_flows.md), [`pm-metrics-experiment`](../agents/pm_metrics_experiment.md), and [`pm-business-logic`](../agents/pm_business_logic.md) concurrently in read-only mode.
   - **Retry Rule**: Retry any failed Phase 1 critic **once**. If it still fails, record status `failed` in `## 4+1 Product Goldfish Audit Summary`.
2. **Phase 2 (Sequential Read-Only Synthesis)**:
   - Pass all 4 critic outputs and their statuses (`completed | retried | failed`) to [`pm-synthesizer`](../agents/pm_synthesizer.md), which deduplicates findings and returns the compiled Markdown for the Elephant to write to disk.

---

## 4. Artifact Directory Override & Coexistence with Engineering `egm`

* **Zero Namespace Collisions**: Skills (`pm-*`), subagents (`pm-*`), and shared instructions ([`resources/pm_execution_instructions.md`](../resources/pm_execution_instructions.md)) are strictly namespaced so installing `egm-product` alongside engineering `egm` never overwrites `egm` files.
* **Scratch / Working Report Override**: Committed product deliverables live in `docs/product/<feature-slug>/`. Add `EGM artifact directory: .dev/docs` to your prompt, `CLAUDE.md`, or `AGENTS.md` to route `pm_review_report.md` and working scratch reports to `.dev/docs/`.
* **Clean Product-to-Engineering Boundary**: [`/pm-prd`](../skills/pm-prd/SKILL.md) focuses strictly on *what, for whom, and why*, placing an **Engineering Handoff Directive** at the top of `prd.md` so `/egm-draft docs/product/<feature-slug>/prd.md` takes over technical architecture and writes `docs/designs/<feature-slug>.md`.
