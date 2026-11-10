---
name: pm-prototype
description: Generate a zero-build, standalone interactive HTML/CSS/JS prototype for an approved PRD using extracted repository design tokens and Stageshow UI craft rules.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 5: Zero-Build Interactive HTML Prototyping (`pm-prototype`)

Read [`../../resources/execution_instructions.md`](../../resources/execution_instructions.md) before starting.

`pm-prototype` runs **after** [`/pm-review`](../pm-review/SKILL.md) has locked the active `READY_NOW` and `ADAPT_NOW` MVP scope in `docs/product/<feature-slug>/prd.md`. It generates a self-contained, zero-build HTML/CSS/JS prototype at `docs/product/<feature-slug>/prototype.html` without touching any host application source files or build manifests.

---

## Step 1: Intake & Scope Verification

1.  **Read Locked PRD & Design Tokens**:
    *   Read `docs/product/<feature-slug>/prd.md` (specifically `## Critical User Journeys (CUJs)`, `### UX State & Fallback Matrix`, and `## Scope Classification (READY_NOW / ADAPT_NOW)`).
    *   Read `.pm/ui_tokens.md` (and `PRODUCT_CONTEXT.md`). If `.pm/ui_tokens.md` does not exist yet, extract `:root` CSS custom properties from the repository's stylesheets/theme config into `.pm/ui_tokens.md` (max 200 lines) or initialize the neutral system fallback palette.
2.  **Zero `BLOCKED_NOW` Scope Rule**:
    *   Verify that only `READY_NOW` and `ADAPT_NOW` requirements are rendered in the prototype. Never render controls or data fields that were deferred to `## Prerequisite Ledger (BLOCKED_NOW)`.

---

## Step 2: Sandbox & Embedded Stageshow UI Craft Rules

Generate `docs/product/<feature-slug>/prototype.html` under the following strict architectural and visual craft invariants:

1.  **Zero-Build & Offline Sandbox Invariants**:
    *   **Single Self-Contained File**: Write plain HTML5, scoped `<style>`, and vanilla `<script>` inside `docs/product/<feature-slug>/prototype.html` (**hard cap: 400 lines**).
    *   **Zero Host Repo Mutation**: Never modify `package.json`, `tsconfig.json`, or any file outside `docs/product/<feature-slug>/`.
    *   **Zero External Network Requests**: Never load external CDN fonts, external scripts, or unbundled remote images (`http://` or `https://`). All icons must be inline single-family stroke SVGs so offline/headless browser rendering achieves `console.error = 0` and `pageerror = 0`.
2.  **3–4 Switchable Interactive States**:
    *   Include a compact, non-intrusive state switcher bar at the top or corner of the stage allowing the PM and engineers to toggle interactively between the states defined in `### UX State & Fallback Matrix`:
        1.  `Default / Ready` (populated realistic domain records and primary user action)
        2.  `Loading / Streaming` (skeleton matching the exact row geometry and line box of the real content)
        3.  `Empty / Zero-Result` (calm empty state with one clear recovery/reset action)
        4.  `Error / Low-Confidence Fallback` (deterministic fallback banner/card mapped to the PRD's guardrail threshold)
3.  **Embedded Stageshow UI Craft Standard**:
    *   **Token Fidelity**: Bind all surfaces, text, borders, radii, and accents to the `:root` CSS custom properties from `.pm/ui_tokens.md` (`--pm-surface-0..3`, `--pm-text-primary`, `--pm-text-secondary`, `--pm-accent`, `--pm-border`, `--pm-radius-*`, `--pm-space-*`).
    *   **Surface Restraint (3–4 Levels Max)**: Use quiet surface steps (`canvas -> window/panel -> raised row/control -> floating popover`). Never nest bordered cards inside bordered cards (`cards-in-cards`), and never add neon glows or redundant tonal borders.
    *   **Typography & Hierarchy**: Use sentence case across headings, labels, and buttons (never tracked all-caps spam). Keep UI text at `12px–15px` with `line-height >= 1.3`. Group a title over its subtitle as one unit (`4px–6px` gap; never `space-between` voids). Apply `font-variant-numeric: tabular-nums` on all metrics, counts, latencies, and prices, and `white-space: nowrap; flex-shrink: 0` on status pills and badges.
    *   **Spacing & Reading-Edge Alignment**: Maintain at least `12px` content inset from container edges and at least `8px` gap between interactive controls. Align left reading edges across headers, form fields, and table/list rows using shared grid column tracks.
    *   **Icon & Anti-Slop Discipline**: Use one consistent inline SVG stroke family (`14px–16px`, uniform `1.5px` or `1.75px` stroke width, `flex: none`). Never use emoji as UI icons, never draw purple-to-pink AI gradients, and never add generic AI sparkle/wand decorations.
    *   **Responsive Reflow**: Support both `390×844` mobile and `1440×900` desktop viewports cleanly without horizontal overflow or clipped labels.

---

## Step 3: Progressive Headless Browser & `stageshow-critic` Verification

1.  **Static Self-Check (Always Required)**:
    *   Verify `docs/product/<feature-slug>/prototype.html` is under 400 lines, contains zero external network URLs, defines `:root` tokens from `.pm/ui_tokens.md`, and implements all 3–4 interactive states from `prd.md`.
2.  **Progressive Live Browser & Visual Critic Check (When Available)**:
    *   If headless browser automation (Playwright / Puppeteer / browser tool) is available in the host session:
        *   Render `file:///.../docs/product/<feature-slug>/prototype.html` at `390×844` (mobile) and `1440×900` (desktop).
        *   Verify `console.error = 0` and `pageerror = 0` while toggling through all interactive states.
        *   If the `stageshow-critic` subagent is available in the harness, invoke `stageshow-critic` with the captured `390×844` and `1440×900` screenshots to audit visual craft and fix any layout or hierarchy defects before presenting the prototype.
3.  **Deliverable Presentation**:
    *   Present the clickable file link to `docs/product/<feature-slug>/prototype.html` alongside `docs/product/<feature-slug>/prd.md`, noting that the specification and interactive preview are ready for stakeholder review or engineering handoff via `/egm-draft docs/product/<feature-slug>/prd.md`.
