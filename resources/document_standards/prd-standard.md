# Product Requirements Document Standard (`prd-standard.md`)

This rubric defines the pass/fail audit criteria used by `/pm-review` and the 4 + 1 PM Goldfish swarm (`pm-value-metrics`, `pm-tech-lead`, `pm-data-eval`, `pm-ux-risk`, `pm-scope-slicer`) when evaluating `docs/product/<feature-slug>/prd.md`.

---

## Severity Definitions

*   **`Blocker`**: A defect that makes the PRD unimplementable, unmeasurable, or unsafe to hand off to engineering (for example: a `BLOCKED_NOW` requirement leaked into active MVP scope, a missing Evidence Citation Tuple, an unguarded permission/ACL leak, or a broken metric causal chain). Must be resolved before approval.
*   **`Major`**: A gap in UX state coverage, incomplete `ADAPT_NOW` specification, missing rollback/kill-switch mapping, or missing evaluation rubric (`evals`) on search/AI features.
*   **`Nit`**: Minor wording ambiguity, table formatting inconsistency, or violation of the Plain-English Standard in [`execution_instructions.md`](../execution_instructions.md).

---

## 5 Core Audit Pillars

### 1. Falsifiable Metric Causal Chain & Telemetry Readiness (`pm-value-metrics`)
*   **Pass Criteria**:
    1.  `## Metrics & Telemetry Contract` states an explicit causal chain (`Feature Mechanism -> User Behavior Shift -> Input Driver Delta -> North Star Outcome`) referencing valid `Metric ID`s from `METRICS.md`.
    2.  Every target metric is paired with at least one counter-metric **Guardrail** (`MET-GRD-*`).
    3.  If any referenced metric has readiness `INSTRUMENTATION_REQUIRED`, an explicit `ADAPT_NOW` requirement (`REQ-xxx`) exists in `## Scope Classification (READY_NOW / ADAPT_NOW)` specifying the event name, call site (`[file:function:line]`), and entity correlation keys (`user_id`, `tenant_id`, `trace_id`).
*   **Blocker Trigger**: Vague vanity targets ("improve UX") with no `Metric ID`, missing guardrail metric, or an `INSTRUMENTATION_REQUIRED` metric with no corresponding `ADAPT_NOW` instrumentation requirement in the MVP scope.

### 2. Evidence Citation Tuples & Boundary Feasibility (`pm-tech-lead`)
*   **Pass Criteria**:
    1.  Every requirement in `## Scope Classification (READY_NOW / ADAPT_NOW)` carries a unique `REQ-ID`, a classification (`READY_NOW` or `ADAPT_NOW`), deterministic acceptance criteria, and a verified `[file:symbol_or_line]` Evidence Citation Tuple pointing to existing files in the repository.
    2.  No requirement classified as `READY_NOW` or `ADAPT_NOW` depends on unbuilt external team APIs, unpopulated upstream schemas, or cross-repo migrations listed as external boundaries in `PRODUCT_CONTEXT.md`.
*   **Blocker Trigger**: Any `REQ-ID` missing a `[file:symbol_or_line]` citation, citing a non-existent file/symbol, or requiring an external team dependency without being isolated in `## Prerequisite Ledger (BLOCKED_NOW)`.

### 3. Semantic Split & Zero `BLOCKED_NOW` Leakage (`pm-scope-slicer` & `pm-tech-lead`)
*   **Pass Criteria**:
    1.  All `BLOCKED_NOW` requirements reside exclusively below the `## Prerequisite Ledger (BLOCKED_NOW)` header and are explicitly listed as out-of-scope in `## Non-Goals`.
    2.  The engineering handoff directive banner immediately follows `## Prerequisite Ledger (BLOCKED_NOW)`, instructing `/egm-draft` to ignore `BLOCKED_NOW` rows and save engineering specs to `docs/designs/<feature-slug>.md`.
*   **Blocker Trigger**: Any `BLOCKED_NOW` capability referenced as part of a Day-1 CUJ, `## Goals`, or `## Scope Classification (READY_NOW / ADAPT_NOW)`.

### 4. Data Integrity & Evaluation Gates (`pm-data-eval`)
*   **Pass Criteria**:
    1.  All data entities and fields referenced by `READY_NOW` and `ADAPT_NOW` requirements exist in `.pm/schemas.md` (or have an explicit owned local migration defined under `ADAPT_NOW`).
    2.  If the feature modifies search ranking, retrieval, classification, or LLM generation, `## Data, Quality & Evaluation Gates` defines a golden evaluation dataset (`evals`), scoring rubric, and minimum pass threshold before launch.
*   **Blocker Trigger**: Assuming an unpopulated or non-existent schema column is available without migration, or shipping non-deterministic AI/search behavior without an evaluation gate.

### 5. UX State Matrix, Security, Cost & Portability (`pm-ux-risk`)
*   **Pass Criteria**:
    1.  `### UX State & Fallback Matrix` specifies deterministic UI behavior and copy for **Default / Ready**, **Loading / Streaming**, **Empty / Zero-Result**, and **Error / Low-Confidence Fallback** states.
    2.  `## Security, Cost & Operational Guardrails` documents route/retrieval RBAC/ACL enforcement, per-action cost/rate ceilings, a concrete feature-flag/rollback trigger, and—when `PRODUCT_CONTEXT.md` specifies `B2B_COMMERCIALIZATION_CANDIDATE`—verification that no hardcoded single-tenant assumptions are introduced.
*   **Blocker Trigger**: Missing error/empty/fallback states, retrieval-time ACL bypass risk, unbounded token/query cost loop, or missing rollback mechanism.
