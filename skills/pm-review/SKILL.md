---
name: pm-review
description: Audit a PRD with the 4+1 PM Goldfish swarm against prd-standard.md and resolve findings inline within a 2-round convergence cap.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 4: Antagonistic PRD Review & Inline Resolution (`pm-review`)

Read [`../../resources/execution_instructions.md`](../../resources/execution_instructions.md), [`../../resources/document_standards/prd-standard.md`](../../resources/document_standards/prd-standard.md), and [`../../docs/harnesses.md`](../../docs/harnesses.md) before starting.

`pm-review` audits `docs/product/<feature-slug>/prd.md` using fresh-context PM Goldfish subagents and resolves findings inline within a strict **2-round convergence cap** (Round 1: Initial Audit + Resolution; Round 2: Verification Pass).

---

## Step 1: Pre-Flight Boundary & Prerequisite Promotion Check

1.  **Locate Target PRD**:
    *   Accept an explicit path to `docs/product/<feature-slug>/prd.md` or resolve the most recently modified `<feature-slug>` under `docs/product/`.
2.  **Verify Semantic Split Boundary**:
    *   Check that `docs/product/<feature-slug>/prd.md` contains `## Prerequisite Ledger (BLOCKED_NOW)` and the `/egm-draft` handoff directive banner.
3.  **Prerequisite Promotion Check**:
    *   Compare the `generated_at_commit` in `PRODUCT_CONTEXT.md` and `.pm/schemas.md` against the items in `## Prerequisite Ledger (BLOCKED_NOW)`.
    *   If `PRODUCT_CONTEXT.md` was refreshed after upstream engineering prerequisites landed, instruct [`pm-tech-lead`](../../agents/pm_tech_lead.md) and [`pm-data-eval`](../../agents/pm_data_eval.md) to evaluate whether any `BLOCKED_NOW` item in the ledger now qualifies for promotion to `READY_NOW`.

---

## Step 2: Two-Phase 4 + 1 PM Goldfish Audit Dispatch

Follow the harness delegation contract in [`../../docs/harnesses.md`](../../docs/harnesses.md). Single-instance dispatch is enforced (never spawn duplicate A/B instances of the same persona).

1.  **Phase 1 (Parallel Diagnostic Audit)**:
    *   Spawn the 4 diagnostic Goldfish subagents concurrently in `Mode: REVIEW` (read-only, max 8 targeted file reads / 1,500 lines each) to audit `docs/product/<feature-slug>/prd.md` against [`../../resources/document_standards/prd-standard.md`](../../resources/document_standards/prd-standard.md):
        *   [`pm-value-metrics`](../../agents/pm_value_metrics.md) (Pillar 1: Metric Causal Chain, Guardrails & Telemetry Readiness)
        *   [`pm-tech-lead`](../../agents/pm_tech_lead.md) (Pillars 2 & 3: Evidence Citation Tuples, Boundary Feasibility & Zero `BLOCKED_NOW` Leakage)
        *   [`pm-data-eval`](../../agents/pm_data_eval.md) (Pillar 4: Schema Population & Search/AI Evaluation Gates)
        *   [`pm-ux-risk`](../../agents/pm_ux_risk.md) (Pillar 5: 4-State UX Matrix, RBAC/ACL Security, Cost Ceilings, B2B Portability & Rollback)
    *   Retry any failed Phase 1 subagent **once** before falling back to a bounded inline check.
2.  **Phase 2 (Sequential Synthesis via `pm-scope-slicer`)**:
    *   Pass the 4 raw diagnostic reports and their execution statuses (`completed | retried | failed`) to [`pm-scope-slicer`](../../agents/pm_scope_slicer.md) in `Mode: REVIEW`.
    *   Write the compiled report returned by `pm-scope-slicer` to `docs/product/<feature-slug>/pm_review_report.md`.

---

## Step 3: Four-Disposition Inline Resolution Gate

Categorize every finding in `docs/product/<feature-slug>/pm_review_report.md` into one of four dispositions:
*   **`PROPOSE FIX`**: Concrete, evidence-backed edit to `prd.md` (adding a missing citation, adding an `ADAPT_NOW` telemetry task, completing a UX fallback state, or moving a leaked item to `## Prerequisite Ledger (BLOCKED_NOW)`).
*   **`CONTEST`**: Finding is contradicted by verified repository or contract evidence (for example, telemetry is already emitted via a shared middleware wrapper).
*   **`ESCALATE`**: Requires a Product Manager business decision (for example, choosing between two `ADAPT_NOW` scope trade-offs or accepting a `BLOCKED_NOW` deferral).
*   **`DECLINE`**: Redundant or stylistic nit that does not improve specification precision.

Present the single-select Resolution Gate:
*   `(Recommended) Auto accept all PROPOSE FIX items and resolve any ESCALATE items`
*   `Interactive item-by-item breakdown`
*   `Continue without changes`

Apply all accepted edits directly to `docs/product/<feature-slug>/prd.md`.

---

## Step 4: Convergence Check (Max 2 Rounds) & Stage Handoff

1.  **Convergence Rule**:
    *   If Round 1 had **zero `Blocker` and zero `Major` findings** (or all `Blocker` and `Major` findings were resolved via `PROPOSE FIX` and verified), set `Status: Approved` in `docs/product/<feature-slug>/prd.md`.
    *   If structural scope changes were made in Round 1 and the PM requests a verification pass, run at most **one** verification round (Round 2). Never exceed 2 total review rounds.
2.  **Final Handoff Gate**:
    *   Once `docs/product/<feature-slug>/prd.md` is set to `Status: Approved`, present a single-select gate:
        *   `(Recommended) Proceed to /pm-prototype to generate the interactive HTML preview (docs/product/<feature-slug>/prototype.html)`
        *   `Conclude PM workflow (ready for engineering handoff via /egm-draft docs/product/<feature-slug>/prd.md)`
    *   If the PM selects `/pm-prototype`, read and execute [`../pm-prototype/SKILL.md`](../pm-prototype/SKILL.md).
