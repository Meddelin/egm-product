---
schema_version: "2.0"
company_context_source: "<NONE | ./COMPANY_CONTEXT.md | ~/.pm/COMPANY_CONTEXT.md | path/to/docs>"
updated_at: "<YYYY-MM-DD>"
---

# Product Context Contract (`PRODUCT_CONTEXT.md`)

> Captures what the product does for users, strategic context, existing user-facing capabilities, and empirical user roles. Re-running `/pm-discover` updates `## 1. Existing Product Surface (Observed User Capabilities)` and `.pm/ui_tokens.md` while preserving `## 2. Product Identity, Company Context & Strategy (Human-Curated)` and role definitions.

---

## 1. Existing Product Surface (Observed User Capabilities)
*   **Live User Areas & Screens**: `<Plain-language summary of existing user-facing screens, flows, and capabilities observed in the product — or Greenfield>`
*   **Key Integrations & Adjacent Products**: `<External or internal products users move between before/after using this product>`
*   **Visual Design System & Shell Pointer**: `.pm/ui_tokens.md` (App Shell & Navigation Blueprint, Frontend File Map, UI language, component style signatures, and `:root` CSS custom properties used by `/pm-prototype`)

---

## 2. Product Identity, Company Context & Strategy (Human-Curated)
*   **Product Summary & Value Proposition**: `[NEEDS_PM_INPUT: 1–3 sentences explaining what problem this product solves and why it exists]`
*   **Product Archetype**: `[NEEDS_PM_INPUT: Internal Corporate Product | Internal Platform | B2B SaaS | B2C Product | Commercialization Candidate]`
*   **Company & Strategic Context**: `[NEEDS_PM_INPUT: Current strategic goals, business constraints, and key domain terms — or summarized from COMPANY_CONTEXT.md / strategy docs]`

## 3. Active Product Roles & Workflows (Empirical — Zero Assumed Personas)
> List **only** the roles that actually use, configure, or approve things in this product (`1` row for single-role products; multiple rows only when goals, usage frequency, UI needs, or permissions genuinely differ). Never invent stereotyped personas.

| Role ID | User / Company Role | Core Job-to-be-Done in This Product | Empirical Usage Pattern & UI Need | Access & Decision Scope (`View / Act / Approve`) |
| :--- | :--- | :--- | :--- | :--- |
| `ROLE-01` | `[NEEDS_PM_INPUT: Actual user group]` | `[NEEDS_PM_INPUT: Tasks or decisions performed in this product]` | `[NEEDS_PM_INPUT: Observed frequency, workflow/density need, or UNKNOWN_COLD_START]` | `[NEEDS_PM_INPUT: What this role can view, edit, or approve]` |

*   **Out-of-Scope / Non-User Roles**: `[NEEDS_PM_INPUT: Company roles that do NOT use this product directly, or NONE for single-role consumer products]`
*   **Customer & Problem Evidence Sources**: `[NEEDS_PM_INPUT: User interviews, support tickets, search/funnel analytics, docs/research/, or NONE_COLD_START]`
*   **Known Organizational & Product Constraints**: `[NEEDS_PM_INPUT: Cross-team boundaries, compliance/approval rules, or rollout constraints to keep in mind during scoping]`
