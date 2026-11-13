# PRD: <Feature Title> (`<feature-slug>`)

*   **Author:** <pm-name>
*   **Status:** Draft | Draft (Needs Revision) | Approved
*   **Date:** <YYYY-MM-DD>
*   **Opportunity Brief:** `docs/product/<feature-slug>/opportunity_brief.md`

> [!IMPORTANT]
> **Engineering Handoff Directive**:
> 1. **Product Source of Truth**: Treat `## 1. Problem & Strategic Context`, `## 2. Goals & Non-Goals`, `## 3. Jobs-to-be-Done (JTBD), User Stories & Scenarios (CUJs)`, `## 4. Functional Requirements, Business Rules & Edge Cases`, `## 5. UI Placement, Screen States & Copy`, and `## 6. Success Metrics, Product Events & Rollout Plan` as approved product requirements.
> 2. **Strict MVP Boundary**: Implement **only** active MVP `US-*` / `REQ-*` items. Exclude everything listed under `### Non-Goals (Out of Scope / Deferred)`.
> 3. **Technical Ownership**: Resolve `## 7. Alternatives Considered & Open Questions for Engineering` in the codebase during technical design and implementation (never overwrite `prd.md`).

--------------------------------------------------------------------------------

## 1. Problem & Strategic Context

*   **Context & Why Now**: <How this fits into the product surface and strategic horizon in `PRODUCT_CONTEXT.md`>
*   **User & Business Problem**: <Concrete workflow pain point or missed outcome experienced by specific product roles>
*   **Demand Evidence Posture**: `EVIDENCE_BACKED` (`<research / tickets / funnel analytics>`) | `UNVALIDATED_ASSUMPTION`
*   **Validation Hypothesis & Kill/Pivot Criterion**: <Required when `UNVALIDATED_ASSUMPTION` (recommended for all features): measurable threshold over a defined window below which the feature is iterated or turned off>

## 2. Goals & Non-Goals

### MVP Goals (`In Scope`)
*   **`GOAL-01` (`JOB-01` -> `<MET-DRV-01>`)**: <Measurable user/business outcome>
*   **`GOAL-02` (`JOB-01` -> `<MET-NS-01>`)**: <Measurable user/business outcome>

### Non-Goals (`Out of Scope / Deferred`)
*   <Explicitly excluded capabilities so scope does not creep during design or engineering>

--------------------------------------------------------------------------------

## 3. Jobs-to-be-Done (JTBD), User Stories & Scenarios (CUJs)

### Jobs-to-be-Done (JTBD)
> Include one `JOB-xx` per distinct user struggle (and cover every participating empirical `ROLE-xx` when `>= 2` roles interact).
*   **`JOB-01` [`<ROLE-01: Role Name>`]**: **When** <concrete situation, context, or trigger>, **I want to** <motivation / capability>, **so I can** <expected outcome / progress>.
    *   *Current Workaround & Friction*: <How the user handles this job today and why it breaks, slows work down, or causes errors>

### User Stories

| Story ID | Parent Job | Role ID | User Story (`As a <Role>, I want <atomic capability>, so that <value>`) | Linked `REQ-*` |
| :--- | :--- | :--- | :--- | :--- |
| `US-01` | `JOB-01` | `ROLE-01` | As `<empirical role>`, I want `<atomic capability>`, so that `<observable user/business value>`. | `REQ-001` |
| `US-02` | `JOB-01` | `ROLE-01` | As `<empirical role>`, I want `<secondary control or feedback>`, so that `<observable value>`. | `REQ-002` |

### Critical User Journeys (CUJs)

#### CUJ 1 [`<ROLE-01>`, `US-01`]: <Primary End-to-End Flow> (`REQ-001`, `REQ-002`)
*   **Entry Point in Product UI**: <Existing navigation section / screen / trigger where the user starts>
*   **Given**: <User's role, starting screen context, and business preconditions>
*   **When**: <Steps the user takes>
*   **Then**: <Observable outcome, user payoff, and UI state transition>

### Cross-Role Handoffs & Permissions
*   <State `Single-Role Scope (<ROLE-01>) — no cross-role branching` when only one role is affected. When `>= 2` roles from `PRODUCT_CONTEXT.md` interact with or govern this feature, specify each `Role ID`'s visible information density, allowed actions (`View / Act / Approve`), and handoff transition.>

--------------------------------------------------------------------------------

## 4. Functional Requirements, Business Rules & Edge Cases

| REQ-ID | Story / Role | User / Business Requirement | Business Rules & Edge Cases (Conflicts, Limits, Undo, Permissions) | User-Observable Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| `REQ-001` | `US-01` / `ROLE-01` | <Clear product requirement> | <Rules for empty/duplicate input, edits, cancellations, limits, approvals> | <Testable user-level behavior> |
| `REQ-002` | `US-02` / `ROLE-01` | <Clear product requirement> | <Governance, auditability, or AI/search quality & fallback expectation> | <Testable user-level behavior> |

## 5. UI Placement, Screen States & Copy

*   **Host Screen & UI Mount Point**: <Exact existing screen / navigation section where this feature lives, and how it mounts inside the real App Shell — e.g. inline panel, tab, side drawer, modal, split view, or new route>
*   **UI Language & Domain Copy**: <Match the live product interface language (e.g. Russian / English) and domain terminology from `PRODUCT_CONTEXT.md` / `COMPANY_CONTEXT.md`>

> Define the **actual screen states, workflow steps, and edge/fallback views dictated by the User Stories (`US-*`), `CUJs`, and business rules above** (rather than forcing generic states that do not apply):

| State / Step | Trigger (`US-*` / Rule) | What the User Sees in the Interface | User Action / Recovery |
| :--- | :--- | :--- | :--- |
| `<Primary / Active State>` | `<e.g. US-01 entry>` | `<Layout, controls, and realistic data inside the host screen>` | `<Primary action>` |
| `<Transition / Secondary / Edge State>` | `<e.g. US-02, empty data, conflict, pending approval, or error>` | `<Exact feedback, warning, empty guidance, or role-specific view>` | `<Next step, undo, reset, or retry>` |

--------------------------------------------------------------------------------

## 6. Success Metrics, Product Events & Rollout Plan

*   **Falsifiable Causal Chain**:
    `Product Change -> User Behavior Shift -> Input Driver Delta -> North Star Outcome`

| Metric ID | Tier (`North Star` / `Input Driver` / `Guardrail`) | Role Segment (`ALL_ROLES` or `ROLE-xx`) | Current Baseline | Target Goal / Guardrail Bound |
| :--- | :--- | :--- | :--- | :--- |
| `MET-NS-01` | `North Star` | `ALL_ROLES` | `<Baseline>` | `<Target>` |
| `MET-DRV-01` | `Input Driver` | `<ALL_ROLES or ROLE-01>` | `<Baseline>` | `<Target>` |
| `MET-GRD-01` | `Guardrail` | `ALL_ROLES` | `<Current bound>` | `<Max acceptable regression>` |

*   **Required Product Analytics Events (Domain Level)**: <User actions and breakdown properties—such as `role`, cohort, or outcome—needed by analytics to measure the causal chain>
*   **Rollout & Experimentation Plan**: <Pilot cohort, A/B test, staged rollout by role/team, and rollback condition if `MET-GRD-*` degrades>

--------------------------------------------------------------------------------

## 7. Alternatives Considered & Open Questions for Engineering

### Product Alternatives Considered
*   **Alternative A (<Title>)**: <Pros, cons, and why rejected in favor of the MVP approach>

### Open Questions for Engineering
*   <High-level technical sizing, data availability, or external integration questions for engineering to verify during technical design>
