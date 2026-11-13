# Product Requirements Document Standard (`prd-standard.md`)

This rubric defines the pure-product pass/fail audit criteria used by the built-in 4 + 1 Product Goldfish review in `/pm-prd` (`pm-value-strategy`, `pm-ux-flows`, `pm-metrics-experiment`, `pm-business-logic` -> `pm-synthesizer`) when evaluating `docs/product/<feature-slug>/prd.md`.

> **Product-Only Boundary**: Audit strictly on user value, role workflows, UX states, product analytics, and business logic completeness. Never require source-code `[file:line]` citations, database table schemas, or backend implementation details.

---

## Severity Definitions

*   **`Blocker`**: A product defect that makes the PRD ambiguous, unmeasurable, self-contradictory, or unsafe to build (for example: missing problem/demand posture, `UNVALIDATED_ASSUMPTION` with no validation/kill criterion, `Out of Scope` items leaking into active `CUJs` or requirements, missing any of the 4 mandatory UI states, broken cross-role handoff when `>= 2` roles interact, missing guardrail metric, unaddressed business-rule contradiction, or missing top-level Engineering Handoff Directive). Must be resolved before `Status: Approved`.
*   **`Major`**: Over-scoped MVP feature creep that can be simplified, PRD length exceeding the `250-line` cap, unnecessary multi-step UX friction where an inline default suffices, unexplained internal jargon or mismatch with the `COMPANY_CONTEXT.md` glossary (when present), missing role-segment metric breakdown when targeting specific roles, missing domain event definitions for funnel tracking, or missing edge-case rules (cancellation, undo, empty input, permission boundary).
*   **`Nit`**: Minor wording ambiguity, formatting inconsistency, or violation of the Plain-English Standard in [`pm_execution_instructions.md`](../pm_execution_instructions.md).

---

## 4 Core Product Audit Pillars

### 1. Problem Sharpness, Strategic Fit & MVP Focus (`pm-value-strategy`)
*   **Pass Criteria**:
    1.  Top-of-document **Engineering Handoff Directive** appears immediately below PRD metadata, separating approved MVP product scope from `Out of Scope / Deferred` items and leaving technical architecture to engineering (`/egm-draft` or coding agents), and the complete `prd.md` stays `<= 250 lines`.
    2.  `## 1. Problem & Strategic Context` states a clear user/business bottleneck aligned with `PRODUCT_CONTEXT.md` (and `COMPANY_CONTEXT.md` when present), declares `Demand Evidence Posture` (`EVIDENCE_BACKED` with source or `UNVALIDATED_ASSUMPTION`), and defines a concrete **Validation Hypothesis & Kill/Pivot Criterion** whenever `UNVALIDATED_ASSUMPTION` is used.
    3.  `## 2. Goals & Non-Goals` defines outcome-oriented MVP goals, isolates deferred ideas into `### Non-Goals (Out of Scope / Deferred)`, and avoids shipping complex features where a simpler product change solves the core pain.
*   **Blocker Trigger**: Missing Engineering Handoff Directive, solution-first framing with no articulated user problem, `UNVALIDATED_ASSUMPTION` without a validation/kill criterion, or `Out of Scope` items appearing inside active `CUJs` or `## 4. Functional Requirements, Business Rules & Edge Cases`.

### 2. User Scenarios, Empirical Role Flows & 4-State UX (`pm-ux-flows`)
*   **Pass Criteria**:
    1.  `## 3. Target Roles & Critical User Journeys (CUJs)` tags each `Given / When / Then` flow with its empirical `Role ID` from `PRODUCT_CONTEXT.md` (`Zero Assumed Personas`), matches information density and vocabulary to that role's documented usage pattern and the `COMPANY_CONTEXT.md` glossary (when present), and defines `### Cross-Role Handoffs & Permissions` whenever `>= 2` roles participate (`Single-Role Scope` otherwise).
    2.  `## 5. UX States & Copy Guidelines` defines clear user-visible behavior and recovery actions across all 4 states: **Default / Ready**, **Loading / Progress**, **Empty / Zero-Result**, and **Error / No-Access Fallback** (including read-only or access-request guidance when role restrictions exist).
*   **Blocker Trigger**: Missing any of the 4 mandatory UI states, dead-end empty/error/no-access screens with no user recovery path, or undefined state handoff between roles when `>= 2` roles interact (`Major`: excessive interaction steps, unexplained jargon, or role density mismatch against `PRODUCT_CONTEXT.md`).

### 3. Metric Causal Chain, Product Events & Experimentation (`pm-metrics-experiment`)
*   **Pass Criteria**:
    1.  `## 6. Success Metrics, Product Events & Rollout Plan` states a falsifiable causal chain (`Product Change -> User Behavior Shift -> Input Driver Delta -> North Star Outcome`) tied to `METRICS.md`, paired with at least one counter-metric **Guardrail** (`MET-GRD-*`).
    2.  Metrics specify `Role Segment` (`ALL_ROLES` or `ROLE-xx`) when the feature targets a subset of product roles, defines the domain-level product analytics events and properties needed to measure the funnel, and states rollout/experimentation decision criteria.
*   **Blocker Trigger**: Vanity metrics with no causal link to user value, or missing counter-metric guardrail (`Major`: missing `Role Segment` breakdown on role-specific features, missing domain analytics events, or missing baseline/target thresholds).

### 4. Business Rules, Edge Cases, Quality & Governance (`pm-business-logic`)
*   **Pass Criteria**:
    1.  `## 4. Functional Requirements, Business Rules & Edge Cases` assigns stable IDs (`REQ-001`, `REQ-002`, ...) with unambiguous user-observable acceptance criteria, covering conflict/boundary cases (edits, cancellations, limits, duplicate actions, stale data, and role permission boundaries).
    2.  Documents applicable business governance from `PRODUCT_CONTEXT.md` / `COMPANY_CONTEXT.md` (approval / `maker-checker` workflows, auditability expectations, or abuse/cost caps) and—if the feature uses search ranking, recommendations, or AI generation—defines user-perceived quality expectations and low-confidence fallback behavior.
    3.  Surfaces cross-team or technical unknowns cleanly under `## 7. Alternatives Considered & Open Questions for Engineering` rather than guessing implementation details.
*   **Blocker Trigger**: Contradictory business rules between requirements, missing permission/approval rules on sensitive actions, or shipping non-deterministic AI/search behavior with no user-level quality expectation or fallback.
