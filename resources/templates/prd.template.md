# PRD: <Feature Title> (`<feature-slug>`)

*   **Author:** <pm-name>
*   **Status:** Draft | Draft (Needs Revision) | Approved
*   **Date:** <YYYY-MM-DD>
*   **Opportunity Brief:** `docs/product/<feature-slug>/opportunity_brief.md`

> [!IMPORTANT]
> **Engineering Handoff Directive (`/egm-draft` & Coding Agents)**:
> 1. **Product Source of Truth**: Treat `## 1. Problem & Strategic Context`, `## 2. Goals & Non-Goals`, `## 3. Target Roles & Critical User Journeys (CUJs)`, `## 4. Functional Requirements, Business Rules & Edge Cases`, `## 5. UX States & Copy Guidelines`, and `## 6. Success Metrics, Product Events & Rollout Plan` as approved product requirements.
> 2. **Strict MVP Boundary**: Implement **only** active MVP `REQ-*` items. Exclude everything listed under `### Non-Goals (Out of Scope / Deferred)`.
> 3. **Technical Ownership**: Resolve `## 7. Alternatives Considered & Open Questions for Engineering` in the codebase and write the technical design spec to **`docs/designs/<feature-slug>.md`** (never overwrite `prd.md`).

--------------------------------------------------------------------------------

## 1. Problem & Strategic Context

*   **Context & Why Now**: <How this fits into the product surface and strategic horizon in `PRODUCT_CONTEXT.md`>
*   **User & Business Problem**: <Concrete workflow pain point or missed outcome experienced by specific product roles>
*   **Demand Evidence Posture**: `EVIDENCE_BACKED` (`<research / tickets / funnel analytics>`) | `UNVALIDATED_ASSUMPTION`
*   **Validation Hypothesis & Kill/Pivot Criterion**: <Required when `UNVALIDATED_ASSUMPTION` (recommended for all features): measurable threshold over a defined window below which the feature is iterated or turned off>

## 2. Goals & Non-Goals

### MVP Goals (`In Scope`)
*   **`REQ-001` (<Outcome Title>)**: <User/business outcome>
*   **`REQ-002` (<Outcome Title>)**: <User/business outcome>

### Non-Goals (`Out of Scope / Deferred`)
*   <Explicitly excluded capabilities so scope does not creep during design or engineering>

--------------------------------------------------------------------------------

## 3. Target Roles & Critical User Journeys (CUJs)

### CUJ 1 [`<ROLE-01: Role Name>`]: <Primary User Flow> (`REQ-001`, `REQ-002`)
*   **Given**: <User's role, starting context, and business preconditions>
*   **When**: <Steps the user takes>
*   **Then**: <Observable outcome, user payoff, and state change>

### Cross-Role Handoffs & Permissions
*   <State `Single-Role Scope (<ROLE-01>) — no cross-role branching` when only one role is affected. When `>= 2` roles from `PRODUCT_CONTEXT.md` interact with or govern this feature, specify each `Role ID`'s visible information density, allowed actions (`View / Act / Approve`), and handoff transition.>

--------------------------------------------------------------------------------

## 4. Functional Requirements, Business Rules & Edge Cases

| REQ-ID | User / Business Requirement | Affected Role(s) | Business Rules & Edge Cases (Conflicts, Limits, Undo, Permissions) | User-Observable Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| `REQ-001` | <Clear product requirement> | `ROLE-01` | <Rules for empty/duplicate input, edits, cancellations, limits, approvals> | <Testable user-level behavior> |
| `REQ-002` | <Clear product requirement> | `ROLE-01` | <Governance, auditability, or AI/search quality & fallback expectation> | <Testable user-level behavior> |

## 5. UX States & Copy Guidelines

| UI State | When User Sees This | Layout, Density & Copy Behavior | User Recovery / Next Action |
| :--- | :--- | :--- | :--- |
| **Default / Ready** | Normal populated state | <Primary layout aligned to `.pm/ui_tokens.md` and empirical role workflow> | <Primary user action> |
| **Loading / Progress** | Operation takes noticeable time | <Calm geometry-matched skeleton or progress indicator> | <Cancel or non-blocking wait> |
| **Empty / Zero-Result** | No items match or first-time use | <Plain-language explanation with zero jargon> | <One clear reset or creation action> |
| **Error / No-Access Fallback** | System failure, low AI confidence, or role restriction (when role-gated) | <Honest explanation preserving user input; read-only explanation when role-gated> | <Retry, fallback view, or access-request path> |

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

### Open Questions for Engineering (`/egm-draft`)
*   <High-level technical sizing, data availability, or external integration questions for engineering to verify when drafting `docs/designs/<feature-slug>.md`>
