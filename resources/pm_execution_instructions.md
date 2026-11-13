# Shared Execution Instructions (`egm-product`)

All skills and subagents in `egm-product` must adhere to the following operational rules:

## 1. Product-First Boundary & Sandbox Isolation
*   **Product Owns "What, For Whom & Why" — Engineering Owns "How"**: Operate strictly in product, user, business-rule, workflow, UX, and metric terms. Never turn product artifacts into pseudo-technical specs: do **not** inspect database schemas, require source-code `[file:line]` citations, design backend APIs/migrations, or track git commit SHAs. Technical architecture belongs downstream to `/egm-draft` or coding agents after the PRD is approved.
*   **Light Repository Awareness Only**: When run inside a code repository, inspect existing product surfaces only at a high level to understand live user-facing screens/flows and extract visual CSS design tokens (`.pm/ui_tokens.md`) for prototyping.
*   **Never Mutate Host Application Code**: Only create or modify product/company context contracts (`PRODUCT_CONTEXT.md`, `METRICS.md`, optional `COMPANY_CONTEXT.md`, `.pm/ui_tokens.md`) and product feature artifacts under `docs/product/<feature-slug>/` (`opportunity_brief.md`, `prd.md`, `pm_review_report.md`, `prototype.html`). When `EGM artifact directory: <path>` is specified in the prompt, `CLAUDE.md`, or `AGENTS.md`, route working review/diagnostic reports (`pm_review_report.md` and scratch files) to `<path>` while keeping committed feature deliverables in `docs/product/<feature-slug>/`. Never edit `package.json`, `pyproject.toml`, application source files, or host `README.md` files (including engineering `egm-bootstrap` contracts), and never run `git commit` or `git push` autonomously.

## 2. Artifact-First Delivery
*   Always write or update the target Markdown or HTML artifact on disk **before** presenting a gate or summary to the Product Manager.
*   Never emit a structured question tool call with an empty chat message: always output a concise conversational summary and a link to the saved artifact first, then present the gate.

## 3. Plain-English Standard
*   Write in direct, objective, falsifiable product prose free of unexplained engineering jargon.
*   **Banned Vocabulary**: Never use validating or flattering adjectives (`great`, `brilliant`, `smart`, `correct`, `perfect`, `excellent`, `spot-on`), polite apologies (`I apologize`, `I am sorry`), or promotional buzzwords (`seamless`, `robust`, `blazingly fast`, `seamlessly`, `effortlessly`, `literally`, `drastically`, `obviously`).

## 4. Customer Evidence & Empirical Role Grounding
*   **Demand Evidence Posture**: Challenge whether the proposed user pain point and behavior shift rest on empirical evidence (`EVIDENCE_BACKED`: user research, support tickets, search/funnel analytics, or connected workspace docs) or on an unverified hypothesis (`UNVALIDATED_ASSUMPTION`). When `UNVALIDATED_ASSUMPTION`, require an explicit **Validation Hypothesis & Kill/Pivot Criterion** (measurable adoption/outcome threshold over a bounded window) rather than blocking exploration.
*   **Empirical Role & Organizational Grounding (`Zero Assumed Personas`)**: Never invent persona stereotypes or assume how executives, engineers, PMs, editors, support, or operations staff use a product before inspecting product evidence, `METRICS.md`, company/strategy docs (`--context <path>` > `./COMPANY_CONTEXT.md` > `~/.pm/COMPANY_CONTEXT.md` > `NONE`, recorded in `PRODUCT_CONTEXT.md` as `company_context_source`), and PM answers. Map actual product roles into `Active Product Roles & Workflows` in `PRODUCT_CONTEXT.md` (`1` row for single-role tools; `N` rows when scenarios diverge). Activate multi-role `CUJs`, `### Cross-Role Handoffs & Permissions`, role-segmented metrics, and `prototype.html` role switching **only** when a feature genuinely affects `>= 2` distinct roles.

## 5. Interactive Question Protocol (Progression Gates vs. Trade-Off Gates)
*   **Open-Ended Clarification**: Ask at most **one** open-ended question per turn in plain text when exploring problem framing, user pain points, roles, or metric goals. Never use multiple-choice tools during open-ended exploration.
*   **Structured Checkpoint Gates**: Call the harness's structured question tool (`ask_question` / `ask_user_question` / `AskUserQuestion` / `request_user_input`) with strictly **one** single-select question (`len(questions) == 1`, `is_multi_select: false`):
    *   **Progression Gates** (advancing to the next drafting step, running inline bootstrap discovery, or launching the Product Goldfish swarm): Place the standard forward action first prefixed with `(Recommended)`.
    *   **Trade-Off & Escalation Gates** (`ESCALATE` dispositions during PRD review, choosing between competing MVP scope cuts in `/pm-brainstorm`, or strategic product forks): **Owner Decides Product Scope** — **DO NOT** add `(Recommended)` or rank options. Present up to 3 neutral, action-oriented choices stating each option's user value and trade-off.
*   **Terminal Chat Fallback (For CLI Harnesses Without a Question Tool)**: Render the single question and its options as a numbered Markdown list (`1. ...`, `2. ...`, `3. ...`) at the end of your turn and wait for the user's reply.

## 6. MVP Scope Consistency Across Artifacts
*   Before finalizing `opportunity_brief.md`, `prd.md`, or `prototype.html`, verify that every capability placed under `### Deferred & Out of Scope (Not in MVP)` (in `opportunity_brief.md`) or `### Non-Goals (Out of Scope / Deferred)` (in `prd.md`) is completely absent from `### MVP Scope`, active `CUJs`, `## 4. Functional Requirements, Business Rules & Edge Cases`, and `prototype.html`.
