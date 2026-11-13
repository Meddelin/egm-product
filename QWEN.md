# EGM Product (`egm-product`) — Context & Routing for Qwen Code / Qwen CLI Forks

`egm-product` is an AI-native Product Management framework built on the **Elephant-Goldfish Model (EGM)**. Whenever the user invokes a `/pm-*` command or asks for Product Management workflows, load and follow the corresponding skill and subagent personas from this extension directory (`./skills/`, `./agents/`, `./resources/`).

---

## 1. 4-Stage Product Pipeline & Skill Paths

| Stage / Slash Command | Skill File to Read | Primary Deliverable |
| :--- | :--- | :--- |
| **Stage 1: `/pm-discover`** (`--scope <subdir>`, `--context <path>`) | [`skills/pm-discover/SKILL.md`](./skills/pm-discover/SKILL.md) | `PRODUCT_CONTEXT.md`, `METRICS.md`, optional `COMPANY_CONTEXT.md`, `.pm/ui_tokens.md` |
| **Stage 2: `/pm-brainstorm`** | [`skills/pm-brainstorm/SKILL.md`](./skills/pm-brainstorm/SKILL.md) | `docs/product/<feature-slug>/opportunity_brief.md` |
| **Stage 3: `/pm-prd`** (JTBD + User Stories + built-in 4+1 product review) | [`skills/pm-prd/SKILL.md`](./skills/pm-prd/SKILL.md) | `docs/product/<feature-slug>/prd.md` + `pm_review_report.md` |
| **Stage 4: `/pm-prototype`** | [`skills/pm-prototype/SKILL.md`](./skills/pm-prototype/SKILL.md) | `docs/product/<feature-slug>/prototype.html` (rendered 1:1 inside real product canvas with story-driven flows & states) |

---

## 2. Qwen CLI & Fork Tool Mapping (4 + 1 Product Goldfish Swarm)

1.  **Subagent Delegation (`task` / `subagent` / `spawn_agent` tool)**:
    *   **Discovery Overview (`/pm-discover`)**: Spawn [`pm-product-scanner`](./agents/pm_product_scanner.md) in read-only mode to scan user-visible product screens, App Shell chrome, UI language, and CSS tokens without backend/DB schema noise.
    *   **Phase 1 (Parallel Product Audit)**: Spawn the 4 Product Goldfish personas ([`pm-value-strategy`](./agents/pm_value_strategy.md), [`pm-ux-flows`](./agents/pm_ux_flows.md), [`pm-metrics-experiment`](./agents/pm_metrics_experiment.md), [`pm-business-logic`](./agents/pm_business_logic.md)) concurrently in read-only mode.
    *   **Phase 2 (Sequential Synthesis)**: Pass the 4 critic reports and their execution statuses (`completed | retried | failed`) to [`pm-synthesizer`](./agents/pm_synthesizer.md). Only the root Elephant writes artifacts to disk.
2.  **Interactive Gates & Shared Standards**:
    *   Follow [`resources/pm_execution_instructions.md`](./resources/pm_execution_instructions.md) and [`resources/document_standards/prd-standard.md`](./resources/document_standards/prd-standard.md).
