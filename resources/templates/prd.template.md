# PRD: <Feature Title> (`<feature-slug>`)

*   **Author:** <pm-name>
*   **Status:** Draft | Approved
*   **Date:** <YYYY-MM-DD>
*   **Opportunity Brief:** `docs/product/<feature-slug>/opportunity_brief.md`

--------------------------------------------------------------------------------

## Overview

<Concise summary of the feature, the system capabilities it builds upon in `PRODUCT_CONTEXT.md`, and the approved Day-1 MVP slice (`READY_NOW` and `ADAPT_NOW` requirements).>

## The Problem

<Concrete user workflow friction, capability-to-workflow gap, or system bottleneck backed by repository citations and `METRICS.md` baselines.>

## Goals

*   **`REQ-001` (<Title>)**: <Measurable Day-1 capability (`READY_NOW`)>
*   **`REQ-002` (<Title>)**: <Measurable adapted capability or telemetry instrumentation task (`ADAPT_NOW`)>

## Non-Goals

*   **Deferred `BLOCKED_NOW` Scope**: `REQ-003` (tracked exclusively under `## Prerequisite Ledger (BLOCKED_NOW)` and excluded from Day-1 implementation).
*   <Explicit non-goals>

## Metrics & Telemetry Contract

*   **Falsifiable Causal Chain**:
    `Feature Mechanism -> User Behavior Shift -> Input Driver Delta -> North Star Outcome`

| Metric ID | Role (North Star / Input Driver / Guardrail) | Baseline | Target Delta | Telemetry Readiness | Call-Site / Instrumentation Spec `[file:function:line]` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `MET-NS-01` | `North Star` | `<Baseline>` | `<Target>` | `INSTRUMENTED_IN_CODE` | `[path/to/file:func:line]` |
| `MET-DRV-01` | `Input Driver` | `<Baseline>` | `<Target>` | `INSTRUMENTATION_REQUIRED` | Add emitter at `[path/to/file:func:line]` with keys `user_id, tenant_id, trace_id` (`REQ-002`) |
| `MET-GRD-01` | `Guardrail` | `<Threshold>` | `<Max regression>` | `SLA_INVARIANT` | `[path/to/file:func:line]` |

## Critical User Journeys (CUJs)

### CUJ 1: <Primary Day-1 Workflow> (`REQ-001`, `REQ-002`)
*   **Given**: <Initial user state, permissions, and data state>
*   **When**: <User action>
*   **Then**: <Deterministic system response and emitted telemetry event>

### UX State & Fallback Matrix

| UI State | Trigger Condition | User-Visible Copy & Layout Behavior | Mapped Backend Status / Metric ID |
| :--- | :--- | :--- | :--- |
| **Default / Ready** | Valid session and populated data | <Primary view using `.pm/ui_tokens.md` surfaces> | `HTTP 200` / `MET-DRV-01` |
| **Loading / Streaming** | Request in flight (`>150ms`) | <Skeleton matching final row geometry> | `MET-GRD-01` (latency guardrail) |
| **Empty / Zero-Result** | Query returns `0` records | <Actionable empty state with clear filter reset> | `HTTP 200 (count=0)` |
| **Error / Low-Confidence Fallback** | Upstream timeout, `403`, or confidence `< threshold` | <Deterministic fallback message + retry control> | `HTTP 4xx/5xx` / `MET-GRD-01` |

--------------------------------------------------------------------------------

## Scope Classification (READY_NOW / ADAPT_NOW)

| REQ-ID | Requirement Specification | Classification (`READY_NOW` / `ADAPT_NOW`) | Evidence Citation Tuple `[file:symbol_or_line]` | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| `REQ-001` | <Detailed requirement> | `READY_NOW` | `[path/to/service:func:10]`, `[path/to/schema:Model:15]` | <Deterministic test/verification condition> |
| `REQ-002` | <Adapted requirement / telemetry emitter> | `ADAPT_NOW` | `[path/to/handler:emit:45]` | <Deterministic test/verification condition> |

## Data, Quality & Evaluation Gates

*   **Schema & Field Availability**: <Citations to `.pm/schemas.md` verifying required fields are populated>
*   **Evaluation Dataset & Quality Gate (`evals`)**: <Required when search, ranking, retrieval, or LLM generation is touched: golden query/input distribution, pass/fail rubric, and minimum threshold before rollout; state `N/A — Deterministic CRUD workflow` when no AI/ranking logic is involved>

## Security, Cost & Operational Guardrails

*   **Authentication & RBAC/ACL Enforcement**: <Route and retrieval-time permission checks cited from `PRODUCT_CONTEXT.md`>
*   **Unit Economics & Rate/Token Ceilings**: <Max cost/tokens/queries per request and caching/debounce rules>
*   **B2B Multi-Tenant Portability Check**: <Tenant isolation verification when `PRODUCT_CONTEXT.md` specifies `B2B_COMMERCIALIZATION_CANDIDATE`, or `Internal-Only`>
*   **Kill-Switch & Operational Rollback**: <Feature flag or config toggle in `[file:symbol_or_line]` and metric threshold in `METRICS.md` that triggers automatic or manual rollback>

--------------------------------------------------------------------------------

## Alternatives Considered (Alternatives Weighed)

### Alternative A: <Rejected Scope or Unadapted Feature Variant>
*   **Pros**: <Pros>
*   **Cons**: <Why it failed the 4+1 Reality Check>
*   **Reason for Rejection**: <Evidence-backed reason>

--------------------------------------------------------------------------------

## Prerequisite Ledger (BLOCKED_NOW)

> [!IMPORTANT]
> **Engineering Handoff Directive (`/egm-draft` & Coding Agents)**: All requirements listed below `## Prerequisite Ledger (BLOCKED_NOW)` are **OUT OF SCOPE** for the current implementation plan. When `/egm-draft docs/product/<feature-slug>/prd.md` is invoked, generate the technical design specification for `READY_NOW` and `ADAPT_NOW` requirements only, and save the engineering design output to `docs/designs/<feature-slug>.md`.

| REQ-ID | Blocked Requirement | Missing Prerequisite `[service/schema/endpoint/permission]` | Owning Team / Boundary | Unblock Condition |
| :--- | :--- | :--- | :--- | :--- |
| `REQ-003` | <Blocked requirement> | `<Missing schema field / upstream service / permission>` | `<Owning team>` | `<Specific prerequisite required to promote to READY_NOW>` |
