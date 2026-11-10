---
name: pm-brainstorm
description: Stress-test a product feature idea or capability gap with the 4+1 PM Goldfish swarm and generate an Opportunity Brief with READY_NOW, ADAPT_NOW, and BLOCKED_NOW scope slicing.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 2: Opportunity Brainstorming & 4+1 Reality Check (`pm-brainstorm`)

Read [`../../resources/execution_instructions.md`](../../resources/execution_instructions.md) and [`../../docs/harnesses.md`](../../docs/harnesses.md) before starting.

`pm-brainstorm` turns a raw feature idea—or a capability-to-workflow gap discovered in the repository—into a stress-tested Opportunity Brief (`docs/product/<feature-slug>/opportunity_brief.md`) evaluated by the 4 + 1 PM Goldfish swarm.

---

## Step 1: Pre-Flight Context Check & Hypothesis Drilling

1.  **Preserve Initial Prompt & Check Layer 1 Contracts**:
    *   Record the user's initial feature request in working memory immediately.
    *   Check whether `PRODUCT_CONTEXT.md` and `METRICS.md` exist in the repository root and contain populated strategy/metric targets (no unresolved `[NEEDS_PM_INPUT]` placeholders).
    *   **Inline Bootstrap Recovery Gate**: If either file is missing or unpopulated, do **not** abort. Present a single-select gate:
        *   `(Recommended) Run inline discovery now to initialize PRODUCT_CONTEXT.md and METRICS.md, then continue brainstorming`
        *   `Provide minimal metric and service-boundary context inline for this feature`
        If the user selects inline discovery, read and execute [`../pm-discover/SKILL.md`](../pm-discover/SKILL.md) in-thread, then resume Step 1.2 automatically using the preserved initial feature request.
2.  **Capability-to-Workflow Gap Analysis & Drilling**:
    *   Read `PRODUCT_CONTEXT.md`, `METRICS.md`, and `.pm/schemas.md`.
    *   If the PM asked for open-ended opportunity suggestions ("what should we build next?"), compare populated backend schemas/endpoints in `PRODUCT_CONTEXT.md` and `.pm/schemas.md` against current user workflows and funnel bottlenecks in `METRICS.md` to propose 2–3 high-leverage capability gaps.
    *   Ask at most **one** open-ended question per turn to clarify:
        1.  The target user persona and workflow bottleneck.
        2.  The falsifiable metric causal chain (`Feature Mechanism -> User Behavior Shift -> Input Driver Delta -> North Star Outcome`) and paired counter-metric guardrail in `METRICS.md`.
        3.  The candidate `<feature-slug>` (kebab-case directory name under `docs/product/<feature-slug>/`).
3.  **Readiness Checkpoint Gate**:
    *   Once the feature hypothesis and metric causal chain are clear, present a single-select gate:
        *   `(Recommended) Launch the 4+1 PM Goldfish Reality Check swarm`
        *   `Refine feature hypothesis or metric targets first`

---

## Step 2: Two-Phase 4 + 1 PM Goldfish Swarm Dispatch

Follow the harness delegation rules in [`../../docs/harnesses.md`](../../docs/harnesses.md):

1.  **Phase 1 (Parallel Diagnostic Dispatch)**:
    *   Spawn the 4 diagnostic Goldfish subagents concurrently in `Mode: BRAINSTORM` (read-only, max 8 targeted file reads / 1,500 lines each):
        *   [`pm-value-metrics`](../../agents/pm_value_metrics.md)
        *   [`pm-tech-lead`](../../agents/pm_tech_lead.md)
        *   [`pm-data-eval`](../../agents/pm_data_eval.md)
        *   [`pm-ux-risk`](../../agents/pm_ux_risk.md)
    *   **Retry & Degraded-Quorum Handling**: If any Phase 1 subagent fails or times out, retry that subagent **once**. If it still fails after 1 retry, record its status as `failed` and perform a bounded inline check for that pillar (under the same 8-file read cap) or mark affected requirements `UNVERIFIED (NEEDS_MANUAL_CHECK)`.
2.  **Phase 2 (Sequential Synthesis via `pm-scope-slicer`)**:
    *   Once all 4 Phase 1 diagnostic reports are collected, invoke [`pm-scope-slicer`](../../agents/pm_scope_slicer.md) in `Mode: BRAINSTORM` (read-only), passing the 4 raw diagnostic reports and their execution statuses (`completed | retried | failed`).
    *   `pm-scope-slicer` deduplicates findings under strict **`BLOCKED_NOW > ADAPT_NOW > READY_NOW`** precedence, assigns sequential `REQ-001`, `REQ-002` identifiers, and returns the compiled Markdown conforming to [`../../resources/templates/opportunity_brief.template.md`](../../resources/templates/opportunity_brief.template.md).
3.  **Write Artifact**:
    *   The Elephant writes the synthesized Opportunity Brief to `docs/product/<feature-slug>/opportunity_brief.md`.

---

## Step 3: Interactive Scope Triage Gate

Present the saved [`opportunity_brief.md`](../../resources/templates/opportunity_brief.template.md) to the PM and call the single-select Scope Triage Gate:
*   `(Recommended) Approve Day-1 MVP slice (READY_NOW + proposed ADAPT_NOW adaptations) and move BLOCKED_NOW items to the Prerequisite Ledger`
*   `Review and customize individual ADAPT_NOW / BLOCKED_NOW requirement classifications`
*   `Contest a finding with additional repository or business context`

Apply any PM adjustments directly to `docs/product/<feature-slug>/opportunity_brief.md` and set `Status: Approved for PRD`.

---

## Step 4: Stage Handoff Gate to `/pm-prd`

Present a final single-select gate:
*   `(Recommended) Proceed to /pm-prd to draft docs/product/<feature-slug>/prd.md`
*   `Stop here and keep docs/product/<feature-slug>/opportunity_brief.md`

If the PM selects proceeding to `/pm-prd`, read and execute [`../pm-prd/SKILL.md`](../pm-prd/SKILL.md) on `docs/product/<feature-slug>/opportunity_brief.md`.
