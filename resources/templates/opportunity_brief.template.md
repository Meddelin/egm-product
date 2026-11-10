# Opportunity Brief: <Feature Title> (`<feature-slug>`)

*   **Author:** <pm-name>
*   **Status:** Draft | Approved for PRD
*   **Date:** <YYYY-MM-DD>
*   **Context Contracts:** `PRODUCT_CONTEXT.md` (`<commit>`), `METRICS.md` (`<commit>`)

--------------------------------------------------------------------------------

## 4+1 Swarm Execution Audit Table

| Subagent | Status (completed / retried / failed) | Blockers | Adaptations |
| :--- | :--- | :--- | :--- |
| `pm-value-metrics` | `completed` | 0 | 0 |
| `pm-tech-lead` | `completed` | 0 | 0 |
| `pm-data-eval` | `completed` | 0 | 0 |
| `pm-ux-risk` | `completed` | 0 | 0 |
| `pm-scope-slicer` | `completed` | — | — |

--------------------------------------------------------------------------------

## Overview & Metric Causal Chain

*   **Problem Statement**: <Falsifiable description of the user or system bottleneck grounded in `PRODUCT_CONTEXT.md` and `METRICS.md`>
*   **Target Persona**: <Persona from `PRODUCT_CONTEXT.md`>
*   **Falsifiable Causal Chain**:
    `Feature Mechanism (<change>) -> User Behavior Shift (<action>) -> Input Driver Delta (<Metric ID: baseline -> target>) -> North Star Outcome (<Metric ID>)`
*   **Paired Counter-Metric Guardrail**: `<Metric ID>` (<threshold that must not degrade>)
*   **Telemetry Readiness Status**: `INSTRUMENTED_IN_CODE` | `INSTRUMENTATION_REQUIRED` (adds `ADAPT_NOW` instrumentation requirement) | `SLA_INVARIANT`

--------------------------------------------------------------------------------

## Cross-Functional Reality Check Matrix

> **Precedence Rule**: `BLOCKED_NOW > ADAPT_NOW > READY_NOW`. Every row requires a machine-verifiable `[file:symbol_or_line]` Evidence Citation Tuple.

| REQ-ID | Requirement | Verdict (READY_NOW / ADAPT_NOW / BLOCKED_NOW) | Lens | Evidence Citation [file:symbol_or_line] | Proposed Adaptation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `REQ-001` | <Core capability> | `READY_NOW` | `pm-tech-lead` | `[path/to/service:func:10]` | None — self-contained in owned service. |
| `REQ-002` | <Adapted capability or telemetry task> | `ADAPT_NOW` | `pm-value-metrics` | `[path/to/handler:emit:45]` | Emit `<event_name>` with `user_id, trace_id` on completion. |
| `REQ-003` | <Blocked capability> | `BLOCKED_NOW` | `pm-data-eval` | `[path/to/schema:Model:22]` | Defer to Prerequisite Ledger until upstream producer populates `<field>`. |

--------------------------------------------------------------------------------

## Goals vs. Non-Goals

### Goals (Day-1 MVP Slice: `READY_NOW` + Approved `ADAPT_NOW`)
*   **`REQ-001`**: <Goal statement>
*   **`REQ-002`**: <Adapted goal statement>

### Non-Goals (Out of Scope & Deferred `BLOCKED_NOW` Items)
*   **Deferred `BLOCKED_NOW` Requirements**: `REQ-003` (isolated in `## Prerequisite Ledger (BLOCKED_NOW)`).
*   <Additional explicit exclusions>

--------------------------------------------------------------------------------

## Alternatives Weighed

### Alternative 1: <Unadapted Proposal / Alternative Approach>
*   **Pros**: <Pros>
*   **Cons**: <Why it triggered `BLOCKED_NOW` or degraded guardrails>
*   **Decision**: Rejected in favor of `<ADAPT_NOW counter-proposal>`.

--------------------------------------------------------------------------------

## Prerequisite Ledger (BLOCKED_NOW)

> **Engineering Handoff Boundary**: Items below are **excluded** from the Day-1 MVP slice until their external or architectural prerequisites are satisfied.

| REQ-ID | Blocked Requirement | Missing Prerequisite `[service/schema/endpoint/permission]` | Owning Team / Boundary | Unblock Condition |
| :--- | :--- | :--- | :--- | :--- |
| `REQ-003` | <Blocked capability> | `<Missing upstream field / API / infra>` | `<External team from PRODUCT_CONTEXT.md>` | `<Schema migration or upstream producer contract landed>` |
