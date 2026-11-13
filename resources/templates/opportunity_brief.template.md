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

## 1. Problem, Evidence & Causal Hypothesis

*   **User & Business Bottleneck**: <Falsifiable statement of the problem, why it matters now, and what happens if we do nothing>
*   **Affected Product Roles**: `<ROLE-01 (Single-Role Scope) | ROLE-01, ROLE-02 (Multi-Role — explain how goals, views, or handoffs differ across roles from PRODUCT_CONTEXT.md)>`
*   **Demand Evidence Posture**: `EVIDENCE_BACKED` (`<interviews / support tickets / funnel data / research doc>`) | `UNVALIDATED_ASSUMPTION`
*   **Validation Hypothesis & Kill/Pivot Criterion**: <Mandatory when `UNVALIDATED_ASSUMPTION` (recommended for all features): measurable adoption/outcome threshold over N days/users below which we iterate or sunset the feature>
*   **Falsifiable Causal Chain**:
    `Product Change (<mechanism>) -> User Behavior Shift (<action>) -> Input Driver Delta (<Metric ID>) -> North Star Outcome (<Metric ID>)`
*   **Paired Counter-Metric Guardrail**: `<Metric ID>` (<acceptable bound that must not degrade>)

--------------------------------------------------------------------------------

## 2. Proposed Product Solution & MVP Scope Cut

### MVP Scope (`In Scope` — High-Leverage Day-1 Slice)
*   **`REQ-001` (<Capability Title>)**: <User-facing behavior and expected value>
*   **`REQ-002` (<Simplified Workflow / Guardrail>)**: <Simplified product behavior chosen to maximize value without bloat>

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
*   **Questions for Engineering Grooming**: <High-level feasibility, sizing, or integration questions to clarify during `/egm-draft`>
