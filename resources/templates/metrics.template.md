---
schema_version: "1.0"
generated_at_commit: "<git-sha-or-UNCOMMITTED>"
generated_at_timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
---

# Product Metrics & Telemetry Contract (`METRICS.md`)

> **Contract Cap**: Maximum 300 lines (~3,500 tokens). Re-running `/pm-discover` preserves `## Human-Curated Metric Targets (Preserved Across Runs)` and refreshes `## Machine-Discovered Telemetry Inventory (Auto-Refreshed)` by reconciling each `Metric ID` against active code emitters.

---

## Human-Curated Metric Targets (Preserved Across Runs)

Every feature evaluated by `/pm-brainstorm` and `/pm-prd` must link a falsifiable causal chain (`Feature Mechanism -> User Behavior Shift -> Input Driver Delta -> North Star Outcome`) to at least one **Input Driver** and one **Guardrail** metric below.

| Metric ID | Tier (North Star / Input Driver / Guardrail) | Definition & Formula | Baseline | Target Delta |
| :--- | :--- | :--- | :--- | :--- |
| `MET-NS-01` | `North Star` | `[NEEDS_PM_INPUT: Primary business/product outcome formula]` | `[NEEDS_PM_INPUT: Current value or UNKNOWN_COLD_START]` | `[NEEDS_PM_INPUT: Target improvement over window]` |
| `MET-DRV-01` | `Input Driver` | `[NEEDS_PM_INPUT: Leading behavioral indicator directly moved by feature UX/backend]` | `[NEEDS_PM_INPUT: Current value or UNKNOWN_COLD_START]` | `[NEEDS_PM_INPUT: Target delta]` |
| `MET-GRD-01` | `Guardrail` | `[NEEDS_PM_INPUT: Counter-metric protecting latency, error rate, unit cost, or quality]` | `[NEEDS_PM_INPUT: Current threshold]` | `[NEEDS_PM_INPUT: Max acceptable regression]` |

---

## Machine-Discovered Telemetry Inventory (Auto-Refreshed)

### Telemetry Readiness Enum
*   **`INSTRUMENTED_IN_CODE`**: Active emission call site verified in source code with entity correlation keys (`user_id`, `tenant_id`, `session_id`, `trace_id`) and destination sink.
*   **`INSTRUMENTATION_REQUIRED`**: Metric is defined in `## Human-Curated Metric Targets`, but no active emitter exists in code. Any feature targeting this metric automatically receives an `ADAPT_NOW` telemetry instrumentation requirement in its Day-1 MVP slice.
*   **`SLA_INVARIANT`**: Binary latency, reliability, security, or compliance threshold verified via automated tests or infrastructure monitors rather than user event analytics.

| Metric ID | Telemetry Readiness | Call-Site Citation [file:function:line] | Entity Join Keys | Sink / Table |
| :--- | :--- | :--- | :--- | :--- |
| `MET-NS-01` | `INSTRUMENTATION_REQUIRED` | `NONE (No emitter found in repository)` | `user_id, tenant_id` | `analytics.events` |
| `MET-DRV-01` | `INSTRUMENTED_IN_CODE` | `[path/to/file:emit_event:42]` | `user_id, session_id, trace_id` | `analytics.events` |
| `MET-GRD-01` | `SLA_INVARIANT` | `[path/to/middleware:record_latency:88]` | `request_id, route` | `prometheus / logs` |
