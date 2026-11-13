# Opportunity Brief: <Feature Title> (`<feature-slug>`)

*   **Author:** <pm-name>
*   **Status:** Draft | Approved for PRD
*   **Date:** <YYYY-MM-DD>

--------------------------------------------------------------------------------

## 4+1 Product Goldfish Audit Summary

| Product Lens | Status (`completed` / `retried` / `failed`) | Key Risks Flagged | Scope Simplifications Proposed |
| :--- | :--- | :--- | :--- |
| `pm-value-strategy` | `completed` | 0 | 0 |
| `pm-ux-flows` | `completed` | 0 | 0 |
| `pm-metrics-experiment` | `completed` | 0 | 0 |
| `pm-business-logic` | `completed` | 0 | 0 |
| `pm-synthesizer` | `completed` | — | — |

--------------------------------------------------------------------------------

## 1. Problem, Jobs-to-be-Done & Causal Hypothesis

*   **User & Business Bottleneck**: <Falsifiable statement of the problem, why it matters now, and what happens if we do nothing>
*   **Affected Product Roles**: `<ROLE-01 (Single-Role Scope) | ROLE-01, ROLE-02 (Multi-Role — explain how goals, views, or handoffs differ across roles from PRODUCT_CONTEXT.md)>`
*   **Primary Jobs-to-be-Done (JTBD)** *(include `JOB-xx` for every participating `ROLE-xx` when `>= 2` roles interact)*:
    *   **`JOB-01` [`<ROLE-01>`]**: **When** <concrete situation / trigger>, **I want to** <motivation / capability>, **so I can** <expected outcome / progress>.
        *   *Current Workaround & Friction*: <How users handle this job today and why it fails, wastes time, or causes errors>
*   **Target Product Surface / Host Screen**: <Existing navigation section or screen where users encounter this capability — or new surface if greenfield>
*   **Demand Evidence Posture**: `EVIDENCE_BACKED` (`<interviews / support tickets / funnel data / research doc>`) | `UNVALIDATED_ASSUMPTION`
*   **Validation Hypothesis & Kill/Pivot Criterion**: <Mandatory when `UNVALIDATED_ASSUMPTION` (recommended for all features): measurable adoption/outcome threshold over N days/users below which we iterate or sunset the feature>
*   **Falsifiable Causal Chain**:
    `Product Change (<mechanism>) -> User Behavior Shift (<action>) -> Input Driver Delta (<Metric ID>) -> North Star Outcome (<Metric ID>)`
*   **Paired Counter-Metric Guardrail**: `<Metric ID>` (<acceptable bound that must not degrade>)

--------------------------------------------------------------------------------

## 2. Proposed Product Solution & MVP Scope Cut

### MVP Scope (`In Scope` — High-Leverage Day-1 Slice)
*   **`US-01` (`JOB-01`, `<ROLE-01>` -> `REQ-001`)**: As `<empirical role>`, I want `<core capability>`, so that `<observable user/business value>`.
*   **`US-02` (`JOB-01`, `<ROLE-01>` -> `REQ-002`)**: As `<empirical role>`, I want `<simplified workflow / control>`, so that `<value without bloat>`.

### Deferred & Out of Scope (`Not in MVP`)
*   **`<Deferred Idea>`**: <Why excluded from MVP (low leverage, unvalidated demand, or cross-org dependency) and what signal would justify revisiting it later>

--------------------------------------------------------------------------------

## 3. Product Alternatives Weighed

### Alternative A: <Do Nothing / Simpler Copy or Default Change / Different Flow>
*   **Pros**: <Pros>
*   **Cons**: <Why insufficient or why rejected/adopted>
*   **Decision**: <Adopted into MVP | Rejected — reason>

--------------------------------------------------------------------------------

## 4. Key Risks & Open Questions for Engineering
*   **Product / Business Risks**: <Adoption, workflow friction, role conflict, or quality risks>
*   **Questions for Engineering Grooming**: <High-level feasibility, sizing, or integration questions to clarify with engineering>
