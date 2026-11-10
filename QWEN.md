# EGM Product (`egm-product`) — Context & Routing for Qwen Code / Qwen CLI Forks

`egm-product` is an AI-native Product Management framework built on the **Elephant-Goldfish Model (EGM)**. Whenever the user invokes a `/pm-*` command or asks for Product Management workflows (discovering product context/metrics, brainstorming feature scope, writing or reviewing a PRD, or building an interactive HTML prototype from a PRD), load and follow the corresponding skill and subagent personas from this extension/plugin directory (`./skills/`, `./agents/`, `./resources/`).

---

## 1. 5-Stage Product Pipeline & Skill Paths

| Stage / Slash Command | Skill File to Read | Primary Deliverable |
| :--- | :--- | :--- |
| **Stage 1: `/pm-discover`** | [`skills/pm-discover/SKILL.md`](./skills/pm-discover/SKILL.md) | `PRODUCT_CONTEXT.md` (max 300 lines), `METRICS.md` (max 300 lines), `.pm/schemas.md` (max 400 lines), `.pm/ui_tokens.md` (max 200 lines) |
| **Stage 2: `/pm-brainstorm`** | [`skills/pm-brainstorm/SKILL.md`](./skills/pm-brainstorm/SKILL.md) | `docs/product/<feature-slug>/opportunity_brief.md` |
| **Stage 3: `/pm-prd`** | [`skills/pm-prd/SKILL.md`](./skills/pm-prd/SKILL.md) | `docs/product/<feature-slug>/prd.md` |
| **Stage 4: `/pm-review`** | [`skills/pm-review/SKILL.md`](./skills/pm-review/SKILL.md) | `docs/product/<feature-slug>/pm_review_report.md` + updated `prd.md` |
| **Stage 5: `/pm-prototype`** | [`skills/pm-prototype/SKILL.md`](./skills/pm-prototype/SKILL.md) | `docs/product/<feature-slug>/prototype.html` (max 400 lines, zero-build HTML/CSS/JS) |

---

## 2. Qwen CLI & Fork Tool Mapping (4 + 1 PM Goldfish Swarm)

When executing `/pm-brainstorm` or `/pm-review` in Qwen Code (or any Qwen CLI / Gemini CLI fork):

1.  **Subagent Delegation (`task` / `subagent` / `spawn_agent` tool)**:
    *   **Phase 1 (Parallel Diagnostic Audit)**: Spawn the 4 diagnostic Goldfish personas (`pm-value-metrics`, `pm-tech-lead`, `pm-data-eval`, `pm-ux-risk`) defined in [`agents/`](./agents/) using your CLI's subagent tool (`task` in Qwen Code). If your CLI fork uses a generic subagent tool without pre-registered agent names, instruct each spawned subagent to first read its persona file (`agents/pm_value_metrics.md`, `agents/pm_tech_lead.md`, `agents/pm_data_eval.md`, `agents/pm_ux_risk.md`) and operate strictly read-only (`read_file`, `grep_search`, `glob`, max 8 repository file reads).
    *   **Phase 2 (Sequential Synthesis)**: Pass the 4 Phase 1 diagnostic reports and their execution statuses (`completed | retried | failed`) to [`pm-scope-slicer`](./agents/pm_scope_slicer.md) (`agents/pm_scope_slicer.md`). The root Elephant agent writes the synthesized output to disk.
2.  **Interactive Gates**:
    *   If your CLI exposes a structured question tool (`ask_user_question` / `ask_question` / `request_user_input`), call it with a single question (`len(questions) == 1`, `is_multi_select: false`).
    *   If your CLI fork uses standard terminal chat without a structured multiple-choice tool, present the gate options as a numbered Markdown list (`1. (Recommended) ...`, `2. ...`, `3. ...`) and wait for the user's reply before continuing.
3.  **Shared Rules & Templates**:
    *   Always follow [`resources/execution_instructions.md`](./resources/execution_instructions.md) and [`resources/document_standards/prd-standard.md`](./resources/document_standards/prd-standard.md).
