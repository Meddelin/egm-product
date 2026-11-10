---
name: pm-discover
description: Discover repository capabilities, data schemas, UI design tokens, and product metrics to build or refresh PRODUCT_CONTEXT.md and METRICS.md.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 1: Assisted Product & Metric Discovery (`pm-discover`)

Read [`../../resources/execution_instructions.md`](../../resources/execution_instructions.md) (or `${CLAUDE_PLUGIN_ROOT}/resources/execution_instructions.md` in Claude Code) before starting.

`pm-discover` builds and non-destructively refreshes the Layer 1 Repository Context Contracts (`PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/schemas.md`, and `.pm/ui_tokens.md`) so the 4 + 1 PM Goldfish swarm can evaluate features against your real codebase without domain-specific hardcoding.

---

## Step 1: Single-Pass Repository Scan (Read-Only Discovery)

1.  **Check Existing Contracts & Incremental Diff**:
    *   Check whether `PRODUCT_CONTEXT.md` and `METRICS.md` already exist in the repository root.
    *   If they exist and contain a `generated_at_commit` SHA in YAML frontmatter, verify whether the commit is reachable via `git cat-file -e <generated_at_commit>^{commit}`.
        *   If reachable, run `git diff --name-only <generated_at_commit>..HEAD` to scope the refresh to modified routes, schemas, telemetry emitters, and stylesheets while preserving `## Human-Curated Strategy (Preserved Across Runs)` and `## Human-Curated Metric Targets (Preserved Across Runs)`.
        *   If the commit is unreachable (for example, after a rebase or shallow clone) or the files do not exist, perform a full single-pass scan of the machine-discovered sections.
2.  **Extract Machine-Discovered Capabilities**:
    *   Read root build manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.) and any existing directory `README.md` contracts (read-only; never modify `README.md` files).
    *   Locate primary API routes/controllers, domain services, background workers, authentication/RBAC middleware, and feature-flag hooks.
    *   Collect raw analytics/telemetry emission call sites (`track`, `emit`, `log_event`, ` capture`, Prometheus counters/histograms, or shared telemetry middleware wrappers) in memory for Step 3 reconciliation.
3.  **Write Bounded On-Demand Catalogs (`.pm/schemas.md` and `.pm/ui_tokens.md`)**:
    *   Write `.pm/schemas.md` (**hard cap: 400 lines**) as a single flat Markdown index table:
        `| Entity / Model Name | Source File & Line Range | Key Fields & Types | Relations / Notes |`
    *   Write `.pm/ui_tokens.md` (**hard cap: 200 lines**) by extracting design tokens from repository CSS/SCSS variables, Tailwind configs (`tailwind.config.*`), or JS/TS theme objects and normalizing them into standard `:root` CSS custom properties (`--pm-surface-0`, `--pm-surface-1`, `--pm-surface-2`, `--pm-surface-3`, `--pm-text-primary`, `--pm-text-secondary`, `--pm-accent`, `--pm-border`, `--pm-radius-sm`, `--pm-radius-md`, `--pm-radius-lg`, `--pm-space-1..6`, `--pm-font-sans`, `--pm-font-mono`). If the repository is backend-only with no UI stylesheets, write a clean neutral system token palette and note `Source: Neutral System Fallback (Backend-Only Repo)`.

---

## Step 2: Targeted PM Interview (`[NEEDS_PM_INPUT]`)

If `## Human-Curated Strategy (Preserved Across Runs)` in `PRODUCT_CONTEXT.md` or `## Human-Curated Metric Targets (Preserved Across Runs)` in `METRICS.md` is missing or contains `[NEEDS_PM_INPUT]` placeholders, interview the Product Manager **one question at a time** (following [`../../resources/execution_instructions.md`](../../resources/execution_instructions.md)) to capture:

1.  **Product Identity & Strategic Archetype**:
    *   What is the 1–3 sentence product summary, primary user persona, and strategic archetype (`INTERNAL_TOOL`, `INTERNAL_PLATFORM_SERVICE`, or `B2B_COMMERCIALIZATION_CANDIDATE`)?
2.  **Team Ownership Boundaries**:
    *   Which services/tables does this team own directly (`READY_NOW` / `ADAPT_NOW` boundary) versus which upstream data producers or platform APIs are owned by external teams (`BLOCKED_NOW` boundary)?
3.  **Metric Hierarchy & Guardrails**:
    *   What is the **North Star Metric** (`MET-NS-01`), the primary **Input Driver Metrics** (`MET-DRV-*`, with current baseline and target delta, or `UNKNOWN_COLD_START`), and the **Counter-Metric Guardrails** (`MET-GRD-*`, such as p95 latency, error rate, cost per query, or answer/ranking quality)?

---

## Step 3: Telemetry Reconciliation & Atomic Contract Write

1.  **In-Memory Telemetry Reconciliation**:
    *   Cross-reference each `Metric ID` defined by the PM in Step 2 against the raw telemetry emission call sites discovered in Step 1.
    *   Assign each `Metric ID` one of the three `Telemetry Readiness` states in `## Machine-Discovered Telemetry Inventory (Auto-Refreshed)`:
        *   `INSTRUMENTED_IN_CODE`: Active emission call site verified (`[file:function:line]`) with entity join keys (`user_id`, `tenant_id`, `trace_id`) and destination table/sink.
        *   `INSTRUMENTATION_REQUIRED`: Metric is defined by the PM, but no active emission call site exists in code (this will automatically schedule an `ADAPT_NOW` instrumentation requirement in features targeting this metric).
        *   `SLA_INVARIANT`: Binary latency, uptime, security, or compliance threshold verified via automated tests or infrastructure monitors.
2.  **Write Contracts**:
    *   Write `PRODUCT_CONTEXT.md` (**hard cap: 300 lines**) conforming to [`../../resources/templates/product_context.template.md`](../../resources/templates/product_context.template.md).
    *   Write `METRICS.md` (**hard cap: 300 lines**) conforming to [`../../resources/templates/metrics.template.md`](../../resources/templates/metrics.template.md).
3.  **Completion & Next-Stage Gate**:
    *   If `pm-discover` was invoked inline by [`../pm-brainstorm/SKILL.md`](../pm-brainstorm/SKILL.md) or [`../pm-prd/SKILL.md`](../pm-prd/SKILL.md) via the Inline Bootstrap Recovery Gate, return control immediately to the calling skill using the preserved initial user prompt.
    *   Otherwise, present a single-select gate offering to proceed to [`/pm-brainstorm`](../pm-brainstorm/SKILL.md) or conclude discovery.
