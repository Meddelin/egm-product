---
schema_version: "2.0"
updated_at: "<YYYY-MM-DD>"
---

# Product Metrics & Experimentation Contract (`METRICS.md`)

> **Contract Cap**: Maximum 200 lines. Defines the product's North Star, leading input drivers, counter-metric guardrails, and domain-level product analytics vocabulary in business terms (without source-code line citations).

---

## 1. Product Metric Tree

Every feature shaped in `/pm-brainstorm` and `/pm-prd` must connect a falsifiable causal chain (`Product Change -> User Behavior Shift -> Input Driver Delta -> North Star Outcome`) to at least one **Input Driver** and one **Guardrail** below.

| Metric ID | Tier (`North Star` / `Input Driver` / `Guardrail`) | Role Segment (`ALL_ROLES` or `ROLE-xx`) | Definition & Business Formula | Current Baseline | Target Goal / Threshold |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `MET-NS-01` | `North Star` | `ALL_ROLES` | `[NEEDS_PM_INPUT: Core user/business value outcome formula]` | `[NEEDS_PM_INPUT: Current value or UNKNOWN_COLD_START]` | `[NEEDS_PM_INPUT: Target improvement]` |
| `MET-DRV-01` | `Input Driver` | `[NEEDS_PM_INPUT: ALL_ROLES or specific ROLE-01]` | `[NEEDS_PM_INPUT: Leading user behavior directly moved by product changes]` | `[NEEDS_PM_INPUT: Current value or UNKNOWN_COLD_START]` | `[NEEDS_PM_INPUT: Target delta]` |
| `MET-GRD-01` | `Guardrail` | `ALL_ROLES` | `[NEEDS_PM_INPUT: Counter-metric protecting task completion quality, error rate, speed, or unit cost]` | `[NEEDS_PM_INPUT: Current acceptable bound]` | `[NEEDS_PM_INPUT: Max acceptable regression]` |

---

## 2. Domain Product Events & Rollout Norms
*   **Core Funnel / Lifecycle Events (Product Vocabulary)**: `[NEEDS_PM_INPUT: Key user milestones in business language — e.g., Search Submitted, Result Opened, Draft Submitted, Item Approved — and key breakdown dimensions such as role or cohort]`
*   **Experimentation & Decision Norms**: `[NEEDS_PM_INPUT: How launches are evaluated — e.g., A/B test, staged rollout by role/department, pilot cohort feedback, or kill/pivot window]`
