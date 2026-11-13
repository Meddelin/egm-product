# Product Requirements Document Standard (`prd-standard.md`)

This rubric defines the pure-product evaluation criteria used by the built-in 4 + 1 Product Goldfish review in `/pm-prd` (`pm-value-strategy`, `pm-ux-flows`, `pm-metrics-experiment`, `pm-business-logic` -> `pm-synthesizer`) when auditing `docs/product/<feature-slug>/prd.md`.

> **Product-Only & Story-Driven Boundary**: Audit strictly on user value, JTBD & User Stories, role workflows, story-driven screen states, product analytics, and business logic completeness. Never require source-code `[file:line]` citations, database schemas, backend implementation details, or artificial boilerplate states unrelated to the feature's stories.

---

## Severity Definitions

*   **`Blocker`**: A product defect that makes the PRD ambiguous, unmeasurable, self-contradictory, or unsafe to build (for example: missing problem/demand posture, `UNVALIDATED_ASSUMPTION` with no validation/kill criterion, missing `### Jobs-to-be-Done (JTBD)` or `### User Stories`, broken `JOB -> US -> CUJ & REQ` traceability, missing `JOB-*`/`US-*` coverage for any active role in a multi-role feature, `Out of Scope` items leaking into active `User Stories`/`CUJs`/requirements, missing UI placement on an existing product, missing a screen state or user recovery path required by the PRD's own stories/edge cases, broken cross-role handoff when `>= 2` roles interact, missing guardrail metric, unaddressed business-rule contradiction, or missing top-level Engineering Handoff Directive). Must be resolved before `Status: Approved`.
*   **`Major`**: Over-scoped MVP feature creep that can be simplified, circular/widget-restating JTBD Job Stories or User Stories (`"want <widget> so I can use <widget>"`), bundled multi-capability mega-stories instead of atomic `US-*` stories, backend `"As the system..."` pseudo-stories instead of real empirical `ROLE-xx` User Stories, unnecessary multi-step UX friction where an inline default suffices, unexplained internal jargon or mismatch with the `COMPANY_CONTEXT.md` glossary (when present), missing role-segment metric breakdown when targeting specific roles, missing domain event definitions for funnel tracking, or missing edge-case rules (cancellation, undo, conflicts, limits, permission boundary).
*   **`Nit`**: Minor wording ambiguity, formatting inconsistency, or violation of the Plain-English Standard in [`pm_execution_instructions.md`](../pm_execution_instructions.md).

---

## 4 Core Product Audit Pillars

### 1. Problem Sharpness, JTBD Clarity & MVP Focus (`pm-value-strategy`)
*   **Pass Criteria**:
    1.  Top-of-document **Engineering Handoff Directive** appears immediately below PRD metadata, separating approved MVP product scope from `Out of Scope / Deferred` items and leaving technical architecture to engineering.
    2.  `## 1. Problem & Strategic Context` states a clear user/business bottleneck aligned with `PRODUCT_CONTEXT.md` (and `COMPANY_CONTEXT.md` when present), declares `Demand Evidence Posture` (`EVIDENCE_BACKED` with source or `UNVALIDATED_ASSUMPTION`), and defines a concrete **Validation Hypothesis & Kill/Pivot Criterion** whenever `UNVALIDATED_ASSUMPTION` is used.
    3.  `### Jobs-to-be-Done (JTBD)` in `## 3` frames each `JOB-xx` around a real situational trigger, motivation, expected outcome (`When ... I want to ... so I can ...`), and **Current Workaround & Friction**, rather than echoing a UI button click.
    4.  `## 2. Goals & Non-Goals` defines outcome-oriented MVP goals (`GOAL-*`), isolates deferred ideas into `### Non-Goals (Out of Scope / Deferred)`, and avoids shipping complex features where a simpler product change solves the core pain.
*   **Blocker Trigger**: Missing Engineering Handoff Directive, solution-first framing with no articulated user problem, missing `### Jobs-to-be-Done (JTBD)`, `UNVALIDATED_ASSUMPTION` without a validation/kill criterion, or `Out of Scope` items appearing inside active `User Stories`, `CUJs`, or `## 4. Functional Requirements, Business Rules & Edge Cases`.

### 2. User Stories, Empirical Role Flows & Story-Driven UX States (`pm-ux-flows`)
*   **Pass Criteria**:
    1.  `## 3. Jobs-to-be-Done (JTBD), User Stories & Scenarios (CUJs)` decomposes every `JOB-xx` into atomic, role-owned **`### User Stories` (`US-xx`)** (`As a <Role>, I want <capability>, so that <value>`) covering **every participating `ROLE-xx`** when `>= 2` roles interact, with full bidirectional traceability (`every JOB-xx -> >= 1 US-xx -> >= 1 CUJ & >= 1 REQ-*`, and every `REQ-*` linked to `US-*`), tags each `Given / When / Then` flow in `### Critical User Journeys (CUJs)` with its empirical `Role ID` (`Zero Assumed Personas`) and `Entry Point in Product UI`, matches vocabulary to the `COMPANY_CONTEXT.md` glossary (when present), and defines `### Cross-Role Handoffs & Permissions` whenever `>= 2` roles participate (`Single-Role Scope` otherwise).
    2.  `## 5. UI Placement, Screen States & Copy` specifies `Host Screen & UI Mount Point` (where the feature sits inside the live product's navigation/screen) and `UI Language & Domain Copy`, and defines the **concrete screen states, transitions, and edge/fallback states dictated by the PRD's User Stories and business rules** (with clear user actions and recovery paths—never dead ends, and never robotic filler states irrelevant to the workflow).
*   **Blocker Trigger**: Missing `### User Stories`, unmapped `JOB-xx` (zero `US-*`), unmapped `US-xx` (missing from `CUJs` or `## 4` `REQ-*`), orphaned `REQ-*` items not linked to any `US-*`, multi-role feature (`>= 2` active roles) missing `JOB-*`/`US-*` coverage for a participating role, missing `Host Screen & UI Mount Point` on a non-greenfield product, missing a screen state or recovery path genuinely required by the feature's stories/rules, or undefined state handoff between roles when `>= 2` roles interact (`Major`: widget-restating or bundled mega `US-*` stories, `"As the system..."` pseudo-stories, excessive interaction steps, unexplained jargon, or role density mismatch against `PRODUCT_CONTEXT.md`).

### 3. Metric Causal Chain, Product Events & Experimentation (`pm-metrics-experiment`)
*   **Pass Criteria**:
    1.  `## 6. Success Metrics, Product Events & Rollout Plan` states a falsifiable causal chain (`Product Change -> User Behavior Shift -> Input Driver Delta -> North Star Outcome`) tied to `METRICS.md`, paired with at least one counter-metric **Guardrail** (`MET-GRD-*`).
    2.  Metrics specify `Role Segment` (`ALL_ROLES` or `ROLE-xx`) when the feature targets a subset of product roles, defines the domain-level product analytics events and properties needed to measure the funnel, and states rollout/experimentation decision criteria.
*   **Blocker Trigger**: Vanity metrics with no causal link to user value, or missing counter-metric guardrail (`Major`: missing `Role Segment` breakdown on role-specific features, missing domain analytics events, or missing baseline/target thresholds).

### 4. Business Rules, Edge Cases, Quality & Governance (`pm-business-logic`)
*   **Pass Criteria**:
    1.  `## 4. Functional Requirements, Business Rules & Edge Cases` assigns stable IDs (`REQ-001`, `REQ-002`, ...) linked to `US-*` / `Role ID` with unambiguous user-observable acceptance criteria, covering conflict/boundary cases (edits, cancellations, limits, duplicate actions, stale data, and role permission boundaries).
    2.  Documents applicable business governance from `PRODUCT_CONTEXT.md` / `COMPANY_CONTEXT.md` (approval / `maker-checker` workflows, auditability expectations, or abuse/cost caps) and—if the feature uses search ranking, recommendations, or AI generation—defines user-perceived quality expectations and low-confidence fallback behavior.
    3.  Surfaces cross-team or technical unknowns cleanly under `## 7. Alternatives Considered & Open Questions for Engineering` rather than guessing implementation details.
*   **Blocker Trigger**: Contradictory business rules between requirements, missing permission/approval rules on sensitive actions, or shipping non-deterministic AI/search behavior with no user-level quality expectation or fallback.
