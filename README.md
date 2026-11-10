# EGM for Product Managers (`egm-product`)

`egm-product` adapts the **Elephant-Goldfish Model (EGM)** for AI-native Product Managers working directly inside existing software repositories.

In engineering `egm`, a deep-context orchestrator (the **Elephant**) drafts technical designs while fresh-context, read-only reviewers (the **Goldfish**) stress-test them for implementation flaws. `egm-product` brings this architecture to product discovery, scope slicing, PRD writing, cross-functional review, and interactive HTML prototyping—without hardcoding domain rules for a single product.

---

## Two-Layer Universal Architecture

To operate across any internal product repository—whether an internal platform service such as Search-as-a-Service, an internal operations tool, or a candidate for future B2B commercialization—`egm-product` separates **per-repository context contracts** from **universal PM skills and Goldfish subagents**:

1. **Layer 1: Repository Context Contracts (Per-Repo State)**
   - `PRODUCT_CONTEXT.md` (capped at 300 lines): Service ownership boundaries (owned backend capabilities vs. upstream producers and downstream consumers), tech stack, RBAC/ACL model, strategic archetype (`INTERNAL_TOOL`, `INTERNAL_PLATFORM_SERVICE`, or `B2B_COMMERCIALIZATION_CANDIDATE`), and pointers to `.pm/schemas.md` (max 400 lines) and `.pm/ui_tokens.md` (max 200 lines).
   - `METRICS.md` (capped at 300 lines): North Star metric, input drivers, counter-metric guardrails, and code-verified telemetry readiness (`INSTRUMENTED_IN_CODE`, `INSTRUMENTATION_REQUIRED`, or `SLA_INVARIANT`).

2. **Layer 2: The 4 + 1 Universal PM Goldfish Swarm**
   Every feature hypothesis and PRD is stress-tested by four parallel diagnostic subagents followed by one sequential synthesizer:
   - [`pm-value-metrics`](./agents/pm_value_metrics.md): Audits the falsifiable causal chain (`Feature Mechanism -> Behavior Shift -> Input Metric Delta -> North Star Outcome`), counter-metric guardrails, and telemetry emission call sites. Classifies missing in-code telemetry as `ADAPT_NOW` (`INSTRUMENTATION_REQUIRED`).
   - [`pm-tech-lead`](./agents/pm_tech_lead.md): Simulates the Engineering Tech Lead in a planning sync. Audits requirements against owned vs. external service boundaries and classifies each requirement into `READY_NOW`, `ADAPT_NOW`, or `BLOCKED_NOW` with `[file:symbol_or_line]` citations.
   - [`pm-data-eval`](./agents/pm_data_eval.md): Audits `.pm/schemas.md` and data pipelines to verify field population and enforces evaluation datasets (`evals`) whenever search ranking, retrieval, or LLM generation is involved.
   - [`pm-ux-risk`](./agents/pm_ux_risk.md): Audits workflow step reduction, zero-training comprehension, UI state completeness (Default, Empty, Loading, Error/Fallback), design-token fidelity (`.pm/ui_tokens.md`), RBAC/ACL leakage, unit/token cost, and B2B multi-tenant portability.
   - [`pm-scope-slicer`](./agents/pm_scope_slicer.md): Sequential read-only synthesizer invoked after the 4 diagnostic subagents complete. Deduplicates verdicts under strict `BLOCKED_NOW > ADAPT_NOW > READY_NOW` precedence, assigns stable `REQ-xxx` IDs, and separates the Day-1 MVP slice from the `## Prerequisite Ledger (BLOCKED_NOW)`.

---

## 5-Stage Product Pipeline

| Stage | Skill | Deliverable | Purpose |
| :--- | :--- | :--- | :--- |
| **1. Discover** | [`/pm-discover`](./skills/pm-discover/SKILL.md) | `PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/schemas.md`, `.pm/ui_tokens.md` | Single-pass codebase scan + targeted PM interview to establish repository capabilities, design tokens, and metric baselines. |
| **2. Brainstorm** | [`/pm-brainstorm`](./skills/pm-brainstorm/SKILL.md) | `docs/product/<feature-slug>/opportunity_brief.md` | Drills into the feature hypothesis and metric causal chain, runs the 4 + 1 Reality Check, and triages `READY_NOW`, `ADAPT_NOW`, and `BLOCKED_NOW` scope. |
| **3. PRD** | [`/pm-prd`](./skills/pm-prd/SKILL.md) | `docs/product/<feature-slug>/prd.md` | Section-by-section drafting of the stack-grounded PRD with active MVP requirements separated from the `## Prerequisite Ledger (BLOCKED_NOW)`. |
| **4. Review** | [`/pm-review`](./skills/pm-review/SKILL.md) | `docs/product/<feature-slug>/pm_review_report.md` + updated `prd.md` | 2-round antagonistic audit across the 4 + 1 Goldfish swarm against [`prd-standard.md`](./resources/document_standards/prd-standard.md) with inline resolution (`PROPOSE FIX`, `CONTEST`, `ESCALATE`, `DECLINE`). |
| **5. Prototype** | [`/pm-prototype`](./skills/pm-prototype/SKILL.md) | `docs/product/<feature-slug>/prototype.html` | Zero-build, standalone interactive HTML/CSS/JS preview of the locked `READY_NOW` / `ADAPT_NOW` MVP states styled with `.pm/ui_tokens.md` variables. |

After `/pm-review` approves `docs/product/<feature-slug>/prd.md`, engineering teams can pass the PRD directly into `/egm-draft docs/product/<feature-slug>/prd.md` to generate the engineering design specification at `docs/designs/<feature-slug>.md`.

---

## Installation & Harness Support

### Quick Install

```bash
# Antigravity CLI
git clone https://github.com/Meddelin/egm-product.git
agy plugin install ./egm-product
agy plugin enable egm-product
```

See [`docs/harnesses.md`](./docs/harnesses.md) for harness-specific installation instructions and subagent delegation mechanics across Antigravity, Claude Code, Claude Cowork, OpenAI Codex, ChatGPT Work, and `omp`.

### Quick Verification

Run the structural and packaging test suite from the repository root:

```bash
pytest tests/unit/test_plugin_structure.py
```

---

## License

Licensed under the [Apache License, Version 2.0](./LICENSE).
