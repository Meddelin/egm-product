# EGM for Product Managers (`egm-product`)

`egm-product` adapts the **Elephant-Goldfish Model (EGM)** for AI-native Product Managers: a stateful main agent (**the Elephant**) guides the PM one question at a time and writes bounded product artifacts, while fresh-context stateless read-only subagents (**Goldfish** critics) challenge assumptions with zero author bias.

While engineering specs focus on technical architecture, APIs, and database design, **`egm-product` stays 100% focused on Product Management**—understanding company context, empirical user roles, UI App Shell blueprints, and metric trees; challenging Jobs-to-be-Done (JTBD) and cutting MVP bloat; writing and reviewing JTBD + User Story PRDs with story-driven screen states; and generating interactive zero-build HTML prototypes rendered 1:1 inside the real product UI canvas.

---

## Pure-Product Two-Layer Architecture

1. **Layer 1: Product, Role, UI Shell & Metric Context Contracts (Zero Backend Noise)**
   - Optional `COMPANY_CONTEXT.md` (stored at `~/.pm/COMPANY_CONTEXT.md` across projects or `./COMPANY_CONTEXT.md` locally, or passed via `/pm-discover --context <path>`): Reusable company profile, shared domain glossary, organizational role directory, and business governance/approval norms.
   - `PRODUCT_CONTEXT.md`: Product value proposition, strategic horizon, high-level map of existing user-facing screens/capabilities, elastic **`Active Product Roles & Workflows`** table (`1` row for single-role products; `N` rows only when goals, usage patterns, or permissions genuinely diverge under `Zero Assumed Personas`), and pointer to `.pm/ui_tokens.md` (App Shell & Navigation Blueprint, Frontend Canvas File Map, UI language/`i18n`, active runtime theme, component signatures, and `:root` CSS tokens).
   - `METRICS.md`: North Star metric, role-segmented or product-wide input drivers, counter-metric guardrails, and domain-level product analytics events.

2. **Layer 2: Product Surface & UI Shell Scanner + The 4 + 1 Product Goldfish Swarm (`4` Parallel Critics + `1` Sequential Synthesizer)**
   - [`pm-product-scanner`](./agents/pm_product_scanner.md): Read-only helper used by `/pm-discover` to map existing user-facing screens/navigation, UI language/`i18n`, active runtime theme, App Shell chrome, component anatomy, and `.pm/ui_tokens.md` CSS variables for 1:1 in-canvas prototyping—without scanning database schemas or backend internals.
   - [`pm-value-strategy`](./agents/pm_value_strategy.md) *(CPO Lens)*: Challenges problem & JTBD sharpness (`JOB-xx` Job Stories + current workaround friction), `Demand Evidence Posture` (`EVIDENCE_BACKED` vs. `UNVALIDATED_ASSUMPTION` + validation/kill criterion), strategic alignment, and MVP bloat.
   - [`pm-ux-flows`](./agents/pm_ux_flows.md) *(UX, Stories & Product-Canvas Lens)*: Audits JTBD-to-User-Story (`US-xx`) decomposition, Critical User Journeys (`CUJs`), empirical role fit (`Zero Assumed Personas`), conditional cross-role handoffs, story-driven screen states & transitions, and 1:1 real product-canvas fidelity of `prototype.html` (`Mode: PROTOTYPE_AUDIT`).
   - [`pm-metrics-experiment`](./agents/pm_metrics_experiment.md) *(Lead Product Analyst Lens)*: Audits the falsifiable causal chain, rejects vanity metrics, verifies `Role Segment` attribution and guardrails (`MET-GRD-*`), and checks domain product events and rollout plans.
   - [`pm-business-logic`](./agents/pm_business_logic.md) *(Domain & Logic Lens)*: Audits functional completeness, business rules, user-facing edge cases (edits, undo, conflicts, limits), permissions/approvals, user-perceived AI/search quality, and open questions for engineering.
   - [`pm-synthesizer`](./agents/pm_synthesizer.md): Sequential read-only synthesizer that deduplicates the 4 Product Goldfish reports into `opportunity_brief.md` or `pm_review_report.md`.

---

## 4-Stage Product Pipeline

| Stage | Skill | Deliverable | Purpose |
| :--- | :--- | :--- | :--- |
| **1. Discover** | [`/pm-discover`](./skills/pm-discover/SKILL.md) | `PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/ui_tokens.md` (+ optional `COMPANY_CONTEXT.md`) | User-surface, App Shell & CSS-token scan (`--scope <subdir>`, `--context <path>`) + one-question-at-a-time PM interview. |
| **2. Brainstorm** | [`/pm-brainstorm`](./skills/pm-brainstorm/SKILL.md) | `docs/product/<feature-slug>/opportunity_brief.md` | Challenges Jobs-to-be-Done (`JOB-xx`), demand evidence, affected `Role ID`s, alternatives, and MVP scope with the 4 + 1 Product Goldfish swarm. |
| **3. PRD (+ Review)** | [`/pm-prd`](./skills/pm-prd/SKILL.md) | `docs/product/<feature-slug>/prd.md` + `pm_review_report.md` | Drafts a JTBD + User Story PRD with story-driven screen states and polishes it via a built-in 2-round 4 + 1 Product Goldfish review against [`prd-standard.md`](./resources/document_standards/prd-standard.md). |
| **4. Prototype** | [`/pm-prototype`](./skills/pm-prototype/SKILL.md) | `docs/product/<feature-slug>/prototype.html` | Zero-build HTML/CSS/JS preview rendered 1:1 inside the real product's App Shell & host screen, with interactive User Story flows and PRD-driven scenario/state/role switching, verified via `pm-ux-flows`. |

Once `/pm-prd` marks `docs/product/<feature-slug>/prd.md` as `Approved`, hand the self-contained PRD (and optional `prototype.html`) directly to engineering or any coding agent to design the technical architecture and implement the feature.

---

## Installation & Harness Support

`egm-product` ships native manifests, slash commands (`resources/commands/pm-*.md`), skills (`skills/pm-*/SKILL.md`), subagents (`agents/pm_*.md`), and context rules (`QWEN.md`, `GEMINI_EXTENSION.md`, `rules/AGENTS.md`) for **Antigravity**, **Claude Code / Cowork**, **OpenAI Codex / ChatGPT Work**, **Qwen Code (and custom forks)**, **Gemini CLI**, and **`omp`**.

```bash
# Antigravity CLI
python ./egm-product/scripts/install.py --target antigravity
# or: agy plugin install ./egm-product && agy plugin enable egm-product

# Claude Code (commands invoke as /egm-product:pm-discover, /egm-product:pm-brainstorm, /egm-product:pm-prd, /egm-product:pm-prototype)
claude plugin marketplace add Meddelin/egm-product && claude plugin install egm-product@egm-product

# OpenAI Codex
codex plugin marketplace add Meddelin/egm-product && codex plugin add egm-product@egm-product

# Qwen Code (`qwen` CLI) or custom Qwen CLI fork
qwen extensions install ./egm-product
# or isolated extension install into custom fork config dir:
python ./egm-product/scripts/install.py --target qwen --config-dir ~/.your-qwen-fork

# Gemini CLI
gemini extensions install ./egm-product

# omp (skills invoke as /skill:pm-discover, ...)
omp plugin marketplace add Meddelin/egm-product && omp plugin install egm-product@egm-product
```

See [`docs/harnesses.md`](./docs/harnesses.md), [`docs/claude.md`](./docs/claude.md), and [`docs/codex.md`](./docs/codex.md) for harness-specific delegation and permission rules.

### Packaging & Verification

```bash
pytest tests/unit
python scripts/pack_plugin.py --target claude --output dist/
python scripts/pack_plugin.py --target openai --output dist/
```

---

## License

Licensed under the [Apache License, Version 2.0](./LICENSE).
