---
schema_version: "2.0"
updated_at: "<YYYY-MM-DD>"
---

# Organizational & Domain Context (`COMPANY_CONTEXT.md`)

> **Optional Reusable Context Contract (`<= 200 lines`)**: Captures company-wide business context, organizational contours, shared terminology, and governance norms so multiple internal or external products do not repeat them. Store at `~/.pm/COMPANY_CONTEXT.md` (shared across projects) or `./COMPANY_CONTEXT.md` (project override), or pass existing company/strategy docs via `/pm-discover --context <path>`. Never assume every role listed here uses a specific product—actual product users are mapped empirically in `PRODUCT_CONTEXT.md`.

---

## 1. Organization Profile & Strategic Priorities
*   **Company / Organization Summary**: `[NEEDS_PM_INPUT: Core business model, operating domains, and value delivered]`
*   **Business Units & Contours**: `[NEEDS_PM_INPUT: Key departments, operational contours, or internal ecosystems]`
*   **Current Strategic Horizon**: `[NEEDS_PM_INPUT: Company-level priorities and constraints that guide product trade-offs]`

## 2. Organizational Role Directory (Context Only — Not Assumed Product Users)
> Reference catalog of roles across the organization. `/pm-discover` maps **only** the roles that empirically interact with a given product into `PRODUCT_CONTEXT.md`.

| Org Role Name | Organizational Responsibility | Typical Decisions / Handoffs |
| :--- | :--- | :--- |
| `<Role Name>` | `[NEEDS_PM_INPUT: Role's responsibility in the company]` | `[NEEDS_PM_INPUT: Key decisions, operational tasks, or approvals owned]` |

## 3. Shared Domain Glossary
*   **`<Term / Acronym>`**: `[NEEDS_PM_INPUT: Plain-language definition so PRDs and UI copy use exact company terminology]`

## 4. Business Governance, Privacy & Approval Norms
*   **Data Sensitivity & Access Boundaries**: `[NEEDS_PM_INPUT: Confidential, financial, editorial, or customer-data visibility rules]`
*   **Approvals & Auditability Norms**: `[NEEDS_PM_INPUT: Maker-checker / four-eyes approvals, audit trail expectations, or operational blast-radius safeguards]`
