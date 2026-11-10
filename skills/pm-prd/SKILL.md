---
name: pm-prd
description: Draft a stack-grounded Product Requirements Document (PRD) section-by-section from an Opportunity Brief, separating READY_NOW and ADAPT_NOW MVP scope from the Prerequisite Ledger.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 3: Stack-Grounded PRD Drafting (`pm-prd`)

Read [`../../resources/execution_instructions.md`](../../resources/execution_instructions.md) and [`../../resources/templates/prd.template.md`](../../resources/templates/prd.template.md) before starting.

`pm-prd` drafts `docs/product/<feature-slug>/prd.md` section-by-section with interactive approval gates, ensuring active Day-1 MVP requirements (`READY_NOW` and `ADAPT_NOW`) are backed by `[file:symbol_or_line]` citations and cleanly isolated from `## Prerequisite Ledger (BLOCKED_NOW)`.

---

## Step 0: Intake & Context Verification

1.  **Resolve Target Feature Slug & Opportunity Brief**:
    *   Accept an explicit path to `docs/product/<feature-slug>/opportunity_brief.md` or automatically resolve the most recently modified `<feature-slug>` under `docs/product/` when invoked without arguments.
    *   **Inline Bootstrap Recovery Gate**: Verify that `PRODUCT_CONTEXT.md` and `METRICS.md` exist in the repository root. If either is missing, preserve the user's initial request and offer a single-select gate to run [`../pm-discover/SKILL.md`](../pm-discover/SKILL.md) in-thread before resuming `/pm-prd`.
    *   If no `opportunity_brief.md` exists yet for the requested feature, offer a single-select gate to run [`../pm-brainstorm/SKILL.md`](../pm-brainstorm/SKILL.md) first (recommended) or initialize a brief inline before drafting.
2.  **Read Context Contracts**:
    *   Read `PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/schemas.md`, `.pm/ui_tokens.md`, and `docs/product/<feature-slug>/opportunity_brief.md`.

---

## Step 1: Draft Group 1 — Overview, Problem & Metric Causal Contract

Write the initial `docs/product/<feature-slug>/prd.md` file containing:
*   `## Overview`
*   `## The Problem`
*   `## Goals` (listing only approved `READY_NOW` and `ADAPT_NOW` `REQ-ID`s)
*   `## Non-Goals` (**mandatory**: include an explicit bullet listing all deferred `BLOCKED_NOW` `REQ-ID`s from `opportunity_brief.md`)
*   `## Metrics & Telemetry Contract` (falsifiable causal chain + table mapping `MET-NS-*`, `MET-DRV-*`, and `MET-GRD-*` with `INSTRUMENTED_IN_CODE`, `INSTRUMENTATION_REQUIRED`, or `SLA_INVARIANT` call sites)

Present a single-select Section Approval Gate:
*   `(Recommended) Approve Overview, Goals & Metrics Contract and draft CUJs & UX State Matrix`
*   `Revise Overview, Goals & Metrics Contract`

---

## Step 2: Draft Group 2 — Critical User Journeys & UX State Matrix

Append to `docs/product/<feature-slug>/prd.md`:
*   `## Critical User Journeys (CUJs)` (`Given / When / Then` journeys for active `READY_NOW` and `ADAPT_NOW` scope only)
*   `### UX State & Fallback Matrix` (deterministic table covering **Default / Ready**, **Loading / Streaming**, **Empty / Zero-Result**, and **Error / Low-Confidence Fallback** mapped to backend error codes and `METRICS.md` guardrails)

Present a single-select Section Approval Gate:
*   `(Recommended) Approve CUJs & UX State Matrix and draft Active MVP Scope & System Boundaries`
*   `Revise CUJs & UX State Matrix`

---

## Step 3: Draft Group 3 — Active MVP Scope, Data/Eval Gates & Guardrails

Append to `docs/product/<feature-slug>/prd.md`:
*   `## Scope Classification (READY_NOW / ADAPT_NOW)` (table keyed by `REQ-ID` with `[file:symbol_or_line]` Evidence Citation Tuples and deterministic acceptance criteria, including any `ADAPT_NOW` telemetry instrumentation requirements)
*   `## Data, Quality & Evaluation Gates` (schema citations to `.pm/schemas.md` + golden evaluation dataset rubric `evals` if search, ranking, retrieval, or LLM generation is touched; otherwise `N/A — Deterministic CRUD workflow`)
*   `## Security, Cost & Operational Guardrails` (route/retrieval RBAC/ACL enforcement, unit/token cost ceilings, B2B multi-tenant portability check when `PRODUCT_CONTEXT.md` specifies `B2B_COMMERCIALIZATION_CANDIDATE`, and concrete feature-flag/rollback mechanism)

Present a single-select Section Approval Gate:
*   `(Recommended) Approve Active MVP Scope & Guardrails and draft Alternatives & Prerequisite Ledger`
*   `Revise Active MVP Scope & Guardrails`

---

## Step 4: Draft Group 4 — Alternatives, Prerequisite Ledger & Contradiction Check

1.  Append to `docs/product/<feature-slug>/prd.md`:
    *   `## Alternatives Considered (Alternatives Weighed)`
    *   `## Prerequisite Ledger (BLOCKED_NOW)` followed immediately by the engineering handoff callout banner from [`../../resources/templates/prd.template.md`](../../resources/templates/prd.template.md) instructing `/egm-draft` and coding agents to exclude all `BLOCKED_NOW` rows from engineering implementation plans and save engineering design output to `docs/designs/<feature-slug>.md`.
2.  **Contradiction Reconciliation Pass**:
    *   Verify against `opportunity_brief.md` and [`../../resources/document_standards/prd-standard.md`](../../resources/document_standards/prd-standard.md) that zero `BLOCKED_NOW` requirements leaked into `## Goals`, `## Critical User Journeys (CUJs)`, or `## Scope Classification (READY_NOW / ADAPT_NOW)`.
3.  **Stage Handoff Gate to `/pm-review`**:
    *   Present a single-select gate:
        *   `(Recommended) Proceed to /pm-review to audit docs/product/<feature-slug>/prd.md with the 4+1 PM Goldfish swarm`
        *   `Stop here and keep docs/product/<feature-slug>/prd.md as Draft`
    *   If the PM selects `/pm-review`, read and execute [`../pm-review/SKILL.md`](../pm-review/SKILL.md).
