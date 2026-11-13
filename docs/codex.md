# OpenAI Codex & ChatGPT Work Integration (`egm-product`)

## 1. Install & Resolve Bundled Paths

```sh
codex plugin marketplace add Meddelin/egm-product
codex plugin add egm-product@egm-product
```

Start a new session after installation and select the target `pm-*` skill (`pm-discover`, `pm-brainstorm`, `pm-prd`, or `pm-prototype`).

From `<plugin>/skills/<skill>/SKILL.md`, the plugin root is **two parent directories above the skill folder (`../../` relative to `SKILL.md`)**. Resolve bundled `agents/`, `resources/`, and `docs/` paths against that plugin root. Resolve `PRODUCT_CONTEXT.md`, `METRICS.md`, optional `COMPANY_CONTEXT.md`, `.pm/ui_tokens.md`, and `docs/product/<feature-slug>/` against the user's working directory.

If the prompt or `AGENTS.md` contains `EGM artifact directory: <path>`, route working review reports (`pm_review_report.md` and scratch files) to `<path>` (resolved relative to the working directory).

## 2. Fresh-Context Product Goldfish Delegation (`spawn_agent`)

Inspect the native subagent tool schema in the active Codex or ChatGPT Work session:
* When `spawn_agent` exposes `fork_context`, set **`fork_context: false`** on every Goldfish invocation (`pm-product-scanner` in Stage 1, the 4 Phase 1 product critics and `pm-synthesizer` in Stages 2–3, and `pm-ux-flows` in `Mode: PROTOTYPE_AUDIT` in Stage 4).
* When the schema exposes `fork_turns`, set **`fork_turns: "none"`**.
* Pass absolute paths to the canonical persona file (`<plugin_root>/agents/pm_<role>.md`), [`prd-standard.md`](../resources/document_standards/prd-standard.md), `PRODUCT_CONTEXT.md`, `METRICS.md`, optional `COMPANY_CONTEXT.md`, and the target artifact. Never paste the Elephant's conversation transcript into the child prompt.
* Wait for all 4 Phase 1 product critics to complete before invoking `pm-synthesizer`. If fresh-context subagent tools are unavailable in the current ChatGPT mode, stop and report that fresh-context Goldfish isolation is unavailable for 4+1 swarms (`/pm-brainstorm` and `/pm-prd` review) rather than role-playing all 4 critics in the parent context; single-pass tasks (`/pm-discover` and `/pm-prototype`) may use bounded inline fallback.

## 3. Questions & Artifact Links in Codex Chat

* Map Progression Gates and neutral Trade-Off Gates (`len(questions) == 1`, `is_multi_select: false`) to the host's structured question tool when available, or ask one numbered plain-text question and wait for the user's answer.
* Link generated files using absolute-path Markdown links such as `[prd](/absolute/project/docs/product/search-filters/prd.md)` (wrapping paths with spaces in `<...>`). Do **not** emit `file://` links in Codex chat.

## 4. Packaging for ChatGPT Desktop Upload

Build a clean runtime archive (excluding `tests/`, `docs/designs/`, `.dev/`, and `.claude-plugin/`):

```sh
python scripts/pack_plugin.py --target openai --output dist/
```

Upload `dist/egm-product-openai.zip` via **Plugins > Add > Upload plugin archive** in the ChatGPT desktop app, or import the repository marketplace via **Admin > Plugins > Add > Import marketplace** (repository URL `https://github.com/Meddelin/egm-product`, marketplace path `.agents/plugins`).
