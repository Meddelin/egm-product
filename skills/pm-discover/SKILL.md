---
name: pm-discover
description: Get acquainted with the product, company context, empirical user roles, Jobs-to-be-Done, live user-facing screens, UI App Shell & design tokens, and product metric tree to build PRODUCT_CONTEXT.md, METRICS.md, and .pm/ui_tokens.md.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 1: Product, Role, UI Shell & Metric Discovery (`pm-discover`)

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.
Read [`../../resources/pm_execution_instructions.md`](../../resources/pm_execution_instructions.md) (or `${CLAUDE_PLUGIN_ROOT}/resources/pm_execution_instructions.md` in Claude Code) before starting.

`pm-discover` builds and refreshes the Layer 1 Product Context Contracts (`PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/ui_tokens.md`, and optional `COMPANY_CONTEXT.md`). When run inside a repository containing frontend code, it uses [`pm-product-scanner`](../../agents/pm_product_scanner.md) to map **live user-facing screens/navigation** and build a rich **UI Design System & App Shell Blueprint** (`.pm/ui_tokens.md`) so `/pm-prototype` renders directly inside the real product canvas—without dumping database schemas or backend internals into PM specs.

---

## Step 1: Product-Surface & UI Shell Scan

1.  **Resolve Optional Monorepo Scope & Company/Strategy Docs**:
    *   Accept optional `--scope <subdir>` (default `.`) and optional `--context <path>` pointing to company, org-structure, glossary, or product-strategy docs.
    *   Resolve organizational context under strict precedence: `--context <path>` > `./COMPANY_CONTEXT.md` > `~/.pm/COMPANY_CONTEXT.md` > `NONE`, recording the resolved source in `PRODUCT_CONTEXT.md` frontmatter as `company_context_source`.
2.  **Scan Product Surface & Frontend Shell via `pm-product-scanner`**:
    *   Spawn [`pm-product-scanner`](../../agents/pm_product_scanner.md) (`${CLAUDE_PLUGIN_ROOT}/agents/pm_product_scanner.md` in Claude Code) in read-only mode with `Scope Subdirectory: <subdir or .>` and any resolved company/strategy doc paths (*fallback*: perform the frontend/docs scan inline only if subagent tools are unavailable).
    *   Write `.pm/ui_tokens.md` from `pm-product-scanner`'s blueprint, including:
        *   **Scope Subdirectory, Observed UI Copy Language** (including `i18n` locale resolution), styling stack, **default active runtime theme** (`light` vs. `.dark`), and icon set (stroke vs. filled).
        *   **Frontend Canvas File Map** (workspace-root-relative paths to Authenticated App Shell/Route Layout, Navigation + `i18n` locale files, Global Theme/CSS, Core UI Primitives, and Representative Screens).
        *   **App Shell & Component Anatomy** (sidebar/header dimensions, real navigation menu labels, heading/KPI font scale, button/table/card/input/badge visual signatures).
        *   **Normalized `:root` CSS Custom Properties** resolved for the product's default active theme.

---

## Step 2: Targeted Product Manager Interview (`[NEEDS_PM_INPUT]`)

Preserving any human-curated sections already filled in existing `PRODUCT_CONTEXT.md` or `METRICS.md`, interview the Product Manager **one open-ended question at a time** in plain chat (never via multiple-choice tools) for any missing context:

1.  **Product Identity, Company Context & Strategy**:
    *   Share the brief user-surface summary returned by `pm-product-scanner` (plus any pre-filled notes from `COMPANY_CONTEXT.md` / `--context` docs) and clarify the product's core value proposition, archetype (`Internal Corporate Product`, `Internal Platform`, `B2B SaaS`, `B2C Product`, etc.), and current strategic priorities.
2.  **Empirical Product Roles, Jobs-to-be-Done & Workflows (`Zero Assumed Personas`)**:
    *   Ask which real user/company groups **actually** use, configure, or approve things in *this* product, what core **Jobs-to-be-Done (JTBD)** and usage cadence/UI need each group has (`1` row for single-role tools; multiple `ROLE-xx` rows only where goals, workflows, or permissions genuinely diverge), which company roles are out of scope (or `NONE` for single-role consumer products), and what customer/problem evidence sources exist (`docs/research/`, interviews, support tickets, analytics, or `NONE_COLD_START`). Never invent persona stereotypes.
3.  **Product Metric Tree & Guardrails**:
    *   Clarify the **North Star Metric** (`MET-NS-01`), leading **Input Driver Metrics** (`MET-DRV-*` with `Role Segment`: `ALL_ROLES` or `ROLE-xx`), **Counter-Metric Guardrails** (`MET-GRD-*`), and domain-level funnel events / experimentation norms.

---

## Step 3: Write Contracts & Handoff

1.  **Save Contracts**:
    *   Write `PRODUCT_CONTEXT.md` conforming to [`../../resources/templates/product_context.template.md`](../../resources/templates/product_context.template.md) (`${CLAUDE_PLUGIN_ROOT}/resources/templates/product_context.template.md`).
    *   Write `METRICS.md` conforming to [`../../resources/templates/metrics.template.md`](../../resources/templates/metrics.template.md) (`${CLAUDE_PLUGIN_ROOT}/resources/templates/metrics.template.md`).
    *   If the PM asks to persist reusable company-wide glossary and governance context across projects, write `./COMPANY_CONTEXT.md` (or `~/.pm/COMPANY_CONTEXT.md` when requested) conforming to [`../../resources/templates/company_context.template.md`](../../resources/templates/company_context.template.md) (`${CLAUDE_PLUGIN_ROOT}/resources/templates/company_context.template.md`).
2.  **Completion & Next-Stage Progression Gate**:
    *   If `pm-discover` was invoked inline by [`../pm-brainstorm/SKILL.md`](../pm-brainstorm/SKILL.md) or [`../pm-prd/SKILL.md`](../pm-prd/SKILL.md), return control immediately to the calling skill in the current thread.
    *   Otherwise, summarize the saved product contracts and present a Progression Gate: `(Recommended) Proceed to /pm-brainstorm` vs. `Conclude discovery`.
