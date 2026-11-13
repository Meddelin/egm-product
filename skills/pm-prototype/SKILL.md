---
name: pm-prototype
description: Generate and audit a zero-build, standalone interactive HTML/CSS/JS prototype rendered 1:1 inside the real product's App Shell and host screen canvas, driven by the PRD's User Stories and scenarios.
license: Apache-2.0
disable-model-invocation: true
---

# Stage 4: In-Canvas Interactive HTML Prototyping (`pm-prototype`)

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.
Read [`../../resources/pm_execution_instructions.md`](../../resources/pm_execution_instructions.md) (`${CLAUDE_PLUGIN_ROOT}/resources/pm_execution_instructions.md` in Claude Code) before starting.

`pm-prototype` turns an approved PRD (`docs/product/<feature-slug>/prd.md`) into a self-contained, zero-build HTML/CSS/JS prototype at `docs/product/<feature-slug>/prototype.html` that **reproduces the real product's App Shell and target host screen 1:1**—letting stakeholders click through the PRD's User Stories and inspect the states/scenarios that actually matter to the feature, without touching any host application files or build manifests, verified via [`pm-ux-flows`](../../agents/pm_ux_flows.md) (`Mode: PROTOTYPE_AUDIT`).

---

## Step 1: Intake, MVP Scope & Direct Host-Frontend Inspection

1.  **Resolve Target PRD & Approval Status**:
    *   Accept an explicit path to `docs/product/<feature-slug>/prd.md` or resolve the most recently modified `<feature-slug>` under `docs/product/` when invoked without arguments.
    *   If `prd.md` does not exist, offer a Progression Gate to run [`../pm-prd/SKILL.md`](../pm-prd/SKILL.md) (`${CLAUDE_PLUGIN_ROOT}/skills/pm-prd/SKILL.md` in Claude Code) first. If `prd.md` does not have `Status: Approved` (for example `Draft` or `Draft (Needs Revision)`), offer a Progression Gate: `(Recommended) Run /pm-prd review loop first to lock MVP scope` vs. `Prototype current Draft anyway`.
    *   Read `docs/product/<feature-slug>/prd.md` (`## 3. Jobs-to-be-Done (JTBD), User Stories & Scenarios (CUJs)`, `### Cross-Role Handoffs & Permissions`, `## 4. Functional Requirements, Business Rules & Edge Cases`, and `## 5. UI Placement, Screen States & Copy`), `PRODUCT_CONTEXT.md` (when present), and resolved `COMPANY_CONTEXT.md` (when present).
2.  **Mandatory Host-Frontend Canvas Inspection (Whenever Frontend Code Exists in the Workspace)**:
    *   Read `.pm/ui_tokens.md`. If `.pm/ui_tokens.md` is missing or lacks `Frontend Canvas File Map` / `App Shell & Component Anatomy`, scan the workspace's frontend layout, `i18n` locale dictionary, active theme, and UI primitives following Section 3 of [`../../agents/pm_product_scanner.md`](../../agents/pm_product_scanner.md) (`${CLAUDE_PLUGIN_ROOT}/agents/pm_product_scanner.md` in Claude Code) and write/refresh `.pm/ui_tokens.md`.
    *   **Never generate `prototype.html` from `.pm/ui_tokens.md` alone when frontend files exist in the repo.** Before writing HTML, read the real frontend files needed to replicate the product's interface faithfully:
        1.  **Authenticated / Route-Group App Shell & Navigation**: Trace past bare root provider wrappers (`app/layout.tsx`) to the **actual authenticated or route-group layout** wrapping live screens (e.g. `app/(dashboard)/layout.tsx`, `<MainLayout><Outlet/></MainLayout>`, `layouts/`, or shared `packages/ui/`), including sidebar, header/topbar, breadcrumbs, brand SVG mark, and active menu item styling.
        2.  **Target Host Screen & `i18n` Locale Dictionary**: Read the exact host screen component named in `Host Screen & UI Mount Point` (or closest sibling screen if adding a sub-route)—and, if components use translation keys (`{t('...')}`), read the **default `i18n` locale JSON/YAML dictionary** (`locales/ru*.json`, `messages/ru.json`, etc.) so 100% of navigation, headers, realistic table/form records, messages, currency symbols, and date formats match the live UI language.
        3.  **Default Runtime Theme & Reusable UI Primitives**: Inspect `<html class="dark">`, `data-theme`, or `ThemeProvider defaultTheme` alongside `globals.css` / `tailwind.config.*` / `theme.ts` and core components (`Button`, `Table`/`List`, `Input`/`Select`, `Badge`, `Modal`/`Drawer`/`Tabs`) so you match the **actual default active theme** (`light` vs. `.dark`), exact font scale, border radii, shadows, casing, and SVG icons (filled vs. stroke).
    *   *(Greenfield fallback only when zero frontend code exists in the workspace)*: Build a complete, believable full-screen product App Shell (sidebar/header + main workspace) from `.pm/ui_tokens.md` and `PRODUCT_CONTEXT.md` domain terminology—never an isolated floating card on a blank page.
3.  **Strict MVP Scope Rule**:
    *   Render **only** active `MVP Goals (In Scope)` / `US-*` / `REQ-*` items. Never render capabilities excluded under `### Non-Goals (Out of Scope / Deferred)`.

---

## Step 2: 1:1 Product Canvas & Story-Driven Interactivity

Generate `docs/product/<feature-slug>/prototype.html` following these principles:

1.  **Zero-Build, Offline Self-Containment**:
    *   **Single Self-Contained File**: Write plain HTML5, explicit `<style>` rules (translating any Tailwind/CSS-Module classes from the inspected host components into concrete CSS rules—never leave unstyled utility classes), and vanilla `<script>` inside `docs/product/<feature-slug>/prototype.html`.
    *   **Zero Host Repo Mutation**: Never modify `package.json`, `tsconfig.json`, host application source files, or any file outside `docs/product/<feature-slug>/` (aside from refreshing `.pm/ui_tokens.md` in Step 1 when missing/incomplete).
    *   **Zero External Network Requests & Zero Broken Relative Assets**: Never load external CDN fonts, scripts, or remote images (`http://` or `https://`), and **never reference external relative asset paths (`<img src="/logo.svg">`, `<link href="...">`) that fail when `docs/product/<feature-slug>/prototype.html` opens offline via `file://`**. Inline the host product's real SVG wordmark and icons directly so offline rendering produces zero console/page errors.
2.  **1:1 Product Canvas Fidelity (No Foreign Design Rules)**:
    *   **Real Surrounding App Shell & Host Screen**: Render the product's actual surrounding shell (exact sidebar/topbar dimensions and colors, real navigation menu items with the host section highlighted, real header/breadcrumbs) and realistic surrounding context of the target host screen (existing toolbar, table rows, tabs, or panels), mounting the new feature in its exact real-world placement (inline section, tab, side drawer, modal, split pane, or route).
    *   **Exact Host Visual Language & Copy**: Match the inspected host frontend's colors, active `light`/`.dark` theme, typography, borders, shadows, button/input/table/badge anatomy, icons, and **UI copy language** (e.g., Russian throughout when the frontend is in Russian). Do not impose external typography, card, or icon rules that differ from the host product.
3.  **Story-Driven Interactive Flows, Scenarios & Roles**:
    *   **Walkable User Stories (`US-*` / `CUJs`)**: Wire vanilla JS handlers so stakeholders can click through the PRD's User Stories interactively inside the real interface (opening/closing drawers or modals, filtering/editing rows, submitting forms, triggering validations/confirmations, seeing state transitions).
    *   **PRD-Dictated States & Role Perspectives**: Choose which scenarios, edge/empty/conflict/error states, or multi-role perspectives (`ROLE-01 | ROLE-02...` when `>= 2` roles have distinct views or actions) to expose based **organically on what `prd.md` and its User Stories actually describe**—never forcing irrelevant boilerplate states. When multiple starting scenarios, edge states, or role views exist that cannot all be reached naturally from one default flow, provide a compact, unobtrusive floating switcher (`position: fixed`, outside the product header) so stakeholders can jump between those specific PRD scenarios/roles without distorting the real app chrome.

---

## Step 3: Canvas-Fidelity `pm-ux-flows` Audit & Optional Browser Check

1.  **Mandatory Fresh-Context `pm-ux-flows` Audit (`Mode: PROTOTYPE_AUDIT`, Max 1 Fix Pass)**:
    *   When subagent tools are available, spawn [`pm-ux-flows`](../../agents/pm_ux_flows.md) (`${CLAUDE_PLUGIN_ROOT}/agents/pm_ux_flows.md` in Claude Code) in `Mode: PROTOTYPE_AUDIT`—passing `PRODUCT_CONTEXT.md` (and resolved `COMPANY_CONTEXT.md` when present), `prd.md`, `.pm/ui_tokens.md`, `prototype.html`, **and the exact workspace-root-relative paths of the inspected frontend App Shell, `i18n` locale, theme, and target host screen files**—and resolve any `NEEDS_CRAFT_FIX` (`Blocker` or `Major`) findings in at most 1 fix pass. When subagent tools are unavailable, verify 1:1 host App Shell/screen/theme/language fidelity, interactive User Story coverage, zero network/broken-asset calls, and zero `Out of Scope` leakage inline before delivery.
2.  **Live Browser Check (When Available)**:
    *   If browser automation is available in the host session, open `prototype.html` in the browser and verify `console.error = 0`, `pageerror = 0`, clean visual layout, and working interactive User Story flows.
3.  **Deliverable Presentation**:
    *   Present links to `docs/product/<feature-slug>/prototype.html` and `docs/product/<feature-slug>/prd.md`, ready for stakeholder review and engineering implementation.
