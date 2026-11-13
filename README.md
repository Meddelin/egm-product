# EGM for Product Managers (`egm-product`)

`egm-product` adapts the **Elephant-Goldfish Model (EGM)** for AI-native Product Managers: a stateful main agent (**the Elephant**) guides the PM one question at a time and writes bounded product artifacts, while fresh-context stateless read-only subagents (**Goldfish** critics) challenge assumptions with zero author bias.

While engineering `egm` (`/egm-draft`, `/egm-review`) focuses on technical architecture, APIs, and database design, **`egm-product` stays 100% focused on Product Management**—understanding company context, empirical user roles, and metric trees; challenging feature value and cutting MVP bloat; writing and reviewing user-focused PRDs; and generating interactive zero-build HTML prototypes.

---

## Pure-Product Two-Layer Architecture

1. **Layer 1: Product, Role & Metric Context Contracts (Zero Code Noise)**
   - Optional `COMPANY_CONTEXT.md` (capped at 200 lines, stored at `~/.pm/COMPANY_CONTEXT.md` across projects or `./COMPANY_CONTEXT.md` locally, or passed via `/pm-discover --context <path>`): Reusable company profile, shared domain glossary, organizational role directory, and business governance/approval norms.
   - `PRODUCT_CONTEXT.md` (capped at 250 lines): Product value proposition, strategic horizon, high-level map of existing user-facing screens/capabilities, elastic **`Active Product Roles & Workflows`** table (`1` row for single-role products; `N` rows only when goals, usage patterns, or permissions genuinely diverge under `Zero Assumed Personas`), and pointer to `.pm/ui_tokens.md` (max 150 lines).
   - `METRICS.md` (capped at 200 lines): North Star metric, role-segmented or product-wide input drivers, counter-metric guardrails, and domain-level product analytics events.

2. **Layer 2: Light Product Scanner + The 4 + 1 Product Goldfish Swarm (`4` Parallel Critics + `1` Sequential Synthesizer)**
   - [`pm-product-scanner`](./agents/pm_product_scanner.md): Lightweight read-only helper used by `/pm-discover` to skim existing user-facing screens/flows and extract `.pm/ui_tokens.md` CSS variables for prototyping—without scanning database schemas or backend internals.
   - [`pm-value-strategy`](./agents/pm_value_strategy.md) *(CPO Lens)*: Challenges problem sharpness, `Demand Evidence Posture` (`EVIDENCE_BACKED` vs. `UNVALIDATED_ASSUMPTION` + validation/kill criterion), strategic alignment, and MVP bloat.
   - [`pm-ux-flows`](./agents/pm_ux_flows.md) *(UX & Role Flows Lens)*: Audits Critical User Journeys (`CUJs`), step friction, empirical role fit (`Zero Assumed Personas`), conditional cross-role handoffs, the 4 mandatory UI states, and `prototype.html` craft (`Mode: PROTOTYPE_AUDIT`).
   - [`pm-metrics-experiment`](./agents/pm_metrics_experiment.md) *(Lead Product Analyst Lens)*: Audits the falsifiable causal chain, rejects vanity metrics, verifies `Role Segment` attribution and guardrails (`MET-GRD-*`), and checks domain product events and rollout plans.
   - [`pm-business-logic`](./agents/pm_business_logic.md) *(Domain & Logic Lens)*: Audits functional completeness, business rules, user-facing edge cases (edits, undo, conflicts, limits), permissions/approvals, user-perceived AI/search quality, and open questions for engineering.
   - [`pm-synthesizer`](./agents/pm_synthesizer.md): Sequential read-only synthesizer that deduplicates the 4 Product Goldfish reports into `opportunity_brief.md` or `pm_review_report.md`.

---

## 4-Stage Product Pipeline

| Stage | Skill | Deliverable | Purpose |
| :--- | :--- | :--- | :--- |
| **1. Discover** | [`/pm-discover`](./skills/pm-discover/SKILL.md) | `PRODUCT_CONTEXT.md`, `METRICS.md`, `.pm/ui_tokens.md` (+ optional `COMPANY_CONTEXT.md`) | Light user-surface & CSS-token overview (`--scope <subdir>`, `--context <path>`) + one-question-at-a-time PM interview. |
| **2. Brainstorm** | [`/pm-brainstorm`](./skills/pm-brainstorm/SKILL.md) | `docs/product/<feature-slug>/opportunity_brief.md` (max 200 lines) | Challenges demand evidence, affected `Role ID`s, alternatives, and MVP scope with the 4 + 1 Product Goldfish swarm. |
| **3. PRD (+ Review)** | [`/pm-prd`](./skills/pm-prd/SKILL.md) | `docs/product/<feature-slug>/prd.md` (max 250 lines) + `pm_review_report.md` | Drafts a user-focused PRD and polishes it via a built-in 2-round 4 + 1 Product Goldfish review against [`prd-standard.md`](./resources/document_standards/prd-standard.md). |
| **4. Prototype** | [`/pm-prototype`](./skills/pm-prototype/SKILL.md) | `docs/product/<feature-slug>/prototype.html` | Zero-build HTML/CSS/JS preview (max 400 lines, 4 switchable states + conditional `Role` switcher) verified via `pm-ux-flows`. |

Once `/pm-prd` marks `docs/product/<feature-slug>/prd.md` as `Approved`, hand it to `/egm-draft docs/product/<feature-slug>/prd.md` (when the optional engineering `egm` companion plugin is installed) or directly to any coding agent so engineering designs the technical architecture in `docs/designs/<feature-slug>.md`. Likewise, `/pm-prototype` optionally uses `stageshow-critic` when the `stageshow-craft` plugin is installed.

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
