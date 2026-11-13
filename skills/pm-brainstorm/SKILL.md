---
name: pm-brainstorm
description: Shape and challenge a feature idea across Jobs-to-be-Done (JTBD), User Stories, customer demand, user roles, simpler alternatives, and product metrics with the 4+1 Product Goldfish swarm to produce an Opportunity Brief.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 2: Product Opportunity, JTBD & 4+1 Challenge (`pm-brainstorm`)

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.
Read [`../../resources/pm_execution_instructions.md`](../../resources/pm_execution_instructions.md) (`${CLAUDE_PLUGIN_ROOT}/resources/pm_execution_instructions.md` in Claude Code) and [`../../docs/harnesses.md`](../../docs/harnesses.md) before starting.

`pm-brainstorm` turns a raw feature idea or product problem into a focused, bloat-free Opportunity Brief (`docs/product/<feature-slug>/opportunity_brief.md`) grounded in concrete **Jobs-to-be-Done (`JOB-xx`)**, role-owned **User Stories (`US-xx`)**, host-screen placement, and falsifiable product metrics—without drifting into backend or database design.

---

## Step 1: Context Check & JTBD / Outcome Drilling

1.  **Preserve Initial Prompt & Check Layer 1 Contracts**:
    *   Record the user's initial request immediately.
    *   Check whether `PRODUCT_CONTEXT.md` and `METRICS.md` exist in the workspace root without unresolved `[NEEDS_PM_INPUT]` placeholders.
    *   **Inline Bootstrap Recovery Gate**: If either file is missing or unpopulated, present a single-select Progression Gate:
        *   `(Recommended) Run inline discovery (/pm-discover) now to capture product, role, UI shell, and metric context, then continue brainstorming`
        *   `Capture minimal product, role, and metric context inline for this feature`
        If Option 1 is selected, read and execute [`../pm-discover/SKILL.md`](../pm-discover/SKILL.md) (`${CLAUDE_PLUGIN_ROOT}/skills/pm-discover/SKILL.md` in Claude Code; never use the `Skill` tool) in-thread, then resume Step 1.2 automatically. If Option 2 is selected, ask at most 2 concise open-ended questions, one per turn (product summary + active role(s) `ROLE-01...`, then target metric + guardrail) and write minimal `PRODUCT_CONTEXT.md` and `METRICS.md` files to disk before proceeding.
2.  **JTBD, Host Screen, Role & Outcome Drilling**:
    *   Read `PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/ui_tokens.md` (when present), and the resolved organizational context (`company_context_source`, `./COMPANY_CONTEXT.md`, or `~/.pm/COMPANY_CONTEXT.md` when present).
    *   If the PM asked for open-ended growth/product ideas, compare `Existing Product Surface` and `Active Product Roles & Workflows` in `PRODUCT_CONTEXT.md` against bottlenecks in `METRICS.md` to propose 2–3 high-leverage product opportunities.
    *   Ask at most **one** open-ended question per turn in plain chat to clarify:
        1.  **Primary Job-to-be-Done (JTBD)** (`When <situation / trigger>, I want to <motivation / action>, so I can <expected outcome>`), **Current Workaround & Friction** (how users handle this today and why it breaks), **Demand Evidence Posture** (`EVIDENCE_BACKED` vs. `UNVALIDATED_ASSUMPTION` + validation & kill criterion), and affected `Role ID`(s) (`Single-Role Scope` vs. `Multi-Role`).
        2.  **Target Product Surface / Host Screen** (which existing screen or navigation section of the product hosts this workflow) and falsifiable metric causal chain (`Product Change -> User Behavior Shift -> Input Driver Delta -> North Star Outcome`) + guardrail (`MET-GRD-*`).
        3.  Candidate `<feature-slug>` (`docs/product/<feature-slug>/`).
3.  **Readiness Progression Gate**:
    *   Summarize the framed JTBD, candidate User Stories, and target screen in 2–3 sentences and present a Progression Gate:
        *   `(Recommended) Challenge this opportunity with the 4+1 Product Goldfish swarm`
        *   `Refine JTBD, problem framing, or target roles first`

---

## Step 2: Two-Phase 4 + 1 Product Goldfish Swarm

Follow the harness delegation rules in [`../../docs/harnesses.md`](../../docs/harnesses.md):

1.  **Phase 1 (Parallel Product Critics)**:
    *   Spawn the 4 Product Goldfish critics concurrently in `Mode: BRAINSTORM` (read-only, passing `PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/ui_tokens.md` when present, resolved `COMPANY_CONTEXT.md` when present, and the opportunity summary):
        *   [`pm-value-strategy`](../../agents/pm_value_strategy.md) (Problem & JTBD sharpness, demand evidence, validation/kill gate & cutting MVP bloat)
        *   [`pm-ux-flows`](../../agents/pm_ux_flows.md) (JTBD-to-User-Story flow, host-screen entry point, empirical role fit & cross-role handoffs)
        *   [`pm-metrics-experiment`](../../agents/pm_metrics_experiment.md) (Causal chain, anti-vanity metrics, role segments & guardrails)
        *   [`pm-business-logic`](../../agents/pm_business_logic.md) (Business rules, permissions/approvals, edge cases & questions for engineering)
    *   Retry any failed Phase 1 subagent **once**.
2.  **Phase 2 (Sequential Synthesis via `pm-synthesizer`)**:
    *   Invoke [`pm-synthesizer`](../../agents/pm_synthesizer.md) in `Mode: BRAINSTORM` (read-only), passing the 4 critic reports and execution statuses (`completed | retried | failed`).
    *   Write the compiled brief conforming to [`../../resources/templates/opportunity_brief.template.md`](../../resources/templates/opportunity_brief.template.md) (`${CLAUDE_PLUGIN_ROOT}/resources/templates/opportunity_brief.template.md`) to `docs/product/<feature-slug>/opportunity_brief.md`.

---

## Step 3: Neutral Scope Trade-Offs & Handoff to `/pm-prd`

1.  **Resolve Product Scope Forks Neutrally**:
    *   If the critics surfaced competing product choices (for example, narrower fast-validation MVP vs. broader multi-role workflow), present a neutral **Trade-Off Gate** *without* `(Recommended)` prefixes (`Owner Decides Product Scope`).
2.  **Approve Brief & Stage Handoff**:
    *   Update `docs/product/<feature-slug>/opportunity_brief.md` with the PM's chosen MVP cut (`Status: Approved for PRD`) and present a Progression Gate:
        *   `(Recommended) Proceed to /pm-prd to draft and review docs/product/<feature-slug>/prd.md`
        *   `Stop here and keep docs/product/<feature-slug>/opportunity_brief.md`
    *   If selected, read and execute [`../pm-prd/SKILL.md`](../pm-prd/SKILL.md) (`${CLAUDE_PLUGIN_ROOT}/skills/pm-prd/SKILL.md` in Claude Code).
