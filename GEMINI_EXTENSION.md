# EGM Product (`egm-product`) — Context & Routing for Gemini CLI

`egm-product` is an AI-native Product Management extension built on the **Elephant-Goldfish Model (EGM)**. Whenever the user invokes a `/pm-*` command or requests Product Management workflows (product/role/UI-shell/metric discovery, JTBD opportunity shaping, PRD drafting & review, or in-canvas interactive HTML prototyping), load the corresponding skill from `./skills/` inside this extension directory.

---

## 1. 4-Stage Product Pipeline & Skill Paths

| Stage / Slash Command | Skill File to Read | Primary Deliverable |
| :--- | :--- | :--- |
| **Stage 1: `/pm-discover`** (`--scope <subdir>`, `--context <path>`) | [`skills/pm-discover/SKILL.md`](./skills/pm-discover/SKILL.md) | `PRODUCT_CONTEXT.md`, `METRICS.md`, optional `COMPANY_CONTEXT.md`, `.pm/ui_tokens.md` |
| **Stage 2: `/pm-brainstorm`** | [`skills/pm-brainstorm/SKILL.md`](./skills/pm-brainstorm/SKILL.md) | `docs/product/<feature-slug>/opportunity_brief.md` |
| **Stage 3: `/pm-prd`** (JTBD + User Stories + built-in 4+1 product review) | [`skills/pm-prd/SKILL.md`](./skills/pm-prd/SKILL.md) | `docs/product/<feature-slug>/prd.md` + `pm_review_report.md` |
| **Stage 4: `/pm-prototype`** | [`skills/pm-prototype/SKILL.md`](./skills/pm-prototype/SKILL.md) | `docs/product/<feature-slug>/prototype.html` (rendered 1:1 inside real product canvas with story-driven flows & states) |

---

## 2. Gemini CLI Subagent Delegation & Standards

1.  **Fresh-Context Subagents**:
    *   In `/pm-discover`, delegate user-surface, App Shell, and CSS-token scanning to [`pm-product-scanner`](./agents/pm_product_scanner.md) (read-only).
    *   In `/pm-brainstorm` and `/pm-prd` (Step 3 review loop), dispatch the 4 Product Goldfish critics ([`pm-value-strategy`](./agents/pm_value_strategy.md), [`pm-ux-flows`](./agents/pm_ux_flows.md), [`pm-metrics-experiment`](./agents/pm_metrics_experiment.md), [`pm-business-logic`](./agents/pm_business_logic.md)) in parallel, then pass their reports to [`pm-synthesizer`](./agents/pm_synthesizer.md).
    *   In `/pm-prototype`, verify `prototype.html` against the real frontend canvas via [`pm-ux-flows`](./agents/pm_ux_flows.md) in `Mode: PROTOTYPE_AUDIT`.
2.  **Shared Rules & Rubric**:
    *   Follow [`resources/pm_execution_instructions.md`](./resources/pm_execution_instructions.md) and [`resources/document_standards/prd-standard.md`](./resources/document_standards/prd-standard.md).
