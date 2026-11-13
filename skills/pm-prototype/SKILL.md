---
name: pm-prototype
description: Generate and audit a zero-build, standalone interactive HTML/CSS/JS prototype from an approved PRD using visual design tokens, pm-ux-flows, and Stageshow craft rules.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 4: Zero-Build Interactive HTML Prototyping (`pm-prototype`)

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.
Read [`../../resources/pm_execution_instructions.md`](../../resources/pm_execution_instructions.md) (`${CLAUDE_PLUGIN_ROOT}/resources/pm_execution_instructions.md` in Claude Code) before starting.

`pm-prototype` turns an approved PRD (`docs/product/<feature-slug>/prd.md`) into a self-contained, zero-build HTML/CSS/JS prototype at `docs/product/<feature-slug>/prototype.html` without touching any host application source files or build manifests, then verifies fidelity via [`pm-ux-flows`](../../agents/pm_ux_flows.md) (`Mode: PROTOTYPE_AUDIT`).

---

## Step 1: Intake & MVP Scope Check

1.  **Resolve Target PRD & Approval Status**:
    *   Accept an explicit path to `docs/product/<feature-slug>/prd.md` or resolve the most recently modified `<feature-slug>` under `docs/product/` when invoked without arguments.
    *   If `prd.md` does not exist, offer a Progression Gate to run [`../pm-prd/SKILL.md`](../pm-prd/SKILL.md) (`${CLAUDE_PLUGIN_ROOT}/skills/pm-prd/SKILL.md` in Claude Code) first. If `prd.md` does not have `Status: Approved` (for example `Draft` or `Draft (Needs Revision)`), offer a Progression Gate: `(Recommended) Run /pm-prd review loop first to lock MVP scope` vs. `Prototype current Draft anyway`.
    *   Read `docs/product/<feature-slug>/prd.md` (`## 3. Target Roles & Critical User Journeys (CUJs)`, `### Cross-Role Handoffs & Permissions`, `## 4. Functional Requirements, Business Rules & Edge Cases`, and `## 5. UX States & Copy Guidelines`).
    *   Read `.pm/ui_tokens.md` (and `PRODUCT_CONTEXT.md` if present). If `.pm/ui_tokens.md` is missing, extract `:root` CSS custom properties from existing stylesheets/theme files into `.pm/ui_tokens.md` (max 150 lines) or initialize the neutral system fallback palette.
2.  **Strict MVP Scope Rule**:
    *   Render **only** active `MVP Goals (In Scope)` requirements. Never render features excluded under `### Non-Goals (Out of Scope / Deferred)`.

---

## Step 2: Sandbox & Embedded Stageshow UI Craft Rules

Generate `docs/product/<feature-slug>/prototype.html` under these strict invariants:

1.  **Zero-Build & Offline Sandbox Invariants**:
    *   **Single Self-Contained File**: Write plain HTML5, scoped `<style>`, and vanilla `<script>` inside `docs/product/<feature-slug>/prototype.html` (**hard cap: 400 lines**).
    *   **Zero Host Repo Mutation**: Never modify `package.json`, `tsconfig.json`, host application source files, or any file outside `docs/product/<feature-slug>/` (aside from initializing `.pm/ui_tokens.md` in Step 1 when absent).
    *   **Zero External Network Requests**: Never load external CDN fonts, external scripts, or remote images (`http://` or `https://`). All icons must be inline single-family stroke SVGs so offline/headless browser rendering achieves `console.error = 0` and `pageerror = 0`.
2.  **4 Switchable Interactive States + Conditional Role Switcher**:
    *   Include a compact, non-intrusive control bar allowing stakeholders to toggle interactively across all 4 states from `## 5. UX States & Copy Guidelines`—and, **when `### Cross-Role Handoffs & Permissions` specifies `>= 2` roles with distinct views or allowed actions**, include an interactive **`Role` switcher** (`ROLE-01 | ROLE-02 ...`) updating visible density, controls, and read-only/no-access states (omit the role switcher on `Single-Role Scope`):
        1.  `Default / Ready` (populated realistic domain records and primary user action)
        2.  `Loading / Progress` (skeleton matching exact row geometry and line box of real content)
        3.  `Empty / Zero-Result` (calm empty state with one clear recovery/reset action)
        4.  `Error / No-Access Fallback` (honest fallback preserving user input or explaining role access)
3.  **Embedded Stageshow UI Craft Standard**:
    *   **Token Fidelity**: Bind all surfaces, text, borders, radii, and accents to `:root` CSS custom properties from `.pm/ui_tokens.md` (`--pm-surface-0..3`, `--pm-text-primary`, `--pm-text-secondary`, `--pm-accent`, `--pm-border`, `--pm-radius-*`, `--pm-space-*`).
    *   **Surface Restraint (3–4 Levels Max)**: Quiet surface steps (`canvas -> panel -> raised row/control -> popover`). Never nest bordered cards inside bordered cards (`cards-in-cards`).
    *   **Typography & Hierarchy**: Sentence case across headings, labels, and buttons (never tracked all-caps spam). UI text `12px–15px` with `line-height >= 1.3`. Group title + subtitle tightly (`4px–6px` gap; never `space-between` voids). Apply `font-variant-numeric: tabular-nums` on numbers/metrics, and `white-space: nowrap; flex-shrink: 0` on pills.
    *   **Spacing & Reading-Edge Alignment**: Minimum `12px` content inset and `8px` control gap; shared grid column tracks across rows.
    *   **Icon & Anti-Slop Discipline**: Single inline SVG stroke family (`14px–16px`, uniform `1.5px` or `1.75px` stroke width, `flex: none`). Zero emoji icons, zero purple-pink AI gradients, zero generic AI sparkle/wand decorations.
    *   **Responsive Reflow**: Clean layout at both `390×844` mobile and `1440×900` desktop viewports.

---

## Step 3: Fresh-Context `pm-ux-flows` & Progressive Browser Verification

1.  **Mandatory Fresh-Context `pm-ux-flows` Audit (`Mode: PROTOTYPE_AUDIT`, Max 1 Fix Pass)**:
    *   When subagent tools are available, spawn [`pm-ux-flows`](../../agents/pm_ux_flows.md) (`${CLAUDE_PLUGIN_ROOT}/agents/pm_ux_flows.md` in Claude Code) in `Mode: PROTOTYPE_AUDIT` (passing `prd.md`, `.pm/ui_tokens.md`, and `prototype.html`) and resolve any `NEEDS_CRAFT_FIX` (`Blocker` or `Major`) findings in at most 1 fix pass. When subagent tools are unavailable, run the same 400-line, zero-network, zero-`Out of Scope`, 4-state, conditional `Role` switcher (when `>= 2` roles diverge), and `--pm-*` token checks inline before delivery.
2.  **Progressive Live Browser & `stageshow-critic` Check (When Available)**:
    *   If browser automation is available in the host session:
        *   Render `prototype.html` at `390×844` (mobile) and `1440×900` (desktop), verifying `console.error = 0` and `pageerror = 0` across all 4 states.
        *   If the optional `stageshow-critic` companion subagent is available, invoke `stageshow-critic` with captured screenshots and resolve visual layout defects.
3.  **Deliverable Presentation**:
    *   Present links to `docs/product/<feature-slug>/prototype.html` and `docs/product/<feature-slug>/prd.md`, ready for stakeholder sign-off or engineering handoff via `/egm-draft docs/product/<feature-slug>/prd.md`.
