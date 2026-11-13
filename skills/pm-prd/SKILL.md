---
name: pm-prd
description: Draft a clear, user-and-business-focused PRD covering Jobs-to-be-Done (JTBD), User Stories, CUJs, business rules, story-driven screen states, and metrics, then polish it with a built-in 4+1 Product Goldfish review loop.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 3: Product PRD Drafting (JTBD + User Stories) & Built-In 4+1 Review (`pm-prd`)

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.
Read [`../../resources/pm_execution_instructions.md`](../../resources/pm_execution_instructions.md) (`${CLAUDE_PLUGIN_ROOT}/resources/pm_execution_instructions.md` in Claude Code), [`../../resources/templates/prd.template.md`](../../resources/templates/prd.template.md) (`${CLAUDE_PLUGIN_ROOT}/resources/templates/prd.template.md` in Claude Code), [`../../resources/document_standards/prd-standard.md`](../../resources/document_standards/prd-standard.md) (`${CLAUDE_PLUGIN_ROOT}/resources/document_standards/prd-standard.md` in Claude Code), and [`../../docs/harnesses.md`](../../docs/harnesses.md) before starting.

`pm-prd` writes `docs/product/<feature-slug>/prd.md` strictly in product terms—structured around **Jobs-to-be-Done (`JOB-xx`) -> User Stories (`US-xx`) -> Critical User Journeys (`CUJs`) -> Business Rules (`REQ-xx`) -> Story-Driven Screen States -> Product Metrics** (zero database schemas or source-code citations)—then runs a built-in **4 + 1 Product Goldfish Review** (capped at 2 rounds) before `/pm-prototype` or engineering handoff.

---

## Step 0: Intake & Context Check

1.  **Resolve Target Feature & Entry Mode**:
    *   Accept an explicit path to `opportunity_brief.md` or `prd.md`, or resolve the most recently modified `<feature-slug>` under `docs/product/`.
    *   **Inline Bootstrap Recovery Gate**: Verify that `PRODUCT_CONTEXT.md` and `METRICS.md` exist without unresolved `[NEEDS_PM_INPUT]` placeholders. If missing/unpopulated, offer a Progression Gate: `(Recommended) Run inline discovery (/pm-discover) now, then continue /pm-prd` vs. `Stop and configure contracts manually`, executing [`../pm-discover/SKILL.md`](../pm-discover/SKILL.md) (`${CLAUDE_PLUGIN_ROOT}/skills/pm-discover/SKILL.md` in Claude Code) if selected.
    *   **Existing PRD Entry & Review Shortcut**: If `docs/product/<feature-slug>/prd.md` already exists:
        *   If the PM explicitly asks to audit, review, or polish it, read context contracts and jump directly to **Step 3 (Built-In 4+1 Product Goldfish Review)**.
        *   If the PM's intent (review existing vs. redraft) is ambiguous, present a Progression Gate rather than overwriting silently: `(Recommended) Run the built-in 4+1 Product Goldfish review on existing prd.md` vs. `Redraft prd.md from opportunity_brief.md / prompt`.
    *   If neither `prd.md` nor `opportunity_brief.md` exists yet, offer a Progression Gate: `(Recommended) Run /pm-brainstorm first to shape JTBD and MVP scope` vs. `Draft PRD directly from current prompt` (asking at most 2 open-ended clarifying questions, one per turn, covering affected `ROLE-xx` + JTBD + current workaround friction + demand evidence, then target host screen + metric/guardrail if drafting directly).
2.  **Read Product Context**:
    *   Read `PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/ui_tokens.md` (if present), resolved organizational context (`company_context_source`, `./COMPANY_CONTEXT.md`, or `~/.pm/COMPANY_CONTEXT.md` when present), and `docs/product/<feature-slug>/opportunity_brief.md` (when present).

---

## Step 1: Draft Part 1 — Problem, MVP Scope, JTBD, User Stories & CUJs

Write `docs/product/<feature-slug>/prd.md` containing:
*   Metadata header (`Status: Draft`) + top-of-document **Engineering Handoff Directive** from [`prd.template.md`](../../resources/templates/prd.template.md).
*   `## 1. Problem & Strategic Context` (including `Demand Evidence Posture` and `Validation Hypothesis & Kill/Pivot Criterion`).
*   `## 2. Goals & Non-Goals` (separating outcome-oriented `GOAL-01...` items in `### MVP Goals (In Scope)` from `### Non-Goals (Out of Scope / Deferred)`).
*   `## 3. Jobs-to-be-Done (JTBD), User Stories & Scenarios (CUJs)`:
    1.  `### Jobs-to-be-Done (JTBD)`: `JOB-01`... written in authentic Job Story form (`When <concrete situation / trigger>, I want to <motivation / capability>, so I can <expected outcome / progress>`) plus *Current Workaround & Friction* (covering every participating `ROLE-xx` when `>= 2` roles interact; never a circular UI button restatement).
    2.  `### User Stories`: Table of atomic `US-01`, `US-02`... mapping `Parent Job` (`JOB-xx`), empirical `Role ID` (`ROLE-xx`), User Story (`As a <Role>, I want <atomic capability>, so that <observable value>`), and linked `REQ-*` IDs (every `JOB-xx` -> `>= 1` `US-xx`, and every `US-xx` -> `>= 1` `CUJ` & `>= 1` `REQ-*`).
    3.  `### Critical User Journeys (CUJs)`: End-to-end `Given / When / Then` flows tagged with `Role ID`, `US-xx`, and `Entry Point in Product UI` (where in the live product the user initiates the flow).
    4.  `### Cross-Role Handoffs & Permissions`: `Single-Role Scope` on 1-role features, or explicit visibility/action/handoff rules when `>= 2` roles participate.

Output a brief summary with a link to `prd.md` and present a Progression Gate:
*   `(Recommended) Approve Problem, JTBD & User Stories and draft Business Rules, Screen States & Metrics`
*   `Revise Problem, JTBD & User Stories`

---

## Step 2: Draft Part 2 — Business Rules, Story-Driven Screen States, Metrics & Open Questions

Append to `docs/product/<feature-slug>/prd.md`:
*   `## 4. Functional Requirements, Business Rules & Edge Cases` (`REQ-001...` table linked to `US-* / ROLE-*`, covering conflicts, edits, cancellations/undo, limits, permissions/approvals, and user-level AI/search quality expectations when applicable).
*   `## 5. UI Placement, Screen States & Copy` (`Host Screen & UI Mount Point` specifying the exact existing screen/navigation section and mount pattern—inline panel, tab, drawer, modal, split pane, or sub-route—plus `UI Language & Domain Copy` and the **concrete screen states, workflow transitions, and edge/fallback views genuinely dictated by the User Stories (`US-*`), `CUJs`, and business rules**, aligned to `.pm/ui_tokens.md` and the `COMPANY_CONTEXT.md` glossary when present).
*   `## 6. Success Metrics, Product Events & Rollout Plan` (causal chain, `MET-*` targets with `Role Segment` and guardrails, domain-level product analytics events, and rollout/experiment plan).
*   `## 7. Alternatives Considered & Open Questions for Engineering` (product alternatives rejected + high-level questions for engineering).

Verify that zero `Out of Scope` items leaked into active sections, then present a Progression Gate:
*   `(Recommended) Run the built-in 4+1 Product Goldfish review on docs/product/<feature-slug>/prd.md`
*   `Keep docs/product/<feature-slug>/prd.md as Draft without running review`

---

## Step 3: Built-In 4 + 1 Product Goldfish Review & Resolution (Max 2 Rounds)

1.  **Phase 1 (Parallel Product Audit)**:
    *   Spawn the 4 Product Goldfish critics concurrently in `Mode: REVIEW` (read-only, passing `PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/ui_tokens.md` when present, resolved `COMPANY_CONTEXT.md` when present, and `docs/product/<feature-slug>/prd.md`) against [`prd-standard.md`](../../resources/document_standards/prd-standard.md):
        *   [`pm-value-strategy`](../../agents/pm_value_strategy.md) (Pillar 1: Problem & JTBD sharpness, validation gate & MVP focus)
        *   [`pm-ux-flows`](../../agents/pm_ux_flows.md) (Pillar 2: User Stories, role scenarios, cross-role handoffs & story-driven screen states)
        *   [`pm-metrics-experiment`](../../agents/pm_metrics_experiment.md) (Pillar 3: Causal chain, role segments, guardrails & domain events)
        *   [`pm-business-logic`](../../agents/pm_business_logic.md) (Pillar 4: Business rules, edge cases, approvals & engineering questions)
    *   Retry any failed critic **once**.
2.  **Phase 2 (Sequential Synthesis via `pm-synthesizer`)**:
    *   Invoke [`pm-synthesizer`](../../agents/pm_synthesizer.md) in `Mode: REVIEW` (read-only, passing the 4 critic reports, their `completed | retried | failed` execution statuses, and `Review Round` `1` or `2`) and write the compiled report to `docs/product/<feature-slug>/pm_review_report.md` (or `<override_dir>/pm_review_report.md` when `EGM artifact directory` is set).
3.  **Inline Disposition & Neutral Escalation Gates**:
    *   Classify each finding into `PROPOSE FIX` (concrete spec gap to fix directly in `prd.md`), `CONTEST` (false positive or contradicts `PRODUCT_CONTEXT.md` / `METRICS.md`), `ESCALATE` (genuine product scope/policy trade-off requiring PM choice), or `DECLINE` (low-value `Nit` out of proportion to MVP scope).
    *   For any `ESCALATE` product trade-off, present a neutral **Trade-Off Gate** one question per turn *without* `(Recommended)` prefixes (`Owner Decides Product Scope`).
    *   Present the Resolution Progression Gate (`(Recommended) Apply all PROPOSE FIX edits and confirmed ESCALATE decisions`, `Review findings item by item`, or `Continue without changes`) and update `prd.md`.
4.  **Convergence (Max 2 Rounds) & Handoff**:
    *   If any `Blocker` or `Major` finding remains unresolved, set `Status: Draft (Needs Revision)` in `prd.md` and stop.
    *   Else if Round 1 had zero `Blocker`/`Major` findings, set `Status: Approved` in `prd.md`.
    *   Else (Round 1 `Blocker`/`Major` or scope edits were resolved in Step 3.3), offer `(Recommended) Run Round 2 verification pass` vs. `Approve without Round 2` (never exceed 2 total rounds; after Round 2, set `Status: Approved` once zero unresolved `Blocker`/`Major` findings remain, otherwise `Status: Draft (Needs Revision)`).
    *   Once `Status: Approved`, present the final Progression Gate:
        *   `(Recommended) Proceed to /pm-prototype to build docs/product/<feature-slug>/prototype.html inside the real product canvas`
        *   `Conclude PM workflow (PRD approved and ready for engineering)`
    *   If selected, read and execute [`../pm-prototype/SKILL.md`](../pm-prototype/SKILL.md) (`${CLAUDE_PLUGIN_ROOT}/skills/pm-prototype/SKILL.md` in Claude Code).
