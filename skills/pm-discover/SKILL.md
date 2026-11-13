---
name: pm-discover
description: Get acquainted with the product, company context, empirical user roles, existing user-facing capabilities, UI design tokens, and product metric tree to build PRODUCT_CONTEXT.md and METRICS.md.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 1: Product, Role & Metric Discovery (`pm-discover`)

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.
Read [`../../resources/pm_execution_instructions.md`](../../resources/pm_execution_instructions.md) (or `${CLAUDE_PLUGIN_ROOT}/resources/pm_execution_instructions.md` in Claude Code) before starting.

`pm-discover` builds and refreshes the Layer 1 Product Context Contracts (`PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/ui_tokens.md`, and optional `COMPANY_CONTEXT.md`). When run inside an existing repository, it uses the lightweight [`pm-product-scanner`](../../agents/pm_product_scanner.md) subagent only to understand **live user-facing screens/capabilities** and extract visual CSS tokens for prototyping—never dumping database schemas or backend internals.

---

## Step 1: Light Product-Surface & Visual Token Overview

1.  **Resolve Optional Monorepo Scope & Company/Strategy Docs**:
    *   Accept optional `--scope <subdir>` (default `.`) and optional `--context <path>` pointing to company, org-structure, glossary, or product-strategy docs.
    *   Resolve organizational context under strict precedence: `--context <path>` > `./COMPANY_CONTEXT.md` > `~/.pm/COMPANY_CONTEXT.md` > `NONE`, recording the resolved source in `PRODUCT_CONTEXT.md` frontmatter as `company_context_source`.
2.  **Skim Existing Product Surface via `pm-product-scanner`**:
    *   Spawn [`pm-product-scanner`](../../agents/pm_product_scanner.md) (`${CLAUDE_PLUGIN_ROOT}/agents/pm_product_scanner.md` in Claude Code) in read-only mode with `Scope Subdirectory: <subdir or .>` and any resolved company/strategy doc paths (*fallback*: perform the bounded 20-file skim inline only if subagent tools are unavailable).
    *   Write `.pm/ui_tokens.md` (**hard cap: 150 lines**) from `pm-product-scanner`'s CSS token payload (`--pm-surface-0..3`, `--pm-text-primary`, `--pm-text-secondary`, `--pm-accent`, `--pm-border`, `--pm-radius-sm|md|lg`, `--pm-space-1..6`, `--pm-font-sans`, `--pm-font-mono`).

---

## Step 2: Targeted Product Manager Interview (`[NEEDS_PM_INPUT]`)

Preserving any human-curated sections already filled in existing `PRODUCT_CONTEXT.md` or `METRICS.md`, interview the Product Manager **one open-ended question at a time** in plain chat (never via multiple-choice tools) for any missing context:

1.  **Product Identity, Company Context & Strategy**:
    *   Share the brief user-surface summary returned by `pm-product-scanner` (plus any pre-filled notes from `COMPANY_CONTEXT.md` / `--context` docs) and clarify the product's core value proposition, archetype (`Internal Corporate Product`, `Internal Platform`, `B2B SaaS`, `B2C Product`, etc.), and current strategic priorities.
2.  **Empirical Product Roles & Workflows (`Zero Assumed Personas`)**:
    *   Ask which real user/company groups **actually** use, configure, or approve things in *this* product, what job-to-be-done and usage cadence/UI need each group has (`1` row for single-role tools; multiple `ROLE-xx` rows only where goals, workflows, or permissions genuinely diverge), which company roles are out of scope (or `NONE` for single-role consumer products), and what customer/problem evidence sources exist (`docs/research/`, interviews, support tickets, analytics, or `NONE_COLD_START`). Never invent persona stereotypes.
3.  **Product Metric Tree & Guardrails**:
    *   Clarify the **North Star Metric** (`MET-NS-01`), leading **Input Driver Metrics** (`MET-DRV-*` with `Role Segment`: `ALL_ROLES` or `ROLE-xx`), **Counter-Metric Guardrails** (`MET-GRD-*`), and domain-level funnel events / experimentation norms.

---

## Step 3: Write Contracts & Handoff

1.  **Save Contracts**:
    *   Write `PRODUCT_CONTEXT.md` (**hard cap: 250 lines**) conforming to [`../../resources/templates/product_context.template.md`](../../resources/templates/product_context.template.md) (`${CLAUDE_PLUGIN_ROOT}/resources/templates/product_context.template.md`).
    *   Write `METRICS.md` (**hard cap: 200 lines**) conforming to [`../../resources/templates/metrics.template.md`](../../resources/templates/metrics.template.md) (`${CLAUDE_PLUGIN_ROOT}/resources/templates/metrics.template.md`).
    *   If the PM asks to persist reusable company-wide glossary and governance context across projects, write `./COMPANY_CONTEXT.md` (or `~/.pm/COMPANY_CONTEXT.md` when requested, **hard cap: 200 lines**) conforming to [`../../resources/templates/company_context.template.md`](../../resources/templates/company_context.template.md) (`${CLAUDE_PLUGIN_ROOT}/resources/templates/company_context.template.md`).
2.  **Completion & Next-Stage Progression Gate**:
    *   If `pm-discover` was invoked inline by [`../pm-brainstorm/SKILL.md`](../pm-brainstorm/SKILL.md) or [`../pm-prd/SKILL.md`](../pm-prd/SKILL.md), return control immediately to the calling skill in the current thread.
    *   Otherwise, summarize the saved product contracts and present a Progression Gate: `(Recommended) Proceed to /pm-brainstorm` vs. `Conclude discovery`.
